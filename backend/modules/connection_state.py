"""Provide `ConnectionState` class and `parse_connection_state` function."""

from enum import Enum


class ConnectionState(Enum):
    """TODO document"""

    NEW = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSED = 3
    FAILED = 4


def parse_connection_state(state) -> ConnectionState:
    """TODO document"""
    match state:
        case "new":
            return ConnectionState.NEW
        case "connecting":
            return ConnectionState.CONNECTING
        case "connected":
            return ConnectionState.CONNECTED
        case "closed":
            return ConnectionState.CLOSED
        case "failed":
            return ConnectionState.FAILED
        case _:
            print("Failed to parse connection state: Unknown state:", state)
            raise ValueError(f"Unknown connection state: {state}.")
