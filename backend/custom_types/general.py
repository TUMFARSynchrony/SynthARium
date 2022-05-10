"""Provide the `SessionIdRequest` and `ParticipantIdRequest` TypedDict.

Also contains functions for checking if something is a valid `SessionIdRequest`
(is_valid_session_id_request) or `ParticipantIdRequest`
(is_valid_participant_id_request).

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict

import modules.util as util


class SessionIdRequest(TypedDict):
    """TypedDict for requests containing a single session ID, e.g. DELETE_SESSION or
    CREATE_EXPERIMENT.

    Attributes
    ----------
    session_id : int
        Session ID for the requested endpoint.
    """

    session_id: int


def is_valid_session_id_request(data) -> bool:
    """Check if `data` is a valid custom_types.general.SessionIdRequest.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid SessionIdRequest.
    """
    return util.check_valid_typeddict_keys(data, SessionIdRequest) and isinstance(
        data["session_id"], int
    )


class MuteRequest(TypedDict):
    """TypedDict for the MUTE request.

    Attributes
    ----------
    participant_id : int
        Participant ID for the requested endpoint.
    mute_video : bool
    mute_audio : bool
    """

    participant_id: int
    mute_video: bool
    mute_audio: bool


def is_valid_mute_request(data) -> bool:
    """Check if `data` is a valid custom_types.general.MuteRequest.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid MuteRequest.
    """
    return (
        util.check_valid_typeddict_keys(data, MuteRequest)
        and isinstance(data["participant_id"], int)
        and isinstance(data["mute_video"], bool)
        and isinstance(data["mute_audio"], bool)
    )
