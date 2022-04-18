"""TODO document"""

from typing import Literal
from aiortc import RTCSessionDescription

from _types.error import ErrorDict

import modules.server as _server
import modules.experiment as _experiment
import modules.experimenter as _experimenter
import modules.participant as _participant
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

    async def handle_offer(self, offer: RTCSessionDescription,
                           user_type: Literal["participant", "experimenter"]):
        """TODO document"""
        if user_type not in ["participant", "experimenter"]:
            err = "Invalid user type"
            return ErrorDict(code=400, type="EXAMPLE_TYPE_2", description=err)

        if user_type == "participant":
            answer, participant = await _participant.participant_factory(offer)
            # TODO handle participant

        elif user_type == "experimenter":
            answer, experimenter = await _experimenter.experimenter_factory(
                offer)
            self.experimenters.append(experimenter)

        return answer

    def start_experiment(self, session):
        """TODO document"""
        pass
