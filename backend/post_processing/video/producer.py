from __future__ import annotations
import json
import jsonpickle
import logging
import os
import subprocess
import time
import zmq

from ..post_processing_interface import PostProcessingInterface

class PostVideoProducer(PostProcessingInterface):
    """Handles producer for post-processing experiments' video."""

    _logger: logging.Logger
    _sock: zmq.Socket

    def __init__(self) -> None:
        """Initialize new PostVideoProducer."""
        super().__init__()
        self._logger = logging.getLogger(f"PostVideoProducer")
        self.run_consumer()
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        try:
            self._sock.bind("tcp://*:6000")
            time.sleep(0.3)
        except zmq.ZMQError as e:
            self._logger.error(f"ZMQError: {e}")

    def execute(self):
        """Publish the recorded data to consumer."""
        for video in self._recording_list:
            try:
                videoJSON = jsonpickle.encode(video)
                message = json.dumps(videoJSON, indent=4)
                self._sock.send_string(message)
                self._logger.info(f"Publish: {message}")
            except Exception as error:
                self._logger.error("Error post-processing producer." + 
                                f"Video: {video}." + 
                                f"Exception: {error}")
        # Exit message for consumer
        self._sock.send_string("0")

    def run_consumer(self):
        """Run consumer subprocess."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        consumer = subprocess.Popen(
                [
                    "python",
                    os.path.join(
                        current_dir,
                        "consumer.py"
                    )
                ]
            )
        self._logger.info(f"[PID {consumer.pid}]. Run: consumer.py")
        return consumer