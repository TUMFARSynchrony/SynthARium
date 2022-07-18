"""provide `FilterSubprocessReceiver` class."""

from modules.filter_api import FilterAPI


class FilterSubprocessReceiver:
    """Receive commands for the FilterAPI from a FilterSubprocessAPI.

    When a modules.filter_subprocess_api.FilterSubprocessAPI wants to execute a API call
    , it sends a command to a FilterSubprocessReceiver running on the main process.
    The FilterSubprocessReceiver then forwards the request to a
    modules.filter_api.FilterAPI.

    See Also
    --------
    modules.filter_subprocess_api.FilterSubprocessAPI :
        FilterSubprocessAPI sending the commands handled by FilterSubprocessReceiver.
    modules.filter_api_interface.FilterAPIInterface : Filter API documentation.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Backend-Architecture
        Architecture UML Diagram.
    """

    _filter_api: FilterAPI

    def __init__(self, filter_api: FilterAPI) -> None:
        """Initialize new FilterSubprocessReceiver.

        Parameters
        ----------
        filter_api : modules.filter_api.FilterAPI
            FilterAPI requests from modules.filter_subprocess_api.FilterSubprocessAPI
            will be forwarded to.
        """
        self._filter_api = filter_api

    async def handle(self, message: dict):
        """Handle a incoming message from a subprocess FilterSubprocessAPI.

        Parameters
        ----------
        message : dict
            Message send by modules.filter_subprocess_api.FilterSubprocessAPI.  There
            are no guarantees about its content, but the intended content is `command`
            and `data`.
        """
        command = message.get("command")
        data = message.get("data")

        if command is None or data is None:
            # TODO handle
            return

        match command:
            case "EXPERIMENT_SEND":
                # TODO handle exception
                await self._filter_api.experiment_send(
                    data["to"], data["data"], data["exclude"]
                )
            case _:
                # TODO handle unknown command
                pass
