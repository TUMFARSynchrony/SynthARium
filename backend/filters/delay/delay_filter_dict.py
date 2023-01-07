from typing import TypeGuard

import custom_types.util as util

from filters.filter_dict import FilterDict


class DelayFilterDict(FilterDict):
    """TypedDict for delay filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    size : int
        Amount of frames that should be delayed / buffer size.
    """

    size: int


def is_valid_delay_filter_dict(data) -> TypeGuard[DelayFilterDict]:
    """Check if `data` is a valid custom_types.filters.DelayFilterDict.

    Does not check base class attributes.  Should only be called from
    is_valid_filter_dict.

    See Also
    --------
    is_valid_filter_dict
    """
    return (
        util.check_valid_typeddict_keys(data, DelayFilterDict)
        and "size" in data
        and isinstance(data["size"], int)
        and data["size"] > 0
    )
