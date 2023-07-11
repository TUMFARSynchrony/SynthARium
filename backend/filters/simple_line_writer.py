import cv2
import numpy


class SimpleLineWriter:
    origin: tuple
    font: int
    font_size: int
    color: tuple
    thickness: int
    offset: int

    def __init__(
        self,
        origin=(50, 50),
        font=cv2.FONT_HERSHEY_SIMPLEX,
        font_size=1,
        color=(0, 255, 0),
        thickness=2,
    ):
        self.origin = origin
        self.font = font
        self.font_size = font_size
        self.color = color
        self.thickness = thickness
        self.offset = 50

    def write_line(
        self, ndarray: numpy.ndarray, line: str, origin: tuple = None
    ) -> numpy.ndarray:
        if origin is None:
            origin = self.origin

        ndarray = cv2.putText(
            ndarray,
            line,
            origin,
            self.font,
            self.font_size,
            (0, 0, 0),
            self.thickness + 6,
        )
        return cv2.putText(
            ndarray, line, origin, self.font, self.font_size, self.color, self.thickness
        )

    def write_lines(self, ndarray: numpy.ndarray, lines: list[str]) -> numpy.ndarray:
        for i, line in enumerate(lines):
            coords = list(self.origin)
            coords[1] = coords[1] + self.offset * i
            new_origin = tuple(coords)
            ndarray = self.write_line(ndarray, line, new_origin)
        return ndarray
