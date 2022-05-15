"""Provide the `SizeDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


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
