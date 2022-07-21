"""Provide `RotationFilter` filter."""

import cv2
import numpy
from av import VideoFrame

from filters.filter import Filter


class RotationFilter(Filter):
    """Filter example rotating a video track."""

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        # For docstring see filters.filter.Filter or hover over function declaration
        # Example based on https://github.com/aiortc/aiortc/tree/main/examples/server
        rows, cols, _ = ndarray.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), original.time * 45, 1)
        ndarray = cv2.warpAffine(ndarray, M, (cols, rows))

        return ndarray
