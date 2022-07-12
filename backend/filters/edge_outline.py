"""TODO document"""

import cv2  # TODO add to requirements
from av import VideoFrame

from filters.filter import VideoFilter


class EdgeOutlineFilter(VideoFilter):
    """TODO document"""

    async def process(self, frame: VideoFrame) -> VideoFrame:
        """TODO document"""
        # Example from https://github.com/aiortc/aiortc/tree/main/examples/server
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.time_base = frame.time_base
        new_frame.pts = frame.pts
        return new_frame
