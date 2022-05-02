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

    _experiment: _experiment.Experiment

    def __init__(self, id: str, experiment: _experiment.Experiment) -> None:
        """Instantiate new Participant instance.

        Parameters
        ----------
        id : str
            Unique identifier for Participant.  Must exist in experiment.
        experiment : modules.experiment.Experiment
            Experiment the participant is part of.

        See Also
        --------
        experimenter_factory : Instantiate connection with a new Experimenter based on
            WebRTC `offer`.  Use factory instead of instantiating Experimenter directly.
        """
        super().__init__(id)

        self._experiment = experiment
        experiment.add_participant(self)

        # TODO Add API endpoints
        # self.on(...

    def kick(self, reason: str):
        """TODO document"""
        pass


async def participant_factory(
    offer: RTCSessionDescription, id: str, experiment: _experiment.Experiment
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
    id : str
        Unique identifier for Participant.  Must exist in experiment.
    experiment : modules.experiment.Experiment
        Experiment the participant is part of.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.participant.Participant
        WebRTC answer that should be send back to the client and Participant
        representing the client.
    """
    participant = Participant(id, experiment)
    answer, connection = await connection_factory(offer, participant.handle_message)
    participant.set_connection(connection)
    return (answer, participant)
