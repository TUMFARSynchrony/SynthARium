"""TODO document"""

from __future__ import annotations
from abc import ABC, abstractmethod

import modules.connection as _connection


class User(ABC):
    """TODO document"""

    id: str
    connection: _connection.Connection

    def __init__(self):
        """TODO document"""
        pass

    def set_connection(self, connection: _connection.Connection):
        """TODO document"""
        self.connection = connection

    def send(self, data):
        """TODO document"""
        pass

    def disconnect(self):
        """TODO document"""
        pass

    def subscribe_to(self, user: User):
        """TODO document"""
        pass

    def set_muted(self, muted: bool):
        """TODO document"""
        pass

    @abstractmethod
    def handle_message(self, message):
        """TODO document"""
        pass
