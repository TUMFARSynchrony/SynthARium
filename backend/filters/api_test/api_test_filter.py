"""Provide the test filter `FilterAPITestFilter` class."""

import numpy
from av import VideoFrame
from datetime import datetime
from custom_types.message import MessageDict

from filters.filter import Filter


class FilterAPITestFilter(Filter):
    """Filter testing filter API."""

    @staticmethod
    def name(self) -> str:
        return "FILTER_API_TEST"

    counter = 0

    async def process(self, _: VideoFrame, ndarray: numpy.ndarray) -> numpy.ndarray:
        # For docstring see filters.filter.Filter or hover over function declaration

        # Send message every 300'th frame = 10 seconds (assuming 30fps)
        # Note: instead of a frame counter, `original.time` could also be used.
        if not self.counter % 300:
            await self.send_test_message()

        self.counter += 1

        return ndarray

    async def send_test_message(self) -> None:
        """Send a test message using `FilterAPI.experiment_send`."""
        filter_api = self.audio_track_handler.filter_api
        msg = MessageDict(
            type="TEST",
            data={
                "description": "Test message sent by FilterAPITestFilter",
                "frame_counter": self.counter,
                "time": str(datetime.now()),
            },
        )
        await filter_api.experiment_send("all", msg, "")
