"""This module provides the Connection class."""

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
    """Connection with a single client.

    Manages one or multiple WebRTC connections with the same client.  Provides interface
    unaffected by the number of actual connections.

    Notes
    -----
    The sequence should be something like this:

    Receive offer -> create Connection (adds event listeners for tracks, datachannel
    etc.) -> set remote description -> create answer -> set local description -> send
    answer to peer.

    This is not intended as a guide to aiortc / WebRTC, just as a reference when to
    create the Connection instance.

    See Also
    --------
    connection_factory : use to create new Connection and answer for an WebRTC offer.
    """

    _main_pc: RTCPeerConnection
    _dc: RTCDataChannel
    _message_handler: Callable[[MessageDict], None]
    _incoming_audio: MediaStreamTrack | None  # AudioStreamTrack ?
    _incoming_video: MediaStreamTrack | None  # VideoStreamTrack ?

    def __init__(
        self, pc: RTCPeerConnection, message_handler: Callable[[MessageDict], None]
    ) -> None:
        """Create new Connection based on a aiortc.RTCPeerConnection.

        Add event listeners to `pc`.  Should be donne the remote description of `pc` is
        set.

        Parameters
        ----------
        pc : aiortc.RTCPeerConnection
            WebRTC peer connection.
        message_handler : function (custom_typed.message.MessageDict) -> None
            Handler for incoming messages over the datachannel.  Incoming messages will
            be parsed and type checked (only top level, not including contents of data).

        See Also
        --------
        connection_factory : use to create new Connection and answer for an WebRTC
            offer.
        """
        self._main_pc = pc
        self._message_handler = message_handler
        self._incoming_audio = None
        self._incoming_video = None

        # Register event handlers
        pc.on("datachannel", f=self._on_datachannel)
        pc.on("connectionstatechange", f=self._on_connection_state_change)
        pc.on("track", f=self._on_track)

    async def stop(self) -> None:
        """Stop this connection.  Use for cleanup."""
        if self._main_pc:
            await self._main_pc.close()

    def send(self, data: MessageDict | dict) -> None:
        """Send `data` to peer over the datachannel.

        Parameters
        ----------
        data : MessageDict or dict
            Data that will be stringified and send to the peer.
        """
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
        """Handle new incoming datachannel.

        Parameters
        ----------
        channel : aiortc.RTCDataChannel
            Incoming data channel.
        """
        print("[CONNECTION]: datachannel")
        self._dc = channel
        self._dc.on("message", self._handle_message)

    def _handle_message(self, message: str):
        """Handle incoming datachannel message.

        Checks if message is a valid string containting a
        custom_types.message.MessageDict JSON object.  If contents are invalid, a error
        response is send.

        Parameters
        ----------
        message : str
            Incoming data channel message.
        """
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
        """Handle connection state change for `_main_pc`."""
        print(f"[CONNECTION] Connection state is {self._main_pc.connectionState}")

    def _on_track(self, track: MediaStreamTrack):
        """Handle incoming tracks.

        Parameters
        ----------
        track : aiortc.MediaStreamTrack
            Incoming track.
        """
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
            """Handles tracks ended event."""
            print("[CONNECTION] Track ended:", track.kind)


async def connection_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], None],
) -> Tuple[RTCSessionDescription, Connection]:
    """Instantiate Connection.

    Parameters
    ----------
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.
    message_handler : function (message: custom_types.message.MessageDict) -> None
        Message handler for Connection.  Connection will pass parsed MessageDicts to
        this handler.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.connection.Connection
        WebRTC answer that should be send back to the client and a Connection.
    """
    pc = RTCPeerConnection()
    connection = Connection(pc, message_handler)

    # handle offer
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)  # type: ignore

    return (pc.localDescription, connection)
