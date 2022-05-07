"""Provide the `PositionDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict

import modules.util as util


class PositionDict(TypedDict):
    """3D position for a user on a canvas.

    Attributes
    ----------
    x : int
        X coordinate.
    y : int
        Y coordinate.
    z : int
        Z coordinate.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#Participant
    """

    x: int
    y: int
    z: int


def is_valid_position(data) -> bool:
    """Check if `data` is a valid PositionDict.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

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
        and isinstance(data["x"], int)
        and isinstance(data["y"], int)
        and isinstance(data["z"], int)
    )
