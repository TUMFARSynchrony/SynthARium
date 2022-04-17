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
        self.experimenters = []
        self.experiments = []
        self.session_manager = _sm.SessionManager()
        self.server = _server.Server(self.handle_offer, host, port)

    async def start(self):
        """TODO document"""
        await self.server.start()

    async def stop(self):
        """TODO document"""
        print("Hub stopping")
        await self.server.stop()
        for experimenter in self.experimenters:
            experimenter.disconnect()
        for experiment in self.experiments:
            experiment.stop()

    def handle_offer(self, offer):
        """TODO document"""
        pass

    def start_experiment(self, session):
        """TODO document"""
        pass
