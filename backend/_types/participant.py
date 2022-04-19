"""TODO Document"""

from typing import Any, TypedDict
from typing_extensions import NotRequired

from _types.size import SizeDict
from _types.position import PositionDict


class ParticipantDict(TypedDict):
    """TODO Document"""
    id: NotRequired[str]
    first_name: str
    last_name: str
    muted: bool
    filters: list[Any]
    position: PositionDict
    size: SizeDict
