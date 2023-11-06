"""Provide the ConnectionRunner class."""

import asyncio
import json
import logging
import sys
import time
from typing import Any

from aiortc import RTCSessionDescription

from connection.connection import Connection, connection_factory
from connection.connection_state import ConnectionState
from connection.messages import ConnectionAnswerDict, ConnectionProposalDict
from custom_types.message import MessageDict
from filters import FilterDict
from hub.exceptions import ErrorDictException
from filter_api import FilterSubprocessAPI
from hub.subprocess_logging import SubprocessLoggingHandler
from server import Config


class ConnectionRunner:
    """Subprocess counterpart to Connection wrapper ConnectionSubprocess.

    Handles incoming commands from main process and relays messages and events from the
    hub.connection.Connection to the main process.

    Intended to be executed on a dedicated subprocess.  Executing other pieces of code
    on the same (sub)process may lead to problems, in case stdin, stderr or stdout are
    also used there.
    """

    _connection: Connection | None
    _lock: asyncio.Lock
    _running: bool
    _stopped_event: asyncio.Event
    _tasks: list[asyncio.Task]
    _logger: logging.Logger

    def __init__(self) -> None:
        """Instantiate new ConnectionRunner."""
        self._connection = None
        self._lock = asyncio.Lock()
        self._running = False
        self._tasks = []
        self._stopped_event = asyncio.Event()
        config = Config()

        # Setup logging for subprocess
        handler = SubprocessLoggingHandler(self._send_command)
        logging.basicConfig(level=logging.getLevelName(config.log), handlers=[handler])

        # Set logging level for libraries
        dependencies_log_level = logging.getLevelName(config.log_dependencies)
        logging.getLogger("aiohttp").setLevel(dependencies_log_level)
        logging.getLogger("aioice").setLevel(dependencies_log_level)
        logging.getLogger("aiortc").setLevel(dependencies_log_level)
        logging.getLogger("PIL").setLevel(dependencies_log_level)

        self._logger = logging.getLogger("ConnectionRunner")

    async def run(
        self,
        offer: RTCSessionDescription,
        log_name_suffix: str,
        audio_filters: list[FilterDict],
        video_filters: list[FilterDict],
        audio_group_filters: list[FilterDict],
        video_group_filters: list[FilterDict],
        record_data: list,
    ) -> None:
        """Run the ConnectionRunner.  Returns after the ConnectionRunner finished.

        Parameters
        ----------
        offer : aiortc.RTCSessionDescription
            Initial connection offer from the client.
        log_name_suffix : str
            Suffix for logger used in Connection.
        """
        self._running = True
        filter_api = FilterSubprocessAPI(self._send_command)
        answer, self._connection = await connection_factory(
            offer,
            self._relay_api_message,
            log_name_suffix,
            audio_filters,
            video_filters,
            audio_group_filters,
            video_group_filters,
            filter_api,
            record_data,
        )
        self._connection.add_listener("state_change", self._handle_state_change)
        self._send_command(
            "SET_LOCAL_DESCRIPTION", {"sdp": answer.sdp, "type": answer.type}
        )

        await self._listen_for_messages()
        self._logger.debug("ConnectionRunner exiting")

    async def stop(self) -> None:
        """Stop the runner.

        Sets `_running` to false, waits for tasks in `_tasks` and sets the
        `_stopped_event`.
        """
        self._logger.debug("ConnectionRunner Stopping")
        async with self._lock:
            self._running = False
        await asyncio.gather(*self._tasks)
        self._stopped_event.set()
        self._logger.debug("Stop complete")

    async def _listen_for_messages(self) -> None:
        """Listen for messages / commands from main / parent process over stdin."""
        self._logger.debug("Listening for messages from main process")
        msg = ""
        while msg != "q":
            async with self._lock:
                if not self._running:
                    return

            msg = await self._read()

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                self._logger.error(f"Failed to parse message from main process: {e}")
                continue

            await self._handle_message(parsed)

    async def _handle_message(self, msg: dict):
        """Handle message / command from main / parent process."""
        data = msg["data"]
        command = msg["command"]
        command_nr = msg["command_nr"]
        # self._logger.debug(f"Received {command} command from main process")

        if self._connection is None:
            self._logger.warning(
                f"Failed to handle {command}, connection is None. Data: {data}"
            )
            return

        match command:
            case "PING":
                self._send_command(
                    "PONG", {"original": msg["data"], "subprocess_time": time.time()}
                )
            case "SEND":
                await self._connection.send(data)
            case "CREATE_PROPOSAL":
                proposal = await self._connection.create_subscriber_proposal(data)
                self._send_command("CONNECTION_PROPOSAL", proposal, command_nr)
            case "HANDLE_OFFER":
                try:
                    answer = await self._connection.handle_subscriber_offer(data)
                except ErrorDictException as e:
                    self._send_command("CONNECTION_ANSWER", e.error_message, command_nr)
                    return
                self._send_command("CONNECTION_ANSWER", answer, command_nr)
            case "ADD_SUBSCRIBER_ICE_CANDIDATE":
                self._connection.handle_subscriber_add_ice_candidate(data)
            case "STOP_SUBCONNECTION":
                await self._connection.stop_subconnection(data)
            case "SET_MUTED":
                video, audio = data
                await self._connection.set_muted(video, audio)
            case "SET_VIDEO_FILTERS":
                await self._connection.set_video_filters(data)
            case "SET_AUDIO_FILTERS":
                await self._connection.set_audio_filters(data)
            case "SET_VIDEO_GROUP_FILTERS":
                await self._connection.set_video_group_filters(data[0], data[1])
            case "SET_AUDIO_GROUP_FILTERS":
                await self._connection.set_audio_group_filters(data[0], data[1])
            case "START_RECORDING":
                await self._connection.start_recording()
            case "STOP_RECORDING":
                await self._connection.stop_recording()
            case _:
                self._logger.error(f"Unrecognized command from main process: {command}")

    async def _read(self):
        """Read line from stdin.  Non-blocking and awaitable."""
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    async def _handle_state_change(self, state: ConnectionState) -> None:
        """Handle state change from `_connection`."""
        self._send_command("STATE_CHANGE", state.value)
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            self._logger.debug(f"Stopping, because state is {state}")
            await self.stop()

    async def _relay_api_message(self, message: MessageDict | Any) -> None:
        """Relay api messages from `_connection` to parent process."""
        self._send_command("API", message)

    def _send_command(
        self,
        command: str,
        data: str
        | int
        | float
        | dict
        | MessageDict
        | ConnectionProposalDict
        | ConnectionAnswerDict,
        command_nr: int = -1,
    ) -> None:
        """Send command to main / parent process via stdout.

        Parameters
        ----------
        command : str
            Command / operator for message.
        data : ...
            Data for command / operator.
        command_nr : int, optional
            Command nr identifying requests with responses.  Only required if response
            must be identified with request.
        """
        data = json.dumps({"command": command, "data": data, "command_nr": command_nr})
        print(data, flush=True)
