"""provide `FilterSubprocessReceiver` class."""

import logging
from hub.exceptions import ErrorDictException
from filter_api.filter_api import FilterAPI


class FilterSubprocessReceiver:
    """Receive commands for the FilterAPI from a FilterSubprocessAPI.

    When a hub.filter_subprocess_api.FilterSubprocessAPI wants to execute an API call
    , it sends a command to a FilterSubprocessReceiver running on the main process.
    The FilterSubprocessReceiver then forwards the request to a
    hub.filter_api.FilterAPI.

    See Also
    --------
    hub.filter_subprocess_api.FilterSubprocessAPI :
        FilterSubprocessAPI sending the commands handled by FilterSubprocessReceiver.
    hub.filter_api_interface.FilterAPIInterface : Filter API documentation.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Backend-Architecture
        Architecture UML Diagram.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Filters
        Details about the filters, including Filter API section
    """

    _filter_api: FilterAPI
    _logger: logging.Logger

    def __init__(self, filter_api: FilterAPI) -> None:
        """Initialize new FilterSubprocessReceiver.

        Parameters
        ----------
        filter_api : filter_api.filter_api.FilterAPI
            FilterAPI requests from hub.filter_subprocess_api.FilterSubprocessAPI
            will be forwarded to.
        """
        self._filter_api = filter_api
        self._logger = logging.getLogger("FilterSubprocessReceiver")

    async def handle(self, message: dict):
        """Handle a incoming message from a subprocess FilterSubprocessAPI.

        Parameters
        ----------
        message : dict
            Message send by hub.filter_subprocess_api.FilterSubprocessAPI.  There
            are no guarantees about its content, but the intended content is `command`
            and `data`.
        """
        command = message.get("command")
        data = message.get("data")

        if command is None or data is None:
            self._logger.error(f"Missing command or data in message: {message}")
            return

        match command:
            case "EXPERIMENT_SEND":
                try:
                    await self._filter_api.experiment_send(
                        data["to"], data["data"], data["exclude"]
                    )
                except ErrorDictException as e:
                    self._logger.error(f"Failed experiment_send: {e}")
            case _:
                self._logger.warning(f'Unknown command: "{command}"')
