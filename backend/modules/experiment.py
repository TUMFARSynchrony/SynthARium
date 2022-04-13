"""TODO document"""

from types.experiment_state import ExperimentState
from modules.experimenter import Experimenter
from modules.participant import Participant
from modules.session import Session


class Experiment():
    """TODO document"""
    state: ExperimentState
    session: Session
    experimenters: list[Experimenter]
    participants: list[Participant]

    def start(self):
        """TODO document"""
        pass

    def stop(self):
        """TODO document"""
        pass

    def send(self, to, data):
        """TODO document"""
        pass
