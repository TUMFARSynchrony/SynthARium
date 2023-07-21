from typing import TypeGuard

import cv2
import numpy
from .audio_speaking_time_filter import AudioSpeakingTimeFilter

from custom_types import util
from filters.filter import Filter
from .display_speaking_time_filter_dict import DisplaySpeakingTimeFilterDict

class DisplaySpeakingTimeFilter(Filter):
    """A simple example filter printing `Name` on a video Track.
    Can be used to as a template to copy when creating a new showing filter."""

    _config: DisplaySpeakingTimeFilterDict
    _speaking_time_filter: AudioSpeakingTimeFilter

    async def complete_setup(self) -> None:
        speaking_time_filter_id = self._config["audio_speaking_time_filter_id"]
        speaking_time_filter = self.audio_track_handler.filters[speaking_time_filter_id]
        self._speaking_time_filter =  speaking_time_filter # type: ignore

    '''
    def __init__(
        self, config: NameFilterDict, audio_track_handler, video_track_handler
    ) -> None:
        super().__init__(config, audio_track_handler, video_track_handler)
    '''

    @staticmethod
    def name(self) -> str:
        return "DISPLAY_SPEAKING_TIME"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10,height - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        thickness = 3
        color = (0, 255, 0)

        text = str(self._speaking_time_filter.speaking_time)
        #text = "Test"

        # Put text on image
        ndarray = cv2.putText(ndarray, text, origin, font, font_size, color, thickness)

        # Return modified frame
        return ndarray

    @staticmethod
    def validate_dict(data) -> TypeGuard[DisplaySpeakingTimeFilterDict]:
        return (
            util.check_valid_typeddict_keys(data, DisplaySpeakingTimeFilterDict)
            and "name" in data
            and isinstance(data["name"], str)
            and "audio_speaking_time_filter_id" in data
            and isinstance(data["audio_speaking_time_filter_id"], str)
        )

