"""Provide the `SessionManager` class, which manages session data."""

from __future__ import annotations
import json

import os
from os.path import isfile, join

from custom_types.session import SessionDict, is_valid_session

from modules.util import generate_unique_id
from modules.exceptions import ErrorDictException
from modules.data import SessionData
from modules import BACKEND_DIR


class SessionManager:
    """Manages session data.

    Implements loading and storing sessions from and to the drive.  If a
    session is updated, the SessionManager will update the data on the
    drive to ensure persistency.

    Methods
    -------
    get_session_list() : list of modules.data.SessionData
        Get all sessions.
    get_session(id) : modules.data.SessionData or None
        Get the session with the given id.
    create_session(session_dict) : None
        Instantiate a new session with the given session dict.
    delete_session(id) : bool
        Delete the session with `id`.
    """

    _sessions: dict[str, SessionData]
    _session_dir: str

    def __init__(self, session_dir: str):
        """Instantiate new SessionManager, which manages session data.

        Load existing sessions from `session_dir` when initiating.

        Parameters
        ----------
        session_dir : str
            Directory of session data JSONs relative to the backend folder.
        """
        print("[SessionManager] Initiating SessionManager")
        self._sessions = {}
        self._session_dir = join(BACKEND_DIR, session_dir)
        self._read_files_from_drive()

    def get_session_list(self):
        """Get all sessions.

        Returns
        -------
        list of modules.data.SessionData
            List containing all sessions managed by this SessionManager.
        """
        return list(self._sessions.values())

    def get_session_dict_list(self):
        """Get all sessions as dictionary.

        Returns
        -------
        list of custom_types.session.SessionDict
            List containing all sessions managed by this SessionManager as dictionary.
        """
        response = [s.asdict() for s in list(self._sessions.values())]
        return response

    def get_session(self, id: str):
        """Get the session with the given id.

        Parameters
        ----------
        id : str
            Session id of the requested session.

        Returns
        -------
        modules.data.SessionData or None
            None if `id` does not correlate to a known session, otherwise
            session data.
        """
        return self._sessions.get(id)

    def create_session(self, session_dict: SessionDict):
        """Instantiate a new session with the given session data.

        Generate session id and participant ids inplace.  Then save the session
        in this manager and on the drive for persistence.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            Basic session data without ids

        Returns
        -------
        modules.data.SessionData
            New session object.

        Raises
        ------
        ValueError
            If `id` in session_dict is not an empty string or if a duplicate participant
            ID was found.
        """
        if session_dict["id"] != "":
            print(
                "[SessionManager] ERROR: Cannot create new session with existing id -",
                "in create_session()",
            )
            raise ValueError("Cannot create new session with existing ID.")

        session_id = self._generate_unique_session_id()
        session_dict["id"] = session_id

        session = SessionData(self._handle_session_update, session_dict)
        self._sessions[session_id] = session
        self._write(session.asdict())
        return session

    def delete_session(self, id: str):
        """Delete the session with `id`.

        Parameters
        ----------
        id : str
            Session id of the session data that will be deleted.

        Returns
        -------
        bool
            True, if the session was found and successfully deleted, otherwise
            False.

        Raises
        ------
        ErrorDictException
            If there is no session with `id`.
        """
        if id not in self._sessions:
            print(
                f"[SessionManager] Cannot delete session with id {id}, no ",
                "session with this id was found.",
            )
            raise ErrorDictException(
                code=404,
                type="INVALID_REQUEST",
                description="No session found for the given ID.",
            )

        # TODO check if the session obj is used in an experiment.

        print("[SessionManager] Deleting session. ID:", id)
        self._delete_file(f"{id}.json")
        return self._sessions.pop(id, None) != None

    def _handle_session_update(self, session_id: str):
        """Update session data changes on the drive.

        Parameters
        ----------
        session_id : str
            ID of the session that was updated.

        Notes
        -----
        Use `SessionData.update()` to update a session, it will call this function.
        """
        # TODO further error handling in this function
        if session_id is None:
            print("[SessionManager] ERROR: Cannot update session without id")
            return

        if session_id not in self._sessions:
            print("[SessionManager] ERROR: Cannot update unknown session", session_id)
            return

        session = self._sessions[session_id]
        self._write(session.asdict())

    def _generate_unique_session_id(self):
        """Generate an unique session id."""
        existing_ids = list(self._sessions)
        return generate_unique_id(existing_ids)

    def _read_files_from_drive(self):
        """Read sessions saved on the drive, save in `self._sessions`."""
        filenames = self._get_filenames()
        print(f"[SessionManager] Found {len(filenames)} files: {filenames}")

        sessions_with_missing_ids: list[SessionDict] = []
        for file in filenames:
            session_dict: SessionDict = self._read(file)
            if not is_valid_session(session_dict, True):
                print(
                    f"[SessionManager] ERROR invalid session file: {file}. Ignoring",
                    "file.",
                )
                continue

            if session_dict["id"] == "":
                # Generate ID after loading the rest of the files.
                sessions_with_missing_ids.append(session_dict)
                continue

            if session_dict["id"] in self._sessions:
                print(
                    "[SessionManager] ERROR: Session ID duplicate:",
                    f"{session_dict['id']}. Ignoring file: {file}.",
                )
                continue

            try:
                session_obj = SessionData(self._handle_session_update, session_dict)
            except ErrorDictException:
                print(f"[SessionManager] ERROR: Participant ID duplicate in: {file}.")
                continue
            self._sessions[session_dict["id"]] = session_obj

        # Create sessions for files with missing session IDs
        for session_dict in sessions_with_missing_ids:
            session_obj = self.create_session(session_dict)

    def _get_filenames(self):
        """Get all filenames of files in `self._session_dir`."""
        filenames: list[str] = []
        for filename in os.listdir(self._session_dir):
            if isfile(join(self._session_dir, filename)):
                filenames.append(filename)
        return filenames

    def _read(self, filename: str):
        """Read a json file.

        Parameters
        ----------
        filename : str
            name of the required file inside `self._session_dir`.
        """
        path = join(self._session_dir, filename)
        with open(path, "r") as file:
            data = json.load(file)
            return data

    def _write(self, session_dict: SessionDict):
        """Write a json file.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            session data that should be written to the self._session_dir
            directory.
        """
        if session_dict["id"] == "":
            print("[SessionManager] ERROR: Cannot save session without ID.")
            return

        filename = f"{session_dict['id']}.json"
        path = join(self._session_dir, filename)
        with open(path, "w") as file:
            json.dump(session_dict, file, indent=4)

    def _delete_file(self, filename: str):
        """Delete a file in the sessions folder.

        Parameters
        ----------
        filename : str
            name of the file inside `self._session_dir`.
        """
        path = join(self._session_dir, filename)
        if os.path.exists(path):
            os.remove(path)
        else:
            print("[SessionManager] Cant delete file, file not found.", path)
