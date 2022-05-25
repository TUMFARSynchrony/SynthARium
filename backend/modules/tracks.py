from aiortc.mediastreams import MediaStreamTrack, MediaStreamError
from aiortc.contrib.media import MediaRelay
from av import VideoFrame, AudioFrame
from PIL import Image
from os.path import join

from modules import BACKEND_DIR


class AudioTrackHandler(MediaStreamTrack):
    """TODO Document"""

    kind = "audio"

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
            print("MutedAudioFrame:", self.muted_frame)
            return self.muted_frame

        return frame


class VideoTrackHandler(MediaStreamTrack):
    """TODO Document"""

    kind = "video"

    track: MediaStreamTrack
    muted: bool
    _relay: MediaRelay

    _muted_frame_img: Image.Image
    _muted_frame: VideoFrame

    def __init__(self, track: MediaStreamTrack, muted: bool = False):
        super().__init__()
        self.track = track
        self.muted = muted
        self._relay = MediaRelay()

        img_path = join(BACKEND_DIR, "images/muted.png")
        self._muted_frame_img = Image.open(img_path)
        self.muted_frame = VideoFrame.from_image(self._muted_frame_img)

    def subscribe(self):
        return self._relay.subscribe(self, False)

    async def recv(self):
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
