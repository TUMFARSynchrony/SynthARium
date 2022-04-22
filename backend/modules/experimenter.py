"""TODO document"""

from __future__ import annotations
from aiortc import RTCSessionDescription

from modules.connection import connection_factory
import modules.experiment as _experiment
import modules.hub as _hub
import modules.user as _user


class Experimenter(_user.User):
    """TODO document"""

    experiment: _experiment.Experiment
    hub: _hub.Hub

    def handle_message(self, message):
        """TODO document"""
        pass


async def experimenter_factory(offer: RTCSessionDescription):
    """TODO document"""
    experimenter = Experimenter()
    answer, connection = await connection_factory(offer, experimenter.handle_message)
    experimenter.set_connection(connection)
    return (answer, experimenter)
