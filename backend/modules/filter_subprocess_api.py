"""TODO document"""


from typing import Callable
from modules.filter_api_interface import FilterAPIInterface


class FilterSubprocessAPI(FilterAPIInterface):
    """TODO document"""

    _relay_command: Callable

    def __init__(self, relay_command: Callable) -> None:
        """TODO document"""
        super().__init__()
        self._relay_command = relay_command

    async def send_experiment(self, to: str, data, exclude: str) -> None:
        """TODO document"""
        self._send_command(
            "SEND_EXPERIMENT", {"to": to, "data": data, "exclude": exclude}
        )

    def _send_command(self, command: str, data) -> None:
        """TODO document"""
        self._relay_command("FILTER_API", {"command": command, "data": data})
