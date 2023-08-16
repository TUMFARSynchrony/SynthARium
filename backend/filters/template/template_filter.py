# from typing import TypeGuard

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

    @staticmethod
    def get_filter_json(self) -> object:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return {
            "type": name,
            "id": id,
            "channel": "video",
            "groupFilter": False,
            "config": {
                # add or delete this, example of how a filter config can look like
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
            }
        }

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
