"""Provide OpenFace extraction of the experiments' recorded video."""

from __future__ import annotations
import json
import jsonpickle
import logging
import subprocess
import os
import time
import zmq

class PostVideoConsumer():
    """Consume and post-process the experiments' video."""

    _logger: logging.Logger
    _root_dir: str
    _sock: zmq.Socket

    def __init__(self) -> None:
        """Initialize new PostVideoConsumer."""
        super().__init__()
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
        )
        self._logger = logging.getLogger("PostVideoConsumer")
        
        self._root_dir = os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.dirname(os.path.abspath(__file__)))
                                )
                            )
                        )

        context = zmq.Context()
        self._sock = context.socket(zmq.SUB)
        try:
             self._sock.connect("tcp://localhost:6000")
             self._sock.setsockopt_string(zmq.SUBSCRIBE, "")
        except zmq.ZMQError as e:
            self._logger.error(f"ZMQError: {e}")

    def consume(self):
        """Activate consumer to receive messages."""
        while True:
            self._logger.info("Waiting for a message")
            message= self._sock.recv_string()
            if message == "0":
                self._logger.info("Stopped post-processing consumer")
                break
            self._logger.info(f"Receive: {message}")
            try:
                videoJSON = jsonpickle.decode(message)
                video = json.loads(videoJSON)
                start_video = time.time()

                parent_directory =  os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__))))
                out_dir = os.path.join(parent_directory,
                                       "sessions",
                                       video["_session_id"],
                                       "processed")            
                video_path = os.path.join(parent_directory,
                                          "sessions",
                                          video["_session_id"],
                                          video["_filename"])
                subprocess = self.run_feature_extraction(video_path, out_dir)
                output, error = subprocess.communicate()
                if subprocess.returncode < 0:
                    self._logger.error(f"Output: {output}. Error: {error}")
                    continue
                end_video = time.time()
                self._logger.info(f"Feature extraction finished in {(end_video - start_video)} seconds")
            except Exception as error:
                self._logger.error("Error post-processing consumer." + 
                                f"Message: {message}." + 
                                f"Exception: {error}")

    
    def run_feature_extraction(self, video_path: str, out_dir: str):
        """Run FeatureExtraction from OpenFace to do post-processing."""
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
                ]
            )
            self._logger.info(f"[PID {self._feature_extraction.pid}]. Processing: {video_path}")
            return self._feature_extraction
        except Exception as error:
            self._logger.error("Error running OpenFace." + 
                               f"Video path: {video_path}." + 
                               f"Out dir: {out_dir}." + 
                               f"Exception: {error}")

if __name__ == "__main__":
    consumer = PostVideoConsumer()
    consumer.consume()