"""Provide data classes for session, participant, size and position data.

Provides: `SessionData`, `ParticipantData`, `PositionData` and `SizeData` as well as
factory functions for `SessionData`: `session_data_factory` and `ParticipantData`:
`participant_data_factory`.
"""
from dataclasses import dataclass, field
from typing import Any, Callable
from pyee.asyncio import AsyncIOEventEmitter

from modules.util import generate_unique_id
from modules.exceptions import ErrorDictException

from custom_types.participant_summary import ParticipantSummaryDict
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
class _BaseDataClass(AsyncIOEventEmitter):
    """Base dataclass with update recognition and handling.

    When data is changed and `_emit_updates` is true, a `update` event is emitted with
    self as data.
    """

    _emit_updates: bool | None = field(repr=False, init=False, default=False)
    """If true, a `update` event is emitted on changes to class variables.

    Only disable temporarily for bulk updates.
    """

    def __post_init__(self):
        """Initialize AsyncIOEventEmitter and set `_emit_updates` to true."""
        super(_BaseDataClass, self).__init__()
        self._emit_updates = True

    def __setattr__(self, _name: str, _value: Any) -> None:
        """Recognize changes to variables in this class and call `_emit_update_event`.

        Ignores updates to private variables, including `_emit_updates` and private
        variables in parent class.
        """
        object.__setattr__(self, _name, _value)
        if _name[0] != "_":
            self._emit_update_event()

    def _emit_update_event(self, _=None):
        """Emit an `update` event if `_emit_updates` is true."""
        try:
            if self._emit_updates:
                print("_emit_update_event", self)
                self.emit("update", self)
        except AttributeError as e:
            pass


@dataclass(slots=True)
class SizeData(_BaseDataClass):
    """Size data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    width : int or float
    height : int or float

    Methods
    -------
    asdict()
        Get SizeData as dictionary.

    Note
    ----
    Special methods, such as __init__, __str__, __repr__ and equality checks are
    generated automatically by dataclasses.dataclass.
    """

    width: int | float
    height: int | float

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
    x : int or float
        x-coordinate
    y : int or float
        y-coordinate
    z : int or float
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

    x: int | float
    y: int | float
    z: int | float

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

    See Also
    --------
    participant_data_factory : create ParticipantData based on a ParticipantDict.

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
    """Size of participant on the canvas (frontend).

    Notes
    -----
    Replacing the size may break event listeners / emitters.  In case such functionality
    is required in the future, the following must be ensured: when size is replaced,
    this ParticipantData must listen and forward all SizeData "update" events.  Event
    listeners from the previous SizeData should also be removed.
    """

    muted_video: bool = field(repr=False)
    """Whether the participants' video is forcefully muted by the experimenter."""

    muted_audio: bool = field(repr=False)
    """Whether the participants' audio is forcefully muted by the experimenter."""

    position: PositionData = field(repr=False)
    """Position of the participant on the canvas (frontend).

    Notes
    -----
    Replacing the position may break event listeners / emitters.  In case such
    functionality is required in the future, the following must be ensured: when
    position is replaced, this ParticipantData must listen and forward all PositionData
    "update" events.  Event listeners from the previous PositionData should also be
    removed.
    """

    chat: list[ChatMessageDict] = field(repr=False)
    """Chat log between participant and experimenter."""

    filters: list[BasicFilterDict] = field(repr=False)
    """Active filters for participant."""

    def __post_init__(self) -> None:
        """Add event listener to size and position."""
        super(ParticipantData, self).__post_init__()
        self.size.add_listener("update", self._emit_update_event)
        self.position.add_listener("update", self._emit_update_event)

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

    def as_summary_dict(self) -> ParticipantSummaryDict:
        """Get non-sensitive key information from ParticipantData as dictionary.

        Returns
        -------
        custom_types.participant_summary.ParticipantSummaryDict
            ParticipantSummaryDict with some of the data in this ParticipantData.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "size": self.size.asdict(),
            "position": self.position.asdict(),
            "chat": self.chat,
        }


def participant_data_factory(participant_dict: ParticipantDict) -> ParticipantData:
    """Create a ParticipantData object based on a ParticipantDict.

    Parameters
    ----------
    participant_dict : custom_types.participant.ParticipantDict
        Participant dictionary with the data for the resulting ParticipantData

    Returns
    -------
    modules.data.ParticipantData
        ParticipantData based on the data in `participant_dict`.
    """
    size = participant_dict["size"]
    sizeData = SizeData(size["width"], size["width"])

    pos = participant_dict["position"]
    positionData = PositionData(pos["x"], pos["y"], pos["z"])
    return ParticipantData(
        participant_dict["id"],
        participant_dict["first_name"],
        participant_dict["last_name"],
        participant_dict["banned"],
        sizeData,
        participant_dict["muted_video"],
        participant_dict["muted_audio"],
        positionData,
        participant_dict["chat"],
        participant_dict["filters"],
    )


@dataclass(slots=True)
class SessionData(_BaseDataClass):
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

    See Also
    --------
    session_data_factory : create SessionData based on a SessionDict.

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

    Notes
    -----
    Note that this is a dict, while the participants in custom_types.session.SessionDict
    are a list.

    Replacing or modifying this dict may break event listeners / emitters.  In case such
    functionality is required in the future, the following must be ensured: when
    participants changes, this SessionData must listen and forward all ParticipantData
    "update" events.  When a participant is removed, event listeners must be removed as
    well.
    """

    # Variables with default values:
    log: Any = field(repr=False, default_factory=list)
    """TODO Document - log still wip"""

    end_time: int = field(repr=False, default=0)
    """Session end time in milliseconds since January 1, 1970, 00:00:00 (UTC)."""

    start_time: int = field(repr=False, default=0)
    """Session start time in milliseconds since January 1, 1970, 00:00:00 (UTC)."""

    def __post_init__(self):
        """Add event listener to participants."""
        super(SessionData, self).__post_init__()
        for participant in self.participants.values():
            participant.add_listener("update", self._emit_update_event)

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
        if session_dict["id"] != self.id:
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
        self._emit_update_event()

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
            "end_time": self.end_time,
            "start_time": self.start_time,
            "notes": self.notes,
            "participants": [p.asdict() for p in self.participants.values()],
            "log": self.log,
        }

        if self.log is not None:
            session_dict["log"] = self.log
        if self.end_time is not None:
            session_dict["end_time"] = self.end_time
        if self.start_time is not None:
            session_dict["start_time"] = self.start_time

        return session_dict

    def _set_variables(
        self, session_dict: SessionDict, final_emit_updates_value: bool = True
    ) -> None:
        """Set the variables of this data to the contents of `session_dict`.

        Parameters
        ----------
        session_dict : custom_types.session.SessionDict
            Session dictionary containing the data that should be set / parsed into this
            SessionData.
        final_emit_updates_value : bool, default True
            Value `self._emit_updates` should have after this function.

        Raises
        ------
        ValueError
            If `id` in `session_dict` is an empty string.

        See Also
        --------
        _handle_updates() :
            Handle updates in data. See for information about `self._trigger_updates`.
        """
        print("_set_variables")
        if session_dict["id"] == "":
            raise ValueError('Missing "id" in session dict.')

        self._emit_updates = False

        # Save simple variables
        self.id = session_dict["id"]
        self.title = session_dict["title"]
        self.date = session_dict["date"]
        self.record = session_dict["record"]
        self.time_limit = session_dict["time_limit"]
        self.description = session_dict["description"]
        self.notes = session_dict["notes"]
        self.log = session_dict["log"]
        self.end_time = session_dict["end_time"]
        self.start_time = session_dict["end_time"]

        # Remove event listeners from current participants (before deleting them)
        print("removing event listeners from old participants")
        for old_participant in self.participants.values():
            old_participant.remove_all_listeners()

        # Parse participants
        _generate_participant_ids(session_dict)
        self.participants = {}
        print("Generating new participants:\n  -> ", session_dict["participants"])
        for participant_dict in session_dict["participants"]:
            p = participant_data_factory(participant_dict)
            p.add_listener("update", self._emit_update_event)
            self.participants[p.id] = p

        self._emit_updates = final_emit_updates_value

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
            if id != "" and id not in known_ids:
                return True

        return False


