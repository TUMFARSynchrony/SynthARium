import numpy
import SpoutGL
from itertools import islice, cycle, repeat
import time
from OpenGL import GL
from random import randint
import cv2
import array

from filters import Filter
from filters.simple_line_writer import SimpleLineWriter


class SpoutReceiver(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter
    target_fps: int
    sender_width: int
    sender_height: int
    sender_name : str
    pixels : bytes
    # sender : 

    @staticmethod
    def randcolor(self):
        return randint(0, 255)
        

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()
        # self.sender = SpoutGL.SpoutSender()
        # self.sender.setSenderName("chloeR")
        self.receiver = SpoutGL.SpoutReceiver()
        self.name = self.receiver.getSenderName()
        # self.receiver.setReceiverName(str(name))
        self.receiver.setReceiverName("TDSyphonSpoutOut")
        self.buffer = None
        self.result = self.receiver.receiveImage(self.buffer, GL.GL_RGBA, False, 0)
        # self.update = self.receiver.isUpdated()

    @staticmethod
    def name(self) -> str:
        # change this name to your filter name in all capslock
        return "SPOUT_RECEIVER"

    @staticmethod
    def filter_type(self) -> str:
        """ change this according to your filter type (SESSION or TEST)
        SESSION - filters run during an experimental session or 
        during both the lobby page and after experiment is started 
        TEST - filters run only during the lobby page"""
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
            "config": {
                # example of how a filter config can look like
                # add or delete this
                # This would show that there is a string variable (direction) which can
                # have different values and another int variable (size) in the 
                # frontend, we would then have either a dropdown (direction) or input
                # number (size). The values can be changed and sent back to the backend
                # """
                # "direction": {
                #     "defaultValue": ["clockwise", "anti-clockwise"],
                #     "value": "clockwise",
                # },
                # "size": {
                #     "min": 1,
                #     "max": 60,
                #     "step": 1,
                #     "value": 45,
                #     "defaultValue": 45,
                # }, """
            },
        }

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # change this to implement filter
        # pixels = ndarray.tobytes()
        # pixels = bytes(islice(cycle([randcolor(), randcolor(), randcolor(), 255]), send_width * send_height * 4))
        
        # target_fps = 60
        # sender_width = 256
        # sender_height = 256
        # sender_name = "SpoutGL-test3"
        # buffer = None

        self.receiver.receiveImage(self.buffer, GL.GL_RGBA, False, 0)
        image_data= None
        width = self.receiver.getSenderWidth()
        height = self.receiver.getSenderHeight()
        self.buffer = array.array('B', repeat(0, width * height * 4))
        if SpoutGL.helpers.isBufferEmpty(self.buffer):
            image_data = numpy.frombuffer(self.buffer, dtype=numpy.uint8).reshape((height, width, 4))
            self.line_writer.write_line(ndarray, "{0}".format(type(image_data)))
        # name = self.receiver.getSenderName()
        # self.line_writer.write_line(ndarray, "{0}".format(name))
        # if self.receiver.isUpdated():
        #     self.line_writer.write_line(ndarray, "True")
        # else:
        #     self.line_writer.write_line(ndarray, "No update")

        # if self.update:
        #     self.line_writer.write_line(ndarray, "True")
        # else:
        #     self.line_writer.write_line(ndarray, "No update")
        # self.line_writer.write_line(ndarray, "{0}".format(buffer))
        # width = self.receiver.getSenderWidth()
        # height = self.receiver.getSenderHeight()
        # # result = self.receiver.receiveImage("SpoutGL-test", 256, 256,  GL.GL_RGBA, False,)
        # image_data = numpy.frombuffer(buffer, dtype=numpy.uint8).reshape((height, width, 4))
        # # Convert from RGBA to BGR (OpenCV's default color format)
        # image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
        # width = self.receiver.getSenderWidth()
        # height = self.receiver.getSenderHeight()
        # # buffer = array.array('B', repeat(0, width * height * 4))
        # image_data = numpy.frombuffer(buffer, dtype=numpy.uint8).reshape((height, width, 4))
        # image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
        
        # self.sender.sendImage(pixels, sender_width, sender_height, GL.GL_RGBA, False, 0)
#       sender.sendImage(pixels, SEND_WIDTH, SEND_HEIGHT, GL.GL_RGBA, False, 0)
        # print("Send result", result)
        
#         # Indicate that a frame is ready to read
        # sender.setFrameSync(sender_name)
        
#         # Wait for next send attempt
#         time.sleep(1./TARGET_FPS)

        # Return modified frame
        # return numpy.asarray(result)
        return ndarray



# TARGET_FPS = 60
# SEND_WIDTH = 256
# SEND_HEIGHT = 256
# SENDER_NAME = "SpoutGL-test2"
# def randcolor():
#     return randint(0, 255)

# with SpoutGL.SpoutSender() as sender:
#     sender.setSenderName(SENDER_NAME)

#     while True:
#         # Generating bytes in Python is very slow; ideally you should pass in a buffer obtained elsewhere
#         # or re-use an already allocated array instead of allocating one on the fly
#         pixels = bytes(islice(cycle([randcolor(), randcolor(), randcolor(), 255]), SEND_WIDTH * SEND_HEIGHT * 4))

#         result = sender.sendImage(pixels, SEND_WIDTH, SEND_HEIGHT, GL.GL_RGBA, False, 0)
#         print("Send result", result)
        
#         # Indicate that a frame is ready to read
#         sender.setFrameSync(SENDER_NAME)
        
#         # Wait for next send attempt
#         time.sleep(1./TARGET_FPS)