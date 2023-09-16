from filters.filter_dict import FilterDict


class DisplaySpeakingTimeFilterDict(FilterDict):
    """TypedDict for name filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    audio_speaking_time_filter_id : str
        Id for the audio speaking time filter
    """

    audio_speaking_time_filter_id: str
