"""Provide data classes for session, participant, size and position data.

Provides: `SessionData`, `ParticipantData`, `PositionData` and `SizeData`.
"""
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
    """Base dataclass with update recognition and handling.

    When data is changed, this class calls `on_update` passed in the constructor.

    Used to save the data to the drive when changes are made.
    """

    _initialized: bool | None = field(repr=False, init=False)
    _on_update: Callable[[], None] = field(repr=False, compare=False)

    def __post_init__(self):
        """Set `_initialized` to true after initialization."""
        self._initialized = True

    def __setattr__(self, _name: str, _value: Any) -> None:
        """Recognize changes to variables in this class and call `on_update`."""
        object.__setattr__(self, _name, _value)
        try:
            # Signal a update if initialization was already finished
            if self._initialized and _name != "_initialized":
                self._on_update()
        except AttributeError:
            pass


@dataclass(slots=True)
class SizeData(_BaseDataClass):
    """Size data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    width : int
    height : int

    Methods
    -------
    asdict()
        Get SizeData as dictionary.

    Note
    ----
    Special methods, such as __init__, __str__, __repr__ and equality checks are
    generated automatically by dataclasses.dataclass.
    """

    width: int
    height: int

    def asdict(self) -> SizeDict:
        """Get SizeData as dictionary.

        Returns
        -------
        custom_types.size.SizeDict
            SizeDict with the data in this SizeData.
        """
        return {
            "width": self.width,
            "height": self.height,
        }


@dataclass(slots=True)
class PositionData(_BaseDataClass):
    """Position data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    x : int
        x-coordinate
    y : int
        y-coordinate
    z : int
        z-coordinate

    Methods
    -------
    asdict()
        Get PositionData as dictionary.

    Note
    ----
    Special methods, such as __init__, __str__, __repr__ and equality checks are
    generated automatically by dataclasses.dataclass.
    """

    x: int
    y: int
    z: int

    def asdict(self) -> PositionDict:
        """Get PositionData as dictionary.

        Returns
        -------
        custom_types.position.PositionDict
            PositionDict with the data in this PositionData.
        """
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }


