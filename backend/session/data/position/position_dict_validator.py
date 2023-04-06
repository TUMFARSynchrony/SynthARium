from typing import TypeGuard

from custom_types import util
from session.data.position import PositionDict


def is_valid_position(data) -> TypeGuard[PositionDict]:
    """Check if `data` is a valid PositionDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid PositionDict.
    """
    return (
        util.check_valid_typeddict_keys(data, PositionDict)
        and (isinstance(data["x"], int) or isinstance(data["x"], float))
        and (isinstance(data["y"], int) or isinstance(data["y"], float))
        and (isinstance(data["z"], int) or isinstance(data["z"], float))
    )
