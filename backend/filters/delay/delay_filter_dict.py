from filters.filter_dict import FilterDict


class DelayFilterDict(FilterDict):
    """TypedDict for delay filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    size : int
        Amount of frames that should be delayed / buffer size.
    """

    size: int
