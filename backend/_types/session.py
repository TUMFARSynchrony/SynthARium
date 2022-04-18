"""TODO Document"""

from typing import Any, TypedDict

from _types.participant import ParticipantDict
from _types.note import NoteDict


class __SessionDictOptionalKeys(TypedDict, total=False):
    """TODO Document"""
    id: str
    start_time: int
    end_time: int
    log: Any


class SessionDict(__SessionDictOptionalKeys):
    """TODO Document"""
    title: str
    description: str
    date: int
    time_limit: int
    record: bool
    participants: list[ParticipantDict]
    notes: list[NoteDict]
