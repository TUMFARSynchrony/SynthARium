import subprocess
import os
import logging


class OpenFace:
    """Class for running OpenFace as an external process."""

    _logger: logging.Logger
    _own_extractor: None
    _feature_extraction: None
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

    async def run_feature_extraction(self, video_path: str, out_dir: str):
        try:
            self._feature_extraction = subprocess.Popen(
                [
                    os.path.join(
                        self._root_dir,
                        "build",
                        "bin",
                        "FeatureExtraction",
                    ),
                    "-f",
                    f"{video_path}",
                    "-out_dir",
                    f"{out_dir}",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self._logger.debug("Processing: " + str(video_path))
            self._logger.debug("PID: " + str(self._feature_extraction.pid))
            return self._feature_extraction
        except Exception as error:
            self._logger.error("Error running OpenFace. Video path: " + str(video_path) 
                               + ", Out dir: " + str(out_dir)
                               + ". Exception: " + str(error))

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

    def cleanup_own_extractor(self):
        try:
            self._own_extractor.terminate()
        except Exception:
            self._own_extractor.kill()
