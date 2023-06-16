from typing import TypedDict, Any, TypeGuard

from connection.messages import (
    RTCSessionDescriptionDict,
    is_valid_rtc_session_description_dict,
)
from custom_types import util


class ConnectionAnswerDict(TypedDict):
    """TypedDict for the client answer `CONNECTION_ANSWER` to `CONNECTION_OFFER`.

    Attributes
    ----------
    id : str
        Identifier of the original custom_types.connection.ConnectionOfferDict
        / `CONNECTION_OFFER`.
    answer : connection.messages.rtc_session_description_dict.RTCSessionDescriptionDict
        WebRtc answer to the offer send before.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#ConnectionAnswer
    Connection Protocol Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
    """

    id: str
    answer: RTCSessionDescriptionDict


def is_valid_connection_answer_dict(data: Any) -> TypeGuard[ConnectionAnswerDict]:
    """Check if `data` is a valid custom_types.connection.ConnectionAnswerDict.

    Parameters
    ----------
    data : Any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid custom_types.connection.ConnectionAnswerDict.
    """
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, ConnectionAnswerDict):
        return False

    return isinstance(data["id"], str) and is_valid_rtc_session_description_dict(
        data["answer"]
    )
