"""Provide the `ChatMessageDict` TypedDict`.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


class ChatMessageDict(TypedDict):
    """TypedDict for sending chat messages between client and server.

    Attributes
    ----------
    message : str
        Message contents.
    time : int
        Time the message was send in milliseconds since January 1, 1970, 00:00:00 (UTC).
    author : str
        Author of the message. Participant ID or "experimenter".
    target : str
        Intended receiver of the message. Participant ID or "experimenter".
        For participant: always "experimenter".
        For experimenter: specific participant ID or "all" for broadcast.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#chatmessage
    """

    message: str
    time: int
    author: str
    target: str
