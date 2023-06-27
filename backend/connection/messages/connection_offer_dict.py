from typing import TypedDict, TypeGuard, Any

from connection.messages import (
    RTCSessionDescriptionDict,
    is_valid_rtc_session_description_dict,
)
from custom_types import util


class ConnectionOfferDict(TypedDict):
    """TypedDict for sending a `CONNECTION_OFFER` message to the client.

    Attributes
    ----------
    id : str
        Identifier of this offer.  Must be used in the
        connection.messages.connection_answer_dict.ConnectionAnswerDict to identify the answer.
    offer : connection.messages.rtc_session_description_dict.RTCSessionDescriptionDict
        WebRtc offer.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#ConnectionOffer
    Connection Protocol Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
    """

    id: str
    offer: RTCSessionDescriptionDict


def is_valid_connection_offer_dict(data: Any) -> TypeGuard[ConnectionOfferDict]:
    """Check if `data` is a valid custom_types.connection.ConnectionOfferDict.

    Parameters
    ----------
    data : Any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid custom_types.connection.ConnectionOfferDict.
    """
    # Check if all required and only required or optional keys exist in data
    if not util.check_valid_typeddict_keys(data, ConnectionOfferDict):
        return False

    return isinstance(data["id"], str) and is_valid_rtc_session_description_dict(
        data["offer"]
    )
