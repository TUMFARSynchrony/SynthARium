from typing import TypedDict
from .filter_dict import FilterDict


class SetFiltersRequestDict(TypedDict):
    """TypedDict for `SET_FILTERS` requests.

    Attributes
    ----------
    participant_id : str
        Participant ID for the requested endpoint.
    audio_filters : list of filters.FilterDict
        Active audio filters for participant with `participant_id`.
    video_filters : list of filters.FilterDict
        Active video filters for participant with `participant_id`.
    """

    participant_id: str
    audio_filters: list[FilterDict]
    video_filters: list[FilterDict]
