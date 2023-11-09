"""Provide RecordHandler for handling media recorder."""

from __future__ import annotations
import logging
import math
import os
import subprocess
import time

from aiortc.contrib.media import MediaRecorder, MediaBlackhole
from hub.track_handler import TrackHandler


class RecordHandler:
    """Handles audio and video recording of the stream."""

    _logger: logging.Logger
    _recorder: MediaRecorder | MediaBlackhole
    _record: bool
    _record_to: str
    _track: TrackHandler
    _track_format: str
    _start_time: float

    def __init__(
        self, track: TrackHandler, record: bool = False, record_to: str = None
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
        self._start_time = 0

        if self._track.kind == "audio":
            self._track_format = "mp3"
        else:
            self._track_format = "mp4"

        if self._record and self._record_to != "":
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self._record_to = self._record_to + "_" + timestamp + "." + self._track_format
            self._recorder = MediaRecorder(self._record_to)
        else:
            self._recorder = MediaBlackhole()
            
    async def start(self) -> None:
        """Start recorder."""
        self._start_time = time.time()
        await self._recorder.start()
        self._logger.debug(f"Start recording {self._record_to}")

    def add_track(self, track: TrackHandler) -> None:
        """Add track to recorder.

        Parameters
        ----------
        track : TrackHandler
            The audio/video track.
        """
        self._recorder.addTrack(track)
        self._logger.debug(f"Add track: {self._record_to}")

    async def stop(self):
        """Stop RecordHandler."""
        end_time = time.time()
        duration = end_time - self._start_time
        self._recorder.stop()
        self._logger.debug(f"Stop recording {self._record_to}")

        if self._track.kind == 'video':
            while(True):
                if (os.path.isfile(self._record_to)):
                    # Trim black frames
                    self.trim(duration)
                    self._logger.info(f"Finish processing: {self._record_to}")
                    break

                # Need to wait until recording file is saved
                time.sleep(1)

    def trim(self, duration: float):
        try:
            duration_str = str(math.ceil(duration) * -1)
            output = f"{self._record_to}_trimmed.{self._track_format}"
            ffmpeg = subprocess.Popen(
                    [
                        "ffmpeg",
                        "-sseof",
                        duration_str,
                        "-i",
                        self._record_to,
                        output,
                    ]
                )
            self._logger.debug(f"[PID {ffmpeg.pid}]. Run ffmpeg subprocess for trimming {self._record_to}")
            ffmpeg.communicate()
            os.remove(self._record_to)
            os.rename(output, self._record_to)
        except Exception as error:
            self._logger.error("Error running ffmpeg." + 
                               f"Exception: {error}.")
