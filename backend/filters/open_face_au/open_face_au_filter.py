from datetime import datetime
from typing import Optional

import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.filter_data_dict import FilterDataDict
from filters.simple_line_writer import SimpleLineWriter
from filters.open_face_au.open_face_au_extractor import OpenFaceAUExtractor
from .open_face_data_parser import OpenFaceDataParser



class OpenFaceAUFilter(Filter):
    """OpenFace AU Extraction filter."""

    frame: int
    data: dict
    file_writer: OpenFaceDataParser
    line_writer: SimpleLineWriter
    au_extractor: OpenFaceAUExtractor


    def __init__(self, config, audio_track_handler, video_track_handler,participant_id):
        super().__init__(config, audio_track_handler, video_track_handler,participant_id)
        self.au_extractor = OpenFaceAUExtractor()
        self.line_writer = SimpleLineWriter()
        self.file_writer = OpenFaceDataParser(self.participant_id)

        self.data = {"intensity": {"AU06": "-", "AU12": "-"}}
        self.frame = 0
        self.start_time = datetime.now()  # Start time will be recorded when actual video starts

    def __del__(self):
        del self.file_writer, self.line_writer, self.au_extractor

    @staticmethod
    def name() -> str:
        return "OPENFACE_AU"

    @staticmethod
    def type() -> str:
        return "SESSION"

    @staticmethod
    def channel() -> str:
        return "video"

    async def get_filter_data(self) -> None | FilterDataDict:
        return FilterDataDict(
            id=self.id,
            data={"data": self.data},
        )

    async def process(
            self, original: Optional[VideoFrame] = None, ndarray: numpy.ndarray = None, **kwargs
    ) -> numpy.ndarray:

        self.frame += 1

        exit_code, msg, result = self.au_extractor.extract(
            ndarray, self.data.get("roi", None)
        )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        elapsed_time = datetime.now() - self.start_time
        fps = self.frame / elapsed_time.total_seconds() if elapsed_time.total_seconds() > 0 else 0

        au06 = self.data["intensity"]["AU06"]
        au12 = self.data["intensity"]["AU12"]
        if exit_code == 0:
            self.data = result
            self.file_writer.write(timestamp, self.frame, au06, au12, fps)
        else:
            self.file_writer.write(timestamp, self.frame,-1, -1, fps)

        if original is not None:
            ndarray = self.line_writer.write_lines(
                ndarray, [f"AU06: {au06}", f"AU12: {au12}", msg]
            )
            return ndarray
        else:
            return [{"frame": self.frame, "AU06": au06, "AU12": au12, "message": msg}]

    async def cleanup(self) -> None:
        del self
