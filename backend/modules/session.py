"""TODO document"""

from modules.session_manager import SessionManager

from types.session import SessionDict
from types.participant import ParticipantDict
from types.note import NoteDict


class Session():
    """TODO document"""
    # Class data
    session_manager: SessionManager

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
