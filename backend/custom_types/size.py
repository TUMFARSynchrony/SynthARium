"""Provide the `SizeDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict

import custom_types.util as util


class SizeDict(TypedDict):
    """TypedDict for the size of a users's stream on the canvas.

    Attributes
    ----------
    width : int
        Width of the stream.
    height : int
        Height of the stream.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#participant
    """

    width: int
    height: int


def is_valid_size(data) -> bool:
    """Check if `data` is a valid SizeDict.

    Checks if all required and only required or optional keys exist in data as well as
    the data type of the values.

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
        and isinstance(data["width"], int)
        and isinstance(data["height"], int)
    )
