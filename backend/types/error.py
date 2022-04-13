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
    "EXAMPLE_TYPE",
    "EXAMPLE_TYPE_2"
]
"""TODO Document"""
