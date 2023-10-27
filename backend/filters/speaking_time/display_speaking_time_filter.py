import cv2
import numpy
from .audio_speaking_time_filter import AudioSpeakingTimeFilter
from av import VideoFrame

from filters.filter import Filter


class DisplaySpeakingTimeFilter(Filter):
    _speaking_time_filter: AudioSpeakingTimeFilter

    async def complete_setup(self) -> None:
        speaking_time_filter_id = self._config["config"]["filterId"]["value"]
        speaking_time_filter = self.audio_track_handler.filters[speaking_time_filter_id]
        self._speaking_time_filter = speaking_time_filter  # type: ignore

    @staticmethod
    def name() -> str:
        return "DISPLAY_SPEAKING_TIME"

    @staticmethod
    def type() -> str:
        return "SESSION"

    @staticmethod
    def channel() -> str:
        return "video"

    @staticmethod
    def default_config() -> dict:
        return {
            "filterId": {
                "defaultValue": ["AUDIO_SPEAKING_TIME"],
                "value": "",
                "requiresOtherFilter": True,
            }
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
