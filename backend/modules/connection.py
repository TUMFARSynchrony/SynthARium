"""Provide the `Connection` class."""

from __future__ import annotations
from typing import Any, Callable, Coroutine, Tuple
from aiortc import (
    RTCPeerConnection,
    RTCDataChannel,
    RTCSessionDescription,
    MediaStreamTrack,
)
import json

from modules.event_handler import SimpleEventHandler
from modules.util import generate_unique_id
from modules.connection_state import ConnectionState, parse_connection_state

from custom_types.error import ErrorDict
from custom_types.message import MessageDict, is_valid_messagedict
from custom_types.connection_messages import is_valid_connection_answer_dict
from custom_types.connection_messages import (
    ConnectionOfferDict,
    RTCSessionDescriptionDict,
)


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

    _state: ConnectionState
    _state_change: SimpleEventHandler
    _main_pc: RTCPeerConnection
    _dc: RTCDataChannel | None
    _message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]]
    _incoming_audio: MediaStreamTrack | None  # AudioStreamTrack ?
    _incoming_video: MediaStreamTrack | None  # VideoStreamTrack ?

    _sub_connections: dict[str, SubConnection]

    def __init__(
        self,
        pc: RTCPeerConnection,
        message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
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
        self._sub_connections = {}
        self._state = ConnectionState.NEW
        self._state_change = SimpleEventHandler[ConnectionState]()
        self._main_pc = pc
        self._message_handler = message_handler
        self._incoming_audio = None
        self._incoming_video = None
        self._dc = None

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
        if self._dc is None:
            # TODO error handling
            return
        stringified = json.dumps(data)
        print("[Connection] Sending", stringified)
        self._dc.send(stringified)

    @property
    def state(self):
        """TODO document"""
        return self._state

    @property
    def state_change(self):
        """TODO document"""
        return self._state_change

    @property
    def incoming_audio(self):
        """Get incoming audio track."""
        return self._incoming_audio

    @property
    def incoming_video(self):
        """Get incoming video track."""
        return self._incoming_video

    async def add_outgoing_stream(
        self, video_track: MediaStreamTrack, audio_track: MediaStreamTrack
    ):
        """TODO document"""
        id = generate_unique_id(list(self._sub_connections.keys()))
        sc = SubConnection(id, self, video_track, audio_track)
        await sc.start()
        self._sub_connections[id] = sc

    async def _handle_connection_answer_message(self, data):
        """TODO document - handle incoming CONNECTION_ANSWER messages."""
        print("[Connection] received CONNECTION_ANSWER.")
        if not is_valid_connection_answer_dict(data):
            # TODO error handling
            print("[Connection] received invalid CONNECTION_ANSWER.")
            return

        id = data["id"]
        answer = data["answer"]

        sc = self._sub_connections.get(id)
        if sc is None:
            # TODO error handling
            print(f"[Connection] no SubConnection found for ID: {id}.")
            return

        try:
            answer_desc = RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
        except ValueError as err:
            # TODO error handling
            print("[Connection] Failed to parse CONNECTION_ANSWER,", err)
            return

        await sc.handle_answer(answer_desc)

    async def _on_datachannel(self, channel: RTCDataChannel):
        """Handle new incoming datachannel.

        Parameters
        ----------
        channel : aiortc.RTCDataChannel
            Incoming data channel.
        """
        print("[Connection] received datachannel")
        self._dc = channel
        self._dc.on("message", self._parse_and_handle_message)
        self._state = ConnectionState.CONNECTED
        print("[Connection] connection state is: CONNECTED")
        await self._state_change.trigger(self._state)

    async def _parse_and_handle_message(self, message: Any):
        """Handle incoming datachannel message.

        Checks if message is a valid string containting a
        custom_types.message.MessageDict JSON object.  If contents are invalid, a error
        response is send.

        Parameters
        ----------
        message : Any
            Incoming data channel message.  Ignored if type is not str.
        """
        if not isinstance(message, str):
            return

        try:
            message_dict = json.loads(message)
        except Exception as err:
            print("[Connection] Failed to parse message.", err)
            # Send error response in following if statement.
            message_dict = None

        # Handle invalid message type
        if message_dict is None or not is_valid_messagedict(message_dict):
            print("[Connection] Received message with invalid type.", message)
            err = ErrorDict(
                type="INVALID_REQUEST",
                code=400,
                description="Received message is not a valid Message object.",
            )
            response = MessageDict(type="ERROR", data=err)
            self.send(response)
            return

        if message_dict["type"] == "CONNECTION_ANSWER":
            await self._handle_connection_answer_message(message_dict["data"])
            return

        # Pass message to message handler in user.
        await self._message_handler(message_dict)

    async def _on_connection_state_change(self):
        """Handle connection state change for `_main_pc`."""
        print(
            f"[Connection] Peer Connection state change:", self._main_pc.connectionState
        )
        state = parse_connection_state(self._main_pc.connectionState)
        if state == ConnectionState.CONNECTED and self._dc is None:
            # Connection is established, but dc is not yet open.
            print("[Connection] Established connection, waiting for datachannel.")
            return
        print(f"[Connection] connection state is: {state}")
        self._state = state
        await self._state_change.trigger(state)

    def _on_track(self, track: MediaStreamTrack):
        """Handle incoming tracks.

        Parameters
        ----------
        track : aiortc.MediaStreamTrack
            Incoming track.
        """
        print(f"[Connection] {track.kind} Track received")
        if track.kind == "audio":
            self._incoming_audio = track
        elif track.kind == "video":
            self._incoming_video = track
        else:
            # TODO error handling?
            print(f"[Connection] ERROR: unknown track kind {track.kind}.")

        # TODO add modified track back
        self._main_pc.addTrack(track)

        @track.on("ended")
        def on_ended():
            """Handles tracks ended event."""
            print("[Connection] Track ended:", track.kind)


class SubConnection:
    """TODO document"""

    id: str
    connection: Connection
    pc: RTCPeerConnection

    _audio_track: MediaStreamTrack  # AudioStreamTrack ?
    _video_track: MediaStreamTrack  # VideoStreamTrack ?

    def __init__(
        self,
        id: str,
        connection: Connection,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
    ) -> None:
        """TODO document"""
        self.id = id
        self.connection = connection
        self._audio_track = audio_track
        self._video_track = video_track

        self.pc = RTCPeerConnection()
        self.pc.addTrack(video_track)
        self.pc.addTrack(audio_track)

    async def start(self):
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)

        offer = RTCSessionDescriptionDict(
            sdp=self.pc.localDescription.sdp, type=self.pc.localDescription.type  # type: ignore
        )
        connection_offer = ConnectionOfferDict(id=self.id, offer=offer)
        message = MessageDict(type="CONNECTION_OFFER", data=connection_offer)
        self.connection.send(message)

    async def handle_answer(self, answer: RTCSessionDescription):
        """TODO document"""
        await self.pc.setRemoteDescription(answer)


async def connection_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
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
