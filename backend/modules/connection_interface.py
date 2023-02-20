"""Provide the abstract `ConnectionInterface`."""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from pyee.asyncio import AsyncIOEventEmitter

from modules.connection_state import ConnectionState

from filters import FilterDict
from custom_types.message import MessageDict
from custom_types.participant_summary import ParticipantSummaryDict
from custom_types.connection import (
    ConnectionOfferDict,
    ConnectionAnswerDict,
    ConnectionProposalDict,
)


class ConnectionInterface(AsyncIOEventEmitter, metaclass=ABCMeta):
    """Abstract interface for connections with clients.

    Notes
    -----
    Do not instantiate directly, use subclasses / implementations of
    `ConnectionInterface` instead.

    See Also
    --------
    modules.connection.Connection : Implementation for ConnectionInterface.
    modules.connection_subprocess.ConnectionSubprocess :
        Implementation for ConnectionInterface.
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
        data : custom_types.message.MessageDict or dict
            Data that will be stringified and send to the connected client.
        """
        pass

    @property
    @abstractmethod
    def state(self) -> ConnectionState:
        """Get the modules.connection_state.ConnectionState the Connection is in."""
        pass

    @abstractmethod
    async def create_subscriber_proposal(
        self, participant_summary: ParticipantSummaryDict | str | None
    ) -> ConnectionProposalDict:
        """Create a SubConnection proposal.

        Parameters
        ----------
        participant_summary : custom_types.participant_summary.ParticipantSummaryDict, str or None
            Optional participant summary or participant ID that will be included in the
            resulting proposal.

        Returns
        -------
        custom_types.connection.ConnectionProposalDict
            Connection proposal including `participant_summary`.  The `id` in the
            returned dict is the `subconnection_id` for this proposal.  If the
            subscriber should be removed manually, this ID is required for
            `stop_subconnection(subconnection_id)`.  This is not required if the user
            disconnects.

        See Also
        --------
        Connection Protocol Wiki :
            Details about the connection protocol this function is part of.
            https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
        """
        pass

    @abstractmethod
    async def handle_subscriber_offer(
        self, offer: ConnectionOfferDict
    ) -> ConnectionAnswerDict:
        """Handle a ConnectionOffer based on a ConnectionProposal from this Connection.

        The offer should be in response to a
        custom_types.connection.ConnectionProposalDict created by this connection and
        send to a different user.

        Parameters
        ----------
        answer : custom_types.connection.ConnectionAnswerDict
            Answer to a custom_types.connection.ConnectionOfferDict created by this
            connection.  The answer ID must match a offer ID send by this connection.

        Raises
        ------
        ErrorDictException
            If `id` in `offer` is unknown (not a modules.connection.SubConnection ID
            handled by this modules.connection.Connection).

        See Also
        --------
        Connection Protocol Wiki :
            Details about the connection protocol this function is part of.
            https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
        """
        pass

    @abstractmethod
    async def stop_subconnection(self, subconnection_id: str) -> None:
        """Stop the subconnection with `subconnection_id`.

        This can be used to manually remove a subscriber without disconnecting the user,
        e.g. when an experimenter leaves an experiment.  It is not required if the user
        disconnects.

        The `subconnection_id` is obtained from the result of
        `create_subscriber_proposal` (`id` variable).

        Parameters
        ----------
        subconnection_id : str
            ID of the outgoing SubConnection that will be stopped.

        See Also
        --------
        create_subscriber_proposal :
            Create a new subscriber proposal, containing the subconnection ID.
        """
        pass

    @abstractmethod
    async def set_muted(self, video: bool, audio: bool) -> None:
        """Set the muted state for this connection.

        Parameters
        ----------
        video : bool
            Whether the video track should be muted.
        audio : bool
            Whether the audio track should be muted.
        """
        pass

    @abstractmethod
    async def set_video_filters(self, filters: list[FilterDict]) -> None:
        """Set or update video filters to `filters`.

        Parameters
        ----------
        filters : list of filters.FilterDict
            List of video filter configs.
        """
        pass

    @abstractmethod
    async def set_audio_filters(self, filters: list[FilterDict]) -> None:
        """Set or update audio filters to `filters`.

        Parameters
        ----------
        filters : list of filters.FilterDict
            List of audio filter configs.
        """
        pass
