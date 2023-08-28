"""Provide VideoProcessing for extracting the recorded video of experiments."""

from __future__ import annotations
import logging
import os
import time

from filters.open_face_au.open_face import OpenFace
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

    def set_recorded_data(self, video_path: str, session_id: str, 
                          participant_id: str) -> None:
        self._recorded_data = RecordedData("video", video_path, session_id, participant_id)

    async def execute(self) -> None:
        """Execute the post-processing of the recorded video."""
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions", 
                                self._recorded_data.session_id,
                                "processed")
        self._open_face.run_feature_extraction(self._recorded_data.file_path,
                                               out_dir)

    async def cleanup(self) -> None:
        """Kill OpenFace instance after the post-processing is done."""
        self._open_face.stop()
    