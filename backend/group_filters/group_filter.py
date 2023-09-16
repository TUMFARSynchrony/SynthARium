"""Provide abstract `GroupFilter` class."""

from __future__ import annotations

import numpy
import zmq
import zmq.asyncio
from typing import TypeGuard
from abc import ABC, abstractmethod
from av import VideoFrame, AudioFrame

from custom_types import util
from filters.filter_dict import FilterDict
import logging
from scipy import interpolate
from typing import Any


class GroupFilter(ABC):
    """Abstract base class for all group filters.

    Attributes
    ----------
    config
    """

    _config: FilterDict
    _logger: logging.Logger
    is_socket_connected: bool
    _socket: zmq.Socket | None

    data_len: int = 0
    min_participants: int = 2
    align_fn: interpolate = interpolate.interp1d
    align_fn_kwargs: dict = {}

    def __init__(self, config: FilterDict, participant_id: str) -> None:
        """Initialize new Group Filter.

        Parameters
        ----------
        config : custom_types.filter.FilterDict
            Configuration for filter.  `config["type"]` must match the filter
            implementation.

        Notes
        -----
        If other filters need to be accessed or the initiation contains an asynchronous
        part, use `complete_setup`. The other filters may not be initialized when
        __init__ is called. However, filters must be ready to be accessed by other
        filters after __init__ (if they are designed to be).
        """
        self._logger = logging.getLogger(
            f"{config['type']}-GroupFilter-P-{participant_id}"
        )
        self._config = config
        self.participant_id = participant_id
        self.is_socket_connected = False
        self._socket = None

    @property
    def config(self) -> FilterDict:
        """Get Group Filter config."""
        return self._config

    def set_config(self, config: FilterDict) -> None:
        """Update filter config.

        Notes
        -----
        Provide a custom implementation for this function in a subclass in case the
        group filter should react to config changes.
        """
        self._config = config

    def connect_aggregator(self, port: int) -> None:
        self._socket = zmq.asyncio.Context().socket(zmq.PUSH)
        try:
            self._socket.connect(f"tcp://127.0.0.1:{port}")
            self.is_socket_connected = True
        except zmq.ZMQError as e:
            self._logger.error(f"ZMQ Error: {e}")

    async def complete_setup(self) -> None:
        """Complete setup, allowing for asynchronous setup and accessing other filters.

        If the initiation / setup of a filter requires anything asynchronous or other
        filters must be accessed, it should be donne in `complete_setup`.
        `complete_setup` is called when all filters have been set up, therefore other
        filters will be available (may not be the case in __init__, depending on the
        position in the filter pipeline).
        """
        return

    async def cleanup(self) -> None:
        """Cleanup, in case filter will no longer be used.

        Called before the filter is deleted.  In case the filter spawned any
        asyncio.Task tasks they should be stopped & awaited in a custom implementation
        overriding this function.
        """
        self._socket.close()
        self.is_socket_connected = False
        del self

    @staticmethod
    def validate_dict(data) -> TypeGuard[FilterDict]:
        return util.check_valid_typeddict_keys(data, FilterDict)

    def __repr__(self) -> str:
        """Get string representation for this group filter."""
        return f"{self.__class__.__name__}(config={self.config})"

    async def process_individual_frame_and_send_data_to_aggregator(
        self, original: VideoFrame | AudioFrame, ndarray: numpy.ndarray, ts: int
    ) -> None:
        data = await self.process_individual_frame(original, ndarray)
        if self.is_socket_connected:
            message = dict()
            message["participant_id"] = self.participant_id
            message["time"] = ts
            message["data"] = data
            self._socket.send_json(message, flags=zmq.NOBLOCK)

            self._logger.debug(f"Data sent for {self.participant_id}: {message}")

    @staticmethod
    @abstractmethod
    def name() -> str:
        """Provide name of the filter.

        The given name must be unique among all filters.
        The given name is used as the unique ID for communicating the active filters
        between frontend and backend.
        """
        raise NotImplementedError(
            f"{__name__} is missing it's implementation of the static abstract name()"
            " method."
        )

    @abstractmethod
    async def process_individual_frame(
        self, original: VideoFrame | AudioFrame, ndarray: numpy.ndarray
    ) -> dict:
        raise NotImplementedError(
            f"{self} is missing it's implementation of the abstract"
            " `process_individual_frame` method."
        )

    @staticmethod
    @abstractmethod
    def aggregate(data: list[list[Any]]) -> Any:
        raise NotImplementedError(
            f"{__name__} is missing it's implementation of the static"
            " abstract `aggregate` method."
        )
