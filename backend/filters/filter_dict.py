from typing import Literal, TypedDict

FILTER_TYPES = Literal[
    "MUTE_AUDIO",
    "MUTE_VIDEO",
    "DELAY",
    "ROTATION",
    "EDGE_OUTLINE",
    "FILTER_API_TEST",
    "HELLO_WORLD"
]
"""Valid filter types."""


class FilterDict(TypedDict):
    """TypedDict for basic filters with only basic attributes.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#filter
    """

    type: FILTER_TYPES
    id: str
