"""TODO Document"""

import os
import logging
from typing import Callable


class SubprocessLoggingHandler(logging.StreamHandler):
    """TODO Document"""

    _send_command: Callable[[str, dict | str], None]
    _pid: str

    def __init__(self, send_command: Callable[[str, dict | str], None]):
        """TODO Document"""
        super().__init__()
        self._send_command = send_command
        self._pid = str(os.getpid())

    def emit(self, record: logging.LogRecord):
        """TODO Document"""
        data = {
            "name": f"{record.name}[{self._pid}]",
            "levelname": record.levelname,
            "levelno": record.levelno,
            "msg": record.getMessage(),
        }
        self._send_command("LOG", data)


def handle_log_from_subprocess(log_data: dict, logger: logging.Logger):
    """TODO Document"""
    log_record = logging.makeLogRecord(log_data)
    logger.handle(log_record)
