"""Provide the `Experiment` class."""
import time
from typing import Any

from custom_types.message import MessageDict
from custom_types.kick import KickRequestDict
from custom_types.chat_message import ChatMessageDict

from modules.experiment_state import ExperimentState
from modules.exceptions import ErrorDictException
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session as _session


class Experiment:
    """Experiment representing a running session."""

    _state: ExperimentState
    session: _session.Session
    _experimenters: list[_experimenter.Experimenter]
    _participants: dict[str, _participant.Participant]

    def __init__(self, session: _session.Session):
        """Start a new Experiment.

        Parameters
        ----------
        session : modules.session.Session
            Session this experiment is based on. Will modify the session during
            execution.
        """
        self._state = ExperimentState.WAITING
        self.session = session
        self._experimenters = []
        self._participants = {}

    def start(self):
        """Start the experiment.

        If state is `WAITING`, save the current time in `session.start_time` and set
        state to `RUNNING`.  If state is not `WAITING`, an ErrorDictException is raised.

        Raises
        ------
        ErrorDictException
            If experiment state is not `WAITING`.
        """
        if self._state != ExperimentState.WAITING:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Experiment cant be started, state is not WAITING.",
            )

        self._state = ExperimentState.RUNNING
        self.session.start_time = round(time.time() * 1000)

        # Notify all users
        end_message = MessageDict(type="EXPERIMENT_STARTED", data={})
        self.send("", end_message, broadcast=True)

    def stop(self):
        """Stop the experiment.

        If state is not already `ENDED`, save the current time in `session.end_time` and
        set state to `ENDED`.

        Raises
        ------
        ErrorDictException
            If experiment state is already `ENDED`.
        """
        if self._state is ExperimentState.ENDED:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Experiment is already stopped.",
            )

        self._state = ExperimentState.ENDED
        self.session.end_time = round(time.time() * 1000)

        # Notify all users
        end_message = MessageDict(type="EXPERIMENT_ENDED", data={})
        self.send("", end_message, broadcast=True)

    def send(self, to: str, data: Any, exclude: str = "", broadcast: bool = False):
        """Send data to a single or group of users.

        Select the correct target (group) according to the `to` parameter and send the
        given `data` to all targets.

        Parameters
        ----------
        to : str
            Target for the data. Can be a participant ID or one of the following groups:
            -`"all"` send data to all participants.
            -`"experimenter"` send data to all experimenters.
        data : Any
            Data that will be send.
        exclude : str, optional
            User ID to exclude from targets, e.g. ID from sender of `data`.
        broadcast : bool, default False
            For sending a data to all clients, participants and experimenters.  Only for
            internal use.  If true, `to` is ignored.

        Notes
        -----
        broadcast is a separate variable to avoid misbehaving clients sending data to
        everyone.

        Raises
        ------
        ErrorDictException
            If `to` is not "all", "experimenter" or a known participant ID.
        """
        # Select target
        targets: list[_experimenter.Experimenter | _participant.Participant] = []
        if broadcast:
            targets.extend(self._participants.values())
            targets.extend(self._experimenters)
        else:
            match to:
                case "all":
                    targets.extend(self._participants.values())
                case "experimenter":
                    targets.extend(self._experimenters)
                case _:
                    if to in self._participants:
                        targets.append(self._participants[to])
                    else:
                        raise ErrorDictException(
                            404,
                            "UNKNOWN_USER",
                            f"Failed to send data to {to}, user not found.",
                        )

        # Send data
        for user in targets:
            if exclude != user.id:
                user.send(data)

    def send_chat_message(self, chat_message: ChatMessageDict):
        """Log and send a chat message to `target` in `chat_message`.

        Parameters
        ----------
        participant : custom_types.chat_message.ChatMessageDict
            Chat message that will be send.

        Raises
        ------
        ErrorDictException
            If `target` in `chat_message` is not "all", "experimenter" or a known
            participant ID.
        """
        # Save message in log
        self.session.log_chat_message(chat_message)

        # Send message
        msg_dict = MessageDict(type="CHAT", data=chat_message)
        self.send(chat_message["target"], msg_dict)

    def add_participant(self, participant: _participant.Participant):
        """Add participant to experiment.

        Parameters
        ----------
        participant : modules.participant.Participant
            Participant joining the experiment.
        """
        self._participants[participant.id] = participant

    async def kick_participant(self, kick_request: KickRequestDict):
        """Kick a participant from this experiment.

        Notify the participant before disconnecting the connection.

        Parameters
        ----------
        kick_request : custom_types.kick.KickRequestDict
            Kick request received from experimenter.

        Raises
        ------
        ErrorDictException
            If the `participant_id` in `kick_request` is not known.
        """
        participant = self._participants.get(kick_request["participant_id"])
        if participant is None:
            raise ErrorDictException(
                code=404,
                type="UNKNOWN_PARTICIPANT",
                description=(
                    "Failed to kick Participant. Participant with the given ID not "
                    "found."
                ),
            )

        await participant.kick(kick_request["reason"])
        self._participants.pop(kick_request["participant_id"])

    def mute_participant(self, participant_id: str, video: bool, audio: bool):
        """Set the muted state for the participant with `participant_id`.

        Parameters
        ----------
        participant_id : str
            ID of the target participant.
        video : bool
            Whether the participants video should be muted.
        audio : bool
            Whether the participants audio should be muted.
        """
        # Mute participant if participant is already connected
        if participant_id in self._participants:
            self._participants[participant_id].set_muted(video, audio)

    def add_experimenter(self, experimenter: _experimenter.Experimenter):
        """Add experimenter to experiment.

        Parameters
        ----------
        experimenter : modules.experimenter.Experimenter
            Experimenter joining the experiment.
        """
        self._experimenters.append(experimenter)
