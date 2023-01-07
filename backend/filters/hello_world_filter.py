from filters.filter import Filter
import numpy
import cv2


class HelloWorldFilter(Filter):

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # Parameters for cv2.putText
        origin = (50, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        color = (0, 0, 0)

        # Put text on image
        ndarray = cv2.putText(ndarray, "Hello World", origin, font, font_size, color)

        # Return modified frame
        return ndarray