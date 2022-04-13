"""TODO document"""

from modules.experiment import Experiment
from modules.user import User


class Participant(User):
    """TODO document"""
    experiment: Experiment

    def __init__(self):
        """TODO document"""
        pass

    def handle_message(self, message):
        """TODO document"""
        pass

    def kick(self, reason: str):
        """TODO document"""
        pass
