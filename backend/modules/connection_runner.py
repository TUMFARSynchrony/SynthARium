"""TODO document"""
import asyncio
import json
import logging
import sys
from typing import Any
from aiortc import RTCSessionDescription

from custom_types.message import MessageDict

from modules.connection_state import ConnectionState
from modules.connection import Connection, connection_factory


class ConnectionRunner:
    """TODO document"""

    _connection: Connection | None
    _lock: asyncio.Lock
    _running: bool
    _stopped_event: asyncio.Event
    _tasks: list[asyncio.Task]

    def __init__(self) -> None:
        """TODO document"""
        self._connection = None
        self._lock = asyncio.Lock()
        self._running = False
        self._tasks = []
        self._stopped_event = asyncio.Event()

    async def run(
        self,
        offer: RTCSessionDescription,
        log_name_suffix: str,
    ) -> None:
        """TODO document"""
        self._running = True
        answer, self._connection = await connection_factory(
            offer, self.handle_api_message, log_name_suffix
        )
        self._connection.add_listener("state_change", self._handle_state_change)
        self._send_command(
            "SET_LOCAL_DESCRIPTION", {"sdp": answer.sdp, "type": answer.type}
        )

        await self._listen_for_messages()
        logging.info("ConnectionRunner finished")

    async def stop(self) -> None:
        """TODO document"""
        logging.debug("Stopping")
        async with self._lock:
            self._running = False
        await asyncio.gather(*self._tasks)
        self._stopped_event.set()
        logging.debug("Stop complete")

    async def _listen_for_messages(self) -> None:
        """TODO document"""
        logging.debug("Listening for messages from main process")
        msg = ""
        while msg != "q":
            async with self._lock:
                if not self._running:
                    logging.debug(
                        "Stop listening for messages from main process, running is "
                        "False"
                    )
                    return
            try:
                msg = await asyncio.wait_for(self._read(), 5)
            except asyncio.TimeoutError:
                logging.debug("_listen_for_messages timeout.")
                continue

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                logging.error(f"Failed to parse message from main process: {e}")
                continue

            logging.info(f"Received command from main process: {parsed}")
            await self._handle_message(parsed)

    async def _handle_message(self, msg: dict):
        """TODO document"""
        match msg["command"]:
            case "PING":
                self._send_command("PONG", msg["data"])

    async def _read(self):
        """TODO document"""
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    async def _handle_state_change(self, state: ConnectionState) -> None:
        """TODO document"""
        self._send_command("STATE_CHANGE", state.value)
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            logging.debug(f"Stopping, because state is {state}")
            await self.stop()

    async def handle_api_message(self, message: MessageDict | Any) -> None:
        """TODO document"""
        pass

    def _send_command(self, command: str, data: str | int | float | dict) -> None:
        """Send to main process"""
        data = json.dumps({"command": command, "data": data})
        logging.info(f"Sending: {data}")
        print(data)
        sys.stdout.flush()
