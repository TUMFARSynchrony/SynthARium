import base64
import logging
import cv2
import numpy
from av import VideoFrame

from server import Config
from filters.filter import Filter
from filters.simple_line_writer import SimpleLineWriter
from filters.open_face_au.rabbitmq.open_face import OpenFaceMQ
from filters.open_face_au.rabbitmq.mq_publisher import MQPublisher
from filters.open_face_au.rabbitmq.mq_consumer import MQConsumer
from filters.open_face_au.zmq.open_face import OpenFace
from filters.open_face_au.zmq.open_face_au_extractor import OpenFaceAUExtractor


class OpenFaceAUFilter(Filter):
    """OpenFace AU Extraction filter."""

    frame: int
    data: dict
    open_face: OpenFace
    publisher: MQPublisher
    consumer: MQConsumer
    enable_rabbitmq: bool

    def __init__(self, config, audio_track_handler, video_track_handler, participant):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.logger = logging.getLogger("OpenFaceAUFilter")

        self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
        self.frame = 0
        self.participant = participant
        self.enable_rabbitmq = Config().enable_rabbitmq
        if self.enable_rabbitmq:
            self.open_face = OpenFaceMQ(participant["participant_id"])
            self.setup(participant)
            #TODO: reset queue & csv file & frame when experiment starts or start everything when experiment starts
        else:
            self.au_extractor = OpenFaceAUExtractor()
            self.line_writer = SimpleLineWriter()


    def __del__(self):
        del self.publisher, self.consumer, self.open_face

    @staticmethod
    def name(self) -> str:
        return "OPENFACE_AU"

    @staticmethod
    def filter_type(self) -> str:
        return "SESSION"

    @staticmethod
    def get_filter_json(self) -> object:
        # For docstring see filters.filter.Filter or hover over function declaration
        name = self.name(self)
        id = name.lower()
        id = id.replace("_", "-")
        return {
            "name": name,
            "id": id,
            "channel": "video",
            "groupFilter": False,
            "config": {},
        }
    
    def setup(self, participant: dict) -> None:
        self.consumer = MQConsumer(f"{participant['participant_id']}.callback", participant["session_id"])
        self.publisher = MQPublisher(participant["participant_id"], participant["participant_id"], f"{participant['participant_id']}.callback")
    
    def reset(self) -> None:
        self.consumer.reset()
        self.publisher.reset()

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray, reset: bool = False
    ) -> numpy.ndarray:
        self.frame = self.frame + 1

        # If ROI is sent from the OpenFace, only send that region
        if "roi" in self.data.keys() and self.data["roi"]["width"] != 0:
            roi = self.data["roi"]
            ndarray = ndarray[
                    roi["y"] : (roi["y"] + roi["height"]),
                    roi["x"] : (roi["x"] + roi["width"]),
                    ]

        if self.enable_rabbitmq:
            is_success, image_enc = cv2.imencode(".png", ndarray)

            if not is_success:
                self.logger.error(f"Failed to encode image to opencv, frame {self.frame}")
                return ndarray
            
            im_bytes = bytearray(image_enc.tobytes())
            im_64 = base64.b64encode(im_bytes)

            if self.publisher is not None:
                self.publisher.publish(im_64, str(self.frame))
        else:
            exit_code, msg, result = self.au_extractor.extract(ndarray)

            if exit_code == 0:
                self.data = result
                # TODO: use correct frame
                # if a frame is skipped, data corresponds to a frame before current frame, but self.frame does not

            # Put text on image
            au06 = self.data["intensity"]["AU06"]
            au12 = self.data["intensity"]["AU12"]
            ndarray = self.line_writer.write_lines(
                ndarray, [f"AU06: {au06}", f"AU12: {au12}", msg]
            )

        return ndarray

    async def cleanup(self) -> None:
        del self
