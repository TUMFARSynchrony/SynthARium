from typing import Any, List, TypeGuard, TypedDict
from .filter_data_dict import FilterDataDict

import custom_types.util as util


class FiltersDataDict(TypedDict):
    """TypedDict for many filters' data which is sent to the user.

    Attributes
    ----------
    video : list of FilterDataDict
        List of video filter data.
    audio : list of FilterDataDict
        List of audio filter data.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#filtersdata
    """

    video: List[FilterDataDict]
    audio: List[FilterDataDict]


def is_valid_messagedict(data: Any) -> TypeGuard[FiltersDataDict]:
    """Check if `data` is a valid FiltersDataDict.

    Checks if id type of string and no unknown keys exist in data

    Does not check the contents of FiltersDataDict.video / .audio.

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
    return util.check_valid_typeddict_keys(data, FiltersDataDict)
