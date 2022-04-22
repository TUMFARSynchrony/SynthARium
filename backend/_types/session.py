"""TODO Document"""

from typing import Any, TypedDict
from typing_extensions import NotRequired

from _types.participant import ParticipantDict
from _types.note import NoteDict


class SessionDict(TypedDict):
    """TODO Document"""

    id: NotRequired[str]
    title: str
    description: str
    date: int
    time_limit: int
    record: bool
    participants: list[ParticipantDict]
    start_time: NotRequired[int]
    end_time: NotRequired[int]
    notes: list[NoteDict]
    log: NotRequired[Any]
