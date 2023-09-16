from typing import Any

import cv2
import numpy
import dlib
from os.path import join
from hub import BACKEND_DIR

from filters.filter import Filter
from filters import FilterDict


class GlassesDetection(Filter):
    """A glasses detection filter printing on a video Track if there were glasses detected or not."""

    predictor_path: str
    detector: Any
    predictor: Any
    counter: int
    text: str

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
            "filters/glasses_detection/shape_predictor_5_face_landmarks.dat",
        )
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)

    @staticmethod
    def name(self) -> str:
        return "GLASSES_DETECTION"

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
            "config": {}
        }

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10, height - 10)

        # Process every 30th frame (~1 sec) and only first 30 seconds:
        if not self.counter % 30 and self.counter <= 900:
            self.text = self.glasses_detection(ndarray)

        self.counter += 1

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

        return ndarray

    def glasses_detection(self, ndarray):
        print("perform glasses detection")
        gray = cv2.cvtColor(ndarray, cv2.COLOR_BGR2GRAY)

        rects = self.detector(gray, 0)

        for i, rect in enumerate(rects):
            x_face = rect.left()
            y_face = rect.top()
            w_face = rect.right() - x_face
            h_face = rect.bottom() - y_face

            cv2.rectangle(
                ndarray,
                (x_face, y_face),
                (x_face + w_face, y_face + h_face),
                (0, 255, 0),
                2,
            )

            landmarks = self.predictor(gray, rect)
            landmarks = self.landmarks_to_np(landmarks)

            for x, y in landmarks:
                cv2.circle(ndarray, (x, y), 2, (0, 0, 255), -1)

            LEFT_EYE_CENTER, RIGHT_EYE_CENTER = self.get_centers(ndarray, landmarks)

            aligned_face = self.get_aligned_face(
                gray, LEFT_EYE_CENTER, RIGHT_EYE_CENTER
            )
            judge = self.judge_eyeglass(aligned_face)

            if judge:
                return "Glasses detected"
            else:
                return "No glasses detected"

        return self.text

    def landmarks_to_np(self, landmarks, dtype="int") -> numpy.ndarray:
        num = landmarks.num_parts

        # initialize the list of (x, y)-coordinates
        coords = numpy.zeros((num, 2), dtype=dtype)

        # loop over the facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, num):
            coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
        # return the list of (x, y)-coordinates
        return coords

    def get_centers(self, img, landmarks):
        """
        1. calculates the eye position according to the landmarks
        2. draws circles and lines on the eye postion
        """
        EYE_LEFT_OUTTER = landmarks[2]
        EYE_LEFT_INNER = landmarks[3]
        EYE_RIGHT_OUTTER = landmarks[0]
        EYE_RIGHT_INNER = landmarks[1]

        x = ((landmarks[0:4]).T)[0]
        y = ((landmarks[0:4]).T)[1]
        A = numpy.vstack([x, numpy.ones(len(x))]).T
        k, b = numpy.linalg.lstsq(A, y, rcond=None)[0]

        x_left = (EYE_LEFT_OUTTER[0] + EYE_LEFT_INNER[0]) / 2
        x_right = (EYE_RIGHT_OUTTER[0] + EYE_RIGHT_INNER[0]) / 2
        LEFT_EYE_CENTER = numpy.array(
            [numpy.int32(x_left), numpy.int32(x_left * k + b)]
        )
        RIGHT_EYE_CENTER = numpy.array(
            [numpy.int32(x_right), numpy.int32(x_right * k + b)]
        )

        pts = numpy.vstack((LEFT_EYE_CENTER, RIGHT_EYE_CENTER))
        cv2.polylines(img, [pts], False, (255, 0, 0), 1)
        cv2.circle(img, (LEFT_EYE_CENTER[0], LEFT_EYE_CENTER[1]), 3, (0, 0, 255), -1)
        cv2.circle(img, (RIGHT_EYE_CENTER[0], RIGHT_EYE_CENTER[1]), 3, (0, 0, 255), -1)

        return LEFT_EYE_CENTER, RIGHT_EYE_CENTER

    def get_aligned_face(self, img, left, right):
        """
        caclulates eye center and algines face according to the eye center
        """
        desired_w = 256
        desired_h = 256
        desired_dist = desired_w * 0.5

        eyescenter = ((left[0] + right[0]) * 0.5, (left[1] + right[1]) * 0.5)  # 眉心
        dx = right[0] - left[0]
        dy = right[1] - left[1]
        dist = numpy.sqrt(dx * dx + dy * dy)
        scale = desired_dist / dist
        angle = numpy.degrees(numpy.arctan2(dy, dx))
        M = cv2.getRotationMatrix2D(eyescenter, angle, scale)

        # update the translation component of the matrix
        tX = desired_w * 0.5
        tY = desired_h * 0.5
        M[0, 2] += tX - eyescenter[0]
        M[1, 2] += tY - eyescenter[1]

        aligned_face = cv2.warpAffine(img, M, (desired_w, desired_h))

        return aligned_face

    def judge_eyeglass(self, img):
        """
        1. Adds gaussian blur (black&white) and sobel (even more black&white) to the video stream to get better edges
        2. calculates coordinates of the ROIs (bridge, left cheek, right cheek)
        3. measures if there eyeglasses are present
        """
        img = cv2.GaussianBlur(img, (11, 11), 0)

        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=-1)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        edgeness = sobel_y

        retVal, thresh = cv2.threshold(
            edgeness, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        d = len(thresh) * 0.5
        x = numpy.int32(d * 6 / 7)
        y = numpy.int32(d * 3 / 4)
        w = numpy.int32(d * 2 / 7)
        h = numpy.int32(d * 2 / 4)

        x_2_1 = numpy.int32(d * 1 / 4)
        x_2_2 = numpy.int32(d * 5 / 4)
        w_2 = numpy.int32(d * 1 / 2)
        y_2 = numpy.int32(d * 8 / 7)
        h_2 = numpy.int32(d * 1 / 2)

        roi_1 = thresh[y : y + h, x : x + w]
        roi_2_1 = thresh[y_2 : y_2 + h_2, x_2_1 : x_2_1 + w_2]
        roi_2_2 = thresh[y_2 : y_2 + h_2, x_2_2 : x_2_2 + w_2]
        roi_2 = numpy.hstack([roi_2_1, roi_2_2])

        measure_1 = sum([sum(roi_1 / 255)]) / (
            numpy.shape(roi_1)[0] * numpy.shape(roi_1)[1]
        )  # 计算评价值
        measure_2 = sum([sum(roi_2 / 255)]) / (
            numpy.shape(roi_2)[0] * numpy.shape(roi_2)[1]
        )  # 计算评价值
        measure = measure_1 * 0.3 + measure_2 * 0.7

        print(measure)

        return True if measure > 0.15 else False
