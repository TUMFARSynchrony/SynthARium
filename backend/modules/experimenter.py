"""TODO document"""

from __future__ import annotations
from aiortc import RTCSessionDescription

from _types.message import MessageDict
from _types.session import SessionDict

from modules.connection import connection_factory
import modules.experiment as _experiment
import modules.hub as _hub
import modules.user as _user


class Experimenter(_user.User):
    """TODO document"""

    _experiment: _experiment.Experiment
    _hub: _hub.Hub

    def __init__(self, id: str):
        """TODO document"""
        super().__init__(id)
        self.add_message_handler("GET_SESSION_LIST", self._handle_get_session_list)
        self.add_message_handler("SAVE_SESSION", self._handle_save_session)

    def _handle_get_session_list(self, _):
        """TODO document"""
        sessions = self._hub.session_manager.get_session_dict_list()
        response = MessageDict(type="SESSION_LIST", data=sessions)
        self.send(response)

    def _handle_save_session(self, data):
        """TODO document"""
        # TODO data checks
        assert type(data) == SessionDict
        sm = self._hub.session_manager
        session = sm.get_session(data)
        if session is not None:
            # Update existing session
            session.update(data)
        else:
            # Create new session
            sm.create_session(data)

        # TODO what data should be send?
        response = MessageDict(type="SUCCESS", data={})
        self.send(response)


async def experimenter_factory(offer: RTCSessionDescription, id: str):
    """TODO document"""
    experimenter = Experimenter(id)
    answer, connection = await connection_factory(offer, experimenter.handle_message)
    experimenter.set_connection(connection)
    return (answer, experimenter)
