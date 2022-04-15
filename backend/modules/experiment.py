"""TODO document"""

from _types.experiment_state import ExperimentState
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session as _session


class Experiment():
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
