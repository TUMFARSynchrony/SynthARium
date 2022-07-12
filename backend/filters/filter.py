"""TODO document"""

from abc import ABC, abstractmethod
from av import VideoFrame, AudioFrame


class Filter(ABC):
    """TODO document"""

    _id: str
    _config: dict

    def __init__(self, id: str, config: dict) -> None:
        """TODO document"""
        self.id = id
        self.config = config

    @property
    def id(self) -> str:
        """TODO document"""
        return self._id

    @property
    def config(self) -> dict:
        """TODO document"""
        return self._config

    @id.setter
    def id(self, value: str) -> None:
        """TODO document"""
        self.id = value

    @config.setter
    def config(self, value: dict) -> None:
        """TODO document"""
        self.config = value

    @abstractmethod
    async def process(self, frame: VideoFrame | AudioFrame) -> VideoFrame | AudioFrame:
        """TODO document"""
        pass

    def __repr__(self) -> str:
        """TODO document"""
        return f"{self.__class__.__name__}(id={self.id}, config={self.config})"


class VideoFilter(Filter):
    """TODO document"""

    @abstractmethod
    async def process(self, frame: VideoFrame) -> VideoFrame:
        """TODO document"""
        pass


class AudioFilter(Filter):
    """TODO document"""

    @abstractmethod
    async def process(self, frame: AudioFrame) -> AudioFrame:
        """TODO document"""
        pass
