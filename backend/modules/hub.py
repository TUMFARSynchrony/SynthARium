"""TODO document"""

import modules.server as _server
import modules.experiment as _experiment
import modules.experimenter as _experimenter
import modules.session_manager as _sm


class Hub():
    """TODO document"""
    experimenters: list[_experimenter.Experimenter]
    experiments: list[_experiment.Experiment]
    session_manager: _sm.SessionManager
    server: _server.Server

    def __init__(self, host: str, port: int):
        """TODO document"""
        print("init hub")

    def stop(self):
        """TODO document"""
        pass

    def handle_offer(self, offer):
        """TODO document"""
        pass

    def start_experiment(self, session):
        """TODO document"""
        pass
