from typing import TypeGuard

import cv2
import numpy
import dlib

from custom_types import util
from filters.filter import Filter


class GlassesDetection(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    @staticmethod
    def name(self) -> str:
        return "GLASSES_DETECTION"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # Return modified frame
        return ndarray
