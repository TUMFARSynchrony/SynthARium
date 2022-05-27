"""Provide the `Connection` class."""

from __future__ import annotations
from typing import Any, Callable, Coroutine, Tuple
from aiortc import (
    RTCPeerConnection,
    RTCDataChannel,
    RTCSessionDescription,
    MediaStreamTrack,
    RTCRtpSender,
)
from pyee.asyncio import AsyncIOEventEmitter
import asyncio
import json

from modules.tracks import AudioTrackHandler, VideoTrackHandler
from modules.util import generate_unique_id
from modules.connection_state import ConnectionState, parse_connection_state

from custom_types.error import ErrorDict
from custom_types.message import MessageDict, is_valid_messagedict
from custom_types.connection_messages import is_valid_connection_answer_dict
from custom_types.connection_messages import (
    ConnectionOfferDict,
    RTCSessionDescriptionDict,
)


class Connection(AsyncIOEventEmitter):
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

    _stopped: bool
    _state: ConnectionState
    _main_pc: RTCPeerConnection
    _dc: RTCDataChannel | None
    _message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]]
    _incoming_audio: AudioTrackHandler | None
    _incoming_video: VideoTrackHandler | None

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
        super().__init__()
        self._stopped = False
        self._sub_connections = {}
        self._state = ConnectionState.NEW
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
        if self._stopped:
            return
        self._stopped = True
        print("[Connection] Stopping")

        if self._state not in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            self._set_state(ConnectionState.CLOSED)

        # Close all SubConnections
        tasks = []
        for sc in self._sub_connections.values():
            tasks.append(sc.stop())
        await asyncio.gather(*tasks)

        # Close main connection
        if self._dc is not None:
            self._dc.close()
        if self._incoming_video is not None:
            self._incoming_video.stop()
        if self._incoming_audio is not None:
            self._incoming_audio.stop()
        await self._main_pc.close()
        self.remove_all_listeners()

    def send(self, data: MessageDict | dict) -> None:
        """Send `data` to peer over the datachannel.

        Parameters
        ----------
        data : MessageDict or dict
            Data that will be stringified and send to the peer.
        """
        if self._dc is None or self._dc.readyState != "open":
            # TODO error handling
            print(
                "[Connection] WARN: Not sending data because datachannel is not open."
            )
            return
        stringified = json.dumps(data)
        print("[Connection] Sending", stringified)
        self._dc.send(stringified)

    @property
    def state(self):
        """TODO document"""
        return self._state

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
    ) -> str:
        """TODO document"""
        stream_id = generate_unique_id(list(self._sub_connections.keys()))
        sc = SubConnection(stream_id, self, video_track, audio_track)
        sc.add_listener("connection_closed", self._handle_closed_subconnection)
        await sc.start()
        self._sub_connections[stream_id] = sc
        return stream_id

    async def stop_outgoing_stream(self, stream_id: str):
        """TODO document"""
        if stream_id not in self._sub_connections:
            return False

        sub_connection = self._sub_connections[stream_id]
        await sub_connection.stop()
        return True

    async def _handle_closed_subconnection(self, subconnection_id: str):
        """TODO document"""
        print("[Connection] Remove sub connection", subconnection_id)
        self._sub_connections.pop(subconnection_id)
        print("[Connection] Sub connections after removing:", self._sub_connections)

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

    def _on_datachannel(self, channel: RTCDataChannel):
        """Handle new incoming datachannel.

        Parameters
        ----------
        channel : aiortc.RTCDataChannel
            Incoming data channel.
        """
        print("[Connection] received datachannel")
        # TODO check channel readyState
        self._dc = channel
        self._dc.on("message", self._parse_and_handle_message)
        self._dc.on("close", self._handle_datachannel_close)
        self._set_state(ConnectionState.CONNECTED)

    async def _handle_datachannel_close(self):
        """TODO document"""
        print("[Connection] Datachannel closed")
        await self._check_if_closed()

    async def _check_if_closed(self):
        """TODO document"""
        incoming_audio = self._incoming_audio
        incoming_video = self._incoming_video
        if (
            self._dc is not None
            and self._dc.readyState == "closed"
            and (incoming_audio is not None and incoming_audio.readyState == "ended")
            and (incoming_video is not None and incoming_video.readyState == "ended")
        ):
            print("[Connection] datachannel and all incoming tracks are closed")
            await self.stop()

    async def _parse_and_handle_message(self, message: Any):
        """Handle incoming datachannel message.

        Checks if message is a valid string containing a
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

    def _on_connection_state_change(self):
        """Handle connection state change for `_main_pc`."""
        print(
            f"[Connection] Peer Connection state change:", self._main_pc.connectionState
        )
        state = parse_connection_state(self._main_pc.connectionState)
        if state == ConnectionState.CONNECTED and self._dc is None:
            # Connection is established, but dc is not yet open.
            print("[Connection] Established connection, waiting for datachannel.")
            return
        self._set_state(state)

    def _set_state(self, state: ConnectionState):
        """TODO document"""
        if self._state == state:
            return

        print(f"[Connection] connection state is: {state}")
        self._state = state
        self.emit("state_change", state)

    def _on_track(self, track: MediaStreamTrack):
        """Handle incoming tracks.

        Parameters
        ----------
        track : aiortc.MediaStreamTrack
            Incoming track.
        """
        print(f"[Connection] {track.kind} Track received")
        if track.kind == "audio":
            self._incoming_audio = AudioTrackHandler(track)
            sender = self._main_pc.addTrack(self._incoming_audio.subscribe())
            self._listen_to_track_close(self._incoming_audio, sender)
        elif track.kind == "video":
            self._incoming_video = VideoTrackHandler(track)
            sender = self._main_pc.addTrack(self._incoming_video.subscribe())
            self._listen_to_track_close(self._incoming_video, sender)
        else:
            # TODO error handling?
            print(f"[Connection] ERROR: unknown track kind {track.kind}.")

        @track.on("ended")
        def on_ended():
            """Handles tracks ended event."""
            print("[Connection] Track ended:", track.kind)

    def _listen_to_track_close(
        self, track: AudioTrackHandler | VideoTrackHandler, sender: RTCRtpSender
    ):
        """TODO document"""

        @track.on("ended")
        async def _close_audio_sender():
            for transceiver in self._main_pc.getTransceivers():
                if transceiver.sender is sender:
                    print("[Connection] Found transceiver, closing")
                    await transceiver.stop()
                    break
            await self._check_if_closed()


class SubConnection(AsyncIOEventEmitter):
    """TODO document"""

    id: str
    connection: Connection
    _pc: RTCPeerConnection

    _audio_track: MediaStreamTrack  # AudioStreamTrack ?
    _video_track: MediaStreamTrack  # VideoStreamTrack ?

    _closed: bool

    def __init__(
        self,
        id: str,
        connection: Connection,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
    ) -> None:
        """TODO document"""
        super().__init__()
        self.id = id
        self.connection = connection
        self._audio_track = audio_track
        self._video_track = video_track
        self._closed = False

        self._pc = RTCPeerConnection()
        self._pc.addTrack(video_track)
        self._pc.addTrack(audio_track)
        self._pc.on("connectionstatechange", f=self._on_connection_state_change)

        # Stop SubConnection if one of the tracks ends
        # audio_track.on("ended", self.stop)
        # video_track.on("ended", self.stop)

    async def start(self):
        """TODO document"""
        offer = await self._pc.createOffer()
        await self._pc.setLocalDescription(offer)

        offer = RTCSessionDescriptionDict(
            sdp=self._pc.localDescription.sdp, type=self._pc.localDescription.type  # type: ignore
        )
        connection_offer = ConnectionOfferDict(id=self.id, offer=offer)
        message = MessageDict(type="CONNECTION_OFFER", data=connection_offer)
        self.connection.send(message)

    async def stop(self):
        """TODO document"""
        if self._closed:
            return

        self._audio_track.stop()
        self._video_track.stop()

        print(f"[SubConnection - {self.id}] Closing")
        self._closed = True
        await self._pc.close()
        self.emit("connection_closed", self.id)
        self.remove_all_listeners()

    async def handle_answer(self, answer: RTCSessionDescription):
        """TODO document"""
        await self._pc.setRemoteDescription(answer)

    async def _on_connection_state_change(self):
        """Handle connection state change."""
        print(
            f"[SubConnection - {self.id}] Peer Connection state change:",
            self._pc.connectionState,
        )
        if self._pc.connectionState in ["closed", "failed"]:
            await self.stop()


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
