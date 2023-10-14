import numpy

from typing import Callable
from pyts.bag_of_words import BagOfWords
import numpy as np


class BoW:
    _bow: BagOfWords

    def __init__(self, window_size: int, word_size: int, n_bins: int):
        self._bow = BagOfWords(
            window_size=window_size,
            word_size=word_size,
            n_bins=n_bins,
            window_step=1,
            numerosity_reduction=False,
            strategy="normal",
        )

    def apply_bow(self, data: np.ndarray, preprocessing: Callable) -> np.ndarray:
        # Normalize data
        data = self.normalize_data(data)

        # Apply custom preprocessing on data
        data = preprocessing(data)

        # Transform data into BoW
        bow_list = self._bow.transform([data])

        # Split words into buckets
        bow_list = bow_list[0].split(" ")
        n_buckets = self._bow.window_size // self._bow.window_step
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
