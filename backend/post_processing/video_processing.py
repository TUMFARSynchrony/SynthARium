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
        start = time.time()
        for video in self._recording_list:
            start_video = time.time()
            out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions", 
                                    video.session_id,
                                    "processed")            
            video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions", 
                                    video.session_id,
                                    video.filename)
            subprocess = await self._open_face.run_feature_extraction(video_path, out_dir)
            self._logger.debug(f"Processing: {video_path}")
            subprocess.wait()
            end_video = time.time()
            self._logger.debug(f"Feature extraction finished for {(end_video - start_video)} seconds")

        end = time.time()
        self._logger.debug(f"Total time: {(end - start)} seconds")
    