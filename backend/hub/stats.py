"""Provide statistics of an experiment."""

from __future__ import annotations
import logging
import os
import psutil
import time

from hub.util import write_csv_file, get_sessions_path


class Stats:
    """Handles statistics of an experiment."""

    _logger: logging.Logger
    session_id: str
    stats_dir: str

    FPS_HEADERS: list = ["timestamp", "elapsed_time_in_seconds", "fps"]
    USAGE_HEADERS: list = ["timestamp", "elapsed_time_in_seconds", "cpu_percentage", "ram_percentage", "ram_usage_in_GB"]
    CONNECTED_PARTICIPANT_HEADERS: list = ["timestamp", "elapsed_time_in_seconds", "number_of_participants"]

    def __init__(
        self, session_id: str) -> None:
        """Initialize new Stats for current session.

        Parameters
        ----------
        session_id : str
            The session id of the running experiment.
        
        """
        super().__init__()
        self._logger = logging.getLogger(f"{session_id}-Stats")
        self.session_id = session_id
        self.stats_dir = os.path.join(get_sessions_path(), self.session_id, "stats")
        if not os.path.isdir(self.stats_dir):
            os.mkdir(self.stats_dir)
        #TODO: refactor write method into switch case

    def write_fps_data(self, data: list, participant_id: str) -> None:
        """Write fps data to csv file."""
        csv_filename = f'{self.stats_dir}/{participant_id}_fps.csv'
        self._logger.debug(f"Writing fps data to: {csv_filename}")
        write_csv_file(csv_filename, data, self.FPS_HEADERS)
        self._logger.debug(f"Finish writing: {csv_filename}")

    def write_usage_data(self, data: list) -> None:
        """Write usage data to csv file."""
        csv_filename = f'{self.stats_dir}/usage.csv'
        self._logger.debug(f"Writing usage data to: {csv_filename}")
        write_csv_file(csv_filename, data, self.USAGE_HEADERS)
        self._logger.debug(f"Finish writing: {csv_filename}")

    def write_connected_participant_data(self, data: list) -> None:
        """Write connected participant data to csv file."""
        csv_filename = f'{self.stats_dir}/connected_participant.csv'
        self._logger.debug(f"Writing connected_participant data to: {csv_filename}")
        write_csv_file(csv_filename, data, self.CONNECTED_PARTICIPANT_HEADERS)
        self._logger.debug(f"Finish writing: {csv_filename}")
