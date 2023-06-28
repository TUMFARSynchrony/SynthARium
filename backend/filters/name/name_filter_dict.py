from filters.filter_dict import FilterDict


class NameFilterDict(FilterDict):
    """TypedDict for name filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    name : str
        Name of the participant. Is displayed in left bottom corner.
    """

    name: str
