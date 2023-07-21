from typing import TypeGuard

import cv2
import numpy
from queue import Queue
from av import VideoFrame, AudioFrame

from custom_types import util
from filters.filter import Filter
from .audio_speaking_time_filter_dict import AudioSpeakingTimeFilterDict


class AudioSpeakingTimeFilter(Filter):
    """Filter calculating how much time the participant has spoken"""

    buffer: Queue[int]
    speaking_time: int
    _config: AudioSpeakingTimeFilterDict

    def __init__(
        self, config: AudioSpeakingTimeFilterDict, audio_track_handler, video_track_handler
    ) -> None:
        super().__init__(config, audio_track_handler, video_track_handler)
        self.buffer = Queue(config["frames"])
        self.speaking_time = config["seconds"]

    @staticmethod
    def name(self) -> str:
        return "AUDIO_SPEAKING_TIME"

    async def process(self, _: AudioFrame, ndarray: numpy.ndarray) -> numpy.ndarray:
        if numpy.abs(ndarray).mean() > 500:
            self.speaking_time += 1

        return ndarray

    @staticmethod
    def validate_dict(data) -> TypeGuard[AudioSpeakingTimeFilterDict]:
        return (
            util.check_valid_typeddict_keys(data, AudioSpeakingTimeFilterDict)
            and "frames" in data
            and isinstance(data["frames"], int)
            and data["frames"] > 0
            and "seconds" in data
            and isinstance(data["seconds"], int)
            and data["seconds"] >= 0
        )
