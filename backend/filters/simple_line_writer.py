import cv2
import numpy


class SimpleLineWriter:
    def __init__(self):
        self.origin = (50, 50)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 1
        self.color = (0, 255, 0)
        self.thickness = 2
        self.offset = 0

    def __int__(self, origin=(50, 50), font=cv2.FONT_HERSHEY_SIMPLEX, font_size=1, color=(0, 255, 0), thickness=2):
        self.origin = origin
        self.font = font
        self.font_size = font_size
        self.color = color
        self.thickness = thickness
        self.offset = 0

    def write_line(self, ndarray: numpy.ndarray, line: str):
        ndarray = cv2.putText(ndarray, line, self.origin, self.font, self.font_size, (0, 0, 0), self.thickness + 6)
        return cv2.putText(ndarray, line, self.origin, self.font, self.font_size, self.color, self.thickness)

    def write_lines(self, ndarray: numpy.ndarray, lines: [str]):
        for i, line in enumerate(lines):
            l = list(self.origin)
            l[1] = l[1] + 50 * i
            new_origin = tuple(l)
            ndarray = cv2.putText(ndarray, line, new_origin, self.font, self.font_size, (0, 0, 0), self.thickness + 6)
            ndarray = cv2.putText(ndarray, line, new_origin, self.font, self.font_size, self.color, self.thickness)
        return ndarray

    def reset(self):
        self.offset = 0
