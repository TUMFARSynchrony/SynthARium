from typing import Any
import numpy as np
from av import VideoFrame, AudioFrame
from filters.filter_dict import FilterDict
from group_filters import GroupFilter
from scipy.interpolate import interp1d

from filters.open_face_au.open_face import OpenFace
from filters.open_face_au.open_face_au_extractor import OpenFaceAUExtractor
from group_filters import group_filter_utils
import zmq
from queue import Queue
import cv2
import base64
from group_filters.sync_score.bow import BoW
from group_filters.sync_score.oasis import oasis


class SyncScoreGroupFilter(GroupFilter):
    data_len_per_participant = 1
    num_participants_in_aggregation = 2

    window_size = 8  # how many frames each window contains
    word_size = 4  # how many symbols each window is mapped to (window_length / word_length is a prositive integer)
    n_bins = 3  # the size of the alphabet or the number of symbols used to represent the time series signal

    def __init__(self, config: FilterDict, participant_id: str):
        super().__init__(config, participant_id)

        self.au_extractor = OpenFaceAUExtractor()

        # open_face_port = 5555  # group_filter_utils.find_an_available_port()
        # self.open_face = OpenFace(open_face_port)

        # self._open_face_socket = zmq.Context().socket(zmq.REQ)
        self.au_data = {}
        self.smile_data = Queue()

        # try:
        #     self._open_face_socket.bind(f"tcp://127.0.0.1:{open_face_port}")
        #     self.is_open_face_socket_connected = True
        # except zmq.ZMQError as e:
        #     self.is_open_face_socket_connected = False
        #     self._logger.error(f"ZMQ Error: {e}")

        self._bow = BoW(
            window_size=__class__.window_size,
            word_size=__class__.word_size,
            n_bins=__class__.n_bins,
        )

    @staticmethod
    def name() -> str:
        return "SYNC_SCORE_GF"

    async def cleanup(self) -> None:
        super().cleanup()
        # self._open_face_socket.close()
        # self.is_open_face_socket_connected = False
        # del self.open_face,
        del self

    async def process_individual_frame(
        self, original: VideoFrame | AudioFrame, ndarray: np.ndarray
    ) -> Any:
        # If ROI is sent from the OpenFace, only send that region
        if "roi" in self.au_data.keys() and self.au_data["roi"]["width"] != 0:
            roi = self.au_data["roi"]
            ndarray = ndarray[
                roi["y"] : (roi["y"] + roi["height"]),
                roi["x"] : (roi["x"] + roi["width"]),
            ]

        # Extract AU from the frame
        exit_code, msg, result = self.au_extractor.extract(ndarray)

        if exit_code == 0:
            self._logger.debug(f"Got results: {result}")
        else:
            self._logger.debug(f"Error [{exit_code}]: {msg}")

        # frame_sent_to_open_face = self.send_frame_to_open_face(ndarray)
        # if not frame_sent_to_open_face:
        #     return None

        # latest_au_data = self.get_open_face_result()

        # if not latest_au_data:
        #     return None

        # self.au_data = latest_au_data

        # self._logger.debug(f"[AU extraction completed] data: {latest_au_data}")

        # # Parse AU data
        # au06_c = latest_au_data.get("presence", {}).get("AU06", "-")
        # au12_r = latest_au_data.get("intensity", {}).get("AU12", "-")

        # if au06_c == "-" or au12_r == "-":
        #     return None

        # smile = au12_r if au06_c == 1 else 0
        # self.smile_data.put(smile)

        # if self.smile_data.qsize() < 2 * __class__.window_size - 1:
        #     return None

        # # Apply BoW algorithm on the AU data
        # latest_smile_data = list(self.smile_data.queue)
        # words_in_bins = self._bow.apply_bow(latest_smile_data, self._bow.derivative)

        # return [words_in_bins, latest_smile_data]

    # def send_frame_to_open_face(self, ndarray: np.ndarray) -> bool:
    #     # If ROI is sent from the OpenFace, only send that region
    #     if "roi" in self.au_data.keys() and self.au_data["roi"]["width"] != 0:
    #         roi = self.au_data["roi"]
    #         ndarray = ndarray[
    #             roi["y"] : (roi["y"] + roi["height"]),
    #             roi["x"] : (roi["x"] + roi["width"]),
    #         ]

    #     if not self.is_open_face_socket_connected:
    #         return False

    #     is_success, image_enc = cv2.imencode(".png", ndarray)

    #     if not is_success:
    #         return False

    #     im_bytes = bytearray(image_enc.tobytes())
    #     im_64 = base64.b64encode(im_bytes)

    #     try:
    #         self._open_face_socket.send(im_64, flags=zmq.NOBLOCK)
    #         self._logger.debug(f"[send_frame_to_open_face] Sent frame: {ndarray.shape}")
    #         return True
    #     except zmq.ZMQError as e:
    #         self._logger.debug(f"[send_frame_to_open_face] error: {e}")
    #         return False

    # def get_open_face_result(self) -> Any:
    #     if self.is_open_face_socket_connected:
    #         try:
    #             data = self._open_face_socket.recv_json(flags=zmq.NOBLOCK)
    #             self._logger.debug(f"[get_open_face_result] Got results: {data}")
    #             return data
    #         except zmq.ZMQError as e:
    #             self._logger.debug(f"[get_open_face_result] error: {e}")
    #             return None

    def align_data(x: list, y: list, base_timeline: list) -> list:
        interpolator = interp1d(x, y, kind="nearest", fill_value="extrapolate")
        return list(interpolator(base_timeline))

    def aggregate(data: list[list[Any]]) -> Any:
        sync_score = oasis(
            word_bins_user1=data[0][0],
            smile_user1=data[0][1],
            word_bins_user2=data[1][0],
            smile_user2=data[1][1],
            window_size=__class__.window_size,
            n_bins=__class__.n_bins,
            energy_threshold=0.1,
        )
        return sync_score
