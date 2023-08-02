import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.open_face_au import OpenFaceAUFilter
from custom_types import util
from typing import TypeGuard
from .bow_dict import BoWDict
from pyts.bag_of_words import BagOfWords
import numpy as np


class BoWFilter(Filter):
    _openface_au_filter: OpenFaceAUFilter | None
    au_data: dict
    bow: BagOfWords

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._openface_au_filter = None
        self.au_data = dict()
        self.group_filter = True

        window_length = 8  # how many frames each window contains
        word_length = 4  # how many symbols each window is mapped to (window_length / word_length is a prositive integer)
        num_bins = 3  # the size of the alphabet or the number of symbols used to represent the time series signal
        self.bow = BagOfWords(
            window_size=window_length,
            word_size=word_length,
            n_bins=num_bins,
            window_step=1,
            numerosity_reduction=False,
            strategy="normal",
        )

    @staticmethod
    def name(self) -> str:
        return "BOW"

    async def complete_setup(self) -> None:
        openface_au_filter_id = self._config["openface_au_filter_id"]
        self._openface_au_filter = self.video_track_handler.filters[
            openface_au_filter_id
        ]

    @staticmethod
    def validate_dict(data) -> TypeGuard[BoWDict]:
        return (
            util.check_valid_typeddict_keys(data, BoWDict)
            and "openface_au_filter_id" in data
            and isinstance(data["openface_au_filter_id"], str)
        )

    async def process(
        self, original: VideoFrame, ndarray: numpy.ndarray
    ) -> numpy.ndarray:
        au06_c = self._openface_au_filter.data.get("presence", {}).get("AU06", "-")
        au12_r = self._openface_au_filter.data.get("intensity", {}).get("AU12", "-")

        if au06_c == "-" or au12_r == "-":
            return ndarray

        smile = au12_r if au06_c == 1 else 0
        self.au_data[original.time] = smile

        if len(self.au_data) < 2 * self.bow.window_size - 1:
            return ndarray

        # Apply BoW algorithm on AU data
        words_in_bins = self.apply_bow(list(self.au_data.values()))

        data = dict(zip(self.au_data.keys(), words_in_bins))

        await self.send_group_filter_message(data)

        return ndarray

    def apply_bow(self, data: np.ndarray):
        # Normalize data
        data = self.normalize_data(data)

        # Apply custom preprocessing on data
        data = self.derivative(data)

        # Transform data into BoW
        bow_list = self.bow.transform([data])

        # Split words into buckets
        bow_list = bow_list[0].split(" ")
        n_buckets = self.bow.window_size // self.bow.window_step
        words_in_buckets = self.split_words_into_buckets(bow_list, n_buckets)

        return words_in_buckets

    def normalize_data(self, data: np.ndarray) -> np.ndarray:
        min_val = np.min(data)
        max_val = np.max(data)
        if min_val == max_val:
            if min_val > 0:
                return data // min_val
            else:
                return data

        data_norm = (data - min_val) / (max_val - min_val)

        return data_norm

    def derivative(self, data: np.ndarray) -> np.ndarray:
        dx = 0.1
        return np.gradient(data, dx)

    def split_words_into_buckets(self, bow_list: list, n_buckets: int) -> list[list]:
        buckets = [[] for _ in range(n_buckets)]
        for i, word in enumerate(bow_list):
            bin = buckets.pop(i % n_buckets)
            bin.append(word)
            buckets.insert(i % n_buckets, bin)
        return buckets
