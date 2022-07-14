"""TODO document"""

import cv2  # TODO add to requirements
import numpy
from av import VideoFrame

from filters.filter import VideoFilter


class EdgeOutlineFilter(VideoFilter):
    """TODO document"""

    async def process(self, _: VideoFrame, ndarray: numpy.ndarray) -> numpy.ndarray:
        """TODO document"""
        # Example based on https://github.com/aiortc/aiortc/tree/main/examples/server
        ndarray = cv2.cvtColor(cv2.Canny(ndarray, 100, 200), cv2.COLOR_GRAY2BGR)
        return ndarray
