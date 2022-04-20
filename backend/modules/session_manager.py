"""This module provides the SessionManager class, which Manages session data.
"""

from __future__ import annotations
import json
import uuid
from os import listdir
from os.path import isfile, join

from _types.session import SessionDict


class SessionManager():
    """Manages session data.

    Implements loading and storing sessions from and to the drive.  If a
    session is updated, the SessionManager will update the data on the
    drive to ensure persistency.

    Methods
    -------
    get_session_list() : list of _types.session.SessionDict
        Get all sessions.
    get_session(id) : _types.session.SessionDict
        Get the session with the given id.
    update_session(session) : None
        Update session data to save changes on the drive.
    create_session(session) : None
        Instantiate a new session with the given session data.
    delete_session(id) : bool
        Delete the session with `id`.
    """

    _sessions: dict[str, SessionDict]
    _session_dir: str

    def __init__(self, session_dir: str):
        """Instantiate new SessionManager, which manages session data.

        Load existing sessions from `session_dir` when initiating.

        Parameters
        ----------
        session_dir : str
            Directory of session data JSONs relative to the backend folder.
        """
        print("[SessionManager]: Initiating SessionManager")
        self._sessions = {}
        self._session_dir = session_dir
        self._read_files_from_drive()

    def get_session_list(self):
        """Get all sessions.

        Returns
        -------
        list of _types.session.SessionDict
            List containing all sessions managed by this SessionManager.
        """
        return list(self._sessions.values())

    def get_session(self, id: str):
        """Get the session with the given id.

        Parameters
        ----------
        id : str
            Session id of the requested session.

        Returns
        -------
        _types.session.SessionDict or None
            None if `id` does not correlate to a known session, otherwise
            session data.
        """
        return self._sessions.get(id)

    def update_session(self, session: SessionDict):
        """Update session data to save changes on the drive.

        Parameters
        ----------
        session : _types.session.SessionDict
            Session data.  Must contain an id known to this SessionManager.
        """
        # TODO further error handling in this function
        if "id" not in session:
            print("[SessionManager]: ERROR: Cannot update session without id")
            return

        if session["id"] not in self._sessions.keys():
            print("[SessionManager]: ERROR: Cannot update unknown session")
            return

        self._sessions[session["id"]].update(session)
        self._write(self._sessions[session["id"]])

    def create_session(self, session: SessionDict):
        """Instantiate a new session with the given session data.

        Generate session id and participant ids inplace.  Then save the session
        in this manager and on the drive for persistence.

        Parameters
        ----------
        session : _types.session.SessionDict
            Basic session data without ids
        """
        if "id" in session:
            print("[SessionManager]: ERROR: Cannot create new session with",
                  "existing id - in create_session()")
            return

        session_id = self._generate_unique_session_id()
        session["id"] = session_id

        participant_ids = []
        for participant in session["participants"]:
            id = self._generate_unique_id(participant_ids)
            participant_ids.append(id)
            participant["id"] = id

        self._sessions[session_id] = session
        self._write(session)

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
        """
        if id not in self._sessions:
            print("[SessionManager]: WARNING: Cannot delete session with id",
                  f"{id}, no session with this id was found.")
            return False
        return self._sessions.pop(id, None) != None

    def _generate_unique_session_id(self):
        """Generate an unique session id."""
        existing_ids = list(self._sessions.keys())
        return self._generate_unique_id(existing_ids)

    def _generate_unique_id(self, existing_ids: list[str]):
        """Generate an unique id without collision with `existing_ids`.

        Parameters
        ----------
        existing_ids : list of str
            Existing ids which may not include the new, generated id.

        Returns
        -------
        str
            Unique id generated.

        See Also
        --------
        SessionManager._generate_unique_session_id : Generate an unique session
            id.
        """
        id = ""
        while len(id) == 0 or id in existing_ids:
            id = uuid.uuid4().hex[:10]
        return id

    def _read_files_from_drive(self):
        """Read sessions saved on the drive, save in `self._sessions`."""
        filenames = self._get_filenames()
        print(f"[SessionManager]: Found {len(filenames)} files: {filenames}")

        for file in filenames:
            session: SessionDict = self._read(file)
            # TODO data checks

            if "id" not in session:
                # TODO handle
                print("[SessionManager]: ERROR Session ID missing in",
                      file)
                continue

            if session["id"] in self._sessions.keys():
                print("[SessionManager]: ERROR Session ID duplicate:",
                      session["id"])
                continue

            self._sessions[session["id"]] = session

    def _get_filenames(self):
        """Get all filenames of files in `self._session_dir`."""
        filenames: list[str] = []
        for filename in listdir(self._session_dir):
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

    def _write(self, session: SessionDict):
        """Write a json file.

        Parameters
        ----------
        session : _types.session.SessionDict
            session data that should be written to the self._session_dir
            directory.
        """
        if "id" not in session:
            print("[SessionManager]: ERROR: Cannot save session without ID")
            return

        filename = session["id"] + ".json"
        path = join(self._session_dir, filename)
        with open(path, 'w') as file:
            json.dump(session, file, indent=4)
