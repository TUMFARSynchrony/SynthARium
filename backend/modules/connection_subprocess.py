"""TODO document"""

import sys
import time
import json
import logging
import asyncio
from os.path import join
from aiortc import RTCSessionDescription
from typing import Any, Callable, Coroutine, Tuple
from asyncio.subprocess import Process, PIPE, create_subprocess_exec

from modules import BACKEND_DIR
from modules.connection_state import ConnectionState
from modules.connection_interface import ConnectionInterface

from custom_types.message import MessageDict
from custom_types.connection import RTCSessionDescriptionDict
from custom_types.participant_summary import ParticipantSummaryDict
from custom_types.connection import ConnectionOfferDict, ConnectionAnswerDict


class ConnectionSubprocess(ConnectionInterface):
    """TODO document"""

    _offer: RTCSessionDescriptionDict
    _log_name_suffix: str
    _message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]]

    _running_lock: asyncio.Lock
    _running: bool
    _process: Process | None
    _state: ConnectionState
    _logger: logging.Logger
    _subscriber_offers: asyncio.Queue
    _tasks: list[asyncio.Task]

    _local_description_received: asyncio.Event
    _local_description: RTCSessionDescription | None

    def __init__(
        self,
        offer: RTCSessionDescriptionDict,
        message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
        log_name_suffix: str,
    ):
        """TODO document"""
        super().__init__()
        self._offer = offer
        self._log_name_suffix = log_name_suffix
        self._message_handler = message_handler

        self._running_lock = asyncio.Lock()
        self._running = True
        self._process = None
        self._state = ConnectionState.NEW
        self._logger = logging.getLogger("ConnectionSubprocess")
        self._subscriber_offers = asyncio.Queue()

        self._local_description_received = asyncio.Event()
        self._local_description = None

        self._tasks = [
            asyncio.create_task(self._run(), name=f"ConnectionSubprocess.run")
        ]

    @property
    def state(self) -> ConnectionState:
        """TODO document"""
        return self._state

    async def create_subscriber_offer(
        self, participant_summary: ParticipantSummaryDict | None
    ) -> ConnectionOfferDict:
        """TODO document"""
        await self._send_command("CREATE_OFFER", participant_summary)
        offer = await self._subscriber_offers.get()
        return offer

    async def handle_subscriber_answer(self, answer: ConnectionAnswerDict) -> None:
        """TODO document"""
        await self._send_command("HANDLE_ANSWER", answer)

    async def get_local_description(self) -> RTCSessionDescription:
        """TODO document"""
        self._logger.debug("Wait for local_description")
        await self._local_description_received.wait()
        self._logger.debug("Return local_description")
        assert self._local_description is not None
        return self._local_description

    async def stop(self) -> None:
        """TODO document"""
        self._logger.debug("Stopping ConnectionSubprocess")
        if self._process is not None and self._process.returncode is None:
            self._process.terminate()
        async with self._running_lock:
            self._running = False
        current_task = asyncio.current_task()
        tasks = [t for t in self._tasks if t is not current_task]
        await asyncio.gather(*tasks)
        await self._log_final_stdout_stderr()
        self._set_state(ConnectionState.CLOSED)
        self._logger.debug("Stop complete")

    async def send(self, data: MessageDict | dict) -> None:
        """TODO document"""
        await self._send_command("SEND", data)

    async def stop_subconnection(self, subconnection_id: str) -> bool:
        """TODO document"""
        # TODO implement
        raise NotImplementedError()

    def set_muted(self, video: bool, audio: bool) -> None:
        """TODO document"""
        # TODO implement
        pass

    def _set_state(self, state: ConnectionState):
        """Set connection state and emit `state_change` event."""
        if self._state == state:
            return

        self._logger.debug(f"ConnectionState is: {state}")
        self._state = state
        self.emit("state_change", state)

    async def _run(self) -> None:
        """TODO document"""
        self._logger.debug("Starting subprocess")

        # Start subprocess
        program = [
            sys.executable,
            join(BACKEND_DIR, "subprocess_main.py"),
            "-l",
            f"{self._log_name_suffix}",
            "-o",
            f"{json.dumps(self._offer)}",
        ]
        program_summary = program[:5] + [
            program[5][:10] + ("..." if len(program[5]) >= 10 else "")
        ]

        self._process = await create_subprocess_exec(
            *program, stdin=PIPE, stderr=PIPE, stdout=PIPE
        )
        self._logger.debug(
            f"Subprocess started. Program: {program_summary}, PID: {self._process.pid}"
        )

        # Create task listening for messages from subprocess
        self._tasks.append(
            asyncio.create_task(
                self._wait_for_messages(),
                name="ConnectionSubprocess._wait_for_messages",
            )
        )
        self._tasks.append(
            asyncio.create_task(
                self._ping(),
                name="ConnectionSubprocess.ping",
            ),
        )

    async def _ping(self):
        """Send PING message in interval, until self._running is False."""
        await asyncio.sleep(10)
        self._logger.debug("Start PING loop")
        while True:
            async with self._running_lock:
                if not self._running:
                    self._logger.debug(f"Return from ping, running=False")
                    return
            await self._send_command("PING", time.time())
            await asyncio.sleep(2)

    async def _wait_for_messages(self):
        """TODO document"""
        self._logger.debug("Listen for messages from subprocess")
        if self._process is None:
            self._logger.error(
                "Failed to listen for messages from subprocess, _process is None"
            )
            return
        if self._process.stdout is None:
            self._logger.error(
                "Failed to listen for messages from subprocess, _process.stdout is None"
            )
            return

        while True:
            async with self._running_lock:
                if not self._running:
                    self._logger.debug(
                        "Stop listening for messages from subprocess, running is False"
                    )
                    return

            self._logger.debug("_wait_for_messages - readline")
            try:
                msg = await asyncio.wait_for(self._process.stdout.readline(), 5)
            except asyncio.TimeoutError:
                self._logger.debug("_wait_for_messages - timeout")
                continue

            if len(msg) == 0:
                self._logger.error(
                    "Stop listening for messages from subprocess, len(msg) == 0"
                )
                await self.stop()
                break

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                self._logger.debug(f"Msg: {msg}, len: {len(msg)}")
                self._logger.error(f"Failed to parse message from subprocess: {e}")
                continue

            await self._handle_process_message(parsed)

    async def _handle_process_message(self, msg: dict):
        data = msg["data"]
        command = msg["command"]
        self._logger.debug(f"Received {command} command from subprocess")

        match command:
            case "SET_LOCAL_DESCRIPTION":
                self._local_description = RTCSessionDescription(
                    data["sdp"], data["type"]
                )
                self._local_description_received.set()
            case "PONG":
                t = round((time.time() - data) * 1000, 2)
                self._logger.info(f"Subprocess ping time: {t}ms")
            case "STATE_CHANGE":
                self._set_state(ConnectionState(data))
            case "API":
                await self._message_handler(data)
            case "SUBSCRIBER_OFFER":
                await self._subscriber_offers.put(data)

    async def _log_final_stdout_stderr(self):
        if self._process is None:
            return

        self._logger.debug(f"Wait for final stdout and stderr from subprocess")
        stdout, stderr = await self._process.communicate()
        self._logger.debug(
            f"Subprocess exited with returncode: {self._process.returncode}"
        )
        if stdout:
            self._logger.debug(f"[stdout START]:\n {stdout.decode()}\n[stdout END]")
        if stderr:
            self._logger.error(f"[stderr START]:\n {stderr.decode()}\n[stderr END]")

    async def _send_command(
        self,
        command: str,
        data: str
        | int
        | float
        | dict
        | None
        | ParticipantSummaryDict
        | ConnectionAnswerDict
        | MessageDict,
    ) -> None:
        """Send command to subprocess"""
        data = json.dumps({"command": command, "data": data})
        if self._process is None:
            self._logger.error(f"Failed send {data}, _process is None")
            return
        if self._process.stdin is None:
            self._logger.error(f"Failed send {data}, _process.stdin is None")
            return

        self._logger.debug(f"Sending: {data}")
        self._process.stdin.write(data.encode("utf-8") + b"\n")
        await self._process.stdin.drain()


ConnectionInterface.register(ConnectionSubprocess)


async def connection_subprocess_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
    log_name_suffix: str,
) -> Tuple[RTCSessionDescription, ConnectionSubprocess]:
    """TODO document"""
    # TODO change type of offer parameter to RTCSessionDescriptionDict
    offer_dict = RTCSessionDescriptionDict(sdp=offer.sdp, type=offer.type)  # type: ignore
    print(offer_dict)

    connection = ConnectionSubprocess(offer_dict, message_handler, log_name_suffix)

    local_description = await connection.get_local_description()

    return (local_description, connection)
