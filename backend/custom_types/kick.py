"""Provide the `KickRequestDict` and `KickNotificationDict` TypedDicts.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


class KickRequestDict(TypedDict):
    """TypedDict for `KICK` requests from experimenters.

    Attributes
    ----------
    participant_id : str
        ID of the participant that should be kicked.
    reason : str
        Reason for kicking the participant.
    """

    participant_id: str
    reason: str


class KickNotificationDict(TypedDict):
    """TypedDict for `KICK_NOTIFICATION` messages send to participant.

    Attributes
    ----------
    reason : str
        Reason for kicking the participant.
    """

    reason: str
