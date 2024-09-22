import asyncio
import os

import cv2
import numpy as np

from post_processing.video.video_processor import VideoProcessor


class ManipulativeVideoProcessor(VideoProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.output_path = None
        self.out = None

    async def process(self, batch_size: int = 5):
        """Process the videos by applying manipulative filters."""
        await self.process_videos(batch_size)

    async def setup_output(self, filename: str, cap: cv2.VideoCapture):
        """Set up the video writer for output."""
        self.output_path = os.path.join(self.output_dir, filename)

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')

        self.out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

    async def handle_frame_output(self, frame: np.ndarray):
        """Write the processed frame to the output video."""
        if self.out is not None:
            await asyncio.get_event_loop().run_in_executor(None, self.out.write, frame)
        else:
            self.logger.error("Output VideoWriter is not initialized.")

    async def finalize_output(self):
        """Release the output video writer."""
        if self.out is not None:
            self.out.release()
            self.out = None