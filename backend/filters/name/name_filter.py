from typing import TypeGuard

import cv2
import numpy

from custom_types import util
from filters.filter import Filter
from .name_filter_dict import NameFilterDict

class NameFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    name_participant: str
    _config: NameFilterDict

    def __init__(
        self, config: NameFilterDict, audio_track_handler, video_track_handler
    ) -> None:
        """Initialize new NameFilter.

        Parameters
        ----------
        See base class: filters.filter.Filter.
        """
        super().__init__(config, audio_track_handler, video_track_handler)
        self.name_participant = config["name"]

    @staticmethod
    def name(self) -> str:
        return "NAME"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10,height - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        thickness = 3
        color = (0, 255, 0)

        # Put text on image
        ndarray = cv2.putText(ndarray, self.name_participant, origin, font, font_size, color, thickness)

        # Return modified frame
        return ndarray

    @staticmethod
    def validate_dict(data) -> TypeGuard[NameFilterDict]:
        return (
            util.check_valid_typeddict_keys(data, NameFilterDict)
            and "name" in data
            and isinstance(data["name"], str)
        )

