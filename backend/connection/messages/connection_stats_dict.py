from typing import TypedDict

from custom_types.fps_data import FPSDataDict


class ConnectionStatsDict(TypedDict):
    """TypedDict for sending a `CONNECTION_STATS` message to the client.

    Attributes
    ----------
    avg_fps_list : str
        data of average fps over time.

    """

    avg_fps_list: list[FPSDataDict]
