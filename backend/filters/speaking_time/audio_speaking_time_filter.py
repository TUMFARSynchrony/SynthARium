from typing import TypeGuard

import numpy
from queue import Queue
from av import AudioFrame
from filters.filter_dict import FilterDict

from custom_types import util
from filters.filter import Filter


class AudioSpeakingTimeFilter(Filter):
    """Filter calculating how much time the participant has spoken"""

    speaking_time: int
    seconds: int
    sample_rate: int
    has_spoken: bool
    _config: FilterDict

    def __init__(
        self, config: FilterDict, audio_track_handler, video_track_handler
    ) -> None:
        super().__init__(config, audio_track_handler, video_track_handler)
        self.seconds = 0
        self.speaking_time = 0
        self.has_spoken = False
        self.sample_rate = 0

    @staticmethod
    def name(self) -> str:
        return "AUDIO_SPEAKING_TIME"

    async def process(self, original: AudioFrame, ndarray: numpy.ndarray) -> numpy.ndarray:
        if numpy.abs(ndarray).mean() > 250:
            self.has_spoken = True
            self.sample_rate = original.sample_rate
            self.speaking_time += original.samples
        else:
            self.has_spoken = False
        self.seconds = self.speaking_time // original.sample_rate
        # todo: seconds stimmt nicht mit original.time überein
        # time ist 16.46, self.seconds ist 5 obwohl die ganze Zeit geredet (vielleicht aber nicht jeden Frame)
        return ndarray

