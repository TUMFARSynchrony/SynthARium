"""Provide `RotationFilter` filter."""

import cv2
import json
import zmq
import base64
import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.simple_line_writer import SimpleLineWriter
from filters.zmq_au.openface_data_parser import OpenFaceDataParser
from filters.zmq_au.openface_instance import OpenFaceInstance


class ZMQFilterD(Filter):
    """Filter example rotating a video track."""
    has_sent: bool
    socket: zmq.Socket
    frame: int

    writer: OpenFaceDataParser
    open_face: OpenFaceInstance
    line_writer: SimpleLineWriter

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.has_sent = False
        self.is_connected = False
        self.has_found_socket = False

        # self.open_face = OpenFaceInstance(6)
        self.port = 5558 #self.open_face.port
        self.writer = OpenFaceDataParser("9ba5fdccde")
        self.line_writer = SimpleLineWriter()

        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        try:
            self.socket.bind(f"tcp://127.0.0.1:{self.port}")
            self.is_connected = True
        except zmq.ZMQError as e:
            print(f"ZMQError: {e}")

        self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
        self.frame = 0
        self.zmq_count = 0

    def __del__(self):
        self.socket.close()

    @staticmethod
    def name(self) -> str:
        return "ZMQ_d"

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        if not self.is_connected:
            ndarray = self.line_writer.write_line(ndarray, f"Port {self.port} is already taken!")
            return ndarray

        self.frame = self.frame + 1
        if not self.has_sent:
            is_success, image_enc = cv2.imencode(".png", ndarray)
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
                    ndarray = self.line_writer.write_line(ndarray, "No OwnExtractor found!")
                    return ndarray

        else:
            try:
                message = self.socket.recv(flags=zmq.NOBLOCK)
                # print(self.open_face.openface_process.stdout.readline())
                # print(self.open_face.openface_process.stdout.readline())
                # print(self.open_face.openface_process.stdout.readline())
                # print(self.open_face.openface_process.stdout.readline())
                self.data = json.loads(message)
                self.has_sent = False
                self.zmq_count = self.zmq_count + 1
                self.writer.write(self.frame, self.data)

                # print(self.data["intensity"]["AU06"])
            except zmq.Again as e:
                self.writer.write(self.frame, {"intensity": -1})
                #self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
                pass
                # print("waiting")
                # ndarray = cv2.putText(ndarray, "waiting", origin + (50, 50), font, font_size, color)

        # print(self.open_face.openface_process.communicate())

        # Put text on image
        au06 = self.data["intensity"]["AU06"]
        au12 = self.data["intensity"]["AU12"]
        ndarray = self.line_writer.write_lines(ndarray, [f"AU06: {au06}", f"AU12: {au12}", f"Port: {self.port}"])
        return ndarray

    def _cv2_encode(self, ndarray: numpy.ndarray):
        is_success, image_enc = cv2.imencode(".jpg", ndarray)
        # print(type(image_enc))
        if is_success:
            im_bytes = bytearray(image_enc.tobytes())
            im_64 = base64.b64encode(im_bytes)
            return im_64