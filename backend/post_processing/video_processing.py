from __future__ import annotations
import json
import jsonpickle
import logging
import os
import subprocess
import time
import zmq

from filters.open_face_au.open_face import OpenFace
from hub.exceptions import ErrorDictException
from .post_processing_interface import PostProcessingInterface
from .recorded_data import RecordedData
from .video_processing_consumer import VideoProcessingConsumer

class VideoProcessing(PostProcessingInterface):
    """Handles producer and consumer initiation for post-processing experiments' video."""

    _logger: logging.Logger
    _open_face: OpenFace
    _sock: zmq.Socket

    def __init__(self) -> None:
        """Initialize new VideoProcessing and bind socket for the producer."""
        super().__init__()
        self._logger = logging.getLogger(f"VideoProcessing")
        self._open_face = OpenFace()

    async def execute(self) -> None:
        """Execute the post-processing of the recorded video."""
        self.run_consumer()
        self.run_producer()

    def run_producer(self):
        """Publish the recorded data to consumer."""
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        try:
            self._sock.bind("tcp://*:5680")
            time.sleep(0.3) # Time to establish connection
        except zmq.ZMQError as e:
            self._logger.error(f"ZMQError: {e}")
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
                        "video_processing_consumer.py"
                    )
                ]
            )
        self._logger.info(f"[PID {consumer.pid}]. Run: video_processing_consumer.py")
        return consumer