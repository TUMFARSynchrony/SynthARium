"""Provide RecordedData to represent video/audio of the experiments."""

from __future__ import annotations

import logging


class RecordedData():
    """Object class for the recorded data of the experiments."""

    _logger: logging.Logger
    _type: str
    _file_path: str
    _session_id: str
    _participant_id: str

    def __init__(
        self, type: str, file_path: str, session_id: str, participant_id: str
    ) -> None:
        """Initialize new RecordedData.

        Parameters
        ----------
        type : str
            The value would be video/audio.
        file_path : str
            The recorded data file path.
        session_id : str
            Session ID of the recorded data.
        participant_id : str
            Participant ID of the recorded data.
        """
        super().__init__()
        self._logger = logging.getLogger(f"{type.capitalize()}-RecordedData")
        self._type = type
        self._file_path = file_path
        self._session_id = session_id
        self._participant_id = participant_id

    @property
    def type(self) -> str:
        """Get type of RecordedData."""
        return self._type

    @property
    def file_path(self) -> str:
        """Get file path of RecordedData."""
        return self._file_path
    
    @property
    def session_id(self) -> str:
        """Get session ID of RecordedData."""
        return self._session_id
    
    @property
    def participant_id(self) -> str:
        """Get participant ID of RecordedData."""
        return self._participant_id
