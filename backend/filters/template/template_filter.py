import numpy

from filters import Filter
from filters.simple_line_writer import SimpleLineWriter


class TemplateFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()

    @staticmethod
    def name() -> str:
        # TODO: Change this name to a unique name.
        return "TEMPLATE"

    @staticmethod
    def filter_type() -> str:
        # TODO: change this according to your filter type (SESSION, TEST or NONE)
        return "NONE"

    @staticmethod
    def channel() -> str:
        # TODO: change this according to your filter channel (video, audio, both)
        return "video"

    @staticmethod
    def default_config() -> dict:
        # TODO: change this according to your filter config
        return {
            # example of how a filter config can look like
            # add or delete this
            # This would show that there is a string variable (direction) which can have different values
            # and another int variable (size)
            # in the frontend, we would then have either a dropdown (direction) or input number (size)
            # The values can be changed and sent back to the backend
            #
            #
            # "direction": {
            #     "defaultValue": ["clockwise", "anti-clockwise"],
            #     "value": "clockwise",
            #     "requiresOtherFilter": False,
            # },
            # "size": {
            #     "min": 1,
            #     "max": 60,
            #     "step": 1,
            #     "value": 45,
            #     "defaultValue": 45,
            # },
        }

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # TODO: change this to implement filter
        self.line_writer.write_line(ndarray, "Hello World")

        # Return modified frame
        return ndarray
