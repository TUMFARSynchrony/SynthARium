import numpy
from av import VideoFrame

from filters.filter import Filter
from filters.open_face_au import OpenFaceAUFilter
from custom_types import util
from typing import TypeGuard
from .bow_dict import BoWDict
from custom_types.message import MessageDict


class BoWFilter(Filter):
    _openface_au_filter: OpenFaceAUFilter | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._openface_au_filter = None
        self.group_filter = True
        self.data = None

    @staticmethod
    def name(self) -> str:
        return "BOW"

    async def complete_setup(self) -> None:
        openface_au_filter_id = self._config["openface_au_filter_id"]
        openface_au_filter = self.video_track_handler.filters[openface_au_filter_id]
        self._openface_au_filter = openface_au_filter

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
        self.data = self._openface_au_filter.data
        await self.send_au_message(original.time, self.data)

        return ndarray

    async def send_au_message(self, time, au_data) -> None:
        filter_api = self.video_track_handler.filter_api
        msg = MessageDict(
            type="GROUP_FILTER",
            data={
                "p": self.video_track_handler.connection._log_name_suffix[2:],
                "time": time,
                "au_data": au_data,
            },
        )
        await filter_api.experiment_send("experimenter", msg, "")
