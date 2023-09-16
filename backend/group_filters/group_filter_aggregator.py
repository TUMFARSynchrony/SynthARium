"""Provide GroupFilterHandler for handling group filters."""

from typing import Literal
import logging
from group_filters import GroupFilter
import zmq
import zmq.asyncio
from queue import Queue
from itertools import combinations
from typing import Any


class GroupFilterAggregator(object):
    """Handles audio and video group filters aggregation step."""

    _logger: logging.Logger
    _socket: zmq.Socket
    is_socket_connected: bool
    _kind: Literal["video", "audio"]
    _group_filter: GroupFilter
    _data: dict[str, Queue[tuple[float, Any]]]

    def __init__(
        self, kind: Literal["video", "audio"], group_filter: GroupFilter, port: int
    ) -> None:
        super().__init__()
        self._logger = logging.getLogger(
            f"{group_filter.name()}-GroupFilterAggregator-Port-{port}"
        )
        ctx = zmq.asyncio.Context()
        self._socket = ctx.socket(zmq.PULL)
        self._kind = kind
        self._group_filter = group_filter
        self._data = {}

        try:
            self._socket.bind(f"tcp://127.0.0.1:{port}")
            self.is_socket_connected = True
        except zmq.ZMQError as e:
            self.is_socket_connected = False
            self._logger.error(f"ZMQ Error: {e}")

    def __repr__(self) -> str:
        return f"Group filter aggregator for {self._group_filter.name()}"

    async def cleanup(self) -> None:
        self._socket.close()
        self.is_socket_connected = False
        self.delete_data()
        del self

    def delete_data(self) -> None:
        self._data = {}

    def add_data(self, participant_id: str, time: float, data: Any) -> None:
        q = self._data.get(participant_id, Queue(maxsize=self._group_filter.data_len))

        if q.full():
            q.get()
        q.put((time, data))

        self._data[participant_id] = q

    async def run(self) -> None:
        while True:
            if self.is_socket_connected:
                message = await self._socket.recv_json()

                self.add_data(
                    message["participant_id"], message["time"], message["data"]
                )
                self._logger.debug(
                    f"Data added for {message['participant_id']}: {message},"
                    + f" # of data: {[(k, v.qsize()) for k, v in self._data.items()]}"
                )

                if len(self._data) >= self._group_filter.min_participants:
                    for c in combinations(
                        self._data.keys(), self._group_filter.min_participants
                    ):
                        # Check if all participants have enough data to align
                        participants_have_enough_data = True
                        for pid in c:
                            if (
                                self._group_filter.data_len != 0
                                and self._data[pid].qsize()
                                != self._group_filter.data_len
                            ):
                                participants_have_enough_data = False
                                break

                        if participants_have_enough_data:
                            # Align data
                            data = self.align_data(c)

                            # Aggregate data
                            aggregated_data = self._group_filter.aggregate(data)
                            self._logger.debug(
                                "Data aggregation is triggered by participant"
                                + f" {message['participant_id']}: {message}"
                                + f" with data: {data},"
                                + f" aggregation result: {aggregated_data}"
                            )

    def align_data(self, participant_ids: tuple) -> list[list[Any]]:
        data = {}
        for pid in participant_ids:
            data[pid] = list(self._data[pid].queue)

        # Use the first participant's time horizon as the basis for alignment
        p0_x, p0_y = zip(*data[participant_ids[0]])
        aligned_data = [list(p0_y)]

        # Align the data for each participant
        for pid in participant_ids[1:]:
            x, y = zip(*data[pid])

            # Interpolate the data
            interpolator = self._group_filter.align_fn(
                x, y, **self._group_filter.align_fn_kwargs
            )
            y_aligned = list(interpolator(p0_x))

            # Store the aligned data
            aligned_data.append(y_aligned)

        return aligned_data
