"""Provide the `MessageDict` TypedDict and valid `MESSAGE_TYPES`.

Use for type hints and static type checking without any overhead during runtime.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict


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
]
"""Possible message types for custom_types.message.MessageDict.

See Also
--------
Data Types Wiki :
    https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message
"""
