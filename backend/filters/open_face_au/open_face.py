import subprocess
import os
import logging


class OpenFace:
    """Class for running OpenFace as an external process."""

    _logger: logging.Logger
    _own_extractor: None
    _root_dir: str

    def __init__(self):
        self._logger = logging.getLogger(f"OpenFace")
        self._root_dir = os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.dirname(os.path.abspath(__file__))
                                    )
                                )
                            )
                        )

    #customize the OwnExtractor and port
    # differentiate between windows/unix/macOS
    def run_own_extractor(self, port: int):
        try:
            self._own_extractor = subprocess.Popen(
                [
                    os.path.join(
                        self._root_dir,
                        "build",
                        "bin",
                        "OwnExtractor",
                    ),
                    f"{port}",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except Exception as error:
            self._logger.error("Error running OwnExtractor. Port: " + port + ". Exception: " + error)

    def __del__(self):
        try:
            self._own_extractor.terminate()
        except Exception:
            self._own_extractor.kill()
