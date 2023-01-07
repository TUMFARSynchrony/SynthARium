"""Provide `DelayFilter` filter."""

import numpy
from queue import Queue
from av import VideoFrame, AudioFrame

from filters.filter import Filter
from .delay_filter_dict import DelayFilterDict


class DelayFilter(Filter):
    """Filter delaying the input by a set amount of frames.

    Works for audio or video input.
    """

    buffer: Queue[numpy.ndarray]
    _config: DelayFilterDict

    def __init__(
        self, config: DelayFilterDict, audio_track_handler, video_track_handler
    ) -> None:
        """Initialize new MuteVideoFilter.

        Load the muted frame image `/images/muted.png` and store it as av.VideoFrame as
        well as numpy.ndarray for quick access in `process`.

        Parameters
        ----------
        See base class: filters.filter.Filter.
        """
        super().__init__(config, audio_track_handler, video_track_handler)
        self.buffer = Queue(config["size"])

    async def process(
        self, _: VideoFrame | AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        self.buffer.put(ndarray)
        if self.buffer.full():
            return self.buffer.get()
        return self.buffer.queue[0]
