import numpy
import cv2

from filters import Filter
from filter_api import FilterAPIInterface


class PingFilter(Filter):
    """A simple example filter printing the current API ping on a video Track.
    """

    filter_api: FilterAPIInterface
    counter: int
    last_ping: int

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)

        self.filter_api = video_track_handler.filter_api
        self.counter = 0
        self.last_ping = 0

    async def complete_setup(self) -> None:
        await self.filter_api.start_pinging()

    async def cleanup(self) -> None:
        self.filter_api.stop_pinging()

    @staticmethod
    def name(self) -> str:
        # change this name
        return "PING"

    @staticmethod
    def filter_type(self) -> str:
        # change this according to your filter type (SESSION or TEST)
        return "SESSION"

    @staticmethod
    def get_filter_json(self) -> object:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return {
            "name": name,
            "id": id,
            "channel": "video",
            "groupFilter": False,
            "config": {},
        }

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # fetch current ping and display it on the video frame
        height, _, _ = ndarray.shape
        origin = (10, height - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        thickness = 3
        color = (0, 255, 0)

        if not self.counter % 30:
            self.last_ping = await self.filter_api.get_current_ping()

        text = "{:.0f} ms".format(self.last_ping)
        ndarray = cv2.putText(
            ndarray, text, origin, font, font_size, color, thickness
        )

        self.counter += 1

        return ndarray
