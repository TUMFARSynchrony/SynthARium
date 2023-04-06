from dataclasses import dataclass, field

from session.data.base_data import BaseData
from session.data.position.position_data import PositionData
from session.data.size.size_data import SizeData


@dataclass(slots=True)
class ParticipantData(BaseData):
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
    filters : list or filters.FilterDict

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

    audio_filters: list[FilterDict] = field(repr=False)
    """Active audio filters for participant."""

    video_filters: list[FilterDict] = field(repr=False)
    """Active video filters for participant."""

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
            "audio_filters": self.audio_filters,
            "video_filters": self.video_filters,
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
