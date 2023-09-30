from __future__ import annotations
import json
import jsonpickle
import logging
import time
import zmq

from ..post_processing_data import PostProcessingData


class PostVideoProducer():
    """Handles producer for post-processing experiments' video."""

    _logger: logging.Logger
    _sock: zmq.Socket

    def __init__(self) -> None:
        """Initialize new PostVideoProducer."""
        super().__init__()
        self._logger = logging.getLogger(f"PostVideoProducer")
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        try:
            self._sock.bind("tcp://*:6000")
            time.sleep(0.3)
        except zmq.ZMQError as e:
            self._logger.error(f"ZMQError: {e}")

    def publish(self, recording_list: list[PostProcessingData]):
        """Publish the recorded data to consumer."""
        for video in recording_list:
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