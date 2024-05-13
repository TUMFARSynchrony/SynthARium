from __future__ import annotations

import numpy
from typing import TYPE_CHECKING
from av import AudioFrame

from filters.filter import Filter
from filters.filter_dict import FilterDict

if TYPE_CHECKING:
    from hub.track_handler import TrackHandler


class MuteAudioFilter(Filter):
    """Filter returning silent audio frame in `process`."""

    _muted_frame: AudioFrame
    _muted_ndarray: numpy.ndarray

    def __init__(
        self,
        config: FilterDict,
        audio_track_handler: TrackHandler,
        video_track_handler: TrackHandler,
    ) -> None:
        """Initialize new MuteAudioFilter.

        Create new av.AudioFrame used as muted frame in `process()`.

        Parameters
        ----------
        See base class: filters.filter.Filter.
        """
        super().__init__(config, audio_track_handler, video_track_handler)

        # Create a muted audio frame.
        self._muted_frame = AudioFrame(format="s16", layout="mono", samples=1)
        for p in self._muted_frame.planes:
            p.update(bytes(p.buffer_size))
        self._muted_ndarray = self._muted_frame.to_ndarray()

    @staticmethod
    def name() -> str:
        return "MUTE_AUDIO"

    @staticmethod
    def type() -> str:
        return "NONE"

    @staticmethod
    def channel() -> str:
        return "audio"

    async def process(
        self, original: AudioFrame, ndarray: numpy.ndarray | None = None
    ) -> numpy.ndarray | AudioFrame:
        """Return muted audio frame.  Ignores input!

        If `ndarray` is none, the return type is numpy.ndarray. Otherwise, the return
        value is av.AudioFrame.

        This is an exception for mute filters, and not intended for other filters.  Mute
        filters are used outside the normal filter pipeline, where returning an
        av.AudioFrame is quicker than numpy.ndarray.  They can however also be used in
        the normal filter pipeline.
        See hub.track_handler.TrackHandler for details.

        See Also
        ----------
        filters.filter.Filter : for parameters, return value, ... documentation.
        """
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
