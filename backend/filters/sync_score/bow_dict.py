from filters.filter_dict import FilterDict


class BoWDict(FilterDict):
    """TypedDict for BoW Filter used in Synchrony Score Filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    openface_au_filter_id : str
        OpenFace Filter id which extracts AU from frames
    """

    openface_au_filter_id: str
