"""Provide the abstract `ConnectionInterface`."""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from pyee.asyncio import AsyncIOEventEmitter

from modules.connection_state import ConnectionState

from custom_types.message import MessageDict
from custom_types.participant_summary import ParticipantSummaryDict
from custom_types.connection import ConnectionOfferDict, ConnectionAnswerDict


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
    async def create_subscriber_offer(
        self, participant_summary: ParticipantSummaryDict | str | None
    ) -> ConnectionOfferDict:
        """Create a subconnection offer.

        Parameters
        ----------
        participant_summary : custom_types.participant_summary.ParticipantSummaryDict, str or None
            Optional participant summary or participant ID that will be included in the
            resulting offer.

        Returns
        -------
        custom_types.connection.ConnectionOfferDict
            Connection offer including `participant_summary`.
        """
        pass

    @abstractmethod
    async def handle_subscriber_answer(self, answer: ConnectionAnswerDict) -> None:
        """Handle answer to a connection offer.

        Parameters
        ----------
        answer : custom_types.connection.ConnectionAnswerDict
            Answer to a custom_types.connection.ConnectionOfferDict created by this
            connection.  The answer ID must match a offer ID send by this connection.
        """
        pass

    @abstractmethod
    async def stop_subconnection(self, subconnection_id: str) -> bool:
        """Stop the subconnection with `subconnection_id`.

        Parameters
        ----------
        subconnection_id : str
            ID of the outgoing SubConnection that will be stopped.

        Returns
        -------
        bool
            True if a outgoing stream with `subconnection_id` was found and closed.
            Otherwise False.

        See Also
        --------
        add_outgoing_stream : add a new outgoing SubConnection.
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
