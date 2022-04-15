"""TODO document"""

from __future__ import annotations

import modules.session_manager as _sm

from _types.session import SessionDict
from _types.participant import ParticipantDict
from _types.note import NoteDict


class Session():
    """TODO document"""
    # Class data
    session_manager: _sm.SessionManager

    # Session data
    id: str
    title: str
    description: str
    date: int
    time_limit: int
    record: bool
    participants: list[ParticipantDict]
    start_time: int
    end_time: int
    notes: list[NoteDict]
    # log: WIP

    def update(self, session: SessionDict):
        """TODO document"""
        pass

    def add_note(self, note: NoteDict):
        """TODO document"""
        pass

    def set_started(self, time: int):
        """TODO document"""
        pass

    def set_ended(self, time: int):
        """TODO document"""
        pass
