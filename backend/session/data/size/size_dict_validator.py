from typing import TypeGuard

from custom_types import util
from session.data.size.size_dict import SizeDict


def is_valid_size(data) -> TypeGuard[SizeDict]:
    """Check if `data` is a valid SizeDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid SizeDict.
    """
    return (
        util.check_valid_typeddict_keys(data, SizeDict)
        and (isinstance(data["width"], int) or isinstance(data["width"], float))
        and (isinstance(data["height"], int) or isinstance(data["height"], float))
    )