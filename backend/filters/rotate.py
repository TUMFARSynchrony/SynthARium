"""TODO document"""

import cv2  # TODO add to requirements
from av import VideoFrame

from filters.filter import VideoFilter


class RotationFilter(VideoFilter):
    """TODO document"""

    async def process(self, frame: VideoFrame) -> VideoFrame:
        """TODO document"""
        # Example from https://github.com/aiortc/aiortc/tree/main/examples/server
        img = frame.to_ndarray(format="bgr24")
        rows, cols, _ = img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
        img = cv2.warpAffine(img, M, (cols, rows))

        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.time_base = frame.time_base
        new_frame.pts = frame.pts
        return new_frame
