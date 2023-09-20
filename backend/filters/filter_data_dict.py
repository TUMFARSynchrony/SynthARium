from typing import Any, TypeGuard, TypedDict, get_args

import custom_types.util as util


class FilterDataDict(TypedDict):
    """TypedDict for basic filters with only basic attributes.

    Attributes
    ----------
    name : str
        filter name (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    channel: str
        Either "video", "audio" or "both"
    groupFilter: bool
        If true, the filter is a groupFilter
    config: dict
        Filter configuration. Contains all variables for the filter


    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#filter
    """

    id: str
    data: Any


def is_valid_messagedict(data: Any) -> TypeGuard[FilterDataDict]:
    """Check if `data` is a valid FilterDataDict.

    Checks if id type of string and no unknown keys exist in data

    Does not check the contents of FilterDataDict.data / non recursive.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid MessageDict.
    """
    # Check if all required and only required or optional keys exist in data
    return util.check_valid_typeddict_keys(data, FilterDataDict)
