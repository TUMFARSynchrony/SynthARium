"""Utility functions for tests modules."""

from typing import Any

from custom_types.size import SizeDict
from custom_types.note import NoteDict
from custom_types.session import SessionDict
from custom_types.position import PositionDict
from custom_types.filters import BasicFilterDict
from custom_types.participant import ParticipantDict
from custom_types.chat_message import ChatMessageDict


def testing_size_dict_factory(
    width: int = 0,
    height: int = 0,
) -> SizeDict:
    """Create a valid custom_types.size.SizeDict with default values."""
    return SizeDict(
        width=width,
        height=height,
    )


def testing_position_dict_factory(
    x: int = 0,
    y: int = 0,
    z: int = 0,
) -> PositionDict:
    """Create a valid custom_types.position.PositionDict with default values."""
    return PositionDict(
        x=x,
        y=y,
        z=z,
    )


def testing_participant_dict_factory(
    id: str = "factory_id",
    first_name: str = "factory_first_name",
    last_name: str = "factory_last_name",
    muted_video: bool = False,
    muted_audio: bool = False,
    filters: list[BasicFilterDict] = [],
    position: PositionDict = testing_position_dict_factory(),
    size: SizeDict = testing_size_dict_factory(),
    chat: list[ChatMessageDict] = [],
    banned: bool = False,
) -> ParticipantDict:
    """Create a valid custom_types.participant.ParticipantDict with default values."""
    return ParticipantDict(
        id=id,
        first_name=first_name,
        last_name=last_name,
        muted_video=muted_video,
        muted_audio=muted_audio,
        filters=filters,
        position=position,
        size=size,
        chat=chat,
        banned=banned,
    )


def testing_session_dict_factory(
    id: str = "factory_id",
    title: str = "factory_title",
    description: str = "factory_description",
    date: int = 0,
    time_limit: int = 0,
    record: bool = True,
    participants: list[ParticipantDict] = [],
    start_time: int = 0,
    end_time: int = 0,
    notes: list[NoteDict] = [],
    log: Any = [],
) -> SessionDict:
    """Create a valid custom_types.session.SessionDict with default values."""
    return SessionDict(
        id=id,
        title=title,
        description=description,
        date=date,
        time_limit=time_limit,
        record=record,
        participants=participants,
        start_time=start_time,
        end_time=end_time,
        notes=notes,
        log=log,
    )
