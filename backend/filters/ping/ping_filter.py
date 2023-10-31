import numpy

from filters import Filter
from filter_api import FilterAPIInterface
from filters.simple_line_writer import SimpleLineWriter


class PingFilter(Filter):
    """A simple example filter printing the current API ping on a video Track."""

    line_writer: SimpleLineWriter
    filter_api: FilterAPIInterface

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()

        self.filter_api = video_track_handler.filter_api

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
        # add ping to image
        self.line_writer.write_line(ndarray, f"{await self.get_current_ping()}")

        # Return modified frame
        return ndarray

    async def get_current_ping(self) -> int:
        return await self.filter_api.get_current_ping()
