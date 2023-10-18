import numpy

from filters import Filter
from filters import FilterDict
from filters.simple_line_writer import SimpleLineWriter


class TemplateFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()

    @staticmethod
    def name(self) -> str:
        # change this name
        return "TEMPLATE"

    @staticmethod
    def filter_type(self) -> str:
        # change this according to your filter type (SESSION or TEST)
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
            channel="video",
            groupFilter=False,
            config={
                # example of how a filter config can look like
                # add or delete this
                # This would show that there is a string variable (direction) which can have different values
                # and another int variable (size)
                # in the frontend, we would then have either a dropdown (direction) or input number (size)
                # The values can be changed and sent back to the backend
                """
                "direction": {
                    "defaultValue": ["clockwise", "anti-clockwise"],
                    "value": "clockwise",
                },
                "size": {
                    "min": 1,
                    "max": 60,
                    "step": 1,
                    "value": 45,
                    "defaultValue": 45,
                }, """
            },
        )

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # change this to implement filter
        self.line_writer.write_line(ndarray, "Hello World")

        # Return modified frame
        return ndarray
