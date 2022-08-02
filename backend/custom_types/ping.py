"""Provides `PongDict` TypedDict for `PONG` messages."""

from typing import Any, TypedDict


class PongDict(TypedDict):
    """TypedDict for `PONG` messages sent as a response to `PING`.

    Attributes
    ----------
    server_time : int
        Server timestamp when message was handled.
    ping_data : Any
        Data from original `PING` message
    """

    server_time: int
    ping_data: Any
