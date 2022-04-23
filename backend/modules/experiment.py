"""This module provides the Experiment class."""
import time
from typing import Any, Optional

from _types.experiment_state import ExperimentState
from modules.exceptions import ErrorDictException
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session as _session


class Experiment:
    """Experiment representing a running session."""

    _state: ExperimentState
    session: _session.Session
    _experimenters: list[_experimenter.Experimenter]
    _participants: list[_participant.Participant]

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
        self._participants = []

    def start(self):
        """Start the experiment.

        If state is `WAITING`, save the current time in `session.start_time` and set
        state to `RUNNING`.  If state is not `WAITING`, a ErrorDictException is raised.

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

    def send(
        self,
        to: str,
        data: Any,
        exclude: Optional[_experimenter.Experimenter | _participant.Participant],
    ):
        """Send data to a single or group of users.

        Select the correct target (group) according to the `to` parameter and send the
        given `data` to all targets.

        Parameters
        ----------
        to : str
            Target for the data. Can be a participant id or one of the following groups:
            -`"all"` send data to all experimenters and participants.
            -`"experimenters"` send data to all experimenters.
            -`"participants"` send data to all participants.
        data : Any
            Data that will be send.
        exclude : modules.experimenter.Experimenter or modules.participant.Participant, optional
            User to exclude from targets, e.g. sender of `data`.
        """
        # Select target
        targets: list[_experimenter.Experimenter | _participant.Participant] = []
        match to:
            case "all":
                targets.extend(self._experimenters)
                targets.extend(self._participants)
            case "experimenters":
                targets.extend(self._experimenters)
            case "participants":
                targets.extend(self._participants)
            case _:
                for participant in self._participants:
                    if participant.id is to:
                        targets.append(participant)

        # Send data
        for user in targets:
            if exclude is None or exclude.id is not user.id:
                user.send(data)

    def knows_participant_id(self, participant_id: str) -> bool:
        """Check if `participant_id` is a id for a participant in this experiment."""
        known_ids = map(lambda p: p.get("id", ""), self.session.participants)
        return participant_id is not "" and participant_id in known_ids

    def add_participant(self, participant: _participant.Participant):
        """Add participant to experiment.

        Parameters
        ----------
        participant : modules.participant.Participant
            Participant joining the experiment.
        """
        self._participants.append(participant)

    def add_experimenter(self, experimenter: _experimenter.Experimenter):
        """Add experimenter to experiment.

        Parameters
        ----------
        experimenter : modules.experimenter.Experimenter
            Experimenter joining the experiment.
        """
        self._experimenters.append(experimenter)
