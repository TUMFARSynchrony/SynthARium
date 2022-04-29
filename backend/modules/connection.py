"""TODO document"""

import json
from typing import Callable, Tuple
from aiortc import (
    RTCPeerConnection,
    RTCDataChannel,
    RTCSessionDescription,
    MediaStreamTrack,
)

from modules.util import check_valid_typed_dict

from custom_types.error import ErrorDict
from custom_types.message import MessageDict


class Connection:
    """TODO document"""

    _main_pc: RTCPeerConnection
    _dc: RTCDataChannel
    _message_handler: Callable[[MessageDict], None]
    _incoming_audio: MediaStreamTrack | None  # AudioStreamTrack ?
    _incoming_video: MediaStreamTrack | None  # VideoStreamTrack ?

    def __init__(
        self, pc: RTCPeerConnection, message_handler: Callable[[MessageDict], None]
    ):
        """TODO document"""
        self._main_pc = pc
        self._message_handler = message_handler
        self._incoming_audio = None
        self._incoming_video = None

        # Register event handlers
        pc.on("datachannel", f=self._on_datachannel)
        pc.on("connectionstatechange", f=self._on_connection_state_change)
        pc.on("track", f=self._on_track)

    def send(self, data):
        stringified = json.dumps(data)
        print("[Connection] Sending", stringified)
        self._dc.send(stringified)

    @property
    def incoming_audio(self):
        """Get incoming audio track."""
        return self._incoming_audio

    @property
    def incoming_video(self):
        """Get incoming video track."""
        return self._incoming_video

    def add_outgoing_stream(
        self, video_track: MediaStreamTrack, audio_track: MediaStreamTrack
    ):
        """TODO document"""
        pass

    def _on_datachannel(self, channel: RTCDataChannel):
        """TODO document"""
        print("[CONNECTION]: datachannel")
        self._dc = channel
        self._dc.on("message", self._handle_message)

    def _handle_message(self, message):
        """TODO document"""
        if not isinstance(message, str):
            return

        try:
            message_obj = json.loads(message)
        except Exception as err:
            print("[CONNECTION] Failed to parse message.", err)
            # Send error response in following if statement.
            message_obj = None

        # Handle invalid message type
        if message_obj is None or not check_valid_typed_dict(message_obj, MessageDict):
            print("[CONNECTION] Received message with invalid type.", message)
            err = ErrorDict(
                type="INVALID_REQUEST",
                code=400,
                description="Received message is not a valid Message object.",
            )
            response = MessageDict(type="ERROR", data=err)
            self.send(response)
            return

        # Pass message to message handler in user.
        self._message_handler(message_obj)

    def _on_connection_state_change(self):
        """TODO document"""
        print(f"[CONNECTION] Connection state is {self._main_pc.connectionState}")

    def _on_track(self, track: MediaStreamTrack):
        """TODO document"""
        print(f"[CONNECTION] {track.kind} Track received")
        if track.kind == "audio":
            self._incoming_audio = track
        elif track.kind == "video":
            self._incoming_video = track
        else:
            # TODO error handling?
            print(f"[CONNECTION] ERROR: unknown track kind {track.kind}.")

        # TODO add modified track back
        self._main_pc.addTrack(track)

        @track.on("ended")
        def on_ended():
            print("[CONNECTION] Track ended:", track.kind)


async def connection_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], None],
) -> Tuple[RTCSessionDescription, Connection]:
    """TODO document"""
    pc = RTCPeerConnection()
    connection = Connection(pc, message_handler)

    # handle offer
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)  # type: ignore

    return (pc.localDescription, connection)
