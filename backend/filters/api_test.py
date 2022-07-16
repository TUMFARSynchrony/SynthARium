"""TODO document"""

import numpy
from av import VideoFrame
from datetime import datetime
from custom_types.message import MessageDict

from filters.filter import VideoFilter


class FilterAPITestFilter(VideoFilter):
    """TODO document"""

    counter = 0

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        """TODO document"""
        # Send message every 300'th frame = 10 seconds (assuming 30fps)
        if not self.counter % 300:
            await self.send_test_message(original)

        self.counter += 1

        return ndarray

    async def send_test_message(self, original) -> None:
        """TODO document"""
        filter_api = self.audio_track_handler.filter_api
        msg = MessageDict(
            type="TEST",
            data={
                "description": "Test message send by FilterAPITestFilter",
                "frame_counter": self.counter,
                "time": str(datetime.now()),
            },
        )
        await filter_api.experiment_send("all", msg, "")
