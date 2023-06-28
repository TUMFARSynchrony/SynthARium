"""Provide `DelayFilter` filter."""
from typing import TypeGuard

import numpy
from queue import Queue
from av import VideoFrame, AudioFrame

from custom_types import util
from filters.filter import Filter


class SpeakingTimeFilter(Filter):
    """Filter calculating how much time the participant has spoken
    """

    @staticmethod
    def name(self) -> str:
        return "DELAY"

    async def process(
        self, _: AudioFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        #TODO: get audio stream of user and calculate time speaking
        return ndarray
