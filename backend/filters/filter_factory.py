from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.track_handler import TrackHandler

from custom_types.filters import FilterDict
from filters.HelloWorldFilter import HelloWorldFilter
from filters.api_test import FilterAPITestFilter
from filters.edge_outline import EdgeOutlineFilter
from filters.filter import Filter
from filters.mute import MuteAudioFilter, MuteVideoFilter
from filters.rotate import RotationFilter
from modules.exceptions import ErrorDictException


def create_filter(filter_config: FilterDict,
                  audio_track_handler: TrackHandler,
                  video_track_handler: TrackHandler) -> Filter:
    """Create a filter based on `type` of `filter_config`.

    Parameters
    ----------
    filter_config : custom_types.filters.FilterDict
        Filter config used to determine type of filter.  Also passed to new filter.
    audio_track_handler : TrackHandler
        The audio TrackHandler to assign
    video_track_handler : TrackHandler
        The video TrackHandler to assign

    Raises
    ------
    modules.exceptions.ErrorDictException
        If the filter type is unknown.
    """
    filter_type = filter_config["type"]

    match filter_type:
        case "MUTE_AUDIO":
            return MuteAudioFilter(filter_config, audio_track_handler, video_track_handler)
        case "MUTE_VIDEO":
            return MuteVideoFilter(filter_config, audio_track_handler, video_track_handler)
        case "ROTATION":
            return RotationFilter(filter_config, audio_track_handler, video_track_handler)
        case "EDGE_OUTLINE":
            return EdgeOutlineFilter(filter_config, audio_track_handler, video_track_handler)
        case "DELAY":
            return DelayFilter(filter_config, audio_track_handler, video_track_handler)  # type: ignore
        case "FILTER_API_TEST":
            return FilterAPITestFilter(filter_config, audio_track_handler, video_track_handler)
        case "HELLO_WORLD":
            return HelloWorldFilter(filter_config, audio_track_handler, video_track_handler)
        case _:
            raise ErrorDictException(
                code=404,
                type="UNKNOWN_FILTER_TYPE",
                description=f'Unknown filter type "{filter_type}".',
            )
