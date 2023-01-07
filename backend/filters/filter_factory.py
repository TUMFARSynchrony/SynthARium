from __future__ import annotations
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.track_handler import TrackHandler

from filters import *

from modules.exceptions import ErrorDictException
import logging


logger = logging.getLogger("Filters")

filter_dict = {}

for concrete_filter in Filter.__subclasses__():
    filter_name = concrete_filter.name(concrete_filter)
    if filter_name in filter_dict:
        # Error handling
        # Doesn't exactly work right now because of import order issues, but not problematic for now
        logger.warning(f"WARNING:Filters: Filter name {filter_name} "
                       f"already exists for class {concrete_filter.__name__}")
    else:
        filter_dict[filter_name] = concrete_filter


def create_filter(filter_config: FilterDict,
                  audio_track_handler: TrackHandler,
                  video_track_handler: TrackHandler) -> Filter:
    """Create a filter based on `type` of `filter_config`.

    Parameters
    ----------
    filter_config : filters.FilterDict
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

    if filter_type not in filter_dict:
        raise ErrorDictException(
            code=404,
            type="UNKNOWN_FILTER_TYPE",
            description=f'Unknown filter type "{filter_type}".',
        )

    return filter_dict[filter_type](filter_config, audio_track_handler, video_track_handler)


def init_mute_filter(
        kind: Literal["audio", "video"],
        audio_track_handler: TrackHandler,
        video_track_handler: TrackHandler) -> MuteAudioFilter | MuteVideoFilter:

    if kind == "audio":
        return MuteAudioFilter(
            {"id": "0", "type": "MUTE_AUDIO"},
            audio_track_handler,
            video_track_handler,
        )
    else:
        return MuteVideoFilter(
            {"id": "0", "type": "MUTE_VIDEO"},
            audio_track_handler,
            video_track_handler,
        )
