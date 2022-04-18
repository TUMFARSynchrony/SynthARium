"""TODO document"""

from __future__ import annotations
from aiortc import RTCSessionDescription

from modules.connection import connection_factory
import modules.experiment as _experiment
import modules.user as _user


class Participant(_user.User):
    """TODO document"""
    experiment: _experiment.Experiment

    def __init__(self):
        """TODO document"""
        pass

    def handle_message(self, message):
        """TODO document"""
        pass

    def kick(self, reason: str):
        """TODO document"""
        pass


async def participant_factory(offer: RTCSessionDescription):
    """TODO document"""
    participant = Participant()
    answer, connection = await connection_factory(
        offer, participant.handle_message)
    participant.set_connection(connection)
    return (answer, participant)
