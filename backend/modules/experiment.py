"""TODO document"""

from _types.experiment_state import ExperimentState
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session as _session


class Experiment:
    """TODO document"""

    state: ExperimentState
    session: _session.Session
    experimenters: list[_experimenter.Experimenter]
    participants: list[_participant.Participant]

    def start(self):
        """TODO document"""
        pass

    def stop(self):
        """TODO document"""
        pass

    def send(self, to, data):
        """TODO document"""
        pass

    def knows_participant_id(self, participant_id: str) -> bool:
        """TODO document"""
        # known_ids = map(lambda p: p.id, self.session.participants)
        # return participant_id in known_ids
        return True

    def add_participant(self, participant: _participant.Participant):
        """TODO document"""
        pass
