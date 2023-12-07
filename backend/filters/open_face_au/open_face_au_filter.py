import base64
import logging
import cv2
import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.open_face_au.open_face import OpenFace
from filters.open_face_au.rabbitmq.mq_publisher import MQPublisher
from filters.open_face_au.rabbitmq.mq_consumer import MQConsumer


class OpenFaceAUFilter(Filter):
    """OpenFace AU Extraction filter."""

    frame: int
    data: dict
    open_face: OpenFace
    publisher: MQPublisher
    consumer: MQConsumer

    def __init__(self, config, audio_track_handler, video_track_handler, participant):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.logger = logging.getLogger("OpenFaceAUFilter")

        self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
        self.frame = 0
        self.participant = participant
        self.open_face = OpenFace(participant["participant_id"])
        self.setup(participant)
        # self.reset()
        #TODO: reset queue & csv file & frame when experiment starts or start everything when experiment starts

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
        if reset:
            self.frame = 1
            self.reset()
            self.setup(self.participant)

        # If ROI is sent from the OpenFace, only send that region
        if "roi" in self.data.keys() and self.data["roi"]["width"] != 0:
            roi = self.data["roi"]
            ndarray = ndarray[
                    roi["y"] : (roi["y"] + roi["height"]),
                    roi["x"] : (roi["x"] + roi["width"]),
                    ]

        is_success, image_enc = cv2.imencode(".png", ndarray)

        if not is_success:
            self.logger.error(f"Failed to encode image to opencv, frame {self.frame}")
            return ndarray
        
        im_bytes = bytearray(image_enc.tobytes())
        im_64 = base64.b64encode(im_bytes)

        if self.publisher is not None:
            self.publisher.publish(im_64, str(self.frame))

        return ndarray

    async def cleanup(self) -> None:
        del self
