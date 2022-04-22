"""TODO Document"""

from __future__ import annotations

from typing import TypedDict, Literal


class ErrorDict(TypedDict):
    """TODO Document"""

    code: int
    type: ERROR_TYPES
    description: str


# TODO define valid types
ERROR_TYPES = Literal[
    "TO_BE_DEFINED",  # Placeholder
    "INVALID_REQUEST",
    "UNKNOWN_SESSION",
    "UNKNOWN_PARTICIPANT",
]
"""TODO Document"""
