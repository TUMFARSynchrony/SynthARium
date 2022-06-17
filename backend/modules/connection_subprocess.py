"""TODO document"""

import asyncio
import json
import logging
from os.path import join
import sys
from typing import Any, Callable, Coroutine, Tuple
from aiortc import MediaStreamTrack, RTCSessionDescription
from asyncio.subprocess import Process, PIPE, create_subprocess_exec

from modules import BACKEND_DIR
from modules.connection_state import ConnectionState
from modules.connection_interface import ConnectionInterface
from modules.tracks import AudioTrackHandler, VideoTrackHandler

from custom_types.message import MessageDict
from custom_types.connection import RTCSessionDescriptionDict
from custom_types.participant_summary import ParticipantSummaryDict


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

        self._local_description_received = asyncio.Event()
        self._local_description = None

        self._tasks = [
            asyncio.create_task(self._run(), name=f"ConnectionSubprocess.run")
        ]

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
        program_summary = program[:3] + [
            program[3][:10] + ("..." if len(program[3]) >= 10 else "")
        ]

        self._logger.debug(f"Starting subprocess: {program_summary}")
        self._process = await create_subprocess_exec(
            *program, stdin=PIPE, stderr=PIPE, stdout=PIPE
        )
        self._logger.debug(f"Subprocess started. PID: {self._process.pid}")

        # Create task listening for messages from subprocess
        self._tasks.append(
            asyncio.create_task(
                self._wait_for_messages(),
                name="ConnectionSubprocess._wait_for_messages",
            )
        )

        # Wait for process exit
        stdout, stderr = await self._process.communicate()
        self._logger.debug(
            f"Subprocess exited with returncode: {self._process.returncode}"
        )
        if stdout:
            self._logger.debug(f"[stdout START]:\n {stdout.decode()}\n[stdout END]")
        if stderr:
            self._logger.error(f"[stderr START]:\n {stderr.decode()}\n[stderr END]")

    async def _wait_for_messages(self):
        """TODO document"""
        self._logger.debug("_wait_for_messages")
        if self._process is None:
            self._logger.error("Failed to wait for messages, _process is None")
            return
        if self._process.stdout is None:
            self._logger.error("Failed to wait for messages, _process.stdout is None")
            return

        # TODO
        timeout = 1

        while True:
            async with self._running_lock:
                if not self._running:
                    self._logger.debug(f"Return from _wait_for_messages, running=False")
                    return

            try:
                self._logger.debug(f"_wait_for_messages - wait for {timeout}s")
                msg = await self._process.stdout.readline()
            except asyncio.TimeoutError:
                self._logger.debug("_wait_for_messages - timeout")
                continue

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                self._logger.error(f"Failed to parse message from subprocess: {e}")
                continue

            self._logger.debug(f"Received: {parsed}")

            await self.handle_process_message(parsed)

    async def handle_process_message(self, msg: dict):
        match msg["command"]:
            case "SET_LOCAL_DESCRIPTION":
                self._local_description = RTCSessionDescription(
                    msg["data"]["sdp"], msg["data"]["type"]
                )
                self._local_description_received.set()

    async def get_local_description(self) -> RTCSessionDescription:
        """TODO document"""
        await self._local_description_received.wait()
        assert self._local_description is not None
        return self._local_description

    async def stop(self) -> None:
        """TODO document"""
        self._logger.debug("STOP called in ConnectionSubprocess")
        if self._process is not None:
            self._process.terminate()
        async with self._running_lock:
            self._running = False
        asyncio.gather(*self._tasks)

    def send(self, command, data):
        """Send to main process"""
        data = json.dumps({"command": command, "data": data})
        if self._process is None:
            self._logger.error(f"Failed send {data}, _process is None")
            return
        if self._process.stdin is None:
            self._logger.error(f"Failed send {data}, _process.stdin is None")
            return

        self._logger.debug(f"Sending: {data}")
        self._process.stdin.write(data.encode("utf-8") + b"\n")

    @property
    def state(self) -> ConnectionState:
        """TODO document"""
        return self._state

    @property
    def incoming_audio(self) -> AudioTrackHandler | None:
        """TODO document"""
        # TODO implement
        raise NotImplementedError()

    @property
    def incoming_video(self) -> VideoTrackHandler | None:
        """TODO document"""
        # TODO implement
        raise NotImplementedError()

    async def add_outgoing_stream(
        self,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
        participant_summary: ParticipantSummaryDict | None,
    ) -> str:
        """TODO document"""
        # TODO implement
        raise NotImplementedError()

    async def stop_outgoing_stream(self, stream_id: str) -> bool:
        """TODO document"""
        # TODO implement
        raise NotImplementedError()


ConnectionInterface.register(ConnectionSubprocess)


async def connection_subprocess_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
    log_name_suffix: str,
) -> Tuple[RTCSessionDescription, ConnectionSubprocess]:
    """TODO document"""
    # TODO change type of offer parameter to RTCSessionDescriptionDict
    offer_dict = RTCSessionDescriptionDict(sdp=offer.sdp, type=offer.type)  # type: ignore

    connection = ConnectionSubprocess(offer_dict, message_handler, log_name_suffix)

    local_description = await connection.get_local_description()

    return (local_description, connection)
