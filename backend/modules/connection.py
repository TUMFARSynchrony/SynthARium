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
import shortuuid
import asyncio
import logging
import json

from modules.connection_interface import ConnectionInterface
from modules.tracks import AudioTrackHandler, VideoTrackHandler
from modules.connection_state import ConnectionState, parse_connection_state

from custom_types.error import ErrorDict
from custom_types.message import MessageDict, is_valid_messagedict
from custom_types.participant_summary import ParticipantSummaryDict
from custom_types.connection import (
    RTCSessionDescriptionDict,
    ConnectionOfferDict,
    ConnectionAnswerDict,
)


class Connection(ConnectionInterface):
    """Connection with a single client using multiple sub-connections.

    Implements modules.connection_interface.ConnectionInterface.

    Extends AsyncIOEventEmitter, providing the following events:
    - `state_change` : modules.connection_state.ConnectionState
        Emitted when the state of this connection changes.
    - `tracks_complete` : tuple of modules.track.VideoTrackHandler and modules.track.AudioTrackHandler
        Emitted when both tracks are received from the client and ready to be
        distributed / subscribed to.

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

    _log_name_suffix: str
    _stopped: bool
    _state: ConnectionState
    _main_pc: RTCPeerConnection
    _dc: RTCDataChannel | None
    _message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]]
    _incoming_audio: AudioTrackHandler
    _incoming_video: VideoTrackHandler
    _sub_connections: dict[str, SubConnection]

    def __init__(
        self,
        pc: RTCPeerConnection,
        message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
        log_name_suffix: str,
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
        log_name_suffix : str
            Suffix for logger.  Format: Connection-<log_name_suffix>.

        See Also
        --------
        connection_factory : use to create new Connection and answer for an WebRTC
            offer.
        """
        super().__init__()
        self._logger = logging.getLogger(f"Connection-{log_name_suffix}")
        self._stopped = False
        self._log_name_suffix = log_name_suffix
        self._sub_connections = {}
        self._state = ConnectionState.NEW
        self._main_pc = pc
        self._message_handler = message_handler
        self._incoming_audio = AudioTrackHandler()
        self._incoming_video = VideoTrackHandler()
        self._dc = None

        # Register event handlers
        pc.on("datachannel", f=self._on_datachannel)
        pc.on("connectionstatechange", f=self._on_connection_state_change)
        pc.on("track", f=self._on_track)

    def __str__(self) -> str:
        """Get string representation of this Connection."""
        return f"state={self._state}"

    def __repr__(self) -> str:
        """Get representation of this Connection obj."""
        return (
            f"Connection({str(self)}, logger_name=Connection-{self._log_name_suffix})"
        )

    async def stop(self) -> None:
        # For docstring see ConnectionInterface or hover over function declaration
        if self._stopped:
            return
        self._stopped = True
        self._logger.debug("Stopping Connection")

        if self._state not in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            self._set_state(ConnectionState.CLOSED)

        # Close all SubConnections
        coros: list[Coroutine] = []
        for sc in self._sub_connections.values():
            coros.append(sc.stop())
        await asyncio.gather(*coros)

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
        # For docstring see ConnectionInterface or hover over function declaration
        if self._dc is None or self._dc.readyState != "open":
            self._logger.warning("Can not send data because datachannel is not open")
            await self._set_failed_state_and_close()
            return
        stringified = json.dumps(data)
        self._logger.debug(f"Sending data: {stringified}")
        self._dc.send(stringified)

    @property
    def state(self) -> ConnectionState:
        # For docstring see ConnectionInterface or hover over function declaration
        return self._state

    async def create_subscriber_offer(
        self, participant_summary: ParticipantSummaryDict | None
    ) -> ConnectionOfferDict:
        # For docstring see ConnectionInterface or hover over function declaration

        subconnection_id = shortuuid.uuid()
        sc = SubConnection(
            subconnection_id,
            self._incoming_video.subscribe(),
            self._incoming_audio.subscribe(),
            participant_summary,
            self._log_name_suffix,
        )
        sc.add_listener("connection_closed", self._handle_closed_subconnection)
        self._sub_connections[subconnection_id] = sc
        offer = await sc.generate_offer()
        return offer

    async def handle_subscriber_answer(self, answer: ConnectionAnswerDict) -> None:
        # For docstring see ConnectionInterface or hover over function declaration
        subconnection_id = answer["id"]
        sc = self._sub_connections.get(subconnection_id)
        if sc is None:
            # TODO error handling
            self._logger.error(f"SubConnection for ID: {subconnection_id} not found.")
            return

        answer_description = RTCSessionDescription(
            answer["answer"]["sdp"], answer["answer"]["type"]
        )
        await sc.handle_answer(answer_description)

    async def stop_subconnection(self, subconnection_id: str) -> bool:
        # For docstring see ConnectionInterface or hover over function declaration
        if subconnection_id not in self._sub_connections:
            return False

        sub_connection = self._sub_connections[subconnection_id]
        await sub_connection.stop()
        return True

    async def set_muted(self, video: bool, audio: bool) -> None:
        # For docstring see ConnectionInterface or hover over function declaration
        if self._incoming_video is not None:
            self._incoming_video.muted = video
        if self._incoming_audio is not None:
            self._incoming_audio.muted = audio

    async def _handle_closed_subconnection(self, subconnection_id: str) -> None:
        """Remove a closed SubConnection from Connection."""
        self._logger.debug(f"Remove sub connection {subconnection_id}")
        self._sub_connections.pop(subconnection_id)
        self._logger.debug(f"SubConnections after removing: {self._sub_connections}")

    def _on_datachannel(self, channel: RTCDataChannel) -> None:
        """Handle new incoming datachannel.

        Parameters
        ----------
        channel : aiortc.RTCDataChannel
            Incoming data channel.
        """
        self._logger.debug("Received datachannel")
        self._dc = channel
        self._dc.on("message", self._parse_and_handle_message)
        self._dc.on("close", self._handle_datachannel_close)
        self._set_state(ConnectionState.CONNECTED)

    async def _handle_datachannel_close(self) -> None:
        """Handle the `close` event on datachannel."""
        self._logger.debug("Datachannel closed")
        await self._check_if_closed()

    async def _check_if_closed(self) -> None:
        """Check if this Connection is closed and should stop."""
        if (
            self._incoming_audio is not None
            and self._incoming_video is not None
            and self._incoming_audio.readyState == "ended"
            and self._incoming_video.readyState == "ended"
        ):
            self._logger.debug("All incoming tracks are closed -> stop connection")
            await self.stop()

        if self._dc is not None and self._dc.readyState == "closed":
            self._logger.debug("Datachannel closed -> stop connection")
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
            self._logger.warning(f"Failed to parse message. Error: {err}")
            # Send error response in following if statement.
            message_dict = None

        # Handle invalid message type
        if message_dict is None or not is_valid_messagedict(message_dict):
            self._logger.info(f"Received invalid message.")
            self._logger.debug(f"Invalid message: {message}")
            err = ErrorDict(
                type="INVALID_REQUEST",
                code=400,
                description="Received message is not a valid Message object.",
            )
            response = MessageDict(type="ERROR", data=err)
            await self.send(response)
            return

        # Pass message to message handler in user.
        await self._message_handler(message_dict)

    def _on_connection_state_change(self):
        """Handle connection state change for `_main_pc`."""
        self._logger.debug(
            f"Peer Connection state change: {self._main_pc.connectionState}"
        )
        state = parse_connection_state(self._main_pc.connectionState)
        if state == ConnectionState.CONNECTED and self._dc is None:
            # Connection is established, but dc is not yet open.
            self._logger.debug("Established connection, waiting for datachannel")
            return
        self._set_state(state)

    def _set_state(self, state: ConnectionState):
        """Set connection state and emit `state_change` event."""
        if self._state == state:
            return

        self._logger.debug(f"Connection state is: {state}")
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
        self._logger.debug(f"{track.kind} track received")
        if track.kind == "audio":
            self._incoming_audio.track = track
            sender = self._main_pc.addTrack(self._incoming_audio.subscribe())
            self._listen_to_track_close(self._incoming_audio, sender)
        elif track.kind == "video":
            self._incoming_video.track = track
            sender = self._main_pc.addTrack(self._incoming_video.subscribe())
            self._listen_to_track_close(self._incoming_video, sender)
        else:
            self._logger.error(f"Unknown track kind {track.kind}. Ignoring track")
            return

        if self._incoming_audio is not None and self._incoming_video is not None:
            self.emit("tracks_complete", (self._incoming_video, self._incoming_audio))

        @track.on("ended")
        def _on_ended():
            """Handles tracks ended event."""
            self._logger.debug(f"{track.kind} track ended")

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
                    self._logger.debug("Found transceiver, closing")
                    await transceiver.stop()
                    break
            await self._check_if_closed()


