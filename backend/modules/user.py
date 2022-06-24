"""Provide the abstract `User` class.

See Also
--------
modules.participant.Participant : Participant implementation of User.
modules.experimenter.Experimenter : Experimenter implementation of User.
"""

from __future__ import annotations

import logging
import traceback
from abc import ABCMeta, abstractmethod
from pyee.asyncio import AsyncIOEventEmitter
from typing import Callable, Any, Coroutine, Tuple

from custom_types.error import ErrorDict
from custom_types.message import MessageDict
from custom_types.participant_summary import ParticipantSummaryDict

from modules.exceptions import ErrorDictException
from modules.connection_state import ConnectionState
from modules.connection_interface import ConnectionInterface
from modules.tracks import AudioTrackHandler, VideoTrackHandler
from custom_types.connection import (
    ConnectionAnswerDict,
    is_valid_connection_answer_dict,
)


class User(AsyncIOEventEmitter, metaclass=ABCMeta):
    """User class representing a connected client.

    Provides client connection and message handling logic for child classes.

    Extends AsyncIOEventEmitter, providing the following events:
    - `disconnected` : modules.user.User
        Emitted when the connection with the client closes.
    - `tracks_complete` : tuple of modules.track.VideoTrackHandler and modules.track.AudioTrackHandler
        Forwarded from modules.connection.Connection.  Emitted when both tracks are
        received from the client and ready to be distributed / subscribed to.

    Attributes
    ----------
    id : str
        ID of this User.

    Methods
    -------
    on_message(endpoint, handler)
        Register an `handler` function for incoming messages with type `endpoint`.
    handle_message(message)
        Handle incoming message from client.
    set_connection(connection)
        Set the connection of this user.
    send(message)
        Send a custom_types.message.MessageDict to the connected client.
    disconnect()
        Closes the connection with the client.
    subscribe_to(user)
        Add incoming tracks from `user` to this User.
    set_muted(video, audio)
        Set the muted state for this user
    get_summary()
        Get summary of User for client

    See Also
    --------
    modules.participant.Participant : Participant implementation of User.
    modules.experimenter.Experimenter : Experimenter implementation of User.

    Notes
    -----
    Messages received from the client are handled using the custom event handler in User
    (add handler using: `on_message` and internally emit event using: `handle_message`).
    Do not confuse this with the events the User provides using the AsyncIOEventEmitter.
    """

    id: str
    _logger: logging.Logger
    _muted_video: bool
    _muted_audio: bool
    _connection: ConnectionInterface
    _handlers: dict[str, list[Callable[[Any], Coroutine[Any, Any, MessageDict | None]]]]
    __disconnected: bool

    def __init__(
        self, id: str, muted_video: bool = False, muted_audio: bool = False
    ) -> None:
        """Instantiate new User base class.

        Should only be called by child classes.

        Parameters
        ----------
        id : str
            Unique identifier for this Experimenter.
        muted_video : bool, default False
            Whether the users video should be muted.
        muted_audio : bool, default False
            Whether the users audio should be muted.
        """
        super().__init__()
        self._logger = logging.getLogger(f"User-{id}")
        self.id = id
        self._muted_video = muted_video
        self._muted_audio = muted_audio
        self._handlers = {}
        self.__disconnected = False

    @property
    def muted_video(self) -> bool:
        """bool indicating if the users video is muted."""
        return self._muted_video

    @property
    def muted_audio(self) -> bool:
        """bool indicating if the users audio is muted."""
        return self._muted_audio

    def get_summary(self) -> ParticipantSummaryDict | None:
        """Get summary of User for client.

        Base implementation returns None.  Should be implemented in classes extending
        User to provide a summary.

        Returns
        -------
        ParticipantSummaryDict | None
            Summary of user.  Subclasses may override this function and return values
            other than None.

        See Also
        --------
        modules.participant.Participant.get_summary
            Participant implementation for get_summary.
        """
        return None

    def set_connection(self, connection: ConnectionInterface) -> None:
        """Set the connection of this user.

        This should only be used once before using this User.  See factory functions.

        See Also
        --------
        modules.participant.Participant : Participant implementation of User.
        modules.experimenter.Experimenter : Experimenter implementation of User.
        """
        self._logger.debug(f"Added Connection: {repr(connection)}")
        self._connection = connection
        self._connection.add_listener(
            "state_change", self._handle_connection_state_change
        )
        self._connection.add_listener(
            "state_change", self._handle_connection_state_change_user
        )
        self._connection.on("tracks_complete", self._emit_tracks_complete_event)

    async def send(self, message: MessageDict) -> None:
        """Send a custom_types.message.MessageDict to the connected client.

        Parameters
        ----------
        message : custom_types.message.MessageDict
            Message for the client.
        """
        await self._connection.send(message)

    async def disconnect(self) -> None:
        """Disconnect.  Closes the connection with the client."""
        await self._connection.stop()
        self._handle_disconnect()

    async def add_subscriber(self, user: User) -> None:
        """Add `user` as a subscriber to this User.

        Sends a `CONNECTION_OFFER` to `user` and waits for an `CONNECTION_ANSWER`.
        After receiving the answer, the incoming streams from this user will also be
        send to `user`.

        Parameters
        ----------
        user : modules.user.User
            New subscriber to this User.
        """
        self._logger.debug(f"Adding subscriber: {repr(user)}")
        offer = await self._connection.create_subscriber_offer(self.get_summary())
        msg = MessageDict(type="CONNECTION_OFFER", data=offer)
        await user.send(msg)

        @user.on("CONNECTION_ANSWER")
        async def _handle_answer(answer: ConnectionAnswerDict):
            if answer["id"] == offer["id"]:
                await self._connection.handle_subscriber_answer(answer)
                user.remove_listener("CONNECTION_ANSWER", _handle_answer)

        @self.on("disconnected")
        def _remove_listener(_):
            try:
                user.remove_listener("CONNECTION_ANSWER", _handle_answer)
            except KeyError:
                return

        @user.on("disconnected")
        async def _remove_subconnection(_):
            await self._connection.stop_subconnection(offer["id"])

    def on_message(
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
        if endpoint in self._handlers:
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

        # TODO temp
        if endpoint == "CONNECTION_ANSWER":
            if not is_valid_connection_answer_dict(message["data"]):
                self._logger.warning(f"Received invalid CONNECTION_ANSWER")
                return
            self.emit("CONNECTION_ANSWER", message["data"])
            return

        handler_functions = self._handlers.get(endpoint, None)

        if handler_functions is None:
            self._logger.warning(f"No handler for {endpoint} found")
            return

        self._logger.info(f"Received {endpoint}")
        self._logger.debug(f"Calling {len(handler_functions)} handler(s)")
        for handler in handler_functions:
            try:
                response = await handler(message["data"])
            except ErrorDictException as err:
                self._logger.info(
                    f"Failed to handle {endpoint} message. {err.description}"
                )
                response = err.error_message
            except Exception as err:
                self._logger.error(f"INTERNAL SERVER ERROR: {err}")
                self._logger.error(traceback.format_exc())
                err = ErrorDict(
                    type="INTERNAL_SERVER_ERROR",
                    code=500,
                    description="Internal server error. See server log for details.",
                )
                response = MessageDict(type="ERROR", data=err)

            if response is not None:
                await self.send(response)

    async def set_muted(self, video: bool, audio: bool) -> None:
        """Set the muted state for this user.

        Parameters
        ----------
        video : bool
            Whether the users video should be muted.
        audio : bool
            Whether the users audio should be muted.
        """
        if self._muted_video == video and self._muted_audio == audio:
            return

        self._muted_video = video
        self._muted_audio = audio

        await self._connection.set_muted(video, audio)

    def _handle_disconnect(self) -> None:
        """Handle this user disconnecting.

        Emit "disconnected" event and remove all event listeners on user.
        """
        if self.__disconnected:
            return
        self.__disconnected = True
        self._logger.info("Disconnected")
        self.emit("disconnected", self)
        self.remove_all_listeners()

    def _emit_tracks_complete_event(
        self, tracks: Tuple[VideoTrackHandler, AudioTrackHandler]
    ) -> None:
        """Emits the `tracks_complete` event with `data`.

        Use to forward the event from the connection.
        """
        self.emit("tracks_complete", tracks)

    def _handle_connection_state_change_user(self, state: ConnectionState) -> None:
        """Calls _handle_disconnect if state is CLOSED or FAILED.

        Parameters
        ----------
        state : modules.connection_state.ConnectionState
            New state of `self._connection`.
        """
        if state in [ConnectionState.CLOSED, ConnectionState.FAILED]:
            self._handle_disconnect()

    @abstractmethod
    async def _handle_connection_state_change(self, state: ConnectionState) -> None:
        """Handler for connection "state_change" event.

        Must be implemented in classes extending User.

        Parameters
        ----------
        state : modules.connection_state.ConnectionState
            New state of the connection this user has with the client.
        """
        pass
