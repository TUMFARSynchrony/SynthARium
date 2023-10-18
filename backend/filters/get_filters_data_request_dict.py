from typing import TypedDict


class GetFiltersDataRequestDict(TypedDict):
    """TypedDict for `GET_FILTERS_DATA` requests.

    Attributes
    ----------
    filter_name : str
        Name of the requested filter.
    filter_id : str
        Filter ID of the requested filter. Can be either the id or 'all' for all filters
        with name.
    filter_channel : str
        Filter channel of the requested filter. Can be either 'audio', 'video' or 'both'.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchrony/experimental-hub/wiki/Data-Types#getfiltersdatarequest
    """

    filter_id: str
    filter_name: str
    filter_channel: str
