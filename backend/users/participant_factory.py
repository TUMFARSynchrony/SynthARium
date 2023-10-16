from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from experiment import Experiment

if TYPE_CHECKING:
    from hub.hub import Hub

from aiortc import RTCSessionDescription

from connection.connection import connection_factory
from connection.connection_subprocess import connection_subprocess_factory
from session.data.participant import ParticipantData
from filter_api import FilterAPI

from server import Config
from users.participant import Participant


async def participant_factory(
    offer: RTCSessionDescription,
    participant_id: str,
    experiment: Experiment,
    participant_data: ParticipantData,
    hub: Hub,
    config: Config,
) -> tuple[RTCSessionDescription, Participant]:
    """Instantiate connection with a new Participant based on WebRTC `offer`.

    Instantiate new hub.participant.Participant, handle offer using
    hub.connection.connection_factory and set connection for the Participant.

    This sequence must be donne for all participants.  Instantiating a Participant
    directly will likely lead to problems, since it won't have a Connection.

    Parameters
    ----------
    participant_data : ParticipantData
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.
    participant_id : str
        Unique identifier for Participant.  Must exist in experiment.
    experiment : hub.experiment.Experiment
        Experiment the participant is part of.
    config : hub.config.Config
        Hub configuration / Config object.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, hub.participant.Participant
        WebRTC answer that should be sent back to the client and Participant
        representing the client.
    """
    participant = Participant(participant_id, experiment, participant_data, hub)
    filter_api = FilterAPI(participant)
    record_data = (experiment.session.record, participant.get_recording_path())
    log_name_suffix = f"P-{participant_id}"

    if config.participant_multiprocessing:
        answer, connection = await connection_subprocess_factory(
            offer,
            participant.handle_message,
            log_name_suffix,
            config,
            participant_data.audio_filters,
            participant_data.video_filters,
            participant_data.audio_group_filters,
            participant_data.video_group_filters,
            filter_api,
            record_data,
        )
    else:
        answer, connection = await connection_factory(
            offer,
            participant.handle_message,
            log_name_suffix,
            participant_data.audio_filters,
            participant_data.video_filters,
            participant_data.audio_group_filters,
            participant_data.video_group_filters,
            filter_api,
            record_data,
        )

    participant.set_connection(connection)
    return answer, participant