@dataclass(slots=True)
class ParticipantData(_BaseDataClass):
    """participant data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    id : str
    first_name : str
    last_name : str
    banned : bool
    size : SizeData
    muted_video : bool
    muted_audio : bool
    position : PositionData
    chat : list or custom_types.chat_message.ChatMessageDict
    filters : list or custom_types.filters.BasicFilterDict

    Methods
    -------
    asdict()
        Get ParticipantData as dictionary.

    Note
    ----
    Special methods, such as __str__, __repr__ and equality checks are generated
    automatically by dataclasses.dataclass.
    """

    id: str
    """Participant ID."""

    first_name: str
    """First name of this participant."""

    last_name: str
    """Last name of this participant."""

    banned: bool = field(repr=False)
    """Whether this participant is banned."""

    size: SizeData = field(repr=False)
    """Size of participant on the canvas (frontend)."""

    muted_video: bool = field(repr=False)
    """Whether the participants' video is forcefully muted by the experimenter."""

    muted_audio: bool = field(repr=False)
    """Whether the participants' audio is forcefully muted by the experimenter."""

    position: PositionData = field(repr=False)
    """Position of the participant on the canvas (frontend)."""

    chat: list[ChatMessageDict] = field(repr=False)
    """Chat log between participant and experimenter."""

    filters: list[BasicFilterDict] = field(repr=False)
    """Active filters for participant."""

    def __init__(
        self, _on_update: Callable[[], None], participant_dict: ParticipantDict
    ):
        """Initialize new ParticipantData.

        Parameters
        ----------
        on_update : function () -> None
            Function that informs the parent session when changes occur.
        participant_dict : custom_types.participant.ParticipantDict
            Participant data the ParticipantData represents.

        Raises
        ------
        ValueError
            If `id` is missing in `participant_dict`.
        """
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
        """Get ParticipantData as dictionary.

        Returns
        -------
        custom_types.participant.ParticipantDict
            ParticipantDict with the data in this ParticipantData.
        """
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
    """Session data with update handling.

    Will forward any updates to the SessionManager, making sure all changes are
    persistent.

    Attributes
    ----------
    id : str
    title : str
    date : int
    record : bool
    time_limit : int
    description : str
    notes : list of custom_types.note.NoteDict
    participants : dict
    log : Any or None
    end_time : int or None
    start_time : int or None

    Methods
    -------
    update(session_dict)
        Update the whole Session with the data in `session_dict`.
    asdict()
        Get SessionData as dictionary.

    Note
    ----
    Special methods, such as __str__, __repr__ and equality checks are generated
    automatically by dataclasses.dataclass.
    """

    id: str
    """Session ID."""

    title: str
    """Session title"""

    date: int = field(repr=False)
    """Planned session date in milliseconds since January 1, 1970, 00:00:00 (UTC)."""

    record: bool = field(repr=False)
    """Whether the session will be recorded."""

    time_limit: int = field(repr=False)
    """Session time limit in milliseconds."""

    description: str = field(repr=False)
    """Session description"""

    notes: list[NoteDict] = field(repr=False)
    """Notes taken by a Experimenter during the experiment."""

    participants: dict[str, ParticipantData] = field(repr=False)
    """Participants invited to this session.

    Note that this is a dict, while the participants in custom_types.session.SessionDict
    are a list.
    """

    # Internal / private variables
    _on_update: Callable[[str], None] = field(repr=False, compare=False)
    _trigger_updates: bool | None = field(repr=False, init=False, compare=False)

    # Variables with default values:
    log: Any | None = field(repr=False, default=None)
    """TODO Document - log still wip"""

    end_time: int | None = field(repr=False, default=None)
    """Session end time in milliseconds since January 1, 1970, 00:00:00 (UTC)."""

    start_time: int | None = field(repr=False, default=None)
    """Session start time in milliseconds since January 1, 1970, 00:00:00 (UTC)."""

    def __init__(self, on_update: Callable[[str], None], session_dict: SessionDict):
        """Initialize new SessionData.

        Checks for duplicate participant IDs and generates missing participant IDs.

        Parameters
        ----------
        on_update : function (session_id) -> None
            Function that informs the session manager when changes occur.
        session_dict : custom_types.session.SessionDict
            Session data the session represents.

        Raises
        ------
        ValueError
            If `session_dict` is missing the (session) `id` variable or if a duplicate
            participant ID was found.
        """
        if has_duplicate_participant_ids(session_dict):
            raise ValueError("Duplicate participant ID found in session data.")

        self._set_variables(session_dict, False)
        self._on_update = on_update
        self._trigger_updates = True

    def update(self, session_dict: SessionDict):
        """Update the whole Session with the data in `session_dict`.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            New data that will be parsed into this SessionData.

        Raises
        ------
        ValueError
            If `session_dict` is of invalid type, has a different or missing (session)
            id than this SessionData.
        ErrorDictException
            If a participant with an ID unknown to the server exists in `session`.
            IDs must be generated by the backend.  In case this error occurs, the client
            tried to generate an ID.
            Also occurs if a duplicate participant ID was found.
        """
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
        """Get SessionData as dictionary.

        Returns
        -------
        custom_types.session.SessionDict
            SessionDict with the data in this SessionData.
        """
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
        """Set the variables of this data to the contents of `session_dict`.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            Session dictionary containing the data that should be set / parsed into this
            SessionData.
        final_trigger_updates_state : bool, default True
            State `self._trigger_updates` should be in after this function.

        Raises
        ------
        ValueError
            If `session_dict` is missing the (session) `id` variable.

        See Also
        --------
        _handle_updates() :
            Handle updates in data. See for information about `self._trigger_updates`.
        """
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
        """Handle updates in data, notify SessionManager about changes in data.

        Can be passed to modules.data.ParticipantData and other child data.

        Only notify SessionManager if `self._trigger_updates`.  `self._trigger_updates`
        can temporarily set to false to avoid sending multiple notifications when
        changing multiple variables.  See e.g. `update()` function
        """
        if self._trigger_updates:
            self._on_update(self.id)

    def __setattr__(self, _name: str, _value: Any) -> None:
        """Set attribute with `_name` to `_value` and trigger `self._on_update`."""
        object.__setattr__(self, _name, _value)
        try:
            # Signal a update, unless changing internal variable
            if _name != "_trigger_updates":
                self._handle_updates()
        except AttributeError:
            pass

    def _has_unknown_participant_ids(self, session_dict: SessionDict) -> bool:
        """Check if `session_dict` has participant IDs not known to this Session.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            Session dictionary that should be checked for unknown, and therefore
            invalid, participant IDs.  Ignores missing IDs.

        Returns
        -------
        bool
            True if there are unknown IDs, False if no unknown IDs where found.
        """
        participant_ids = get_filtered_participant_ids(session_dict)
        known_ids = self.participants.keys()

        for id in participant_ids:
            if id is None or id not in known_ids:
                return True

        return False


def _generate_participant_ids(session_dict: SessionDict) -> None:
    """Generate missing participant IDs in `session_dict`.

    Parameters
    ----------
    session_dict : custom_types.session.SessionDict
        Session dictionary where the participant ids will be generated in.
    """
    participant_ids = get_filtered_participant_ids(session_dict)
    for participant in session_dict.get("participants", []):
        id = participant.get("id")
        if id is None:
            # New participant without id
            new_id = generate_unique_id(participant_ids)
            participant_ids.append(new_id)
            participant["id"] = new_id
