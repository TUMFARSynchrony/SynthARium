"""Provide TrackHandler for handing and distributing tracks."""

from __future__ import annotations
import logging
import time
from aiortc.contrib.media import MediaRecorder, MediaBlackhole
from modules.track_handler import TrackHandler

class RecordHandler:
    """Handles audio and video recording of the stream."""

    _logger: logging.Logger
    _recorder: MediaRecorder | MediaBlackhole
    _record: bool
    _record_to: str
    _track: TrackHandler

    def __init__(
        self,
        track: TrackHandler,
        record: bool = False,
        record_to: str = None
    ) -> None:
        """Initialize new RecordHandler for `track`.

        Parameters
        ----------
        track : TrackHandler
            The audio/video track.
        record : bool
            Flag whether the track must be recorded or not.
        record_to : str
            Path for the recording result.

        Notes
        -----
        Full path of the recordings will be:
        ./sessions/<session_id>/<participant_id>_<date>_<start_time>.mp3/mp4
        """
        super().__init__()
        self._logger = logging.getLogger(f"{track.kind.capitalize()}-RecordHandler")
        self._track = track
        self._record = record
        self._record_to = record_to
        if self._track.kind == "audio":
            track_format = "mp3"
        else:
            track_format = "mp4"

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self._record_to = self._record_to + "_" + timestamp + "." + track_format
        if self._record:
            self._recorder = MediaRecorder(self._record_to)
        else:
            self._recorder = MediaBlackhole()

    async def start(self) -> None:
        """Start recorder."""
        await self._recorder.start()
        self._logger.debug("Start recording: " + self._record_to)

    def add_track(self, track: TrackHandler) -> None:
        """Add track to recorder.

        Parameters
        ----------
        track : TrackHandler
            The audio/video track.
        """
        self._recorder.addTrack(track)
        self._logger.debug("add_track: " + self._record_to)

    async def stop(self):
        """Stop RecordHandler."""
        await self._recorder.stop()
        self._logger.debug("Stop recording: " + self._record_to)
