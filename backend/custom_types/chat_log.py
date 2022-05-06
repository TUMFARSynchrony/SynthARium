"""Provide the `ChatLogDict` TypedDict`.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


class ChatLogDict(TypedDict):
    """TypedDict for logged chat messages in custom_types.session.SessionDict.

    Attributes
    ----------
    message : str
        Message contents.
    time : int
        Time the message was send in milliseconds since January 1, 1970, 00:00:00 (UTC).
    author : str
        Author of the message. Participant ID or "experimenter".
    is_broadcast : bool
        True if the message was send by an experimenter to all participants.  False if
        it is a direct message between experimenter and participant.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#chatlog
    """

    message: str
    time: int
    author: str
    is_broadcast: bool
