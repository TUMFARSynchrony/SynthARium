"""Provides `PongDict` TypedDict for `PONG` messages."""

from typing import Any, TypedDict


class PongDict(TypedDict):
    """TypedDict for `PONG` messages sent as a response to `PING`.

    Attributes
    ----------
    handled_time : int
        Server timestamp when message was handled.
    ping_data : Any
        Data from original `PING` message
    """

    handled_time: int
    ping_data: Any


class PingDict(TypedDict):
    """TypedDict for `PING` messages

    Attributes
    ----------
    sent : int
        Server timestamp when ping was sent.
    data : Any
        Any additional data to be sent back with `PONG` message.
    """

    sent: int
    data: Any
