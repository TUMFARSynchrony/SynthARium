"""Provide VideoProcessing for extracting the recorded video of experiments."""

from __future__ import annotations
import asyncio
import logging
import multiprocessing
import os
import time

from filters.open_face_au.open_face import OpenFace
from hub.exceptions import ErrorDictException
from .post_processing_interface import PostProcessingInterface
from .recorded_data import RecordedData

class VideoProcessing(PostProcessingInterface):
    """Handles post-processing of the recorded video of experiments."""

    _logger: logging.Logger
    _open_face: OpenFace

    def __init__(self) -> None:
        """Initialize new VideoProcessing for `RecordedData`."""
        super().__init__()
        self._logger = logging.getLogger(f"VideoProcessing")
        self._open_face = OpenFace()

    async def execute(self) -> None:
        """Execute the post-processing of the recorded video."""
        num_workers = multiprocessing.cpu_count() / 3
        self._logger.debug("Number of workers: " + str(num_workers))
        # Create a queue that we will use to store our "workload".
        queue = asyncio.Queue()

        # Put items into the queue.
        # Execute items into num_workers in parallel 
        # (if one of the child process is finished, then execute the next one in queue)
        for video in self._recording_list:
            out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions", 
                                    video.session_id,
                                    "processed")            
            video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions", 
                                    video.session_id,
                                    video.filename)
            queue.put_nowait(video_path)

        # Create three worker tasks to process the queue concurrently.
        tasks = []
        for i in range(num_workers):
            task = asyncio.create_task(self.worker(out_dir, queue))
            tasks.append(task)

        # Wait until the queue is fully processed.
        started_at = time.monotonic()
        await queue.join()
        total_time = time.monotonic() - started_at
        self._logger.debug("Total time: " + str(total_time) + " seconds")


    async def worker(self, out_dir, queue):
        while True:
            # Get a "work item" out of the queue.
            video_path = await queue.get()

            # Run feature extraction
            subprocess = self._open_face.run_feature_extraction(video_path, out_dir)
            await subprocess
            subprocess.wait()

            self._logger.debug("Processing: " + str(video_path))


    async def cleanup(self) -> None:
        """Kill OpenFace instance after the post-processing is done."""
        self._open_face.stop()
    