"""TODO document"""

from abc import ABC, abstractmethod


class FilterAPIInterface(ABC):
    """TODO document"""

    @abstractmethod
    async def send_experiment(self, to: str, data, exclude: str):
        """TODO document"""
        pass
