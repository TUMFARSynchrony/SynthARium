import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.open_face_au import OpenFaceAUFilter
from custom_types import util
from typing import Callable, TypeGuard
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
        self.frame = 0

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
        self.frame = self.frame + 1

        au06_c = self._openface_au_filter.data.get("presence", {}).get("AU06", "-")
        au12_r = self._openface_au_filter.data.get("intensity", {}).get("AU12", "-")

        if au06_c == "-" or au12_r == "-":
            return ndarray

        smile = au12_r if au06_c == 1 else 0
        self.au_data[self.frame] = smile

        if len(self.au_data) < 2 * self.bow.window_size - 1:
            return ndarray

        # Apply BoW algorithm on AU data
        words_in_bins = self.apply_bow(list(self.au_data.values()), self.derivative)

        data = {max(list(self.au_data.keys())): words_in_bins}

        await self.send_group_filter_message(data)

        return ndarray

    def apply_bow(self, data: np.ndarray, preprocessing: Callable) -> np.ndarray:
        # Normalize data
        data = self.normalize_data(data)

        # Apply custom preprocessing on data
        data = preprocessing(data)

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

        data_normalized = (data - min_val) / (max_val - min_val)

        return data_normalized

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

    def apply_oasis(
        self,
        word_bins_user1: list[list[str]],
        au_data_user1: list[float],
        word_bins_user2: list[list[str]],
        au_data_user2: list[float],
        window_size: int,
        num_bins: int,
        energy_threshold: float = 0.1,
    ) -> float:
        sync_score_list = list()
        original_bin = word_bins_user1[0]
        for i, word in enumerate(original_bin):
            # Initialize the synchrony score as 0
            sync_score = 0

            # Calculate the signal energy for AU data of both user
            energy_user1 = self.calc_signal_energy(
                i * window_size, window_size, au_data_user1
            )
            energy_user2 = self.calc_signal_energy(
                i * window_size, window_size, au_data_user2
            )
            min_energy = min(energy_user1, energy_user2)

            # Continue only if the minimum signal energy > threshold
            if min_energy > energy_threshold:
                n_buckets = len(word_bins_user2)
                for j, compare_bin in enumerate(word_bins_user2):
                    if i < len(compare_bin):
                        offset_coefficient = 1 - (j / n_buckets)
                        if sync_score >= offset_coefficient:
                            break

                        # Calculate shape similarity
                        compare_word = compare_bin[i]
                        shape_similarity = 1 - self.calc_euclidean_word_distance(
                            word, compare_word, num_bins
                        )

                        # Calculate value similarity
                        energy_user2_with_offset = self.calc_signal_energy(
                            (i * window_size) + j, window_size, au_data_user2
                        )
                        value_similarity = 1 - (
                            abs((energy_user1 - energy_user2_with_offset)) / window_size
                        )

                        # Update synchrony score
                        sync_score = max(
                            sync_score,
                            offset_coefficient * shape_similarity * value_similarity,
                        )

            for _ in range(window_size):
                sync_score_list.append(sync_score)
        return sync_score_list

    def calc_signal_energy(self, pos, window_size, signal):
        sum = 0
        for i in range(window_size):
            if pos + i < len(signal):
                sum += abs(signal[pos + i])
        return sum / window_size

    def calc_euclidean_word_distance(self, word, compare_word, num_bins):
        distance = 0
        for c1, c2 in zip(word, compare_word):
            char_distance = abs(ord(c1) - ord(c2)) / (num_bins - 1)
            distance += char_distance
        return distance / len(word)
