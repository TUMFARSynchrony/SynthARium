"""Provide the `FPSDataDict` TypedDict`.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import Any, TypeGuard, TypedDict

import custom_types.util as util


class FPSDataDict(TypedDict):
    """TypedDict for sending chat messages between client and server.

    Attributes
    ----------
    time_in_seconds : int
        Duration seconds.
    fps : float
        Average fps.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#fpsdata
    """

    time_in_seconds: int
    fps: float


def is_valid_fpsdata(data: Any) -> TypeGuard[FPSDataDict]:
    """Check if `data` is a valid FPSDataDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid FPSDataDict.
    """
    return (
        util.check_valid_typeddict_keys(data, FPSDataDict)
        and isinstance(data["time_in_seconds"], int)
        and isinstance(data["fps"], float)
    )
