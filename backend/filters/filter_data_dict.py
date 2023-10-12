from typing import Any, TypeGuard, TypedDict, get_args

import custom_types.util as util


class FilterDataDict(TypedDict):
    """TypedDict for filter data which is sent to the user.

    Attributes
    ----------
    id : str
        filter id.
    data : any
        Filter data. Contains the data to be sent

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