ConnectionInterface.register(Connection)


class SubConnection(AsyncIOEventEmitter):
    """SubConnection used to send additional stream to a client.

    Each SubConnection has a audio and video track -> one stream which they send to the
    client.  For communication it used the datachannel of the parent
    module.connection.Connection.

    Extends AsyncIOEventEmitter, providing the following events:
    - `connection_closed` : str
        Emitted when this SubConnection closes.  Data is the ID of this SubConnection.
    """

    id: str
    _participant_summary: ParticipantSummaryDict | None
    _pc: RTCPeerConnection

    _audio_track: MediaStreamTrack
    _video_track: MediaStreamTrack

    _closed: bool
    _logger: logging.Logger

    def __init__(
        self,
        id: str,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
        participant_summary: ParticipantSummaryDict | None,
        log_name_suffix: str,
    ) -> None:
        """Initialize new SubConnection.

        Parameters
        ----------
        id : str
        video_track : aiortc.MediaStreamTrack
            Video track that will be send in this SubConnection.
        audio_track : aiortc.MediaStreamTrack
            Audio track that will be send in this SubConnection.
        participant_summary : None or custom_types.participant_summary.ParticipantSummaryDict
            Participant summary send to the client with the initial offer.
        """
        super().__init__()
        self._logger = logging.getLogger(f"SubConnection-{log_name_suffix}")
        self.id = id
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

    async def generate_offer(self) -> ConnectionOfferDict:
        """TODO document

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
        return connection_offer

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

        self._logger.debug("Closing SubConnection")
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
        self._logger.debug(f"Peer Connection state change: {self._pc.connectionState}")
        if self._pc.connectionState in ["closed", "failed"]:
            await self.stop()


async def connection_factory(
    offer: RTCSessionDescription,
    message_handler: Callable[[MessageDict], Coroutine[Any, Any, None]],
    log_name_suffix: str,
) -> Tuple[RTCSessionDescription, Connection]:
    """Instantiate Connection.

    Parameters
    ----------
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.
    message_handler : function (message: custom_types.message.MessageDict) -> None
        Message handler for Connection.  Connection will pass parsed MessageDicts to
        this handler.
    log_name_suffix : str
        Suffix for logger used in Connection.  Format: Connection-<log_name_suffix>.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.connection.Connection
        WebRTC answer that should be send back to the client and a Connection.
    """
    pc = RTCPeerConnection()
    connection = Connection(pc, message_handler, log_name_suffix)

    # handle offer
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)  # type: ignore

    return (pc.localDescription, connection)
