import asyncio
import json
import logging
import sys
import time
from typing import Any, Callable, Coroutine
from aiortc import RTCSessionDescription

from custom_types.message import MessageDict

from modules.connection_state import ConnectionState
from modules.connection import Connection, connection_factory


class ConnectionRunner:
    _connection: Connection | None
    _lock: asyncio.Lock
    _running: bool
    _stopped_event: asyncio.Event
    _tasks: list[asyncio.Task]

    def __init__(self) -> None:
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
        self._running = True
        answer, self._connection = await connection_factory(
            offer, self.handle_api_message, log_name_suffix
        )
        self._connection.add_listener("state_change", self._handle_state_change)
        self.send("SET_LOCAL_DESCRIPTION", {"sdp": answer.sdp, "type": answer.type})
        logging.info("Wait for _stopped_event")
        await self._listen_for_messages()

    async def stop(self) -> None:
        logging.debug("Exiting")
        async with self._lock:
            self._running = False
        await asyncio.gather(*self._tasks)
        logging.debug("Set _stopped_event")
        self._stopped_event.set()
        logging.debug("Exit complete")

    async def _listen_for_messages(self):
        msg = ""
        while msg != "q":
            async with self._lock:
                if not self._running:
                    return
            try:
                msg = await asyncio.wait_for(self._read(), 5)
            except asyncio.TimeoutError:
                logging.debug("_listen_for_messages timeout.")
                continue

            try:
                parsed = json.loads(msg)
            except (json.JSONDecodeError, TypeError) as e:
                logging.error(f"Failed to parse message from subprocess: {e}")
                continue

            logging.info(f"_listen_for_messages Received {parsed}")
            if parsed["command"] == "PING":
                t = round(time.time() * 1000)
                self.send("ECHO", {"time": t, "diff": t - parsed["time"]})
            else:
                self.send("ECHO", parsed)

        logging.info("connection_subprocess finished")

    async def _read(self):
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    async def _handle_state_change(self, state: ConnectionState) -> None:
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            await self.stop()

    async def handle_api_message(self, message: MessageDict | Any) -> None:
        pass

    def send(self, command, data):
        """Send to main process"""
        data = json.dumps({"command": command, "data": data})
        logging.info(f"Sending: {data}")
        print(data)
        sys.stdout.flush()
