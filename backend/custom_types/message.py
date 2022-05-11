"""Provide the `MessageDict` TypedDict and valid `MESSAGE_TYPES`.

Use for type hints and static type checking without any overhead during runtime.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict, get_args

import modules.util as util


class MessageDict(TypedDict):
    """TypedDict for api messages.  All messages send should be a MessageDict.

    The `MessageDict` is used to send and receive messages and identify the contents of
    a message via `type`.  The content of a message can be anything, e.g. an ErrorDict,
    Session Data, ...

    Attributes
    ----------
    type : custom_types.message.MESSAGE_TYPES
        Unique message type identifying the contents.
    data : Any
        Content of the message.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message
    """

    type: MESSAGE_TYPES
    data: Any


# TODO define valid types
MESSAGE_TYPES = Literal[
    "TO_BE_DEFINED",  # Placeholder
    "SUCCESS",
    "ERROR",
    "SESSION_DESCRIPTION",
    "SESSION_LIST",
    "SESSION",
    "CHAT",
    "KICK_PARTICIPANT",
    "BAN_PARTICIPANT",
    "KICK_NOTIFICATION",
    "BAN_NOTIFICATION",
    "EXPERIMENT_STARTED",
    "EXPERIMENT_ENDED",
    "MUTE",
    "SET_FILTERS",
]
"""Possible message types for custom_types.message.MessageDict.

See Also
--------
Data Types Wiki :
    https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message
"""


def is_valid_messagedict(data) -> bool:
    """Check if `data` is a valid MessageDict.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.
    Does not check the contents of MessageDict.data / non recursive.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid MessageDict.
    """
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, MessageDict):
        return False

    return data["type"] in get_args(MESSAGE_TYPES)
