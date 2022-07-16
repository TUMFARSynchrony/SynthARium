"""TODO document"""


from __future__ import annotations

import numpy
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from av import VideoFrame, AudioFrame

from custom_types.filters import FilterDict

if TYPE_CHECKING:
    from modules.track_handler import TrackHandler


class Filter(ABC):
    """TODO document"""

    audio_track_handler: TrackHandler
    video_track_handler: TrackHandler
    run_if_muted: bool
    """Whether this filter should be executed if the TrackHandler is muted.

    Call `TrackHandler.reset_execute_filters()` in case the value is changed manually
    after initialization.
    """

    _id: str
    _config: FilterDict

    def __init__(
        self,
        id: str,
        config: FilterDict,
        audio_track_handler: TrackHandler,
        video_track_handler: TrackHandler,
    ) -> None:
        """TODO document"""
        self.run_if_muted = False
        self._id = id
        self._config = config
        self.audio_track_handler = audio_track_handler
        self.video_track_handler = video_track_handler

    @property
    def id(self) -> str:
        """TODO document"""
        return self._id

    @property
    def config(self) -> FilterDict:
        """TODO document"""
        return self._config

    def set_config(self, config: FilterDict) -> None:
        """TODO document"""
        self._config = config

    async def cleanup(self) -> None:
        """TODO document - cleanup called before filter is deleted, stop worker tasks here"""
        return

    @abstractmethod
    async def process(
        self, original: VideoFrame | AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        """TODO document"""
        pass

    def __repr__(self) -> str:
        """TODO document"""
        return f"{self.__class__.__name__}(id={self.id}, config={self.config})"


class VideoFilter(Filter):
    """TODO document"""

    @abstractmethod
    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        """TODO document"""
        pass


class AudioFilter(Filter):
    """TODO document"""

    @abstractmethod
    async def process(
        self, original: AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        """TODO document"""
        pass
