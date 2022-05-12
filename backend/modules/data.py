from dataclasses import dataclass, field
from typing import Any, Callable


from modules.util import generate_unique_id
from modules.exceptions import ErrorDictException


from custom_types.position import PositionDict
from custom_types.size import SizeDict
from custom_types.participant import ParticipantDict
from custom_types.chat_message import ChatMessageDict
from custom_types.filters import BasicFilterDict
from custom_types.note import NoteDict
from custom_types.session import (
    SessionDict,
    has_duplicate_participant_ids,
    get_filtered_participant_ids,
)


@dataclass(slots=True)
class _BaseDataClass:
    """TODO Document"""

    _initialized: bool | None = field(repr=False, init=False)
    _on_update: Callable[[], None] = field(repr=False, compare=False)

    def __post_init__(self):
        """TODO Document"""
        self._initialized = True

    def __setattr__(self, _name: str, _value: Any) -> None:
        """TODO Document"""
        object.__setattr__(self, _name, _value)
        try:
            # Signal a update if initialization was already finished
            if self._initialized and _name != "_initialized":
                self._on_update()
        except AttributeError:
            pass


@dataclass(slots=True)
class SizeData(_BaseDataClass):
    """TODO Document"""

    width: int
    height: int

    def asdict(self) -> SizeDict:
        """TODO Document"""
        return {
            "width": self.width,
            "height": self.height,
        }


@dataclass(slots=True)
class PositionData(_BaseDataClass):
    """TODO Document"""

    x: int
    y: int
    z: int

    def asdict(self) -> PositionDict:
        """TODO Document"""
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }


@dataclass(slots=True)
class ParticipantData(_BaseDataClass):
    """TODO Document"""

    id: str
    first_name: str
    last_name: str
    banned: bool = field(repr=False)
    size: SizeData = field(repr=False)
    muted_video: bool = field(repr=False)
    muted_audio: bool = field(repr=False)
    position: PositionData = field(repr=False)
    chat: list[ChatMessageDict] = field(repr=False)
    filters: list[BasicFilterDict] = field(repr=False)

    def __init__(
        self, _on_update: Callable[[], None], participant_dict: ParticipantDict
    ):
        """TODO document"""
        if "id" not in participant_dict:
            raise ValueError('Missing "id" in participant dict.')

        # Save simple variables
        self.id = participant_dict["id"]
        self.first_name = participant_dict["first_name"]
        self.last_name = participant_dict["last_name"]
        self.banned = participant_dict["banned"]
        self.muted_video = participant_dict["muted_video"]
        self.muted_audio = participant_dict["muted_audio"]
        self.chat = participant_dict["chat"]
        self.filters = participant_dict["filters"]

        # parse size and position
        size = participant_dict["size"]
        self.size = SizeData(_on_update, size["width"], size["width"])

        pos = participant_dict["position"]
        self.position = PositionData(_on_update, pos["x"], pos["y"], pos["z"])

        # Setup variables for _BaseDataClass
        self._on_update = _on_update
        self._initialized = True

    def asdict(self) -> ParticipantDict:
        """TODO Document"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "banned": self.banned,
            "size": self.size.asdict(),
            "muted_video": self.muted_video,
            "muted_audio": self.muted_audio,
            "position": self.position.asdict(),
            "chat": self.chat,
            "filters": self.filters,
        }


@dataclass(slots=True)
class SessionData:
    """TODO Document"""

    id: str
    title: str
    date: int = field(repr=False)
    record: bool = field(repr=False)
    time_limit: int = field(repr=False)
    description: str = field(repr=False)
    notes: list[NoteDict] = field(repr=False)
    participants: dict[str, ParticipantData] = field(repr=False)

    # Variables with default values:
    log: Any | None = field(repr=False)
    end_time: int | None = field(repr=False)
    start_time: int | None = field(repr=False)

    _on_update: Callable[[str], None] = field(repr=False)
    _trigger_updates: bool | None = field(repr=False, init=False)

    def __init__(self, on_update: Callable[[str], None], session_dict: SessionDict):
        """TODO document"""
        self._set_variables(session_dict, False)
        self._on_update = on_update
        self._trigger_updates = True

    def update(self, session_dict: SessionDict):
        """TODO document"""
        # Data checks.
        if session_dict.get("id") is not self.id:
            raise ValueError("Session.update can not change the ID of a Session")

        if self._has_unknown_participant_ids(session_dict):
            raise ErrorDictException(
                code=409,
                type="UNKNOWN_ID",
                description="Unknown participant ID found in session data.",
            )

        if has_duplicate_participant_ids(session_dict):
            raise ErrorDictException(
                code=400,
                type="DUPLICATE_ID",
                description="Duplicate participant ID found in session data.",
            )

        self._set_variables(session_dict)

    def asdict(self) -> SessionDict:
        """TODO Document"""
        session_dict: SessionDict = {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "record": self.record,
            "time_limit": self.time_limit,
            "description": self.description,
            "notes": self.notes,
            "participants": [p.asdict() for p in self.participants.values()],
        }

        if self.log is not None:
            session_dict["log"] = self.log
        if self.end_time is not None:
            session_dict["end_time"] = self.end_time
        if self.start_time is not None:
            session_dict["start_time"] = self.start_time

        return session_dict

    def _set_variables(
        self, session_dict: SessionDict, final_trigger_updates_state: bool = True
    ) -> None:
        """TODO document"""
        if "id" not in session_dict:
            raise ValueError('Missing "id" in session dict.')

        self._trigger_updates = False

        # Save simple variables
        self.id = session_dict["id"]
        self.title = session_dict["title"]
        self.date = session_dict["date"]
        self.record = session_dict["record"]
        self.time_limit = session_dict["time_limit"]
        self.description = session_dict["description"]
        self.notes = session_dict["notes"]

        # Save simple but optional variables
        self.log = session_dict.get("log")
        self.end_time = session_dict.get("end_time")
        self.start_time = session_dict.get("end_time")

        # Parse participants
        _generate_participant_ids(session_dict)
        self.participants = {}
        for participant_dict in session_dict["participants"]:
            p = ParticipantData(self._handle_updates, participant_dict)
            self.participants[p.id] = p

        self._trigger_updates = final_trigger_updates_state

    def _handle_updates(self) -> None:
        """TODO document"""
        if self._trigger_updates:
            print("Trigger Update!")
            self._on_update(self.id)

    def __setattr__(self, _name: str, _value: Any) -> None:
        """TODO Document"""
        object.__setattr__(self, _name, _value)
        try:
            # Signal a update, unless changing internal variable
            if _name != "_trigger_updates":
                self._handle_updates()
        except AttributeError:
            pass

    def _has_unknown_participant_ids(self, session_dict: SessionDict) -> bool:
        """TODO Document"""
        participant_ids = get_filtered_participant_ids(session_dict)
        known_ids = self.participants.keys()

        for id in participant_ids:
            if id is None or id not in known_ids:
                return True

        return False


def _generate_participant_ids(session_dict: SessionDict) -> None:
    """TODO document"""
    participant_ids = get_filtered_participant_ids(session_dict)
    for participant in session_dict.get("participants", []):
        id = participant.get("id")
        if id is None:
            # New participant without id
            new_id = generate_unique_id(participant_ids)
            participant_ids.append(new_id)
            participant["id"] = new_id
