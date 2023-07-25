import collections
import cv2
import numpy
from os.path import join
from hub import BACKEND_DIR


from filters import FilterDict

from filters.filter import Filter

class BufferFilter(Filter):
    """Filter saving the last 60 frames in `frame_buffer`."""

    frame_buffer: collections.deque
    counter: int

    def __init__(
        self, config: FilterDict, audio_track_handler, video_track_handler
    ) -> None:
        """Initialize new BufferFilter.

        Parameters
        ----------
        See base class: filters.filter.Filter.
        """
        super().__init__(config, audio_track_handler, video_track_handler)
        self.frame_buffer = collections.deque(maxlen=30)
        # To run this filter in the muted state:
        self.counter = 0

    @staticmethod
    def name(self) -> str:
        return "BUFFER"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # Add every 30th frame (~1 sec) to buffer:
        if not self.counter % 30 and self.counter <= 900:
            self.frame_buffer.append(ndarray)

            #path = join(BACKEND_DIR, "filters/glasses_detection/images/temp_" + str(self.counter) + ".jpeg")
            #cv2.imwrite(path, ndarray)

        self.counter += 1
        # Return unmodified frame:
        return ndarray