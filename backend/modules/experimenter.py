"""TODO document"""

from modules.experiment import Experiment
from modules.user import User
from modules.hub import Hub


class Experimenter(User):
    """TODO document"""
    experiment: Experiment
    hub: Hub

    def handle_message(self, message):
        """TODO document"""
        pass
