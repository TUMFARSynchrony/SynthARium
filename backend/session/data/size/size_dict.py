from typing import TypedDict


class SizeDict(TypedDict):
    """TypedDict for the size of a users' stream on the canvas.

    Attributes
    ----------
    width : int or float
        Width of the stream.
    height : int or float
        Height of the stream.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#participant
    """

    width: int | float
    height: int | float
