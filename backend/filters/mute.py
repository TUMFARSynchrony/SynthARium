"""TODO document"""

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

    def __init__(
        self, id: str, config: FilterDict, connection: modules.connection.Connection
    ) -> None:
        """TODO document"""
        super().__init__(id, config, connection)

        # Load image that will be broadcasted when track is muted.
        img_path = join(BACKEND_DIR, "images/muted.png")
        muted_frame_img = Image.open(img_path)
        self.muted_frame = VideoFrame.from_image(muted_frame_img)

    async def process(self, frame: VideoFrame) -> VideoFrame:
        """TODO document"""
        if self.muted_frame.format != frame.format:
            self.muted_frame = self.muted_frame.reformat(format=frame.format)
        # Update muted_frame metadata.
        self.muted_frame.pts = frame.pts
        self.muted_frame.time_base = frame.time_base

        return self.muted_frame


class MuteAudioFilter(AudioFilter):
    """TODO document"""

    _muted_frame: AudioFrame | None

    def __init__(
        self, id: str, config: FilterDict, connection: modules.connection.Connection
    ) -> None:
        """TODO document"""
        super().__init__(id, config, connection)

        # Create a muted audio frame.
        self.muted_frame = AudioFrame(format="s16", layout="mono")

    async def process(self, frame: AudioFrame) -> AudioFrame:
        """TODO document"""
        if self.muted_frame.samples != frame.samples:
            self.muted_frame = AudioFrame(
                format="s16", layout="mono", samples=frame.samples
            )
        # Update muted_frame metadata.
        for p in self.muted_frame.planes:
            p.update(bytes(p.buffer_size))

        self.muted_frame.pts = frame.pts
        self.muted_frame.time_base = frame.time_base
        self.muted_frame.sample_rate = frame.sample_rate

        return self.muted_frame
