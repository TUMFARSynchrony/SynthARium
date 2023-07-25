from typing import Any, TypeGuard

import cv2
import numpy
import dlib
from matplotlib import cm
from PIL import Image
from os.path import join
from hub import BACKEND_DIR

from .buffer_filter import BufferFilter

from custom_types import util
from filters.filter import Filter
from .glasses_detection_filter_dict import GlassesDetectionFilterDict

class GlassesDetection(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    predictor_path: str
    detector: Any
    predictor: Any
    counter: int
    glasses: list[bool]
    judge: str

    _config: GlassesDetectionFilterDict
    _buffer_filter: BufferFilter | None = None

    async def complete_setup(self) -> None:
        # Get frame buffer
        buffer_filter_id = self._config["buffer_filter_id"]
        buffer_filter = self.video_track_handler.filters[buffer_filter_id]
        self._buffer_filter = buffer_filter # type: ignore
        self.counter = 0
        self.judge = "Processing ..."

        # self.predictor_path = join(BACKEND_DIR, "filters/glasses_detection/shape_predictor_5_face_landmarks.dat")
        self.predictor_path = join(BACKEND_DIR, "filters/glasses_detection/shape_predictor_68_face_landmarks.dat")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)

    @staticmethod
    def name(self) -> str:
        return "GLASSES_DETECTION"

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        height, _, _ = ndarray.shape
        origin = (10,height - 10)

        if (type(self._buffer_filter) == BufferFilter):
            if self._buffer_filter.frame_buffer == None or len(self._buffer_filter.frame_buffer) == 0:
                if self.counter == 30:
                    self.judge = self.judge_glasses()
                    self.counter += 1
            else:
                img = self._buffer_filter.frame_buffer.pop()
                self.simple_glasses_detection(img)
                # computation takes to long
                # the data channel might be already closed and throws an error
                # this terminates the video stream

        print("Counter is: ", self.counter)
        cv2.putText(ndarray, self.judge, origin, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        return ndarray

    def judge_glasses(self):
        if True in self.glasses:
            return "With Glasses"
        else:
            return "No Glasses"

    def simple_glasses_detection(self, img):
        print("perform simple glasses detection")

        if len(self.detector(img))>0:
            print("if statement")
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = numpy.array([[p.x, p.y] for p in sp.parts()])

            nose_bridge_x = []
            nose_bridge_y = []


            for i in [20,28,29,30,31,33,34,35]:
                nose_bridge_x.append(landmarks[i][0])
                nose_bridge_y.append(landmarks[i][1])


            ### x_min and x_max
            x_min = min(nose_bridge_x)
            x_max = max(nose_bridge_x)

            ### ymin (from top eyebrow coordinate),  ymax
            y_min = landmarks[20][1]
            y_max = landmarks[30][1]


            img2 = Image.fromarray(numpy.uint8(img)).convert('RGB')
            img2 = img2.crop((x_min,y_min,x_max,y_max))

            img_blur = cv2.GaussianBlur(numpy.array(img2),(3,3), sigmaX=0, sigmaY=0)

            edges = cv2.Canny(image =img_blur, threshold1=100, threshold2=200)
            edges_center = edges.T[(int(len(edges.T)/2))]

            self.counter += 1

            if 255 in edges_center:
                print("Glasses are present")
                self.glasses.append(True)
            else:
                print("Glasses are absent")
                self.glasses.append(False)

    def glasses_detection(self, ndarray):
        print("perform glasses detection")
        gray = cv2.cvtColor(ndarray, cv2.COLOR_BGR2GRAY)

        rects = self.detector(gray, 0)

        for i, rect in enumerate(rects):
            x_face = rect.left()
            y_face = rect.top()
            w_face = rect.right() - x_face
            h_face = rect.bottom() - y_face

            cv2.rectangle(ndarray, (x_face, y_face), (x_face+w_face,y_face+h_face), (0,255,0), 2)

            landmarks = self.predictor(gray, rect)
            landmarks = self.landmarks_to_np(landmarks)

            for (x, y) in landmarks:
                cv2.circle(ndarray, (x, y), 2, (0, 0, 255), -1)

            LEFT_EYE_CENTER, RIGHT_EYE_CENTER = self.get_centers(ndarray, landmarks)

            aligned_face = self.get_aligned_face(gray, LEFT_EYE_CENTER, RIGHT_EYE_CENTER)
            judge = self.judge_eyeglass(aligned_face)

            if judge:
                print("Glasses are present")
                self.glasses.append(judge)
            else:
                print("Glasses are absent")
                self.glasses.append(judge)

    def landmarks_to_np(self, landmarks, dtype="int") -> numpy.ndarray:
        num = landmarks.num_parts

        # initialize the list of (x, y)-coordinates
        coords = numpy.zeros((num, 2), dtype=dtype)

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, num):
            coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
        # return the list of (x, y)-coordinates
        return coords

    def get_centers(self, img, landmarks):
        EYE_LEFT_OUTTER = landmarks[2]
        EYE_LEFT_INNER = landmarks[3]
        EYE_RIGHT_OUTTER = landmarks[0]
        EYE_RIGHT_INNER = landmarks[1]

        x = ((landmarks[0:4]).T)[0]
        y = ((landmarks[0:4]).T)[1]
        A = numpy.vstack([x, numpy.ones(len(x))]).T
        k, b = numpy.linalg.lstsq(A, y, rcond=None)[0]

        x_left = (EYE_LEFT_OUTTER[0]+EYE_LEFT_INNER[0])/2
        x_right = (EYE_RIGHT_OUTTER[0]+EYE_RIGHT_INNER[0])/2
        LEFT_EYE_CENTER =  numpy.array([numpy.int32(x_left), numpy.int32(x_left*k+b)])
        RIGHT_EYE_CENTER =  numpy.array([numpy.int32(x_right), numpy.int32(x_right*k+b)])

        pts = numpy.vstack((LEFT_EYE_CENTER,RIGHT_EYE_CENTER))
        cv2.polylines(img, [pts], False, (255,0,0), 1) #画回归线
        cv2.circle(img, (LEFT_EYE_CENTER[0],LEFT_EYE_CENTER[1]), 3, (0, 0, 255), -1)
        cv2.circle(img, (RIGHT_EYE_CENTER[0],RIGHT_EYE_CENTER[1]), 3, (0, 0, 255), -1)

        return LEFT_EYE_CENTER, RIGHT_EYE_CENTER


    def get_aligned_face(self, img, left, right):
        desired_w = 256
        desired_h = 256
        desired_dist = desired_w * 0.5

        eyescenter = ((left[0]+right[0])*0.5 , (left[1]+right[1])*0.5)# 眉心
        dx = right[0] - left[0]
        dy = right[1] - left[1]
        dist = numpy.sqrt(dx*dx + dy*dy)# 瞳距
        scale = desired_dist / dist # 缩放比例
        angle = numpy.degrees(numpy.arctan2(dy,dx)) # 旋转角度
        M = cv2.getRotationMatrix2D(eyescenter,angle,scale)# 计算旋转矩阵

        # update the translation component of the matrix
        tX = desired_w * 0.5
        tY = desired_h * 0.5
        M[0, 2] += (tX - eyescenter[0])
        M[1, 2] += (tY - eyescenter[1])

        aligned_face = cv2.warpAffine(img,M,(desired_w,desired_h))

        return aligned_face

    def judge_eyeglass(self, img):
        img = cv2.GaussianBlur(img, (11,11), 0) #高斯模糊

        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0 ,1 , ksize=-1) #y方向sobel边缘检测
        sobel_y = cv2.convertScaleAbs(sobel_y) #转换回uint8类型
        #cv2.imshow('sobel_y',sobel_y)

        edgeness = sobel_y #边缘强度矩阵

        #Otsu二值化
        retVal,thresh = cv2.threshold(edgeness,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        #计算特征长度
        d = len(thresh) * 0.5
        x = numpy.int32(d * 6/7)
        y = numpy.int32(d * 3/4)
        w = numpy.int32(d * 2/7)
        h = numpy.int32(d * 2/4)

        x_2_1 = numpy.int32(d * 1/4)
        x_2_2 = numpy.int32(d * 5/4)
        w_2 = numpy.int32(d * 1/2)
        y_2 = numpy.int32(d * 8/7)
        h_2 = numpy.int32(d * 1/2)

        roi_1 = thresh[y:y+h, x:x+w] #提取ROI
        roi_2_1 = thresh[y_2:y_2+h_2, x_2_1:x_2_1+w_2]
        roi_2_2 = thresh[y_2:y_2+h_2, x_2_2:x_2_2+w_2]
        roi_2 = numpy.hstack([roi_2_1,roi_2_2])

        measure_1 = sum([sum(roi_1/255)]) / (numpy.shape(roi_1)[0] * numpy.shape(roi_1)[1])#计算评价值
        measure_2 = sum([sum(roi_2/255)]) / (numpy.shape(roi_2)[0] * numpy.shape(roi_2)[1])#计算评价值
        measure = measure_1*0.3 + measure_2*0.7

        #cv2.imshow('roi_1',roi_1)
        #cv2.imshow('roi_2',roi_2)
        print(measure)

        #根据评价值和阈值的关系确定判别值
        if measure > 0.15:#阈值可调，经测试在0.15左右
            judge = True
        else:
            judge = False
        print(judge)
        return judge


    @staticmethod
    def validate_dict(data) -> TypeGuard[GlassesDetectionFilterDict]:
        return (
            util.check_valid_typeddict_keys(data, GlassesDetectionFilterDict)
            and "buffer_filter_id" in data
            and isinstance(data["buffer_filter_id"], str)
        )
