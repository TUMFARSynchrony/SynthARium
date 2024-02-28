"""Provide the abstract `FilterAPIInterface`."""

from abc import ABC, abstractmethod


class FilterAPIInterface(ABC):
    """Abstract interface filter APIs.

    The filter API is intended to provide filters with access to data and functionality
    that may not be available on the same process, in case subprocesses are enabled.
    For this purpose, FilterAPIInterface provides an interface independent of the
    process the filter and data/function a filter may want to access is on.

    Notes
    -----
    Do not instantiate directly, use subclasses / implementations of
    `FilterAPIInterface` instead.

    When a filter requires additional data or access to functionality outside of the
    subprocesses part of the hub, the filter API should be extended.  In theory, the API
    could get access to all parts of the program, e.g. by adding access to the hub to
    hub.filter_api.FilterAPI.

    When adding a function to the filter API, it should be defined in
    hub.filter_api_interface.FilterAPIInterface and implemented in
    hub.filter_api.FilterAPI as well as
    hub.filter_subprocess_api.FilterSubprocessAPI.

    See Also
    --------
    hub.filter_api.FilterAPI
    hub.filter_subprocess_api.FilterSubprocessAPI
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Backend-Architecture
        Architecture UML Diagram.
    https://github.com/TUMFARSynchrony/experimental-hub/wiki/Filters
        Details about the filters, including Filter API section
    """

    @abstractmethod
    async def experiment_send(self, to: str, data, exclude: str) -> None:
        """Send data using the send method in hub.experiment.Experiment.

        See hub.experiment.Experiment `send()` for parameter documentation.
        `secure_origin` is set to True.

        Raises
        ------
        ErrorDictException
            If the user is not connected to an experiment (only for FilterAPI,
            FilterSubprocessAPI currently only logs the error).
        """
        pass

    @abstractmethod
    async def get_current_ping(self) -> int:
        """Get the current API ping in milliseconds.
        """
        pass

    @abstractmethod
    async def start_pinging(
        self,
        period: int,
        buffer_length: int
    ) -> None:
        """Start sending ping messages to the frontend.

        Parameters
        ----------
        period : int, optional
            The period at which to send ping messages, in milliseconds.
        buffer_length : int, optional
            The length of the ping buffer, in seconds.
        """
        pass

    @abstractmethod
    def stop_pinging(self) -> None:
        """Stop sending ping messages to the frontend.
        """
        pass
