"""TODO Document"""

from __future__ import annotations

from typing import Any, Literal, TypedDict


class MessageDict(TypedDict):
    """TODO Document"""
    type: MESSAGE_TYPES
    data: Any


# TODO define valid types
MESSAGE_TYPES = Literal[
    "EXAMPLE_TYPE",
    "EXAMPLE_TYPE_2"
]
"""TODO Document"""
