from typing import Any
import numpy as np
from av import VideoFrame, AudioFrame
from filters.filter_dict import FilterDict
from group_filters import GroupFilter
from scipy.interpolate import interp1d

from filters.open_face_au.open_face_au_extractor import OpenFaceAUExtractor
from group_filters.sync_score.bow import BoW
from group_filters.sync_score.oasis import oasis


class SyncScoreGroupFilter(GroupFilter):
    bow_window_size = 8  # how many frames each window contains
    bow_word_size = 4  # how many symbols each window is mapped to (window_length / word_length is a prositive integer)
    bow_n_bins = 3  # the size of the alphabet or the number of symbols used to represent the time series signal
    bow_strategy = "uniform"
    oasis_energy_threshold = 0.1

    data_len_per_participant = 2 * bow_window_size - 1
    num_participants_in_aggregation = 2

    def __init__(self, config: FilterDict, participant_id: str):
        super().__init__(config, participant_id)

        self.au_extractor = OpenFaceAUExtractor()
        self.au_data = {}

    @staticmethod
    def name() -> str:
        return "SYNC_SCORE_GF"

    async def cleanup(self) -> None:
        del self.au_extractor
        await super().cleanup()

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
        exit_code, _, result = self.au_extractor.extract(ndarray)

        if exit_code != 0:
            return None

        self.au_data = result

        # Parse AU data
        au06_c = result.get("presence", {}).get("AU06", "-")
        au12_r = result.get("intensity", {}).get("AU12", "-")

        if au06_c == "-" or au12_r == "-":
            return None

        smile = au12_r if au06_c == 1 else 0

        return smile

    def align_data(x: list, y: list, base_timeline: list) -> list:
        interpolator = interp1d(x, y, kind="nearest", fill_value="extrapolate")
        return list(interpolator(base_timeline))

    def aggregate(data: list[list[Any]]) -> Any:
        def normalize_data(data: np.ndarray) -> np.ndarray:
            min_val = np.min(data)
            max_val = np.max(data)
            if min_val == max_val:
                if min_val > 0:
                    return data // min_val
                else:
                    return data

            data_normalized = (data - min_val) / (max_val - min_val)

            return data_normalized

        # Normalize data
        normalized_data1 = normalize_data(data[0])
        normalized_data2 = normalize_data(data[1])

        # Apply BoW algorithm on the AU data
        bow = BoW(
            window_size=__class__.bow_window_size,
            word_size=__class__.bow_word_size,
            n_bins=__class__.bow_n_bins,
            strategy=__class__.bow_strategy,
        )

        bow1, bow2 = bow.apply_bow_for_2_participants(
            normalized_data1, normalized_data2
        )

        # Apply OASIS algorithm for user1->user2 and user2->user1 and take the average
        sync_score_u1u2 = oasis(
            word_user1=bow1[0][0],
            smile_user1=normalized_data1,
            word_bins_user2=bow2,
            smile_user2=normalized_data2,
            window_size=__class__.bow_window_size,
            n_bins=__class__.bow_n_bins,
            energy_threshold=__class__.oasis_energy_threshold,
        )

        sync_score_u2u1 = oasis(
            word_user1=bow2[0][0],
            smile_user1=normalized_data2,
            word_bins_user2=bow1,
            smile_user2=normalized_data1,
            window_size=__class__.bow_window_size,
            n_bins=__class__.bow_n_bins,
            energy_threshold=__class__.oasis_energy_threshold,
        )

        return (sync_score_u1u2 + sync_score_u2u1) / 2.0
