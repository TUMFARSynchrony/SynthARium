"""Provide AudioTrackHandler and VideoTrackHandler for handing and distributing tracks.
"""

from aiortc.mediastreams import (
    MediaStreamTrack,
    MediaStreamError,
    AudioStreamTrack,
    VideoStreamTrack,
)
from av import VideoFrame, AudioFrame
from aiortc.contrib.media import MediaRelay

from filters.mute import MuteVideoFilter, MuteAudioFilter


class AudioTrackHandler(MediaStreamTrack):
    """Handles and distributes an incoming audio track to multiple subscribers."""

    kind = "audio"

    muted: bool

    _track: MediaStreamTrack | AudioStreamTrack
    _relay: MediaRelay
    _mute_audio_filter: MuteAudioFilter

    def __init__(
        self, track: MediaStreamTrack | None = None, muted: bool = False
    ) -> None:
        """Initialize new AudioTrackHandler for `track`.

        Parameters
        ----------
        track : aiortc.mediastreams.MediaStreamTrack
            Track this handler should manage and distribute.  None if track is set
            later.
        muted : bool, default False
            Whether this track should be muted.
        """
        super().__init__()
        self._track = track if track is not None else AudioStreamTrack()
        self.muted = muted
        self._relay = MediaRelay()
        self._mute_audio_filter = MuteAudioFilter("0", {})

        # Forward the ended event to this handler.
        self._track.add_listener("ended", self.stop)

    @property
    def track(self):
        """Get source track for this AudioTrackHandler.

        Notes
        -----
        Use `subscribe` to add a subscriber to this track.
        """
        return self._track

    @track.setter
    def track(self, value: MediaStreamTrack):
        """Set source track for this AudioTrackHandler.

        Parameters
        ----------
        value : MediaStreamTrack
            New source track for this AudioTrackHandler.  `kind` of value must be
            "audio".

        Raises
        ------
        ValueError
            If `kind` of value is not "audio".
        """
        if value.kind != "audio":
            raise ValueError(
                'Source track for AudioTrackHandler must be of kind: "audio"'
            )
        self._track.remove_listener("ended", self.stop)
        self._track = value
        self._track.add_listener("ended", self.stop)

    def subscribe(self) -> MediaStreamTrack:
        """Subscribe to this track.

        Creates a new proxy which relays the track.  This is required to add multiple
        subscribers to one track.

        Returns
        -------
        aiortc.mediastreams.MediaStreamTrack
            Proxy track for the track this AudioTrackHandler manages.

        Notes
        -----
        If this track needs to be used somewhere, always use subscribe to create an
        proxy!  If this AudioTrackHandler is used directly, the framerate will be
        divided between the new consumer and all existing subscribers.
        """
        return self._relay.subscribe(self, False)

    async def recv(self) -> AudioFrame:
        """Receive the next av.AudioFrame from this track.

        Checks if this track is muted and returns silence if so.

        Returns
        -------
        av.AudioFrame
            Next audio frame from the track this AudioTrackHandler manages, or silence
            if muted.

        Raises
        ------
        MediaStreamError
            If `self.readyState` is not "live"
        """
        if self.readyState != "live":
            raise MediaStreamError

        frame = await self.track.recv()

        if self.muted:
            muted_frame = await self._mute_audio_filter.process(frame)
            return muted_frame

        return frame


class VideoTrackHandler(MediaStreamTrack):
    """Handles and distributes an incoming video track to multiple subscribers."""

    kind = "video"

    muted: bool

    _track: MediaStreamTrack
    _relay: MediaRelay
    _mute_video_filter: MuteVideoFilter

    def __init__(
        self, track: MediaStreamTrack | None = None, muted: bool = False
    ) -> None:
        """Initialize new VideoTrackHandler for `track`.

        Parameters
        ----------
        track : aiortc.mediastreams.MediaStreamTrack or None
            Track this handler should manage and distribute.  None if track is set
            later.
        muted : bool, default False
            Whether this track should be muted.  When muted, a still image will be
            broadcasted instead of the input `track`.
        """
        super().__init__()
        self._track = track if track is not None else VideoStreamTrack()
        self.muted = muted
        self._relay = MediaRelay()
        self._mute_video_filter = MuteVideoFilter("0", {})

        # Forward the ended event to this handler.
        self._track.add_listener("ended", self.stop)

    @property
    def track(self):
        """Get source track for this AudioTrackHandler.

        Notes
        -----
        Use `subscribe` to add a subscriber to this track.
        """
        return self._track

    @track.setter
    def track(self, value: MediaStreamTrack):
        """Set source track for this VideoTrackHandler.

        Parameters
        ----------
        value : MediaStreamTrack
            New source track for this VideoTrackHandler.  `kind` of value must be
            "video".

        Raises
        ------
        ValueError
            If `kind` of value is not "video".
        """
        if value.kind != "video":
            raise ValueError(
                'Source track for VideoTrackHandler must be of kind: "video"'
            )
        self._track.remove_listener("ended", self.stop)
        self._track = value
        self._track.add_listener("ended", self.stop)

    def subscribe(self) -> MediaStreamTrack:
        """Subscribe to this track.

        Creates a new proxy which relays the track.  This is required to add multiple
        subscribers to one track.

        Returns
        -------
        aiortc.mediastreams.aioMediaStreamTrack
            Proxy track for the track this VideoTrackHandler manages.

        Notes
        -----
        If this track needs to be used somewhere, always use subscribe to create an
        proxy!  If this VideoTrackHandler is used directly, the framerate will be
        divided between the new consumer and all existing subscribers.
        """
        return self._relay.subscribe(self, False)

    async def recv(self) -> VideoFrame:
        """Receive the next av.VideoFrame from this track.

        Checks if this track is muted and returns a still image if so.

        Returns
        -------
        av.VideoFrame
            Next video frame from the track this VideoTrackHandler manages, or still
            image if muted.

        Raises
        ------
        MediaStreamError
            If `self.readyState` is not "live"
        """
        if self.readyState != "live":
            raise MediaStreamError

        frame = await self.track.recv()

        if self.muted:
            muted_frame = await self._mute_video_filter.process(frame)
            return muted_frame

        return frame
