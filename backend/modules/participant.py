"""Provide the `Participant` class and `participant_factory` factory function.

Notes
-----
Use participant_factory for creating new participants to ensure that they have a valid
modules.connection.Connection.
"""

from __future__ import annotations
from aiortc import RTCSessionDescription

from custom_types.chat_message import ChatMessageDict
from custom_types.kick import KickNotificationDict
from custom_types.message import MessageDict
from custom_types.success import SuccessDict

import modules.experiment as _experiment
from modules.exceptions import ErrorDictException
from modules.connection import connection_factory
from modules.util import check_valid_typed_dict
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

        # Add API endpoints
        self.on("CHAT", self._handle_chat)

    async def kick(self, reason: str):
        """TODO document"""
        kick_notification = KickNotificationDict(reason=reason)
        message = MessageDict(type="KICK_NOTIFICATION", data=kick_notification)
        self.send(message)

        await self.disconnect()

    async def _handle_chat(self, data) -> MessageDict:
        """TODO document"""
        if not check_valid_typed_dict(data, ChatMessageDict):
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Expected ChatMessage object.",
            )

        if data["target"] != "experimenter":
            raise ErrorDictException(
                code=403,
                type="INVALID_REQUEST",
                description='Participants can only chat with "experimenter".',
            )

        if data["author"] != self.id:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Author of message must be participant ID.",
            )

        self._experiment.send_chat_message(data)

        success = SuccessDict(
            type="CHAT", description="Successfully send chat message."
        )
        return MessageDict(type="SUCCESS", data=success)


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
