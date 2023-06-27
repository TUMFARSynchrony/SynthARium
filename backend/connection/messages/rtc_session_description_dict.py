from typing import TypedDict, Literal, Any, TypeGuard, get_args

from custom_types import util

RTC_SESSION_TYPES = Literal["offer", "pranswer", "answer", "rollback"]


class RTCSessionDescriptionDict(TypedDict):
    """TypedDict representing a WebRtc session description.

    Attributes
    ----------
    sdp : str
        Session Description Protocol.
    type : custom_types.connection.RTC_SESSION_TYPES
        Type of the session description.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#RTCSessionDescription
    Connection Protocol Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
    """

    sdp: str
    type: RTC_SESSION_TYPES


def is_valid_rtc_session_description_dict(
    data: Any,
) -> TypeGuard[RTCSessionDescriptionDict]:
    """Check if `data` is a valid custom_types.connection.RTCSessionDescriptionDict.

    Parameters
    ----------
    data : Any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid custom_types.connection.RTCSessionDescriptionDict.
    """
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, RTCSessionDescriptionDict):
        return False

    return isinstance(data["sdp"], str) and data["type"] in get_args(RTC_SESSION_TYPES)
