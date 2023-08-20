"""Provide VideoProcessing for extracting the recorded video of experiments."""

from __future__ import annotations
import logging
import time


from post_processing_interface import PostProcessingInterface
from filters.open_face_au.open_face import OpenFace


class VideoProcessing(PostProcessingInterface):
    """Handles post-processing of the recorded video of experiments."""

    _logger: logging.Logger
    _open_face: OpenFace

    def __init__(
        self
    ) -> None:
        """Initialize new VideoProcessing for `RecordedData`."""
        super().__init__()
        self._logger = logging.getLogger(f"VideoProcessing")
        #TODO: modify openface init method
        self._open_face = OpenFace()

    async def execute(self) -> None:
        """Execute the post-processing of the recorded video."""
        pass

    async def cleanup(self) -> None:
        """Kill OpenFace instance after the post-processing is done."""
        pass
