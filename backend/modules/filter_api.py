"""TODO document"""


from modules.filter_api_interface import FilterAPIInterface
from modules.user import User


class FilterAPI(FilterAPIInterface):
    """TODO document"""

    _user: User

    def __init__(self, user: User) -> None:
        super().__init__()
        self._user = user

    async def send_experiment(self, to: str, data, exclude: str) -> None:
        """TODO document"""
        experiment = self._user.get_experiment_or_raise()
        await experiment.send(to, data, exclude, True)