def session_data_factory(session_dict: SessionDict) -> SessionData:
    """Create a SessionData object based on a SessionDict.

    Parameters
    ----------
    session_dict : custom_types.session.SessionDict
        Session dictionary with the data for the resulting SessionData

    Returns
    -------
    modules.data.SessionData
        SessionData based on the data in `session_dict`.

    Raises
    ------
    ValueError
        If `id` in `session_dict` is an empty string.
    ErrorDictException
        If a duplicate participant ID was found.
    """
    if session_dict["id"] == "":
        raise ValueError('Missing "id" in session dict.')

    if has_duplicate_participant_ids(session_dict):
        raise ErrorDictException(
            type="DUPLICATE_ID",
            code=400,
            description="Duplicate participant ID found in session data.",
        )

    _generate_participant_ids(session_dict)
    participants = {}
    for participant_dict in session_dict["participants"]:
        p = participant_data_factory(participant_dict)
        participants[p.id] = p

    return SessionData(
        session_dict["id"],
        session_dict["title"],
        session_dict["date"],
        session_dict["record"],
        session_dict["time_limit"],
        session_dict["description"],
        session_dict["notes"],
        participants,
        session_dict["log"],
    )


def _generate_participant_ids(session_dict: SessionDict) -> None:
    """Generate missing participant IDs in `session_dict`.

    Parameters
    ----------
    session_dict : custom_types.session.SessionDict
        Session dictionary where the participant ids will be generated in.
    """
    participant_ids = get_filtered_participant_ids(session_dict)
    for participant in session_dict["participants"]:
        id = participant["id"]
        if id == "":
            # New participant without id
            new_id = generate_unique_id(participant_ids)
            participant_ids.append(new_id)
            participant["id"] = new_id
