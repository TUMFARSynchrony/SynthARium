"""TODO document"""

from typing import Callable, Any, Tuple
from aiortc import (
    RTCPeerConnection,
    RTCDataChannel,
    RTCSessionDescription,
    MediaStreamTrack
)

from _types.message import MessageDict


class Connection():
    """TODO document"""
    _pc: RTCPeerConnection
    _dc: RTCDataChannel
    _message_handler: Callable[[MessageDict], None]

    def __init__(self, pc: RTCPeerConnection,
                 message_handler: Callable[[MessageDict], None]):
        """TODO document"""
        self._pc = pc
        self._message_handler = message_handler

        # Register event handlers
        pc.on("datachannel", f=self._on_datachannel)
        pc.on("connectionstatechange", f=self._on_connection_state_change)
        pc.on("track", f=self._on_track)

    def send(self, data):
        """TODO document"""
        pass

    def _on_datachannel(self, channel: RTCDataChannel):
        """TODO document"""
        print("[CONNECTION]: datachannel")

        @channel.on("message")
        def on_message(message):
            """TODO document"""
            print("[CONNECTION]: message:", message)
            self._message_handler(message)

    def _on_connection_state_change(self):
        """TODO document"""
        print(f"[CONNECTION] Connection state is {self._pc.connectionState}")

    def _on_track(self, track: MediaStreamTrack):
        """TODO document"""
        print(f"[CONNECTION] {track.kind} Track received")


async def connection_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], None]
) -> Tuple[RTCSessionDescription, Connection]:
    """TODO document"""
    pc = RTCPeerConnection()
    connection = Connection(pc, message_handler)

    # handle offer
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)  # type: ignore

    return (pc.localDescription, connection)
