from __future__ import annotations
from typing import Literal, TYPE_CHECKING

from filters.filter_utils import get_filter_dict

if TYPE_CHECKING:
    from modules.track_handler import TrackHandler

from filters import *

from modules.exceptions import ErrorDictException


def create_filter(
    filter_config: FilterDict,
    audio_track_handler: TrackHandler,
    video_track_handler: TrackHandler,
) -> Filter:
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

    filters = get_filter_dict()

    if filter_type not in filters:
        raise ErrorDictException(
            code=404,
            type="UNKNOWN_FILTER_TYPE",
            description=f'Unknown filter type "{filter_type}".',
        )

    return filters[filter_type](filter_config, audio_track_handler, video_track_handler)


def init_mute_filter(
    kind: Literal["audio", "video"],
    audio_track_handler: TrackHandler,
    video_track_handler: TrackHandler,
) -> MuteAudioFilter | MuteVideoFilter:

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
