"""Provide `RotationFilter` filter."""

import cv2
import json
import zmq
import base64
import numpy
from av import VideoFrame

from filters.filter import Filter


class ZMQFilter(Filter):
    """Filter example rotating a video track."""
    has_sent: bool
    socket: zmq.Socket

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.has_sent = False

        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.bind("tcp://127.0.0.1:5555")
        self.data = None

    @staticmethod
    def name(self) -> str:
        return "ZMQ"

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:

        if not self.has_sent:
            is_success, image_enc = cv2.imencode(".jpg", ndarray)
            # print(type(image_enc))
            if is_success:
                im_bytes = bytearray(image_enc.tobytes())
                im_64 = base64.b64encode(im_bytes)
                self.socket.send(im_64)
                self.has_sent = True
        else:
            try:
                message = self.socket.recv(flags=zmq.NOBLOCK)
                self.data = json.loads(message)
                self.has_sent = False
                # print(self.data["intensity"]["AU06"])
            except zmq.Again as e:
                pass
                # print("waiting")
                # ndarray = cv2.putText(ndarray, "waiting", origin + (50, 50), font, font_size, color)

        origin = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        color = (0, 1, 0)
        if self.data is not None:
            # Put text on image
            au06 = self.data["intensity"]["AU06"]
            ndarray = cv2.putText(ndarray, str(au06), origin, font, font_size, color)

        return ndarray

    def _cv2_encode(self, ndarray: numpy.ndarray):
        is_success, image_enc = cv2.imencode(".jpg", ndarray)
        # print(type(image_enc))
        if is_success:
            im_bytes = bytearray(image_enc.tobytes())
            im_64 = base64.b64encode(im_bytes)
            return im_64