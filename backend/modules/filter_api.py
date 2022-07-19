"""Provide `FilterAPI` implementation of `FilterAPIInterface`."""

from modules.filter_api_interface import FilterAPIInterface
from modules.user import User


class FilterAPI(FilterAPIInterface):
    """API enabling filters to access data and interact with users / experiments.

    FilterAPI is run on the main process and has direct access to data / functionality
    filters may require.  In case this functionality is required from a subprocess,
    modules.filter_subprocess_api.FilterSubprocessAPI is used.

    Implements modules.filter_api_interface.FilterAPIInterface.

    See Also
    --------
    modules.filter_api_interface.FilterAPIInterface : further documentation.
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
        user : modules.user.User
            User the filter API can access.
        """
        super().__init__()
        self._user = user

    async def experiment_send(self, to: str, data, exclude: str) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        experiment = self._user.get_experiment_or_raise()
        await experiment.send(to, data, exclude, True)


FilterAPIInterface.register(FilterAPI)
