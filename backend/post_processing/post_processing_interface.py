"""Provide the abstract `PostProcessingInterface`."""

from __future__ import annotations
from abc import ABCMeta, abstractmethod

from recorded_data import RecordedData

class PostProcessingInterface(metaclass=ABCMeta):
    """Abstract interface for post-processing of the experiments.

    Notes
    -----
    Do not instantiate directly, use subclasses / implementations of
    `PostProcessingInterface` instead.

    See Also
    --------
    post_processing.video_processing : Implementation for PostProcessingInterface.
    """

    @abstractmethod
    async def execute(self) -> None:
        """Execute the post-processing of the recorded data.

        The implementation would depend on the recorded data type, whether it is
        a video or audio.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Kill all external processes after the post-processing is done.

        The implementation would depend on the recorded data type, whether it is
        a video or audio, e.g. it will stop the OpenFace process for video data.
        """
        pass

    @property
    @abstractmethod
    def recorded_data(self) -> RecordedData:
        """Get the post_processing.RecordedData."""
        pass