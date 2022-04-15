"""TODO Document"""

from __future__ import annotations

from typing import TypedDict, Literal


class SuccessDict(TypedDict):
    """TODO Document"""
    type: SUCCESS_TYPES
    description: str


# TODO define valid types
SUCCESS_TYPES = Literal[
    "EXAMPLE_TYPE",
    "EXAMPLE_TYPE_2"
]
"""TODO Document"""
