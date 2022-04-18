"""TODO Document"""

from __future__ import annotations

from typing import Any, Literal, TypedDict


class MessageDict(TypedDict):
    """TODO Document"""
    type: MESSAGE_TYPES
    data: Any


# TODO define valid types
MESSAGE_TYPES = Literal[
    "TO_BE_DEFINED",  # Placeholder
    "SUCCESS",
    "ERROR",
    "SESSION_DESCRIPTION",
]
"""TODO Document"""
