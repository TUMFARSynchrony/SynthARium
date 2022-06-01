"""Provide AudioTrackHandler and VideoTrackHandler for handing and distributing tracks.
"""

from aiortc.mediastreams import MediaStreamTrack, MediaStreamError
from aiortc.contrib.media import MediaRelay
from av import VideoFrame, AudioFrame
from PIL import Image
from os.path import join

from modules import BACKEND_DIR


class AudioTrackHandler(MediaStreamTrack):
    """Handles and distributes an incoming audio track to multiple subscribers."""

    kind = "audio"

    track: MediaStreamTrack
    muted: bool
    _relay: MediaRelay

    def __init__(self, track: MediaStreamTrack, muted: bool = False) -> None:
        """Initialize new AudioTrackHandler for `track`.

        Parameters
        ----------
        track : aiortc.mediastreams.MediaStreamTrack
            Track this handler should manage and distribute.
        muted : bool, default False
            Whether this track should be muted.
        """
        super().__init__()
        self.track = track
        self.muted = muted
        self._relay = MediaRelay()

        # Forward the ended event to this handler.
        track.on("ended", self.stop)

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
            self.muted_frame = AudioFrame(
                format="s16", layout="mono", samples=frame.samples
            )
            for p in self.muted_frame.planes:
                p.update(bytes(p.buffer_size))
            self.muted_frame.pts = frame.pts
            self.muted_frame.sample_rate = frame.sample_rate
            self.muted_frame.time_base = frame.time_base
            return self.muted_frame

        return frame


class VideoTrackHandler(MediaStreamTrack):
    """Handles and distributes an incoming video track to multiple subscribers."""

    kind = "video"

    track: MediaStreamTrack
    muted: bool
    _relay: MediaRelay

    _muted_frame_img: Image.Image
    _muted_frame: VideoFrame

    def __init__(self, track: MediaStreamTrack, muted: bool = False) -> None:
        """Initialize new VideoTrackHandler for `track`.

        Parameters
        ----------
        track : aiortc.mediastreams.MediaStreamTrack
            Track this handler should manage and distribute.
        muted : bool, default False
            Whether this track should be muted.  When muted, a still image will be
            broadcasted instead of the input `track`.
        """
        super().__init__()
        self.track = track
        self.muted = muted
        self._relay = MediaRelay()

        # Forward the ended event to this handler.
        track.on("ended", self.stop)

        # Load image that will be broadcasted when track is muted.
        img_path = join(BACKEND_DIR, "images/muted.png")
        self._muted_frame_img = Image.open(img_path)
        self.muted_frame = VideoFrame.from_image(self._muted_frame_img)

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
            if self.muted_frame.format != frame.format:
                self.muted_frame = self.muted_frame.reformat(format=frame.format)

            self.muted_frame.pts = frame.pts
            self.muted_frame.time_base = frame.time_base

            return self.muted_frame

        return frame
