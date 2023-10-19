import numpy
from av import AudioFrame
from filters.filter import Filter
from filters import FilterDict


class AudioSpeakingTimeFilter(Filter):
    """Filter calculating how much time the participant has spoken"""

    seconds: float
    _config: FilterDict

    def __init__(
        self, config: FilterDict, audio_track_handler, video_track_handler
    ) -> None:
        super().__init__(config, audio_track_handler, video_track_handler)
        self.seconds = float(0)

    @staticmethod
    def name() -> str:
        return "AUDIO_SPEAKING_TIME"

    @staticmethod
    def filter_type() -> str:
        return "SESSION"

    @staticmethod
    def channel() -> str:
        return "audio"

    async def process(
        self, audioFrame: AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        if numpy.abs(ndarray).mean() > 125:
            self.seconds += audioFrame.samples / audioFrame.sample_rate
        return ndarray
