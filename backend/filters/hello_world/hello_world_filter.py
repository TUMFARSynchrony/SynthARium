# from typing import TypeGuard

import cv2
import numpy

# from custom_types import util
from filters import Filter


# from filters.template.template_filter_dict import TemplateFilterDict


class HelloWorldFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    @staticmethod
    def name(self) -> str:
        # TODO: change this name
        return "HELLO WORLD"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # TODO: change this to implement filter
        # Parameters for cv2.putText
        height, _, _ = ndarray.shape
        origin = (10,height - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        thickness = 3
        color = (0, 255, 0)

        # Put text on image
        ndarray = cv2.putText(ndarray, "Hello World", origin, font, font_size, color, thickness)

        # Return modified frame
        return ndarray

