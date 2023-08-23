from typing import TypeGuard

import cv2
import numpy
from .audio_speaking_time_filter import AudioSpeakingTimeFilter
from av import VideoFrame

from custom_types import util
from filters.filter import Filter
from .display_speaking_time_filter_dict import DisplaySpeakingTimeFilterDict


class DisplaySpeakingTimeFilter(Filter):
    _speaking_time_filter: AudioSpeakingTimeFilter

    async def complete_setup(self) -> None:
        speaking_time_filter_id = self._config["config"]["filterId"]["value"]
        speaking_time_filter = self.audio_track_handler.filters[speaking_time_filter_id]
        self._speaking_time_filter = speaking_time_filter  # type: ignore

    @staticmethod
    def name(self) -> str:
        return "DISPLAY_SPEAKING_TIME"

    @staticmethod
    def get_filter_json(self) -> object:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return {
            "type": name,
            "id": id,
            "channel": "video",
            "groupFilter": False,
            "config": {
                "filterId": {
                    "defaultValue": ["audio-speaking-time"],
                    "value": "audio-speaking-time",
                },
            },
        }

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10, height - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        thickness = 3
        color = (0, 255, 0)
        """
        if self._speaking_time_filter.has_spoken:
            self._speaking_time_filter.speaking_time += self._speaking_time_filter.sample_rate // original.pts
            self._speaking_time_filter.seconds = self._speaking_time_filter.speaking_time // self._speaking_time_filter.sample_rate
        """
        text = str(self._speaking_time_filter.seconds)

        # Put text on image
        ndarray = cv2.putText(ndarray, text, origin, font, font_size, color, thickness)

        # Return modified frame
        return ndarray
