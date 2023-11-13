from typing import TypedDict, Any, TypeGuard

from custom_types import util

from connection.messages import (
    RTCIceCandidateDict,
    is_valid_rtc_ice_candidate_dict
)


class AddIceCandidateDict(TypedDict):
    """TypedDict for a `ADD_ICE_CANDIDATE` message from the client.

    Attributes
    ----------
    id : str
        Identifier of this offer. Must be used in the
        connection.messages.connection_answer_dict.ConnectionAnswerDict
        to identify the answer.
    candidate : connection.messages.rtc_ice_candidate_dict.RTCIceCandidateDict
        New ICE candidate.

    See Also
    --------
    Data Types Wiki :
        TODO
    Connection Protocol Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
    """

    id: str
    candidate: RTCIceCandidateDict


def is_valid_add_ice_candidate_dict(
    data: Any,
) -> TypeGuard[AddIceCandidateDict]:
    """Check if `data` is a valid connection.messages.AddIceCandidateDict.

    Parameters
    ----------
    data : Any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid connection.messages.AddIceCandidateDict.
    """
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, AddIceCandidateDict):
        return False

    return isinstance(data["id"], str) and \
    (data["candidate"] is None or is_valid_rtc_ice_candidate_dict(data["candidate"]))
