"""Provide `FilterSubprocessAPI` implementation of `FilterAPIInterface`."""

from typing import Callable
from filter_api.filter_api_interface import FilterAPIInterface


class FilterSubprocessAPI(FilterAPIInterface):
    """API enabling filters to access and interact with data on the main process.

    Implements hub.filter_api_interface.FilterAPIInterface

    FilterSubprocessAPI is run on a subprocess and does not have direct access to data
    / functionality filters may require.  To access that data / functionality, it sends
    commands to a hub.filter_subprocess_receiver.FilterSubprocessReceiver on the
    main process.  Sending the commands is  donne using `_relay_command`, which is
    intended to be the `_send_command` function in
    hub.connection_runner.ConnectionRunner.

    Implements hub.filter_api_interface.FilterAPIInterface.

    See Also
    --------
    hub.filter_api_interface.FilterAPIInterface : further documentation.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Backend-Architecture
        Architecture UML Diagram.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Filters
        Details about the filters, including Filter API section
    """

    _relay_command: Callable
    _relay_command_with_response: Callable

    def __init__(
        self,
        relay_command: Callable,
        relay_command_with_response: Callable
    ) -> None:
        """Initialize new FilterSubprocessAPI.

        Parameters
        ----------
        relay_command : Callable
            Relay function to send data to
            hub.filter_subprocess_receiver.FilterSubprocessReceiver on the main
            process.
        relay_command_with_response : Callable
            Relay function to send data to
            hub.filter_subprocess_receiver.FilterSubprocessReceiver on the main
            process. Waits for a response and returns it.
        """
        super().__init__()
        self._relay_command = relay_command
        self._relay_command_with_response = relay_command_with_response

    async def experiment_send(self, to: str, data, exclude: str) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        self._send_command(
            "EXPERIMENT_SEND", {"to": to, "data": data, "exclude": exclude}
        )

    async def get_current_ping(self) -> int:
        # For docstring see FilterAPIInterface or hover over function declaration
        answer = await self._send_command_wait_for_response(
            "GET_CURRENT_PING",
            {}
        )
        return answer["ping"] if answer is not None else 0

    async def start_pinging(self) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        self._send_command("START_PINGING", {})
    
    def stop_pinging(self) -> None:
        # For docstring see FilterAPIInterface or hover over function declaration
        self._send_command("STOP_PINGING", {})

    def _send_command(self, command: str, data) -> None:
        """Send a command to FilterSubprocessReceiver oin the main process.

        Parameters
        ----------
        command : str
            Command identifier used to identify the command in
            hub.filter_subprocess_receiver.FilterSubprocessReceiver.
        data : anything json serializable
            Data associated with the command.

        See Also
        --------
        hub.filter_subprocess_receiver.FilterSubprocessReceiver
            Handle commands on the main process.  Each command send should have a
            handler in hub.filter_subprocess_receiver.FilterSubprocessReceiver.
        """
        self._relay_command("FILTER_API", {"command": command, "data": data})

    async def _send_command_wait_for_response(
        self,
        command: str,
        data
    ) -> dict | None:
        """Send a command to FilterSubprocessReceiver on the main process and wait for a response.

        Parameters
        ----------
        command : str
            Command identifier used to identify the command in
            hub.filter_subprocess_receiver.FilterSubprocessReceiver.
        data : anything json serializable
            Data associated with the command.

        See Also
        --------
        hub.filter_subprocess_receiver.FilterSubprocessReceiver
            Handle commands on the main process.  Each command send should have a
            handler in hub.filter_subprocess_receiver.FilterSubprocessReceiver.
        """
        return await self._relay_command_with_response(
            "FILTER_API",
            {"command": command, "data": data}
        )


FilterAPIInterface.register(FilterSubprocessAPI)
