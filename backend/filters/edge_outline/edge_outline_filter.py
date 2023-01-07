"""Provide `EdgeOutlineFilter` filter."""

import cv2
import numpy
from av import VideoFrame

from filters.filter import Filter


class EdgeOutlineFilter(Filter):
    """Filter example outlining corners using Canny edge detector algorithm.

    See Also
    --------
    cv2.Canny : Canny edge detector algorithm.
    https://en.wikipedia.org/wiki/Canny_edge_detector : Canny edge detector.
    """

    @staticmethod
    def name(self) -> str:
        return "EDGE_OUTLINE"

    async def process(self, _: VideoFrame, ndarray: numpy.ndarray) -> numpy.ndarray:
        # For docstring see filters.filter.Filter or hover over function declaration
        # Example based on https://github.com/aiortc/aiortc/tree/main/examples/server
        ndarray = cv2.cvtColor(cv2.Canny(ndarray, 100, 200), cv2.COLOR_GRAY2BGR)
        return ndarray
