"""Provide GroupFilterHandler for handling group filters."""

import asyncio
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
    _task: asyncio.Task
    _context: zmq.Context
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
        self._context = zmq.asyncio.Context.instance()
        self._socket = self._context.socket(zmq.PULL)
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

    def set_task(self, task: asyncio.Task) -> None:
        self._task = task

    async def cleanup(self) -> None:
        self.is_socket_connected = False
        self.delete_data()
        self._context.destroy()
        self._task.cancel()

    def delete_data(self) -> None:
        self._data = {}

    def add_data(self, participant_id: str, time: float, data: Any) -> None:
        q = self._data.get(
            participant_id, Queue(maxsize=self._group_filter.data_len_per_participant)
        )

        if q.full():
            q.get()
        q.put((time, data))

        self._data[participant_id] = q

        self._logger.debug(
            f"Data added for {participant_id} at {time}: {data},"
            + f" # of data: {[(k, v.qsize()) for k, v in self._data.items()]}"
        )

    async def run(self) -> None:
        while True:
            if self.is_socket_connected:
                try:
                    message = await self._socket.recv_json()

                    self.add_data(
                        message["participant_id"], message["time"], message["data"]
                    )

                    num_participants_in_aggregation = None
                    if self._group_filter.num_participants_in_aggregation == "all":
                        num_participants_in_aggregation = len(self._data)
                    else:
                        num_participants_in_aggregation = (
                            self._group_filter.num_participants_in_aggregation
                        )

                    if len(self._data) >= num_participants_in_aggregation:
                        for c in combinations(
                            self._data.keys(), num_participants_in_aggregation
                        ):
                            # Check if all participants have enough data
                            participants_have_enough_data = True
                            if self._group_filter.data_len_per_participant != 0:
                                for pid in c:
                                    if (
                                        self._data[pid].qsize()
                                        != self._group_filter.data_len_per_participant
                                    ):
                                        participants_have_enough_data = False
                                        break

                            if not participants_have_enough_data:
                                continue

                            # Align data
                            data = self.align_data(c)

                            # Aggregate data
                            aggregated_data = self._group_filter.aggregate(data)
                            self._logger.debug(
                                "Data aggregation performed."
                                + f"\n\tData: {data}"
                                + f"\n\tResult: {aggregated_data}"
                            )
                except Exception as e:
                    self._logger.debug(
                        f"Exception: {e} | Data aggregation cannot be performed."
                    )
                except asyncio.CancelledError:
                    # If the task is cancelled, break the loop and stop execution
                    break

    def align_data(self, participant_ids: tuple) -> list[list[Any]]:
        data = {}
        for pid in participant_ids:
            data[pid] = list(self._data[pid].queue)

        # Find the participant with the smallest time horizon
        def time_horizon(q):
            return q[-1][0] - q[0][0]

        min_time_horizon = time_horizon(data[participant_ids[0]])
        pid_with_min_time_horizon = 0
        for pid in participant_ids[1:]:
            th = time_horizon(data[pid])
            if th < min_time_horizon:
                min_time_horizon = th
                pid_with_min_time_horizon = pid

        # Use the time horizon of the participant with the smallest time horizon as the basis for alignment
        p0_x, p0_y = map(list, zip(*data[pid_with_min_time_horizon]))
        p0_y = [float(y) for y in p0_y]
        aligned_data = [p0_y]

        debug_str = (
            "Data alignment performed."
            + f"\n\tParticipant: {pid_with_min_time_horizon}"
            + f"\n\tBase Time Horizon: {p0_x}"
            + f"\n\tData: {p0_y}"
        )

        # Align the data for other participants
        for pid in participant_ids:
            if pid == pid_with_min_time_horizon:
                continue

            x, y = map(list, zip(*data[pid]))

            # Align the data
            y_aligned = self._group_filter.align_data(x, y, p0_x)

            # Store the aligned data
            aligned_data.append(y_aligned)

            debug_str += (
                "\n"
                + f"\n\tParticipant: {pid}"
                + f"\n\tTime Horizon: {x}"
                + f"\n\tData: {y}"
                + f"\n\tAligned Data: {y_aligned}"
            )

        self._logger.debug(debug_str)

        return aligned_data
