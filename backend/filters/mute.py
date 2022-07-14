"""TODO document"""

import numpy
from PIL import Image
from os.path import join
from av import VideoFrame, AudioFrame

from custom_types.filters import FilterDict
from filters.filter import VideoFilter, AudioFilter
from modules import BACKEND_DIR

import modules


class MuteVideoFilter(VideoFilter):
    """TODO document"""

    _muted_frame: VideoFrame
    _muted_ndarray: numpy.ndarray

    def __init__(
        self, id: str, config: FilterDict, connection: modules.connection.Connection
    ) -> None:
        """TODO document"""
        super().__init__(id, config, connection)

        # Load image that will be broadcasted when track is muted.
        img_path = join(BACKEND_DIR, "images/muted.png")
        muted_frame_img = Image.open(img_path)
        self._muted_frame = VideoFrame.from_image(muted_frame_img)
        self._muted_ndarray = self._muted_frame.to_ndarray(format="bgr24")

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray | None = None
    ) -> numpy.ndarray | VideoFrame:
        """TODO document"""
        if self._muted_frame.format != original.format:
            self._muted_frame = self._muted_frame.reformat(format=original.format)
            self._muted_ndarray = self._muted_frame.to_ndarray(format="bgr24")

        # Return muted_ndarray if ndarray is defined
        if ndarray is not None:
            return self._muted_ndarray

        # Update muted_frame metadata.
        self._muted_frame.pts = original.pts
        self._muted_frame.time_base = original.time_base

        return self._muted_frame


class MuteAudioFilter(AudioFilter):
    """TODO document"""

    _muted_frame: AudioFrame
    _muted_ndarray: numpy.ndarray

    def __init__(
        self, id: str, config: FilterDict, connection: modules.connection.Connection
    ) -> None:
        """TODO document"""
        super().__init__(id, config, connection)

        # Create a muted audio frame.
        self._muted_frame = AudioFrame(format="s16", layout="mono", samples=1)
        for p in self._muted_frame.planes:
            p.update(bytes(p.buffer_size))
        self._muted_ndarray = self._muted_frame.to_ndarray()

    async def process(
        self, original: AudioFrame, ndarray: numpy.ndarray | None = None
    ) -> numpy.ndarray | AudioFrame:
        """TODO document"""
        if (
            self._muted_frame.format != original.format
            or self._muted_frame.samples != original.samples
        ):
            self._muted_frame = AudioFrame(
                format=original.format, layout="mono", samples=original.samples
            )
            for p in self._muted_frame.planes:
                p.update(bytes(p.buffer_size))
            self._muted_ndarray = self._muted_frame.to_ndarray()

        # Return muted_ndarray if ndarray is defined
        if ndarray is not None:
            return self._muted_ndarray

        self._muted_frame.pts = original.pts
        self._muted_frame.time_base = original.time_base
        self._muted_frame.sample_rate = original.sample_rate

        return self._muted_frame
