"""Provides the `SubprocessLoggingHandler` class."""

import os
import logging
from typing import Callable


class SubprocessLoggingHandler(logging.StreamHandler):
    """Log handler relaying subprocess logs to main process.

    Extends logging.StreamHandler.  Sends incoming logs to main process using
    `send_command`.  The main process can then use `handle_log_from_subprocess` to parse
    and log the log records.

    See Also
    --------
    handle_log_from_subprocess : handle incoming logs from this handler.
    """

    _send_command: Callable[[str, dict | str], None]
    _pid: str

    def __init__(self, send_command: Callable[[str, dict | str], None]):
        """Initiate new SubprocessLoggingHandler.

        Parameters
        ----------
        send_command : Callable(str, dict) -> None
            Function used to send commands (`LOG`) to main process.

        Examples
        --------
        >>> handler = SubprocessLoggingHandler(send_command)
        >>> logging.basicConfig(handlers=[handler], ...)
        """
        super().__init__()
        self._send_command = send_command
        self._pid = str(os.getpid())

    def emit(self, record: logging.LogRecord):
        """Send record to main process using `LOG` command and `send_command`.

        Parameters
        ----------
        record : logging.LogRecord
            Log record that will be send to the main process.
        """
        data = {
            "name": f"{record.name}[{self._pid}]",
            "levelname": record.levelname,
            "levelno": record.levelno,
            "msg": record.getMessage(),
            "created": record.created,
            "msecs": record.msecs,
            "relativeCreated": record.relativeCreated,
        }
        self._send_command("LOG", data)


def handle_log_from_subprocess(log_data: dict, logger: logging.Logger):
    """Parse and handle a log record received from a subprocess.

    Parameters
    ----------
    log_data : dict
        Data received in `LOG` command from subprocess.
    logger : logging.Logger
        Logger that is used to handle `log_data`.  As long as log_data contains `name`,
        the name of `logger` is not used.
    """
    log_record = logging.makeLogRecord(log_data)
    logger.handle(log_record)
