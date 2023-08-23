from typing import TypedDict


class FilterDict(TypedDict):
    """TypedDict for basic filters with only basic attributes.

    Attributes
    ----------
    name : str
        filter name (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    channel: str
        Either "video", "audio" or "both"
    groupFilter: bool
        If true, the filter is a groupFilter
    config: dict
        Filter configuration. Contains all variables for the filter


    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#filter
    """

    name: str
    id: str
    channel: str
    groupFilter: bool
    config: dict
