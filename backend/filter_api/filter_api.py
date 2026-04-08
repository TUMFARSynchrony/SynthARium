"""Provide `FilterAPI` implementation of `FilterAPIInterface`."""
from __future__ import annotations

from typing import TYPE_CHECKING

from filter_api.filter_api_interface import FilterAPIInterface

if TYPE_CHECKING:
    from users.user import User


class FilterAPI(FilterAPIInterface):
    """API enabling filters to access data and interact with users / experiments.

    FilterAPI is run on the main process and has direct access to data / functionality
    filters may require.  In case this functionality is required from a subprocess,
    hub.filter_subprocess_api.FilterSubprocessAPI is used.

    Implements hub.filter_api_interface.FilterAPIInterface.

    See Also
    --------
    hub.filter_api_interface.FilterAPIInterface : further documentation.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Backend-Architecture
        Architecture UML Diagram.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Filters
        Details about the filters, including Filter API section
    """

    _user: User

    def __init__(self, user: User) -> None:
        """Initiate new FilterAPI.

        Parameters
        ----------
        user : hub.user.User
            User the filter API can access.
        """
        super().__init__()
        self._user = user

    async def experiment_send(self, to: str, data, exclude: str) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        experiment = self._user.get_experiment_or_raise()
        await experiment.send(to, data, exclude, True)

    async def get_current_ping(self) -> int:
        # For docstring see FilterAPIInterface or hover over function declaration
        return await self._user.get_current_ping()

    async def start_pinging(
        self,
        period: int,
        buffer_length: int
    ) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        await self._user.start_pinging(period, buffer_length)

    def stop_pinging(self) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        self._user.stop_pinging()


FilterAPIInterface.register(FilterAPI)
