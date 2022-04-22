"""TODO document"""

from typing import Callable
from aiortc import RTCDataChannel


class Connection():
    """TODO document"""
    dc: RTCDataChannel
    message_handler: Callable[[], ]

    def send(self, data):
        """TODO document"""
        pass
