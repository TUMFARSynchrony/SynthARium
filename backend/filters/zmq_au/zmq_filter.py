"""Provide `RotationFilter` filter."""

import cv2
import json
import zmq
import base64
import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.zmq_au.openface_data_parser import OpenFaceDataParser
from filters.zmq_au.openface import OpenFace


class ZMQFilter(Filter):
    """Filter example rotating a video track."""
    has_sent: bool
    socket: zmq.Socket
    frame: int

    writer: OpenFaceDataParser
    open_face: OpenFace

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.has_sent = False
        self.is_connected = False
        self.has_found_socket = False

        """
        self.shared_port = shared_memory.SharedMemory(name="port", create=False, size=4)
        self.lock = NamedAtomicLock("port")
        try:
            self.lock.acquire()
            self.port = int.from_bytes(bytes(self.shared_port.buf), "big")
            self.shared_port.buf[:4] = bytearray((self.port + 1).to_bytes(4, "big"))
            self.lock.release()
            self.has_found_socket = True
        except Exception as e:
            print(f"Error when trying to get or set the port: {e}")
        """
        self.open_face = OpenFace(6)
        self.port = self.open_face.port
        self.writer = OpenFaceDataParser()

        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.bind(f"tcp://127.0.0.1:{self.port}")
            self.is_connected = True
        except zmq.ZMQError as e:
            print(f"ZMQError: {e}")

        self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
        self.frame = 0

    def __del__(self):
        self.socket.close()

    @staticmethod
    def name(self) -> str:
        return "ZMQ"

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        if not self.is_connected:
            origin = (50, 50)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 1
            color = (0, 255, 0)
            thickness = 2
            ndarray = cv2.putText(ndarray, f"Port {self.port} is already taken!", origin, font, font_size,
                                  color, thickness)
            return ndarray

        self.frame = self.frame + 1
        if not self.has_sent:
            is_success, image_enc = cv2.imencode(".jpg", ndarray)
            # print(type(image_enc))
            if is_success:
                im_bytes = bytearray(image_enc.tobytes())
                im_64 = base64.b64encode(im_bytes)
                #self.socket.send(im_64)
                #self.has_sent = True

                try:
                    self.socket.send(im_64)
                    self.has_sent = True
                except zmq.ZMQError as e:
                    origin = (50, 50)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_size = 1
                    color = (0, 255, 0)
                    thickness = 2
                    ndarray = cv2.putText(ndarray, "No OwnExtractor found!", origin,
                                          font, font_size,
                                          color, thickness)
                    return ndarray

        else:
            try:
                message = self.socket.recv(flags=zmq.NOBLOCK)
                self.data = json.loads(message)
                self.has_sent = False
                self.writer.write(self.frame, self.data)

                # print(self.data["intensity"]["AU06"])
            except zmq.Again as e:
                self.writer.write(self.frame, {"intensity": -1})
                pass
                # print("waiting")
                # ndarray = cv2.putText(ndarray, "waiting", origin + (50, 50), font, font_size, color)

        origin = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        color = (0, 255, 0)
        thickness = 2
        # Put text on image
        au06 = self.data["intensity"]["AU06"]
        au12 = self.data["intensity"]["AU12"]
        ndarray = cv2.putText(ndarray, f"AU06: {au06}", origin, font, font_size, color, thickness)
        ndarray = cv2.putText(ndarray, f"AU12: {au12}", (50, 100), font, font_size, color, thickness)
        ndarray = cv2.putText(ndarray, f"Port: {self.port}", (50, 150), font, font_size, color, thickness)
        return ndarray

    def _cv2_encode(self, ndarray: numpy.ndarray):
        is_success, image_enc = cv2.imencode(".jpg", ndarray)
        # print(type(image_enc))
        if is_success:
            im_bytes = bytearray(image_enc.tobytes())
            im_64 = base64.b64encode(im_bytes)
            return im_64