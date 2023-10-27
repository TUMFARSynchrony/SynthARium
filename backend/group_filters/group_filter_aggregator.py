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
import numpy as np
from time import time


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

    def add_data(self, participant_id: str, t: float, data: Any) -> None:
        q = self._data.get(
            participant_id, Queue(maxsize=self._group_filter.data_len_per_participant)
        )

        if q.full():
            q.get()
        q.put((t, data))

        self._data[participant_id] = q

        self._logger.debug(
            f"Data added for {participant_id} at {time()}: ({t}, {data}),"
            + f" # of data: {[(k, v.qsize()) for k, v in self._data.items()]}"
        )

    async def run(self) -> None:
        aggregation_history = {}
        while True:
            if self.is_socket_connected:
                try:
                    message = self._socket.recv_json()

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

                            # Take snapshot from the data queues
                            c_data = {}
                            for pid in c:
                                c_data[pid] = list(self._data[pid].queue)

                            # Check if all participant's data is recently updated
                            participants_data_updated_recently = True
                            latest_aggregated_data = aggregation_history.get(c, None)
                            if latest_aggregated_data is not None:
                                for pid in c:
                                    if np.array_equal(
                                        latest_aggregated_data[pid], c_data[pid]
                                    ):
                                        participants_data_updated_recently = False
                                        break

                            if not participants_data_updated_recently:
                                continue

                            # Align data
                            data, debug_str = self.align_data(c, c_data)

                            # Skip if the alignment cannot be performed because there is no overlapping time horizon among participants
                            if data is None:
                                continue

                            # Aggregate data
                            aggregated_data = self._group_filter.aggregate(data)

                            # Update aggregation history
                            aggregation_history[c] = c_data

                            self._logger.debug(
                                debug_str
                                + "\n"
                                + "\n\tData aggregation performed."
                                + f"\n\tTime: {time()}"
                                + f"\n\tData: {data}"
                                + f"\n\tResult: {aggregated_data}"
                            )
                except asyncio.CancelledError:
                    # If the task is cancelled, break the loop and stop execution
                    break
                except Exception as e:
                    self._logger.debug(
                        f"Exception: {e} | Data aggregation cannot be performed."
                    )

    def align_data(
        self, participant_ids: tuple[str], data: dict[str, list[float]]
    ) -> list[list[Any]] | None:
        # Calculate the base time horizon as the intersection: max of time horizon starts - min of time horizon ends
        base_time_horizon_start = data[participant_ids[0]][0][0]
        base_time_horizon_end = data[participant_ids[0]][-1][0]
        for pid in participant_ids[1:]:
            th_start = data[pid][0][0]
            if th_start > base_time_horizon_start:
                base_time_horizon_start = th_start

            th_end = data[pid][-1][0]
            if th_end < base_time_horizon_end:
                base_time_horizon_end = th_end

        # Return None if the start of base time horizon is greater than its end to prevent aggregation
        if base_time_horizon_start > base_time_horizon_end:
            return None

        base_time_horizon = list(
            np.linspace(
                base_time_horizon_start,
                base_time_horizon_end,
                self._group_filter.data_len_per_participant,
            )
        )

        debug_str = (
            f"Data alignment performed with base time horizon: {base_time_horizon}"
        )

        # Align the data for other participants
        aligned_data = []
        for pid in participant_ids:
            x, y = map(list, zip(*data[pid]))

            # Align the data
            y_aligned = self._group_filter.align_data(x, y, base_time_horizon)

            # Store the aligned data
            aligned_data.append(y_aligned)

            debug_str += (
                "\n"
                + f"\n\tParticipant: {pid}"
                + f"\n\tTime Horizon: {x}"
                + f"\n\tData: {y}"
                + f"\n\tAligned Data: {y_aligned}"
            )

        return aligned_data, debug_str
