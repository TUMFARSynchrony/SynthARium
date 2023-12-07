import logging
import subprocess
import threading
import os


class OpenFace():
    def __init__(self, participant_id: str):
        self.logger = logging.getLogger("OpenFace")
        self.participant_id = participant_id

        try:
            # Adjust environment variables for better performance
            env = os.environ.copy()
            env["OMP_NUM_THREADS"] = "1"
            env["VECLIB_MAXIMUM_THREADS"] = "1"

            self._openface_process = subprocess.Popen(
                [
                    os.path.join(
                        os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.dirname(os.path.abspath(__file__))
                                    )
                                )
                            )
                        ),
                        "experimental-hub-openface",
                        "build",
                        "bin",
                        "AUExtractor",
                    ),
                    self.participant_id,
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )

            self.logger.debug(f"PID OpenFace: {self._openface_process.pid}")
        except Exception:
            pass

    def __del__(self):
        try:
            self._openface_process.terminate()
        except Exception:
            self._openface_process.kill()
