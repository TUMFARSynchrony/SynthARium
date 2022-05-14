"""Provide the `SessionIdRequestDict` and `MuteRequestDict` TypedDict.

Also contains functions for checking if something is a valid `SessionIdRequestDict`
(is_valid_session_id_request) or `MuteRequestDict` (is_valid_mute_request).

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict

import custom_types.util as util


class SessionIdRequestDict(TypedDict):
    """TypedDict for requests containing a single session ID, e.g. DELETE_SESSION or
    CREATE_EXPERIMENT.

    Attributes
    ----------
    session_id : int
        Session ID for the requested endpoint.
    """

    session_id: int


def is_valid_session_id_request(data) -> bool:
    """Check if `data` is a valid custom_types.general.SessionIdRequestDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid SessionIdRequestDict.
    """
    return util.check_valid_typeddict_keys(data, SessionIdRequestDict) and isinstance(
        data["session_id"], int
    )


class MuteRequestDict(TypedDict):
    """TypedDict for the MUTE request.

    Attributes
    ----------
    participant_id : str
        Participant ID for the requested endpoint.
    mute_video : bool
    mute_audio : bool
    """

    participant_id: str
    mute_video: bool
    mute_audio: bool


def is_valid_mute_request(data) -> bool:
    """Check if `data` is a valid custom_types.general.MuteRequestDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid MuteRequestDict.
    """
    return (
        util.check_valid_typeddict_keys(data, MuteRequestDict)
        and isinstance(data["participant_id"], str)
        and isinstance(data["mute_video"], bool)
        and isinstance(data["mute_audio"], bool)
    )
