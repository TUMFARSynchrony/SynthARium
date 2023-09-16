from typing import Any
import cv2
import numpy
import dlib
from PIL import Image
from os.path import join
from hub import BACKEND_DIR


from filters import FilterDict

from filters.filter import Filter


class SimpleGlassesDetection(Filter):
    """Filter saving the last 60 frames in `frame_buffer`."""

    counter: int
    text: str
    predictor_path: str
    detector: Any
    predictor: Any

    def __init__(
        self, config: FilterDict, audio_track_handler, video_track_handler
    ) -> None:
        """Initialize new Simple Glasses Detection Filter.
        Parameters
        ----------
        See base class: filters.filter.Filter.
        """
        super().__init__(config, audio_track_handler, video_track_handler)
        self.counter = 0
        self.text = "Processing ..."

        self.predictor_path = join(
            BACKEND_DIR,
            "filters/glasses_detection/shape_predictor_68_face_landmarks.dat",
        )
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)

    @staticmethod
    def name(self) -> str:
        return "SIMPLE_GLASSES_DETECTION"

    @staticmethod
    def filter_type(self) -> str:
        return "TEST"

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

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10, height - 10)

        # Process every 30th frame (~1 sec) and only first 30 seconds:
        if not self.counter % 30 and self.counter <= 900:
            self.text = self.simple_glasses_detection(ndarray)

        cv2.putText(
            ndarray,
            self.text,
            origin,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        self.counter += 1

        return ndarray

    def simple_glasses_detection(self, img):
        if len(self.detector(img)) > 0:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = numpy.array([[p.x, p.y] for p in sp.parts()])

            nose_bridge_x = []
            nose_bridge_y = []

            for i in [20, 28, 29, 30, 31, 33, 34, 35]:
                nose_bridge_x.append(landmarks[i][0])
                nose_bridge_y.append(landmarks[i][1])

            x_min = min(nose_bridge_x)
            x_max = max(nose_bridge_x)

            y_min = landmarks[20][1]
            y_max = landmarks[30][1]

            img2 = Image.fromarray(numpy.uint8(img)).convert("RGB")
            img2 = img2.crop((x_min, y_min, x_max, y_max))

            img_blur = cv2.GaussianBlur(numpy.array(img2), (3, 3), sigmaX=0, sigmaY=0)

            edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
            edges_center = edges.T[(int(len(edges.T) / 2))]

            self.counter += 1

            if 255 in edges_center:
                return "Glasses detected"
            else:
                return "No glasses detected"

        else:
            return self.text