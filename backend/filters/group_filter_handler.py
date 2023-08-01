"""Provide GroupFilterHandler for handling group filters."""

from typing import Literal
import logging
from hub.track_handler import TrackHandler


class GroupFilterHandler:
    """Handles audio and video group filters."""

    _logger: logging.Logger
    _execute_filters: bool
    _kind: Literal["video", "audio"]
    _tracks: list[TrackHandler]

    def __init__(self, kind: Literal["video", "audio"]) -> None:
        super().__init__()
        self._logger = logging.getLogger(f"{kind.capitalize()} GroupFilterHandler")
        self._execute_filters = True
        self._kind = kind
        self._tracks = []

    def add_track(self, track: TrackHandler) -> None:
        if track.kind == self._kind:
            self._tracks.append(track)
            self._logger.debug("Track added.")
