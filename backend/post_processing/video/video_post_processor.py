import asyncio
from typing import List
from post_processing.video.video_processor import VideoProcessor


class VideoPostProcessor:
    def __init__(self, video_processors: List[VideoProcessor]):
        self.video_processors = video_processors  # Manage a list of VideoProcessor instances

    async def execute(self):
        """Execute processing for each VideoProcessor in the list.
        """
        await asyncio.gather(*(vp.process() for vp in self.video_processors))

