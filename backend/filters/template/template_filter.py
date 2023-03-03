# from typing import TypeGuard

import cv2
import numpy

# from custom_types import util
from filters import Filter


# from filters.template.template_filter_dict import TemplateFilterDict


class TemplateFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    @staticmethod
    def name(self) -> str:
        # TODO: change this name
        return "TEMPLATE"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # TODO: change this to implement filter
        # Parameters for cv2.putText
        origin = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        color = (0, 0, 0)

        # Put text on image
        ndarray = cv2.putText(ndarray, "Hello World", origin, font, font_size, color)

        # Return modified frame
        return ndarray

    # TODO: add or delete this, depending on filters needs
    # When adding this, you also need to uncomment the imports above, otherwise delete
    """"
    @staticmethod
    def validate_dict(data) -> TypeGuard[TemplateFilterDict]:
        # TODO: implement correct validation method
        return (
            util.check_valid_typeddict_keys(data, TemplateFilterDict)
            and "size" in data
            and isinstance(data["size"], int)
            and data["size"] > 0
        )
    """
