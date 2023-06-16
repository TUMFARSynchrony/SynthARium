"""Provide the `PositionDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


class PositionDict(TypedDict):
    """3D position for a user on a canvas.

    Attributes
    ----------
    x : int or float
        X coordinate.
    y : int or float
        Y coordinate.
    z : int or float
        Z coordinate.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#Participant
    """

    x: int | float
    y: int | float
    z: int | float
