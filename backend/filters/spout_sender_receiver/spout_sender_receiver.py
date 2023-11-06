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
from PIL import Image


from filters import Filter
from filters.simple_line_writer import SimpleLineWriter


class SpoutSenderReceiver(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter
    _logger : logging.Logger


    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()
        self._logger = logging.getLogger("SpoutReceiver")

        # Sender Initialize
        #TODO get sendername from filter config
        self.sender = SpoutGL.SpoutSender()
        self.sender.setSenderName("exp-hub-sender")

        #TODO assign getReceiverName from filter config
        # Receiver Initalize
        self.receiver = SpoutGL.SpoutReceiver()
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
        return "SPOUT_SENDER_RECEIVER"

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
        #send ndarray through spout
        image = Image.fromarray(ndarray, 'RGB')
        pixels = image.tobytes()
        SEND_WIDTH, SEND_HEIGHT = image.size

        #TODO try to send same size as receiving array.
        self.sender.sendImage(pixels, SEND_WIDTH, SEND_HEIGHT, GL.GL_BGR, False, 0)
       
       #TODO make buffer a local variable,  - expensive operation?
        #self._logger.info("PRINT TO CONSOLE")
        #receive image from spout
        result = self.receiver.receiveImage(self.buffer, GL.GL_RGBA, False, 0)
        image_data= None
        # self._logger.info(f"shape of ndarray {ndarray.shape} and shape of first 2 dimentions {ndarray[:,:,0].shape} and type of first two dimentions {type(ndarray[:,:,0].shape)}")
        # allocates dsize to resize image from the initial ndarray shape 
        if self.dsize == None:
            out_dim = ndarray[:,:,0].shape
            self.dsize = (out_dim[1], out_dim[0])
        
        # initializes buffer to a byte array of 0s if receiver is updated 
        if self.receiver.isUpdated():
            self.width = self.receiver.getSenderWidth()
            self.height = self.receiver.getSenderHeight()
            self.buffer = array.array('B', repeat(0, self.width * self.height * 4))

        # if buffer and result exist, try to see if buffer is not empty and 
        # receive buffer data updated by calling receiveImage on line 100. 
        if self.buffer and result:
            #and not SpoutGL.helpers.isBufferEmpty(self.buffer):
            try: 
                if not SpoutGL.helpers.isBufferEmpty(self.buffer):
                    image_data = numpy.frombuffer(self.buffer, dtype=numpy.uint8).reshape((self.height, self.width, 4))
                    image_data = image_data[:,:, :-1]
                    ndarray= cv2.resize(image_data, self.dsize)
                    # Optional lines of code to also print the output to a seperate window
                    # image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
                    # cv2.imshow('SpoutGL Image', image_bgr)
                    # cv2.waitKey(1)  # Update the display window
            except Exception as err:
                self._logger.error(err)
            
        # Optional line of code to write text to screen
        # self.line_writer.write_line(ndarray, "{0}".format(time.time()))
      
        return ndarray