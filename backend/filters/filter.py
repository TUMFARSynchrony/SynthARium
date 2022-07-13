"""TODO document"""

from abc import ABC, abstractmethod
from av import VideoFrame, AudioFrame

from custom_types.filters import FilterDict

# Importing from modules in filter package can cause circular dependencies errors.
# Importing the modules package can avoid this.
# See: https://stackoverflow.com/a/37126790
import modules


class Filter(ABC):
    """TODO document"""

    _id: str
    _config: FilterDict
    _connection: modules.connection.Connection

    def __init__(
        self, id: str, config: FilterDict, connection: modules.connection.Connection
    ) -> None:
        """TODO document"""
        self._id = id
        self._config = config
        self._connection = connection

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
