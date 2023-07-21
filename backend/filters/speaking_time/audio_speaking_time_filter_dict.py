from filters.filter_dict import FilterDict


class AudioSpeakingTimeFilterDict(FilterDict):
    """TypedDict for speaking time filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    frames : int
        Amount of frames per second
    seconds : int
        Amount of seconds a participant speaks
    """

    frames: int
    seconds: int
