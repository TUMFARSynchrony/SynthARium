import numpy as np
from av import VideoFrame, AudioFrame
from filters.filter_dict import FilterDict
from group_filters import GroupFilter
from typing import Any, Callable
from scipy.interpolate import interp1d


def custom_align_fn(x: list, y: list, **kwargs: dict) -> Callable:
    return interp1d(x, y, **kwargs)


class TemplateGroupFilter(GroupFilter):
    data_len = 8
    min_participants = 2
    align_fn = custom_align_fn
    align_fn_kwargs = {"kind": "nearest", "fill_value": "extrapolate"}

    def __init__(self, config: FilterDict, participant_id: str):
        super().__init__(config, participant_id)

    @staticmethod
    def name() -> str:
        return "TEMPLATE_GF"

    async def process_individual_frame(
        self, original: VideoFrame | AudioFrame, ndarray: np.ndarray
    ) -> Any:
        return ndarray.mean()

    def aggregate(data: list[list[Any]]) -> Any:
        np_data = np.array(data)
        return np_data.mean(axis=0)
