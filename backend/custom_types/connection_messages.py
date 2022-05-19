"""Provide messages used internally by the Connection classes in front-/backend.

Use for type hints and static type checking without any overhead during runtime.
"""

from __future__ import annotations
from typing import Any, Literal, TypedDict, get_args

import custom_types.util as util


class ConnectionOfferDict(TypedDict):
    """TODO Document"""

    id: str
    offer: RTCSessionDescriptionDict


class RTCSessionDescriptionDict(TypedDict):
    """TODO Document"""

    sdp: str
    type: RTC_SESSION_TYPES


RTC_SESSION_TYPES = Literal["offer", "pranswer", "answer", "rollback"]


def is_valid_rtc_session_description_dict(data) -> bool:
    """TODO Document"""
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, RTCSessionDescriptionDict):
        return False

    return isinstance(data["sdp"], str) and data["type"] in get_args(RTC_SESSION_TYPES)


class ConnectionAnswerDict(TypedDict):
    """TODO Document"""

    id: str
    answer: Any


def is_valid_connection_answer_dict(data) -> bool:
    """TODO Document"""
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, ConnectionAnswerDict):
        return False

    return isinstance(data["id"], str) and is_valid_rtc_session_description_dict(
        data["answer"]
    )
