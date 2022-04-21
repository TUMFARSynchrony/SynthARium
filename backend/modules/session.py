"""TODO document"""

from __future__ import annotations
from typing import Callable, Optional, Any
import json

from modules.util import generate_unique_id

from _types.session import SessionDict
from _types.participant import ParticipantDict
from _types.note import NoteDict


class Session():
    """TODO document"""

    _data: SessionDict
    _on_update: Callable[[Session], None]

    def __init__(self, session: SessionDict,
                 on_update: Callable[[Session], None]):
        """TODO document"""
        self._data = session
        self._on_update = on_update

    def update(self, session: SessionDict | Session):
        """TODO document"""
        # TODO data checks
        if type(session) is Session:
            self._data = session.asdict
        elif type(session) is SessionDict:
            self._data = session
        else:
            raise ValueError("Incorrect type for session argument. Expected: "
                             f"SessionDict or Session, got: {type(session)}")
        self._on_update(self)

    def __str__(self) -> str:
        """Get indented json string for this Session"""
        return json.dumps(self.asdict, indent=4)

    def __repr__(self) -> str:
        """Get representation of this Session obj.  Format: `Session(<id>)`."""
        return f"Session({self.id})"

    @property
    def asdict(self) -> SessionDict:
        """TODO Document"""
        return self._data

    @property
    def id(self) -> str | None:
        """TODO Document"""
        return self._data.get("id")

    @property
    def title(self) -> str:
        """TODO Document"""
        return self._data.get("title")

    @title.setter
    def title(self, value: str):
        """TODO document"""
        self._data["title"] = value
        self._on_update(self)

    @property
    def description(self) -> str:
        """TODO Document"""
        return self._data.get("description")

    @description.setter
    def description(self, value: str):
        """TODO document"""
        self._data["description"] = value
        self._on_update(self)

    @property
    def date(self) -> int:
        """TODO Document"""
        return self._data.get("date")

    @date.setter
    def date(self, value: int):
        """TODO document"""
        self._data["date"] = value
        self._on_update(self)

    @property
    def time_limit(self) -> int:
        """TODO Document"""
        return self._data.get("time_limit")

    @time_limit.setter
    def time_limit(self, value: int):
        """TODO document"""
        self._data["time_limit"] = value
        self._on_update(self)

    @property
    def record(self) -> bool:
        """TODO Document"""
        return self._data.get("record")

    @record.setter
    def record(self, value: bool):
        """TODO document"""
        self._data["record"] = value
        self._on_update(self)

    @property
    def participants(self) -> list[ParticipantDict]:
        """TODO Document"""
        return self._data.get("participants")

    def add_participant(self, participant: ParticipantDict):
        """TODO Document"""
        # TODO data check for participant
        participant_ids = [
            p.get("id", "") for p in self._data.get("participants")]
        id = generate_unique_id(participant_ids)
        participant["id"] = id
        self._data["participants"].append(participant)

    def remove_participant(self, participant_id: str):
        """TODO Document"""
        participant_ids = [
            p.get("id", "") for p in self._data.get("participants")]

        try:
            index = participant_ids.index(participant_id)
        except ValueError:
            print(f"[SESSION]: participant with id {participant_id} was not",
                  "found in participants")
            return

        self._data["participants"].pop(index)

    @property
    def start_time(self) -> Optional[int]:
        """TODO Document"""
        return self._data.get("start_time")

    @start_time.setter
    def start_time(self, value: int):
        """TODO document"""
        self._data["start_time"] = value
        self._on_update(self)

    @property
    def end_time(self) -> Optional[int]:
        """TODO Document"""
        return self._data.get("end_time")

    @end_time.setter
    def end_time(self, value: int):
        """TODO document"""
        self._data["end_time"] = value
        self._on_update(self)

    @property
    def notes(self) -> list[NoteDict]:
        """TODO Document"""
        return self._data.get("notes")

    def add_note(self, note: NoteDict):
        """TODO document"""
        self._data["notes"].append(note)
        self._on_update(self)

    @property
    def log(self) -> Optional[Any]:
        """TODO Document - log still wip"""
        return self._data.get("log")
