"""Provide the abstract `User` class.

See Also
--------
modules.participant.Participant : Participant implementation of User.
modules.experimenter.Experimenter : Experimenter implementation of User.
"""

from __future__ import annotations
from abc import ABC
from typing import Callable, Any, Coroutine

from custom_types.message import MessageDict
from custom_types.error import ErrorDict
from modules.exceptions import ErrorDictException
import modules.connection as _connection


class User(ABC):
    """User class representing a connected client.

    Provides message handling logic for child classes.

    Attributes
    ----------
    id : str
        ID of this User.

    Methods
    -------
    on(endpoint, handler)
        Register an `handler` function for incoming messages with type `endpoint`.
    handle_message(message)
        Handle incoming message from client.
    set_connection(connection)
        Set the connection of this user.
    send(message)
        Send a custom_types.message.MessageDict to the connected client.
    disconnect()
        Closes the connection with the client.
    subscribe_to()
        TODO WIP document when implemented
    set_muted()
        TODO WIP document when implemented

    See Also
    --------
    modules.participant.Participant : Participant implementation of User.
    modules.experimenter.Experimenter : Experimenter implementation of User.
    """

    id: str
    _connection: _connection.Connection
    _handlers: dict[str, list[Callable[[Any], Coroutine[Any, Any, MessageDict | None]]]]

    def __init__(self, id: str):
        """Instantiate new User base class.

        Should only be called by child classes.

        Parameters
        ----------
        id : str
            Unique identifier for this Experimenter.
        """
        self.id = id
        self._handlers = {}

    def set_connection(self, connection: _connection.Connection):
        """Set the connection of this user.

        This should only be used once before using this User.  See factory functions.

        See Also
        --------
        modules.participant.Participant : Participant implementation of User.
        modules.experimenter.Experimenter : Experimenter implementation of User.
        """
        self._connection = connection

    def send(self, message: MessageDict):
        """Send a custom_types.message.MessageDict to the connected client.

        Parameters
        ----------
        message : custom_types.message.MessageDict
            Message for the client.
        """
        self._connection.send(message)

    async def disconnect(self):
        """Disconnect.  Closes the connection with the client."""
        await self._connection.stop()

    def subscribe_to(self, user: User):
        """TODO document when implemented."""
        pass

    def set_muted(self, muted: bool):
        """TODO document when implemented."""
        pass

    def on(
        self,
        endpoint: str,
        handler: Callable[[Any], Coroutine[Any, Any, MessageDict | None]],
    ) -> None:
        """Register an `handler` function for incoming messages with type `endpoint`.

        Parameters
        ----------
        endpoint : str
            Endpoint for `handler`.  When a message with type `endpoint` is received,
            `handler` will be called.
        handler : function(data: Any) -> custom_types.message.MessageDict
            Function that handles incoming data for Messages with type `endpoint`.
        """
        if endpoint in self._handlers.keys():
            self._handlers[endpoint].append(handler)
        else:
            self._handlers[endpoint] = [handler]

    async def handle_message(self, message: MessageDict | Any) -> None:
        """Handle incoming message from client.

        Pass Message data to all functions registered to message type endpoint using
        `on`.
        Send responses or exceptions from message handlers to client.

        Parameters
        ----------
        message : custom_types.message.MessageDict
            Incoming message.  Must be a valid MessageDict dictionary.
        """

        endpoint = message["type"]
        handler_functions = self._handlers.get(endpoint, None)

        if handler_functions is None:
            print(f"[User] No handler for {endpoint} found.")
            return

        print(
            f"[User] Received {endpoint}. Calling {len(handler_functions)} handler(s)."
        )
        for handler in handler_functions:
            try:
                response = await handler(message["data"])
            except ErrorDictException as err:
                response = err.error_message
            except Exception as err:
                print("[User] INTERNAL SERVER ERROR:", err)
                err = ErrorDict(
                    type="INTERNAL_SERVER_ERROR",
                    code=500,
                    description="Internal server error.",
                )
                response = MessageDict(type="ERROR", data=err)

            if response is not None:
                self.send(response)
