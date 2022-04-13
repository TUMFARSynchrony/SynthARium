"""TODO Document"""

from typing import Any, TypedDict

from types.participant import ParticipantDict
from types.note import NoteDict


class __SessionDictOptionalKeys(TypedDict, total=False):
    """TODO Document"""
    id: str
    startTime: int
    endTime: int
    log: Any


class SessionDict(__SessionDictOptionalKeys):
    """TODO Document"""
    title: str
    description: str
    date: int
    timeLimit: int
    record: bool
    participants: list[ParticipantDict]
    notes: list[NoteDict]
