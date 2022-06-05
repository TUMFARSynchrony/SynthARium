"""Provide `ConnectionState` class and `parse_connection_state` function."""

from enum import Enum


class ConnectionState(Enum):
    """State a modules.connection.Connection is in.

    The initial state is `NEW`.  When the Connection is started, the state changes to
    `CONNECTING`.  As soon as the connection is stable and a data channel is open, the
    state changes to `CONNECTED`. When the connection is closed, the state is `CLOSED`.

    Should something fail, the state is set to `FAILED`.
    """

    NEW = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSED = 3
    FAILED = 4


def parse_connection_state(state: str) -> ConnectionState:
    """Parse the state of a connection string.

    Parameters
    ----------
    state : str
        State that should be parsed.  Should be: "new", "connecting", "connected",
        "closed" or "failed".

    Returns
    -------
    modules.connection_state.ConnectionState
        Parsed state.

    Raises
    ------
    ValueError
        if `state` is not "new", "connecting", "connected", "closed" or "failed".
    """
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
