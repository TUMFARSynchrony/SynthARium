"""Provide the `Connection` and `SubConnection` classes."""

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
from custom_types.participant_summary import ParticipantSummaryDict
from custom_types.connection import (
    is_valid_connection_answer_dict,
    RTCSessionDescriptionDict,
    ConnectionOfferDict,
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
        """Stop this connection.

        Stopps all incoming and outgoing streams and emits the `state_change` event.
        When finished, it removes all event listeners from this Connection, as no more
        events will be emitted.
        """
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

    async def send(self, data: MessageDict | dict) -> None:
        """Send `data` to peer over the datachannel.

        Parameters
        ----------
        data : MessageDict or dict
            Data that will be stringified and send to the peer.
        """
        if self._dc is None or self._dc.readyState != "open":
            print(
                "[Connection] WARN: Not sending data because datachannel is not open."
            )
            await self._set_failed_state_and_close()
            return
        stringified = json.dumps(data)
        print("[Connection] Sending", stringified)
        self._dc.send(stringified)

    @property
    def state(self) -> ConnectionState:
        """Get the modules.connection_state.ConnectionState the Connection is in."""
        return self._state

    @property
    def incoming_audio(self) -> AudioTrackHandler | None:
        """Get incoming audio track.

        Returns
        -------
        modules.track.AudioTrackHandler or None
            None if no audio was received by client (yet), otherwise AudioTrackHandler.
        """
        return self._incoming_audio

    @property
    def incoming_video(self) -> VideoTrackHandler | None:
        """Get incoming video track.

        Returns
        -------
        modules.track.VideoTrackHandler or None
            None if no video was received by client (yet), otherwise VideoTrackHandler.
        """
        return self._incoming_video

    async def add_outgoing_stream(
        self,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
        participant_summary: ParticipantSummaryDict | None,
    ) -> str:
        """Add a outgoing stream to this Connection.

        Starts a new modules.connection.SubConnection with `video_track`, `audio_track`
        and `participant_summary`.

        Parameters
        ----------
        video_track : MediaStreamTrack
            Video that will be used in the new SubConnection.
        audio_track : MediaStreamTrack
            Audio that will be used in the new SubConnection.
        participant_summary : ParticipantSummaryDict or None
            Optional participant summary that will be send to the client, informing it
            about the details of the new stream.

        Returns
        -------
        str
            A new ID that identifies the new outgoing stream / SubConnection. It can be
            used to close the stream / SubConnection again using
            `stop_outgoing_stream()`.
        """
        subconnection_id = generate_unique_id(list(self._sub_connections.keys()))
        sc = SubConnection(
            subconnection_id, self, video_track, audio_track, participant_summary
        )
        sc.add_listener("connection_closed", self._handle_closed_subconnection)
        await sc.start()
        self._sub_connections[subconnection_id] = sc
        return subconnection_id

    async def stop_outgoing_stream(self, stream_id: str) -> bool:
        """Stop the outgoing stream with `stream_id`.

        Parameters
        ----------
        stream_id : str
            ID of the outgoing stream / SubConnection that will be stopped.

        Returns
        -------
        bool
            True if a outgoing stream with `stream_id` was found and closed. Otherwise
            False.

        See Also
        --------
        add_outgoing_stream : add a new outgoing stream / SubConnection.
        """
        if stream_id not in self._sub_connections:
            return False

        sub_connection = self._sub_connections[stream_id]
        await sub_connection.stop()
        return True

    async def _handle_closed_subconnection(self, subconnection_id: str) -> None:
        """Remove a closed SubConnection from Connection."""
        print("[Connection] Remove sub connection", subconnection_id)
        self._sub_connections.pop(subconnection_id)
        print("[Connection] Sub connections after removing:", self._sub_connections)

    async def _handle_connection_answer_message(self, data) -> None:
        """Handle incoming `CONNECTION_ANSWER` messages.

        See Also
        --------
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol :
            Connection protocol wiki.
        """
        print("[Connection] received CONNECTION_ANSWER.")
        if not is_valid_connection_answer_dict(data):
            print("[Connection] Received invalid CONNECTION_ANSWER.")
            await self._set_failed_state_and_close()
            return

        id = data["id"]
        answer = data["answer"]

        sc = self._sub_connections.get(id)
        if sc is None:
            print(
                "[Connection] Invalid CONNECTION_ANSWER: No SubConnection found for "
                f"ID: {id}."
            )
            await self._set_failed_state_and_close()
            return

        try:
            answer_desc = RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
        except ValueError as err:
            print("[Connection] Failed to parse CONNECTION_ANSWER:", err)
            await self._set_failed_state_and_close()
            return

        await sc.handle_answer(answer_desc)

    def _on_datachannel(self, channel: RTCDataChannel) -> None:
        """Handle new incoming datachannel.

        Parameters
        ----------
        channel : aiortc.RTCDataChannel
            Incoming data channel.
        """
        print("[Connection] received datachannel")
        self._dc = channel
        self._dc.on("message", self._parse_and_handle_message)
        self._dc.on("close", self._handle_datachannel_close)
        self._set_state(ConnectionState.CONNECTED)

    async def _handle_datachannel_close(self) -> None:
        """Handle the `close` event on datachannel."""
        print("[Connection] Datachannel closed")
        await self._check_if_closed()

    async def _check_if_closed(self) -> None:
        """Check if this Connection is closed and should stop."""
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

    async def _parse_and_handle_message(self, message: Any) -> None:
        """Parse, check and forward incoming datachannel message.

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
            await self.send(response)
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
        """Set connection state and emit `state_change` event."""
        if self._state == state:
            return

        print(f"[Connection] connection state is: {state}")
        self._state = state
        self.emit("state_change", state)

    async def _set_failed_state_and_close(self) -> None:
        """Sets the state to `FAILED` and closes the Connection."""
        self._set_state(ConnectionState.FAILED)
        await self.stop()

    def _on_track(self, track: MediaStreamTrack):
        """Handle incoming tracks.

        Parameters
        ----------
        track : aiortc.MediaStreamTrack
            Incoming track.

        Note
        ----
        This function can not be asynchronous, otherwise it will no longer function
        correctly.
        """
        print(f"[Connection] {track.kind} track received")
        if track.kind == "audio":
            self._incoming_audio = AudioTrackHandler(track)
            sender = self._main_pc.addTrack(self._incoming_audio.subscribe())
            self._listen_to_track_close(self._incoming_audio, sender)
        elif track.kind == "video":
            self._incoming_video = VideoTrackHandler(track)
            sender = self._main_pc.addTrack(self._incoming_video.subscribe())
            self._listen_to_track_close(self._incoming_video, sender)
        else:
            print(
                f"[Connection] ERROR: unknown track kind {track.kind}. Ignoring track."
            )
            return

        @track.on("ended")
        def _on_ended():
            """Handles tracks ended event."""
            print("[Connection] Track ended:", track.kind)

    def _listen_to_track_close(
        self, track: AudioTrackHandler | VideoTrackHandler, sender: RTCRtpSender
    ):
        """Add a handler to the `ended` event on `track` that closes its transceiver.

        Parameters
        ----------
        track : modules.track.AudioTrackHandler or modules.track.VideoTrackHandler
            Track to listen to the `ended` event.
        sender : aiortc.RTCRtpSender
            Sender of the track.  Used to find the correct transceiver.
        """

        @track.on("ended")
        async def _close_transceiver():
            """Find and close the correct transceiver for `sender`."""
            for transceiver in self._main_pc.getTransceivers():
                if transceiver.sender is sender:
                    print("[Connection] Found transceiver, closing")
                    await transceiver.stop()
                    break
            await self._check_if_closed()


class SubConnection(AsyncIOEventEmitter):
    """SubConnection used to send additional stream to a client.

    Each SubConnection has a audio and video track -> one stream which they send to the
    client.  For communication it used the datachannel of the parent
    module.connection.Connection.
    """

    id: str
    connection: Connection
    _participant_summary: ParticipantSummaryDict | None
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
        participant_summary: ParticipantSummaryDict | None,
    ) -> None:
        """Initialize new SubConnection.

        Parameters
        ----------
        id : str
        connection : modules.connection.Connection
            Parent connection, used for communication.
        video_track : aiortc.MediaStreamTrack
            Video track that will be send in this SubConnection.
        audio_track : aiortc.MediaStreamTrack
            Audio track that will be send in this SubConnection.
        participant_summary : None or custom_types.participant_summary.ParticipantSummaryDict
            Participant summary send to the client with the initial offer.
        """
        super().__init__()
        self.id = id
        self.connection = connection
        self._audio_track = audio_track
        self._video_track = video_track
        self._closed = False
        self._participant_summary = participant_summary

        self._pc = RTCPeerConnection()
        self._pc.addTrack(video_track)
        self._pc.addTrack(audio_track)
        self._pc.on("connectionstatechange", f=self._on_connection_state_change)

        # Stop SubConnection if one of the tracks ends
        # audio_track.on("ended", self.stop)
        # video_track.on("ended", self.stop)

    async def start(self) -> None:
        """Start the SubConnection.

        Sends the initial `CONNECTION_OFFER` message to the client.

        See Also
        --------
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol :
            Connection protocol wiki.
        """
        offer = await self._pc.createOffer()
        await self._pc.setLocalDescription(offer)

        offer = RTCSessionDescriptionDict(
            sdp=self._pc.localDescription.sdp, type=self._pc.localDescription.type  # type: ignore
        )
        connection_offer = ConnectionOfferDict(
            id=self.id, offer=offer, participant_summary=self._participant_summary
        )
        message = MessageDict(type="CONNECTION_OFFER", data=connection_offer)
        await self.connection.send(message)

    async def stop(self) -> None:
        """Stop the SubConnection and its associated tracks.

        Emits a `connection_closed` event with the ID of this SubConnection.  When
        finished, it removes all event listeners from this Connection, as no more events
        will be emitted.
        """
        if self._closed:
            return
        self.emit("connection_closed", self.id)

        self._audio_track.stop()
        self._video_track.stop()

        print(f"[SubConnection - {self.id}] Closing")
        self._closed = True
        await self._pc.close()
        self.remove_all_listeners()

    async def handle_answer(self, answer: RTCSessionDescription):
        """Handle a `CONNECTION_ANSWER` message for this SubConnection.

        Parameters
        ----------
        answer : aiortc.RTCSessionDescription
            Answer to the initial offer by this SubConnection.
        """
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
