"""Provide filter TypedDicts: `SetFiltersRequestDict` and `BasicFilterDict`.

Use for type hints and static type checking without any overhead during runtime.

When more complex filters with custom settings are implemented, they should be added
here.  `is_valid_filter_dict` should then include checks for the additional Filters,
based on BasicFilterDict.
"""

from typing import TypedDict

import custom_types.util as util


class BasicFilterDict(TypedDict):
    """TypedDict for basic filters without extra parameters other than a `type`.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#filter
    """

    type: str


def is_valid_filter_dict(data) -> bool:
    """Check if `data` is a valid BasicFilterDict.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid BasicFilterDict.
    """
    return util.check_valid_typeddict_keys(data, BasicFilterDict) and isinstance(
        data["type"], str
    )


class SetFiltersRequestDict(TypedDict):
    """TypedDict for `SET_FILTERS` requests.

    Attributes
    ----------
    participant_id : int
        Participant ID for the requested endpoint.
    filters : list of custom_types.filters.BasicFilterDict
        Active filters for participant with `participant_id`.
    """

    participant_id: int
    filters: list[BasicFilterDict]


def is_valid_set_filters_request(data, recursive: bool = True) -> bool:
    """Check if `data` is a valid custom_types.filters.SetFiltersRequest.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.
    recursive : bool, default True
        If true, filters will be checked recursively.

    Returns
    -------
    bool
        True if `data` is a valid BasicFilterDict.
    """
    if not util.check_valid_typeddict_keys(
        data, SetFiltersRequestDict
    ) or not isinstance(data["filters"], list):
        return False

    if recursive:
        for filter in data["filters"]:
            if not is_valid_filter_dict(filter):
                return False

    return isinstance(data["participant_id"], int)
