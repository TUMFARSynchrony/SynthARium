"""TODO Document"""

from typing import Any, TypedDict

from types.size import Size
from types.position import Position


class __ParticipantDictOptionalKeys(TypedDict, total=False):
    """TODO Document"""
    id: str


class ParticipantDict(__ParticipantDictOptionalKeys):
    """TODO Document"""
    firstName: str
    lastName: str
    muted: bool
    filters: list[Any]
    position: Position
    size: Size
