from aiortc.mediastreams import (
    VideoStreamTrack,
    AudioStreamTrack,
    MediaStreamTrack,
    MediaStreamError,
)
from aiortc.contrib.media import MediaRelay


class AudioTrackHandler(AudioStreamTrack):
    """TODO Document"""

    track: MediaStreamTrack
    muted: bool
    _relay: MediaRelay

    def __init__(self, track: MediaStreamTrack, muted: bool = False):
        super().__init__()
        self.track = track
        self.muted = muted
        self._relay = MediaRelay()

    def subscribe(self):
        return self._relay.subscribe(self, False)

    async def recv(self):
        if self.readyState != "live":
            raise MediaStreamError

        if self.muted:
            return await super().recv()

        frame = await self.track.recv()
        return frame


class VideoTrackHandler(VideoStreamTrack):
    """TODO Document"""

    track: MediaStreamTrack
    muted: bool
    _relay: MediaRelay

    def __init__(self, track: MediaStreamTrack, muted: bool = False):
        super().__init__()
        self.track = track
        self.muted = muted
        self._relay = MediaRelay()

    def subscribe(self):
        return self._relay.subscribe(self, False)

    async def recv(self):
        if self.readyState != "live":
            raise MediaStreamError

        if self.muted:
            return await super().recv()

        frame = await self.track.recv()
        return frame
