import numpy

from filters import Filter
from filters.simple_line_writer import SimpleLineWriter
from ast import parse
import sys
import argparse
from PIL import Image
from collections import namedtuple
# did we want things to be based on time or frames?
import time


# from PyQt5.QtWidgets import QApplication
# from yarppg.rppg.camera import Camera
# from yarppg.ui import MainWindow
from .rppg import RPPG
from .processors.color_mean import ColorMeanProcessor
from .processors.processor import FilteredProcessor
from .hr import HRCalculator
from .filters import get_butterworth_filter
from .processors.li_cvpr import LiCvprProcessor
from .roi.roi_detect import FaceMeshDetector
# from yarppg.ui.cli import (get_detector, get_mainparser, get_processor,
                        #    parse_frequencies, get_delay)

# from PyQt5.QtCore import QThread, pyqtSignal

class yarppgFilter(Filter):
    """A simple example filter printing `Hello World` on a video Track.
    Can be used to as a template to copy when creating an own filter."""

    line_writer: SimpleLineWriter
    # frame_received = pyqtSignal(numpy.ndarray)

    # RppgResults = namedtuple("RppgResults", ["dt",
    #                                      "rawimg",
    #                                      "roi",
    #                                      "hr",
    #                                      "vs_iter",
    #                                      "ts",
    #                                      "fps",
    #                                      ])

    def __init__(self, config, audio_track_handler, video_track_handler):
        super().__init__(config, audio_track_handler, video_track_handler)
        self.line_writer = SimpleLineWriter()

        self._processors = []

        # TODO: can be facemesh, caffe-dnn, haar, or full
        self.roi_detector = FaceMeshDetector()
        # get_detector("facemesh")
        self.digital_lowpass = get_butterworth_filter(30, 1.5)
        self.hr_calc = HRCalculator(update_interval=30, winsize=300,
                            filt_fun=lambda vs: [self.digital_lowpass(v) for v in vs])

        # TODO: can be licvpr, chrom, or pos
        self.processor = LiCvprProcessor()

        #TODO change to other values
        cutoff = list(map(float, "0.5,2".split(","))) 
        if cutoff is not None:
            digital_bandpass = get_butterworth_filter(30, cutoff, "bandpass")
            processor = FilteredProcessor(self.processor, digital_bandpass)
        
        # TODO: go into rppg and fix camera
        # self.rppg = RPPG(roi_detector=self.roi_detector, 
        #             hr_calculator=self.hr_calc,
        #             parent=None,
        #             )
        # TODO: change for other processors, chrom, etc.
        for c in "rgb":
            self._processors.append(ColorMeanProcessor(channel=c, winsize=1))
            # self.add_processor(ColorMeanProcessor(channel=c, winsize=1)

    @staticmethod
    def name() -> str:
        # TODO: Change this name to a unique name.
        return "YARPPG"

    @staticmethod
    def type() -> str:
        # TODO: change this according to your filter type (SESSION, TEST or NONE)
        return "SESSION"

    @staticmethod
    def channel() -> str:
        # TODO: change this according to your filter channel (video, audio, both)
        return "video"

    @staticmethod
    def default_config() -> dict:
        # TODO: change this according to your filter config
        return {
            # example of how a filter config can look like
            # add or delete this
            # This would show that there is a string variable (direction) which can have different values
            # and another int variable (size)
            # in the frontend, we would then have either a dropdown (direction) or input number (size)
            # The values can be changed and sent back to the backend
            #
            #
            # "direction": {
            #     "defaultValue": ["clockwise", "anti-clockwise"],
            #     "value": "clockwise",
            #     "requiresOtherFilter": False,
            # },
            # "size": {
            #     "min": 1,
            #     "max": 60,
            #     "step": 1,
            #     "value": 45,
            #     "defaultValue": 45,
            # },
        }

    # def add_processor(self, processor):
    #     self._processors.append(processor)

    def _update_time(self):
        dt = time.perf_counter()- self.last_update
        self.last_update = time.perf_counter()
        self._dts.append(dt)
    
    def get_vs(self, n=None):
        for processor in self._processors:
            if n is None:
                yield numpy.array(processor.vs, copy=True)
            else:
                yield numpy.array(processor.vs[-n:], copy=True)

    def get_ts(self, n=None):
        if n is None:
            dts = self._dts
        else:
            dts = self._dts[-n:]
        return numpy.cumsum(dts)

    def get_fps(self, n=5):
        return 1/numpy.mean(self._dts[-n:])

    async def process(self, _, ndarray: numpy.ndarray) -> numpy.ndarray:
        # TODO: change this to implement filter

        frame = Image.fromarray(ndarray)
        roi = self.roi_detector(frame)
        self.processor(self.roi)

        if self.hr_calculator is not None:
            self.hr_calculator.update(self)

        dt = self._update_time()
        # need to change below to just calculate hr here..
        hr = self.hr_calc.update()

        # RppgResults(dt=dt, rawimg=frame, roi=self.roi,
                                        #    hr=numpy.nan, 
        
        vs_iter=self.get_vs
        ts=self.get_ts, 
        fps=self.get_fps()
        # if args.savepath:
        # rppg.output_filename = args.savepath
        self.line_writer.write_line(ndarray, "<3 ? : {0}".format(hr))

        # Return modified frame
        return ndarray
