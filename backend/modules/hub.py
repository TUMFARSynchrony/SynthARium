"""TODO document"""

from modules.server import Server
from modules.experiment import Experiment
from modules.experimenter import Experimenter
from modules.session_manager import SessionManager


class Hub():
    """TODO document"""
    experimenters: list[Experimenter]
    experiments: list[Experiment]
    session_manager: SessionManager
    server: Server

    def __init__(self):
        """TODO document"""
        pass

    def stop(self):
        """TODO document"""
        pass

    def handle_offer(self, offer):
        """TODO document"""
        pass

    def start_experiment(self, session):
        """TODO document"""
        pass
