"""This module provides the Participant class and participant_factory.

Use participant_factory for creating new participants to ensure that they have a valid
modules.connection.Connection.
"""

from __future__ import annotations
from aiortc import RTCSessionDescription

from modules.connection import connection_factory
import modules.experiment as _experiment
from modules.user import User


class Participant(User):
    """Participant is a type of modules.user.User with participant rights.

    Has access to a different set of API endpoints than other Users.  API endpoints for
    participants are defined here.

    See Also
    --------
    participant_factory : Instantiate connection with a new Participant based on WebRTC
        `offer`.  Use factory instead of initiating Participants directly.
    """

    experiment: _experiment.Experiment

    def __init__(self):
        """TODO document"""
        pass

    def handle_message(self, message):
        """TODO document"""
        pass

    def kick(self, reason: str):
        """TODO document"""
        pass


async def participant_factory(
    offer: RTCSessionDescription,
) -> tuple[RTCSessionDescription, Participant]:
    """Instantiate connection with a new Participant based on WebRTC `offer`.

    Instantiate new modules.participant.Participant, handle offer using
    modules.connection.connection_factory and set connection for the Participant.

    This sequence must be donne for all participants.  Instantiating an Participant
    directly will likely lead to problems, since it wont have a Connection.

    Parameters
    ----------
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.

    TODO add parameters when implementing Participant

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.participant.Participant
        WebRTC answer that should be send back to the client and Participant
        representing the client.
    """
    participant = Participant()
    answer, connection = await connection_factory(offer, participant.handle_message)
    participant.set_connection(connection)
    return (answer, participant)
