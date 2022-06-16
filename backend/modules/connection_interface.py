"""Provide the abstract `ConnectionInterface`."""

from aiortc import MediaStreamTrack
from abc import ABCMeta, abstractmethod
from pyee.asyncio import AsyncIOEventEmitter

from modules.connection_state import ConnectionState
from modules.tracks import AudioTrackHandler, VideoTrackHandler

from custom_types.message import MessageDict
from custom_types.participant_summary import ParticipantSummaryDict


class ConnectionInterface(AsyncIOEventEmitter, metaclass=ABCMeta):
    """Abstract interface for connections with clients.

    Notes
    -----
    Do not instantiate directly, use subclasses / implementations of
    `ConnectionInterface` instead.
    """

    @abstractmethod
    async def stop(self) -> None:
        """Stop this connection.

        Stopps all incoming and outgoing streams and emits the `state_change` event.
        When finished, it removes all event listeners from this Connection, as no more
        events will be emitted.
        """
        pass

    @abstractmethod
    async def send(self, data: MessageDict | dict) -> None:
        """Send `data` to connected client over the datachannel.

        Parameters
        ----------
        data : MessageDict or dict
            Data that will be stringified and send to the connected client.
        """
        pass

    @property
    @abstractmethod
    def state(self) -> ConnectionState:
        """Get the modules.connection_state.ConnectionState the Connection is in."""
        pass

    @property
    @abstractmethod
    def incoming_audio(self) -> AudioTrackHandler | None:
        """Get incoming audio track.

        Returns
        -------
        modules.track.AudioTrackHandler or None
            None if no audio was received by client (yet), otherwise AudioTrackHandler.
        """
        pass

    @property
    @abstractmethod
    def incoming_video(self) -> VideoTrackHandler | None:
        """Get incoming video track.

        Returns
        -------
        modules.track.VideoTrackHandler or None
            None if no video was received by client (yet), otherwise VideoTrackHandler.
        """
        pass

    @abstractmethod
    async def add_outgoing_stream(
        self,
        video_track: MediaStreamTrack,
        audio_track: MediaStreamTrack,
        participant_summary: ParticipantSummaryDict | None,
    ) -> str:
        """Add an outgoing stream to Connection.

        See implementation for details.

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
            A new ID that identifies the new outgoing stream. It can be used to close
            the stream again using `stop_outgoing_stream()`.
        """
        pass

    @abstractmethod
    async def stop_outgoing_stream(self, stream_id: str) -> bool:
        """Stop the outgoing stream with `stream_id`.

        Parameters
        ----------
        stream_id : str
            ID of the outgoing stream that will be stopped.

        Returns
        -------
        bool
            True if a outgoing stream with `stream_id` was found and closed. Otherwise
            False.

        See Also
        --------
        add_outgoing_stream : add a new outgoing stream.
        """
        pass
