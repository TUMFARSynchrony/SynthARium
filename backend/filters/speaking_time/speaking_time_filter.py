import numpy
from av import AudioFrame
from filters.filter_dict import FilterDict
from filters.filter_data_dict import FilterDataDict

from filters.filter import Filter


class SpeakingTimeFilter(Filter):
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
        return "SPEAKING_TIME"

    @staticmethod
    def type() -> str:
        return "SESSION"

    @staticmethod
    def channel() -> str:
        return "audio"

    async def get_filter_data(self) -> None | FilterDataDict:
        return FilterDataDict(
            id=self.id,
            data={"time": self.seconds},
        )

    async def process(
        self, audioFrame: AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        if numpy.abs(ndarray).mean() > 125:
            self.seconds += audioFrame.samples / audioFrame.sample_rate
        return ndarray
