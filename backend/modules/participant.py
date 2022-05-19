"""Provide the `Participant` class and `participant_factory` factory function.

Notes
-----
Use participant_factory for creating new participants to ensure that they have a valid
modules.connection.Connection.
"""

from __future__ import annotations
import asyncio
from typing import Any
from aiortc import RTCSessionDescription

from custom_types.chat_message import ChatMessageDict, is_valid_chatmessage
from custom_types.kick import KickNotificationDict
from custom_types.message import MessageDict
from custom_types.success import SuccessDict

import modules.experiment as _experiment
from modules.connection_state import ConnectionState
from modules.exceptions import ErrorDictException
from modules.connection import connection_factory
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
    _muted_video: bool
    _muted_audio: bool

    def __init__(
        self,
        id: str,
        experiment: _experiment.Experiment,
        muted_video: bool,
        muted_audio: bool,
    ) -> None:
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
        super(Participant, self).__init__(id)

        self._experiment = experiment
        self._muted_video = muted_video
        self._muted_audio = muted_audio
        experiment.add_participant(self)

        # Add API endpoints
        self.on("CHAT", self._handle_chat)

    def set_muted(self, video: bool, audio: bool):
        """Set the muted state for this participant.

        Parameters
        ----------
        video : bool
            Whether the participants video should be muted.
        audio : bool
            Whether the participants audio should be muted.
        """
        if self._muted_video == video and self._muted_audio == audio:
            return

        self._muted_video = video
        self._muted_audio = audio

        # TODO Implement mute on connection (when connection is finished)

        # TODO Notify user about mute

    async def kick(self, reason: str):
        """Kick the participant.

        Notify the participant about the kick with a `KICK_NOTIFICATION` message and
        disconnect the participant.

        Parameters
        ----------
        reason : str
            Reason for the kick.  Will be send to the participant in the
            `KICK_NOTIFICATION`.
        """
        kick_notification = KickNotificationDict(reason=reason)
        message = MessageDict(type="KICK_NOTIFICATION", data=kick_notification)
        self.send(message)

        await self.disconnect()

    async def ban(self, reason: str):
        """Ban the participant.

        Notify the participant about the ban with a `BAN_NOTIFICATION` message and
        disconnect the participant.

        Parameters
        ----------
        reason : str
            Reason for the kick.  Will be send to the participant in the
            `BAN_NOTIFICATION`.
        """
        ban_notification = KickNotificationDict(reason=reason)
        message = MessageDict(type="BAN_NOTIFICATION", data=ban_notification)
        self.send(message)

        await self.disconnect()

    async def _handle_connection_state_change(self, state: ConnectionState) -> None:
        """TODO Document"""
        print("[Participant] handle state change. State:", state)
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            print("[Participant] Removing self from experiment")
            self._experiment.remove_participant(self)
            return

        if state is ConnectionState.CONNECTED:
            tasks = []
            for p in self._experiment.participants.values():
                if p is self:
                    continue
                tasks.append(self.subscribe_to(p))
                tasks.append(p.subscribe_to(self))
            await asyncio.gather(*tasks)

    async def _handle_chat(self, data: ChatMessageDict | Any) -> MessageDict:
        """Handle requests with type `CHAT`.

        Check if data is a valid custom_types.chat_message.ChatMessageDict, target is
        set to "experimenter", author is the ID of this participant and pass the request
        to the experiment.

        Parameters
        ----------
        data : any or custom_types.chat_message.ChatMessageDict
            Message data.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `CHAT`.

        Raises
        ------
        ErrorDictException
            If data is not a valid custom_types.chat_message.ChatMessageDict, target is
            not set to "experimenter" or author is not the ID of this participant.
        """
        if not is_valid_chatmessage(data):
            raise ErrorDictException(
                code=400,
                type="INVALID_DATATYPE",
                description="Message data is not a valid ChatMessage.",
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

        self._experiment.handle_chat_message(data)

        success = SuccessDict(
            type="CHAT", description="Successfully send chat message."
        )
        return MessageDict(type="SUCCESS", data=success)


async def participant_factory(
    offer: RTCSessionDescription,
    id: str,
    experiment: _experiment.Experiment,
    muted_video: bool,
    muted_audio: bool,
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
    participant = Participant(id, experiment, muted_video, muted_audio)
    answer, connection = await connection_factory(offer, participant.handle_message)
    participant.set_connection(connection)
    return (answer, participant)
