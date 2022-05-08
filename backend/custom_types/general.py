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


class ParticipantIdRequest(TypedDict):
    """TypedDict for requests containing a single participant ID, e.g. for MUTE_AUDIO or
    MUTE_VIDEO.

    Attributes
    ----------
    participant_id : int
        Participant ID for the requested endpoint.
    """

    participant_id: int


def is_valid_participant_id_request(data) -> bool:
    """Check if `data` is a valid custom_types.general.ParticipantIdRequest.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid ParticipantIdRequest.
    """
    return util.check_valid_typeddict_keys(data, ParticipantIdRequest) and isinstance(
        data["participant_id"], int
    )
