"""This module provides the Experimenter class."""

from __future__ import annotations
from aiortc import RTCSessionDescription

from custom_types.message import MessageDict
from custom_types.session import SessionDict
from custom_types.success import SuccessDict
from custom_types.note import NoteDict

from modules.util import check_valid_typed_dict
from modules.connection import connection_factory
from modules.exceptions import ErrorDictException
import modules.experiment as _experiment
import modules.hub as _hub
import modules.user as _user


class Experimenter(_user.User):
    """Experimenter is a type of modules.user.User with experimenter rights.

    Has access to a different set of API endpoints than other Users.  API endpoints for
    experimenters are defined here.
    """

    _experiment: _experiment.Experiment
    _hub: _hub.Hub

    def __init__(self, id: str, hub: _hub.Hub):
        """Instantiate new Experimenter instance.

        Parameters
        ----------
        id : str
            Unique identifier for this Experimenter.
        hub : modules.hub.Hub
            Hub this Experimenter is part of.  Used for api calls.
        """
        super().__init__(id)
        self._hub = hub

        # Add API endpoints
        self.on("GET_SESSION_LIST", self._handle_get_session_list)
        self.on("SAVE_SESSION", self._handle_save_session)
        self.on("DELETE_SESSION", self._handle_delete_session)
        self.on("CREATE_EXPERIMENT", self._handle_create_experiment)
        self.on("JOIN_EXPERIMENT", self._handle_join_experiment)
        self.on("START_EXPERIMENT", self._handle_start_experiment)
        self.on("STOP_EXPERIMENT", self._handle_stop_experiment)
        self.on("ADD_NOTE", self._handle_add_note)

    def _handle_get_session_list(self, _):
        """Handle requests with type `GET_SESSION_LIST`.

        Loads all known sessions from session manager.  Responds with type:
        `SESSION_LIST`.

        Parameters
        ----------
        _ : any
            Message data.  Ignored / not required.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SESSION_LIST` and data: list of
            custom_types.session.SessionDict.
        """
        sessions = self._hub.session_manager.get_session_dict_list()
        return MessageDict(type="SESSION_LIST", data=sessions)

    def _handle_save_session(self, data):
        """Handle requests with type `SAVE_SESSION`.

        Checks if received data is a valid SessionDict.  Try to update existing session,
        if `id` exists in data, otherwise try to create new session.

        Parameters
        ----------
        data : any
            Message data.  Checks if data is valid custom_types.session.SessionDict.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `SAVE_SESSION`.

        Raises
        ------
        ErrorDictException
            If data is not a valid SessionDict or session id is not known (cannot update
            unknown session).
        """
        # Data check
        if not check_valid_typed_dict(data, SessionDict):
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Expected session object."
            )
        assert isinstance(data, SessionDict)

        sm = self._hub.session_manager
        if "id" not in data:
            # Create new session
            sm.create_session(data)
        else:
            # Update existing session
            session = sm.get_session(data["id"])
            if session is not None:
                session.update(data)
            else:
                raise ErrorDictException(
                    code=404,
                    type="UNKNOWN_SESSION",
                    description="No session with the given ID found to update.",
                )

        success = SuccessDict(
            type="SAVE_SESSION", description="Successfully saved session."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_delete_session(self, data):
        """Handle requests with type `DELETE_SESSION`.

        Check if data is a valid dict with `session_id`.  If found, delete session with
        `session_id`.

        Parameters
        ----------
        data : any
            Message data.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `DELETE_SESSION`.

        Raises
        ------
        ErrorDictException
            If data is not a valid dict with an `session_id` str or if `session_id` is
            not known.
        """
        if not isinstance(data, dict) or "session_id" not in data:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Request data must be a valid JSON with session_id.",
            )

        session_id = data["session_id"]
        self._hub.session_manager.delete_session(session_id)

        success = SuccessDict(
            type="DELETE_SESSION", description="Successfully deleted session."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_create_experiment(self, data):
        """Handle requests with type `CREATE_EXPERIMENT`.

        Check if data is a valid dict with `session_id`.  If found, try to create a new
        modules.experiment.Experiment based on the session with `session_id`.

        Parameters
        ----------
        data : any
            Message data.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `CREATE_EXPERIMENT`.

        Raises
        ------
        ErrorDictException
            If data is not a valid dict with an `session_id` str, if `session_id` is not
            known or if there is already an Experiment with `session_id`.
        """
        if not isinstance(data, dict) or "session_id" not in data:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Request data must be a valid JSON with session_id.",
            )

        self._experiment = self._hub.create_experiment(data["session_id"])
        self._experiment.add_experimenter(self)

        success = SuccessDict(
            type="CREATE_EXPERIMENT", description="Successfully started session."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_join_experiment(self, data):
        """Handle requests with type `JOIN_EXPERIMENT`.

        Check if data is a valid dict with `session_id`.  If found, try to join an
        existing modules.experiment.Experiment with ID: `session_id`.

        Parameters
        ----------
        data : any
            Message data.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `JOIN_EXPERIMENT`.

        Raises
        ------
        ErrorDictException
            If data is not a valid dict with a `session_id` str or if there is no
            Experiment with `session_id`.
        """
        if not isinstance(data, dict) or "session_id" not in data:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description="Request data must be a valid JSON with session_id.",
            )

        experiment = self._hub.experiments.get(data["session_id"])

        if experiment is None:
            raise ErrorDictException(
                code=404,
                type="UNKNOWN_EXPERIMENT",
                description="There is no experiment with the given ID.",
            )

        self._experiment = experiment
        self._experiment.add_experimenter(self)

        success = SuccessDict(
            type="JOIN_EXPERIMENT", description="Successfully joined experiment."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_start_experiment(self, _):
        """Handle requests with type `START_EXPERIMENT`.

        Parameters
        ----------
        _ : any
            Message data.  Ignored / not required.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `START_EXPERIMENT`.

        Raises
        ------
        ErrorDictException
            If this Experimenter is not connected to an modules.experiment.Experiment or
            the Experiment has already started.
        """
        if not self._experiment:
            raise ErrorDictException(
                code=409,
                type="INVALID_REQUEST",
                description=(
                    "Cannot start experiment. Experimenter is not connected to an "
                    + "experiment."
                ),
            )

        self._experiment.start()

        success = SuccessDict(
            type="START_EXPERIMENT", description="Successfully started experiment."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_stop_experiment(self, _):
        """Handle requests with type `STOP_EXPERIMENT`.

        Parameters
        ----------
        _ : any
            Message data.  Ignored / not required.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `STOP_EXPERIMENT`.

        Raises
        ------
        ErrorDictException
            If this Experimenter is not connected to an modules.experiment.Experiment or
            the Experiment has already ended.
        """
        if not self._experiment:
            raise ErrorDictException(
                code=409,
                type="INVALID_REQUEST",
                description=(
                    "Cannot start experiment. Experimenter is not connected to an "
                    + "experiment."
                ),
            )

        self._experiment.stop()

        success = SuccessDict(
            type="STOP_EXPERIMENT", description="Successfully stopped experiment."
        )
        return MessageDict(type="SUCCESS", data=success)

    def _handle_add_note(self, data):
        """Handle requests with type `ADD_NOTE`.

        Check if data is a valid custom_types.note.NoteDict and adds the note to the
        modules.experiment.Experiment the Experimenter is connected to.

        Parameters
        ----------
        _ : any
            Message data.  Ignored / not required.

        Returns
        -------
        custom_types.message.MessageDict
            MessageDict with type: `SUCCESS`, data: custom_types.success.SuccessDict and
            SuccessDict type: `ADD_NOTE`.

        Raises
        ------
        ErrorDictException
            If data is not a valid custom_types.note.NoteDict.
        """
        if not check_valid_typed_dict(data, NoteDict):
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Expected note object."
            )
        self._experiment.session.add_note(data)

        success = SuccessDict(type="ADD_NOTE", description="Successfully added note.")
        return MessageDict(type="SUCCESS", data=success)


async def experimenter_factory(offer: RTCSessionDescription, id: str, hub: _hub.Hub):
    """TODO document"""
    experimenter = Experimenter(id, hub)
    answer, connection = await connection_factory(offer, experimenter.handle_message)
    experimenter.set_connection(connection)
    return (answer, experimenter)
