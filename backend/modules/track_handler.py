"""Provide TrackHandler for handing and distributing tracks."""

from __future__ import annotations
import numpy
import asyncio
import logging
from typing import Coroutine, Literal, TYPE_CHECKING
from aiortc.mediastreams import (
    MediaStreamTrack,
    MediaStreamError,
    AudioStreamTrack,
    VideoStreamTrack,
)
from av import VideoFrame, AudioFrame
from aiortc.contrib.media import MediaRelay

from modules.exceptions import ErrorDictException

from custom_types.filters import FilterDict
import filters.filter_factory as filterFactory
from filters.filter import Filter
from filters.mute import MuteVideoFilter, MuteAudioFilter

if TYPE_CHECKING:
    from modules.connection import Connection
    from modules.filter_api_interface import FilterAPIInterface


class TrackHandler(MediaStreamTrack):
    """Handles and distributes an incoming audio track to multiple subscribers."""

    kind = Literal["unknown", "audio", "video"]
    connection: Connection
    filter_api: FilterAPIInterface

    _muted: bool
    _track: MediaStreamTrack
    _relay: MediaRelay
    _mute_filter: MuteAudioFilter | MuteVideoFilter
    _filters: dict[str, Filter]
    _execute_filters: bool
    _logger: logging.Logger
    __lock: asyncio.Lock

    def __init__(
        self,
        kind: Literal["audio", "video"],
        connection: Connection,
        filter_api: FilterAPIInterface,
        track: MediaStreamTrack | None = None,
        muted: bool = False,
    ) -> None:
        """Initialize new TrackHandler for `track`.

        Parameters
        ----------
        kind : str, "audio" or "video"
            Kind of MediaStreamTrack this handler handles.
        connection : modules.connection.Connection
            Connection this track handler belongs to.
        filter_api : subclass of modules.filter_api_interface.FilterAPIInterface
            Filter API for filters.
        track : aiortc.mediastreams.MediaStreamTrack
            Track this handler should manage and distribute.  None if track is set
            later.
        muted : bool, default False
            Whether this track should be muted.

        Raises
        ------
        ValueError
            If kind is not "audio" or "video".

        Notes
        -----
        Make sure to call `complete_setup` after initialization, when `incoming_audio`
        and `incoming_video` of connection are initialized.
        """
        super().__init__()
        self.filter_api = filter_api
        self._logger = logging.getLogger(f"{kind.capitalize()}TrackHandler")
        self.__lock = asyncio.Lock()
        self.kind = kind
        if track is not None:
            self._track = track
        elif kind == "video":
            self._track = VideoStreamTrack()
        elif kind == "audio":
            self._track = AudioStreamTrack()
        else:
            raise ValueError(
                f'Invalid kind: "{kind}". Accepted values: "audio" or "video"'
            )
        self._muted = muted
        self.connection = connection
        self._relay = MediaRelay()
        self._execute_filters = True
        self._filters = {}

        # Forward the ended event to this handler.
        self._track.add_listener("ended", self.stop)

    async def complete_setup(self, filters: list[FilterDict]) -> None:
        """Complete setup of TrackHandler.

        Initializes filter used to mute track and sets filter pipeline according to
        `filters`.

        Parameters
        ----------
        filters : list of custom_types.filters.FilterDict
        """
        if self.kind == "audio":
            self._mute_filter = MuteAudioFilter(
                {"id": "0", "type": "MUTE_AUDIO"},
                self.connection.incoming_audio,
                self.connection.incoming_video,
            )
        else:
            self._mute_filter = MuteVideoFilter(
                {"id": "0", "type": "MUTE_VIDEO"},
                self.connection.incoming_audio,
                self.connection.incoming_video,
            )
        await self.set_filters(filters)

    @property
    def track(self) -> MediaStreamTrack:
        """Get source track for this TrackHandler.

        Notes
        -----
        Use `subscribe` to add a subscriber to this track.
        """
        return self._track

    @property
    def filters(self) -> dict[str, Filter]:
        """Get filters used by this TrackHandler."""
        return self._filters

    @property
    def muted(self) -> bool:
        """Get muted state of TrackHandler."""
        return self._muted

    @muted.setter
    def muted(self, value: bool) -> None:
        """Set muted state of TrackHandler."""
        self._muted = value
        self.reset_execute_filters()

    async def stop(self) -> None:
        """Stop TrackHandler and associated track."""
        super().stop()
        coros = [f.cleanup() for f in self._filters.values()]
        await asyncio.gather(*coros)

    async def set_track(self, value: MediaStreamTrack):
        """Replace source track for this TrackHandler.

        Parameters
        ----------
        value : MediaStreamTrack
            New source track for this TrackHandler.  `kind` of value must match the kind
            of this TrackHandler.

        Raises
        ------
        ValueError
            If `kind` of value doesn't match the kind of this TrackHandler.
        """
        if value.kind != self.kind:
            raise ValueError(
                f"Source track for TrackHandler must be of kind: {self.kind}"
            )

        async with self.__lock:
            previous = self._track
            previous.remove_listener("ended", self.stop)
            self._track = value
            self._track.add_listener("ended", self.stop)
            previous.stop()

    def subscribe(self) -> MediaStreamTrack:
        """Subscribe to the track managed by this handler.

        Creates a new proxy which relays the track.  This is required to add multiple
        subscribers to one track.

        Returns
        -------
        aiortc.mediastreams.MediaStreamTrack
            Proxy track for the track this TrackHandler manages.

        Notes
        -----
        If this track needs to be used somewhere, always use subscribe to create an
        proxy!  If this TrackHandler is used directly, the framerate will be divided
        between the new consumer and all existing subscribers.
        """
        return self._relay.subscribe(self, False)

    async def set_filters(self, filter_configs: list[FilterDict]) -> None:
        """Set or update filters to `filter_configs`.

        Parameters
        ----------
        filter_configs : list of custom_types.filters.FilterDict
            List of filter configs used to modify filters for this TrackHandler.
        """
        async with self.__lock:
            await self._set_filters(filter_configs)

    async def _set_filters(self, filter_configs: list[FilterDict]) -> None:
        """Internal version of `set_filters`, without lock.

        See `set_filters` for docs.
        """

        old_filters = self._filters

        self._filters = {}
        for config in filter_configs:
            id = config["id"]
            # Reuse existing filter for matching id and type.
            if id in old_filters and old_filters[id].config["type"] == config["type"]:
                self._filters[id] = old_filters[id]
                self._filters[id].set_config(config)
                continue

            # Create a new filter for configs with empty id.
            self._filters[id] = filterFactory.create_filter(config, self.connection.incoming_audio,
                                                            self.connection.incoming_video)

        coros: list[Coroutine] = []
        # Cleanup old filters
        for id, filter in old_filters.items():
            if id not in self._filters:
                coros.append(filter.cleanup())

        # Complete setup for new filters
        for filter in self._filters.values():
            coros.append(filter.complete_setup())

        await asyncio.gather(*coros)
        self.reset_execute_filters()

    def reset_execute_filters(self):
        """Reset `self._execute_filters`.

        `self._execute_filters` indicates if the filter pipeline should be executed.
        The pipeline is only executed filters exists and this TrackHandler is not muted
        or any of the filters should be executed even if muted.
        """
        self._execute_filters = len(self._filters) > 0 and (
            not self._muted or any([f.run_if_muted for f in self._filters.values()])
        )

    async def recv(self) -> AudioFrame | VideoFrame:
        """Receive the next av.AudioFrame from this track and apply filter pipeline.

        Checks if this track is muted and returns silence if so.

        Returns
        -------
        av.AudioFrame or av.VideoFrame
            Next frame from the track this TrackHandler manages.  Return type depends
            on `kind` of this TrackHandler.

        Raises
        ------
        MediaStreamError
            If `self.readyState` is not "live"
        """
        if self.readyState != "live":
            raise MediaStreamError

        frame = await self.track.recv()

        if self._execute_filters:
            if self.kind == "video":
                frame = await self._apply_video_filters(frame)
            else:
                frame = await self._apply_audio_filters(frame)

        if self._muted:
            muted_frame = await self._mute_filter.process(frame)
            return muted_frame

        return frame

    async def _apply_video_filters(self, frame: VideoFrame):
        """Parse video frame and pass it to `_apply_filters`."""
        ndarray = frame.to_ndarray(format="bgr24")
        ndarray = await self._apply_filters(frame, ndarray)

        new_frame = VideoFrame.from_ndarray(ndarray, format="bgr24")
        new_frame.time_base = frame.time_base
        new_frame.pts = frame.pts
        return new_frame

    async def _apply_audio_filters(self, frame: AudioFrame):
        """Parse audio frame and pass it to `_apply_filters`."""
        ndarray = frame.to_ndarray()
        ndarray = await self._apply_filters(frame, ndarray)

        new_frame = AudioFrame.from_ndarray(ndarray)
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        new_frame.sample_rate = frame.sample_rate
        return new_frame

    async def _apply_filters(
        self, original: VideoFrame | AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        """Execute filter pipeline."""
        async with self.__lock:
            # Run all filters if not self._muted.
            if not self._muted:
                for filter in self._filters.values():
                    ndarray = await filter.process(original, ndarray)
                return ndarray

            # Muted. Only execute filters where run_if_muted is True.
            for filter in self._filters.values():
                if filter.run_if_muted:
                    ndarray = await filter.process(original, ndarray)

        return ndarray
