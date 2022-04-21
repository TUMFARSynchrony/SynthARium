"""TODO document"""

from typing import Literal, Optional
from aiortc import RTCSessionDescription

import modules.server as _server
import modules.experiment as _experiment
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session_manager as _sm
from modules.exceptions import ErrorDictException
from _types.error import ErrorDict


class Hub():
    """TODO document"""
    experimenters: list[_experimenter.Experimenter]
    experiments: dict[str, _experiment.Experiment]
    session_manager: _sm.SessionManager
    server: _server.Server

    def __init__(self, host: str, port: int):
        """TODO document"""
        print("init hub")
        self.experimenters = []
        self.experiments = {}
        self.session_manager = _sm.SessionManager("sessions")
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
        for experiment in self.experiments.values():
            experiment.stop()

    async def handle_offer(
            self,
            offer: RTCSessionDescription,
            user_type: Literal["participant", "experimenter"],
            participant_id: Optional[str],
            session_id: Optional[str]
    ):
        """TODO document"""
        if user_type == "participant":
            answer = await self._handle_offer_participant(
                offer, participant_id, session_id)

        elif user_type == "experimenter":
            answer, experimenter = await _experimenter.experimenter_factory(
                offer)
            self.experimenters.append(experimenter)

        else:
            raise ErrorDictException(code=400, type="INVALID_REQUEST",
                                     description="Invalid user_type.")
        return answer

    async def _handle_offer_participant(
            self,
            offer: RTCSessionDescription,
            participant_id: Optional[str],
            session_id: Optional[str]
    ):
        """TODO document"""
        if participant_id == None:
            print("[HUB] WARNING: Missing participant_id in offer handler")
            raise ErrorDictException(code=400, type="INVALID_REQUEST",
                                     description="Missing participant_id.")

        if session_id == None:
            print("[HUB] WARNING: Missing session_id in offer handler")
            raise ErrorDictException(code=400, type="INVALID_REQUEST",
                                     description="Missing session_id.")

        if session_id not in self.experiments.keys():
            print(f"[HUB]: WARNING: session {session_id} not found.",
                  f"Participant {participant_id} failed to join")
            raise ErrorDictException(code=400, type="UNKNOWN_SESSION",
                                     description="Session not found.")

        experiment = self.experiments[session_id]
        if not experiment.knows_participant_id(participant_id):
            print(f"[HUB]: WARNING: participant {participant_id} not found in",
                  f"session: {session_id}.")
            raise ErrorDictException(
                code=400, type="UNKNOWN_PARTICIPANT",
                description="Participant not found in the given session.")

        answer, participant = await _participant.participant_factory(offer)
        experiment.add_participant(participant)

        return answer

    def start_experiment(self, session):
        """TODO document"""
        pass
