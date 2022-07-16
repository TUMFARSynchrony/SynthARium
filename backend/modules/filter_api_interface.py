"""TODO document"""

from abc import ABC, abstractmethod


class FilterAPIInterface(ABC):
    """TODO document"""

    @abstractmethod
    def send_experiment(self, to: str, data, exclude: str):
        """TODO document"""
        pass
