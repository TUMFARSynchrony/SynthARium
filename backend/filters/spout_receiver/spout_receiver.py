import numpy
import SpoutGL
from itertools import islice, cycle, repeat
import time
from OpenGL import GL
from random import randint
import cv2
import array
import time
import logging

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
    _logger : logging.Logger
    # sender : 

    @staticmethod
    def randcolor(self):
        return randint(0, 255)
        

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()
        self._logger = logging.getLogger("SpoutReceiver")
        # self.sender = SpoutGL.SpoutSender()
        # self.sender.setSenderName("chloeR")
        self.receiver = SpoutGL.SpoutReceiver()
        # self.receiver.setReceiverName(str(name))
        self.receiver.setReceiverName("TDSyphonSpoutOut")
        self.name = self.receiver.getSenderName()
        self.format = self.receiver.getSenderFormat()
        self.buffer = None
        self.width = 0
        self.height = 0
        self.dsize = None


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
        

        #self._logger.info("PRINT TO CONSOLE")
        #buffer = None
        result = self.receiver.receiveImage(self.buffer, GL.GL_RGBA, False, 0)
        image_data= None
        # dsize = (640, 480)
        # self._logger.info(f"shape of ndarray {ndarray.shape} and shape of first 2 dimentions {ndarray[:,:,0].shape} and type of first two dimentions {type(ndarray[:,:,0].shape)}")
        if self.dsize == None:
            out_dim = ndarray[:,:,0].shape
            self.dsize = (out_dim[1], out_dim[0])

        # make depending on nd array
        # self._logger.info(f"This is the Receiver Result: {result}")
        #TODO make buffer a local variable,  - expensive operation?
        #TODO shape needs to be read from ndarray
        #TODO figure out how to write code to console.

        if self.receiver.isUpdated():
            self.width = self.receiver.getSenderWidth()
            self.height = self.receiver.getSenderHeight()
            self.buffer = array.array('B', repeat(0, self.width * self.height * 4))
            # self._logger.info("SPOUT RECEIVER IS UPDATED")
        
        # self._logger.info(f"buffer content: {self.buffer}")
        # try:
        #     self._logger.info(f"self.buffer: {bool(self.buffer)} and result: {bool(result)} and isBufferEmpy: {SpoutGL.helpers.isBufferEmpty(self.buffer)}")    
        # except Exception as err:
        #     self._logger.error(err)

        if self.buffer and result:
            #and not SpoutGL.helpers.isBufferEmpty(self.buffer):
            try: 
                if not SpoutGL.helpers.isBufferEmpty(self.buffer):
                    image_data = numpy.frombuffer(self.buffer, dtype=numpy.uint8).reshape((self.height, self.width, 4))
                    image_data = image_data[:,:, :-1]
                    ndarray= cv2.resize(image_data, self.dsize)
                    # self._logger.info("Resized Image! Yay!")
                    # image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
                    # cv2.imshow('SpoutGL Image', image_bgr)
                    # cv2.waitKey(1)  # Update the display window
            except Exception as err:
                self._logger.error(err)
            

        # self.line_writer.write_line(ndarray, "{0}".format(time.time()))
        #this line below breaks.
        #self.receiver.waitFrameSync(self.name, 0)
        # received image 360, 640, 4
        # ndarray 480, 640, 3
        
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