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

    @abstractmethod
    async def create_subscriber_offer(
        self, participant_summary: ParticipantSummaryDict | None
    ) -> ConnectionOfferDict:
        """TODO document"""
        pass

    @abstractmethod
    async def handle_subscriber_answer(self, answer: ConnectionAnswerDict) -> None:
        """TODO document"""
        pass

    @abstractmethod
    async def stop_subconnection(self, subconnection_id: str) -> bool:
        """Stop the subconnection with `stream_id`.

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
    def set_muted(self, video: bool, audio: bool) -> None:
        """TODO document"""
        pass
