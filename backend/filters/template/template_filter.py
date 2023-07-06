# from typing import TypeGuard

import cv2
import numpy

# from custom_types import util
from filters import Filter
from filters.simple_line_writer import SimpleLineWriter


# from filters.template.template_filter_dict import TemplateFilterDict


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

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # change this to implement filter
        self.line_writer.write_line(ndarray, "Hello World")

        # Return modified frame
        return ndarray

    # add or delete this, depending on filters needs
    # When adding this, you also need to uncomment the imports above, otherwise delete
    """"
    @staticmethod
    def validate_dict(data) -> TypeGuard[TemplateFilterDict]:
        # implement correct validation method
        return (
            util.check_valid_typeddict_keys(data, TemplateFilterDict)
            and "size" in data
            and isinstance(data["size"], int)
            and data["size"] > 0
        )
    """
