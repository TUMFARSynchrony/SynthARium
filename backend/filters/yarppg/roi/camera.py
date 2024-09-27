import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image


class Camera(QThread):
    """Wraps cv2.VideoCapture and emits Qt signals with frames in RGB format.

    The :py:`run` function launches a loop that waits for new frames in
    the VideoCapture and emits them with a `new_frame` signal.  Calling
    :py:`stop` stops the loop and releases the camera.
    """

    frame_received = pyqtSignal(np.ndarray)

    def __init__(self, video=0, parent=None, limit_fps=None):
        """Initialize Camera instance

        Args:
            video (int or string): ID of camera or video filename
            parent (QObject): parent object in Qt context
            limit_fps (float): force FPS limit, delay read if necessary.
        """

        QThread.__init__(self, parent=parent)
        self.img = Image.fromarray(array)


    # TODO: bring this logic outside. 
    # frame = ndarray. 
    # emit frame to self.frame_recevied as cv2 
    #  but frame_received.emit takes a cv2 image..
    # to convert numpy to img with cv2 use: 
    # img = numpy.zeros([5,5,3])
    # img[:,:,0] = numpy.ones([5,5])*64/255.0
    # img[:,:,1] = numpy.ones([5,5])*128/255.0
    # img[:,:,2] = numpy.ones([5,5])*192/255.0

    # cv2.imwrite('color_img.jpg', img)
    # cv2.imshow("image", img)
    # cv2.waitKey()
    # or
    # img = Image.fromarray(array)
    def run(self, ndarray):
        # ret, frame = self._cap.read()
        frame = Image.fromarray(ndarray)
            
        self.frame_received.emit(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # def stop(self):
    #     self._running = False
    #     time.sleep(0.1)
    #     self._cap.release()
