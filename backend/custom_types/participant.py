"""Provide the `ParticipantDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import Any
from typing_extensions import NotRequired, TypedDict

import modules.util as util

from custom_types.size import SizeDict, is_valid_size
from custom_types.chat_message import ChatMessageDict, is_valid_chatmessage
from custom_types.position import PositionDict, is_valid_position


class ParticipantDict(TypedDict):
    """TypedDict for api messages.  All messages send should be a MessageDict.

    The `MessageDict` is used to send and receive messages and identify the contents of
    a message via `type`.  The content of a message can be anything, e.g. an ErrorDict,
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
    chat : list of custom_types.chat_log.ChatLogDict
        Chat log between experimenter and participant.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#Participant
    """

    id: NotRequired[str]
    first_name: str
    last_name: str
    muted_video: bool
    muted_audio: bool
    filters: list[Any]
    position: PositionDict
    size: SizeDict
    chat: list[ChatMessageDict]


def is_valid_participant(data, recursive: bool) -> bool:
    """Check if `data` is a valid ParticipantDict.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.
    recursive : bool
        If true, filters, chat, position and size will be checked recursively.

    Returns
    -------
    bool
        True if `data` is a valid ParticipantDict.
    """
    if not util.check_valid_typeddict_keys(data, ParticipantDict):
        return False

    # Check filters & chat list
    if (
        not isinstance(data["filters"], list)
        or not isinstance(data["chat"], list)
        or not isinstance(data["position"], dict)
        or not isinstance(data["size"], dict)
    ):
        return False

    if recursive:
        # TODO implement filter checks
        # for entry in data["filters"]:
        #     if not is_valid_filter(entry):
        #         return False
        for entry in data["chat"]:
            if not is_valid_chatmessage(entry):
                return False
        if not is_valid_size(data["size"]) or not is_valid_position(data["position"]):
            return False

    valid_id = "id" not in data or isinstance(data["id"], str)
    return (
        valid_id
        and isinstance(data["first_name"], str)
        and isinstance(data["last_name"], str)
        and isinstance(data["muted_video"], bool)
        and isinstance(data["muted_audio"], bool)
    )
