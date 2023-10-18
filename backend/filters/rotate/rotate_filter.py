"""Provide `RotationFilter` filter."""

import cv2
import numpy
from av import VideoFrame

from filters.filter import Filter
from filters import FilterDict


class RotationFilter(Filter):
    """Filter example rotating a video track."""

    rotation: int

    def __init__(
        self, config: FilterDict, audio_track_handler, video_track_handler
    ) -> None:
        super().__init__(config, audio_track_handler, video_track_handler)
        direction = 1
        if config["config"]["direction"]["value"] == "clockwise":
            direction = -1
        angle = config["config"]["angle"]["value"]
        self.rotation = angle * direction

    @staticmethod
    def name(self) -> str:
        return "ROTATION"

    @staticmethod
    def filter_type(self) -> str:
        return "SESSION"

    @staticmethod
    def init_config(self) -> FilterDict:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return FilterDict(
            name=name,
            id=id,
            channel="video",
            groupFilter=False,
            config={
                "direction": {
                    "defaultValue": ["clockwise", "anti-clockwise"],
                    "value": "clockwise",
                    "requiresOtherFilter": False,
                },
                "angle": {
                    "min": 1,
                    "max": 180,
                    "step": 1,
                    "value": 45,
                    "defaultValue": 45,
                },
            },
        )

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        # For docstring see filters.filter.Filter or hover over function declaration
        # Example based on https://github.com/aiortc/aiortc/tree/main/examples/server
        rows, cols, _ = ndarray.shape

        M = cv2.getRotationMatrix2D(
            (cols / 2, rows / 2), original.time * self.rotation, 1
        )
        ndarray = cv2.warpAffine(ndarray, M, (cols, rows))

        return ndarray
