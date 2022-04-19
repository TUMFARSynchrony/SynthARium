"""TODO document"""

from __future__ import annotations
import json
import uuid
from os import listdir
from os.path import isfile, join

from _types.session import SessionDict


class SessionManager():
    """TODO document"""

    _sessions: dict[str, SessionDict]
    _session_dir: str

    def __init__(self, session_dir: str):
        """TODO document"""
        print("[SessionManager]: Initiating SessionManager")
        self._sessions = {}
        self._session_dir = session_dir
        self._read_files_from_drive()

    def get_session_list(self):
        """TODO document"""
        return list(self._sessions.values())

    def get_session(self, id: str):
        """TODO document"""
        return self._sessions.get(id)

    def update_session(self, session: SessionDict):
        """TODO document"""
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
        """TODO document"""
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

    def _generate_unique_session_id(self):
        """TODO document"""
        existing_ids = list(self._sessions.keys())
        return self._generate_unique_id(existing_ids)

    def _generate_unique_id(self, existing_ids: list[str]):
        """TODO document"""
        id = ""
        while len(id) == 0 or id in existing_ids:
            id = str(uuid.uuid4())
        return id

    def _read_files_from_drive(self):
        """TODO document"""
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
        """TODO document"""
        filenames: list[str] = []
        for filename in listdir(self._session_dir):
            if isfile(join(self._session_dir, filename)):
                filenames.append(filename)
        return filenames

    def _read(self, filename: str):
        """TODO document"""
        path = join(self._session_dir, filename)
        with open(path, "r") as file:
            data = json.load(file)
            return data

    def _write(self, session: SessionDict):
        """TODO document"""
        if "id" not in session:
            print("[SessionManager]: ERROR: Cannot save session without ID")
            return

        filename = session["id"] + ".json"
        path = join(self._session_dir, filename)
        with open(path, 'w') as file:
            json.dump(session, file, indent=4)
