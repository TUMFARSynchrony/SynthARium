import numpy
import SpoutGL
from itertools import islice, cycle
import time
from OpenGL import GL
from random import randint
import logging

from filters import Filter
from filters.simple_line_writer import SimpleLineWriter

from PIL import Image


class SpoutSender(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter
    _logger : logging.Logger
    # target_fps: int
    # sender_width: int
    # sender_height: int
    # sender_name : str
    # pixels : bytes
    # sender : 

    @staticmethod
    def randcolor(self) -> None:
        return randint(0, 255)

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()
        
        #TODO get sendername from filter config
        # Sender Initialize
        self.sender = SpoutGL.SpoutSender()
        self.sender.setSenderName("exp-hub-sender")
    
  

    @staticmethod
    def name(self) -> str:
        # change this name to your filter name in all capslock
        return "SPOUT_SENDER"

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


    # def rescale(arr):
    #     arr_min = arr.min()
    #     arr_max = arr.max()
    #     return (arr- arr_min)/(arr_max - arr_min)

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # change this to implement filter
        # self.line_writer.write_line(ndarray, "Hello")

        image = Image.fromarray(ndarray, 'RGB')
        pixels = image.tobytes()
        SEND_WIDTH, SEND_HEIGHT = image.size

        #TODO try to send same size as receiving array.
        self.sender.sendImage(pixels, SEND_WIDTH, SEND_HEIGHT, GL.GL_BGR, False, 0)

        # Return modified frame
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