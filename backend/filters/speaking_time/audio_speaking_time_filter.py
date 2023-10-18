import numpy
from av import AudioFrame
from filters.filter_dict import FilterDict

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
    def name(self) -> str:
        return "AUDIO_SPEAKING_TIME"

    @staticmethod
    def filter_type(self) -> str:
        return "SESSION"

    @staticmethod
    def init_config(self) -> object:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return FilterDict(
            name=name,
            id=id,
            channel="audio",
            groupFilter=False,
            config={},
        )

    async def process(
        self, audioFrame: AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        if numpy.abs(ndarray).mean() > 125:
            self.seconds += audioFrame.samples / audioFrame.sample_rate
        return ndarray
