from typing import TypedDict
from filters.filter_dict import FilterDict


class SetGroupFiltersRequestDict(TypedDict):
    audio_group_filters: list[FilterDict]
    video_group_filters: list[FilterDict]
