"""Provide the `ParticipantDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import Any, TypedDict
from typing_extensions import NotRequired

from custom_types.size import SizeDict
from custom_types.position import PositionDict


class ParticipantDict(TypedDict):
    """TypedDict for api messages.  All messages send should be a MessageDict.

    The `MessageDict` is used to send and receive messages and identify the contents of
    a message via `type`.  The content of a message can be anything, e.g. a ErrorDict,
    Session Data, ...

    Attributes
    ----------
    id: str, optional
        Unique id for this participant in a Session.  When creating a new Participant in
        a Session, this field is initially left blank.
    first_name : str
        First name of the participant.
    last_name : str
        Last name of the participant.
    muted : bool
        TODO define
    filters : list of TODO define type
        Active filters for this participant.
    position : custom_types.position.PositionDict
        Position of the participant's stream on the canvas.
    size : custom_types.size.SizeDict
        Size of the participant's stream on the canvas.


    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#Participant
    """

    id: NotRequired[str]
    first_name: str
    last_name: str
    muted: bool
    filters: list[Any]
    position: PositionDict
    size: SizeDict
