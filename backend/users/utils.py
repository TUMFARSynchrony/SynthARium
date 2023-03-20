from aiortc import RTCSessionDescription

from modules.connection import connection_factory
from modules.connection_subprocess import connection_subprocess_factory
from modules.filter_api import FilterAPI
from modules.hub import Hub
from server import Config

from modules.data import ParticipantData
from users.experimenter import Experimenter
from users.participant import Participant
from modules.experiment import Experiment


async def participant_factory(
    offer: RTCSessionDescription,
    participant_id: str,
    experiment: Experiment,
    participant_data: ParticipantData,
    config: Config,
) -> tuple[RTCSessionDescription, Participant]:
    """Instantiate connection with a new Participant based on WebRTC `offer`.

    Instantiate new modules.participant.Participant, handle offer using
    modules.connection.connection_factory and set connection for the Participant.

    This sequence must be donne for all participants.  Instantiating a Participant
    directly will likely lead to problems, since it won't have a Connection.

    Parameters
    ----------
    participant_data : ParticipantData
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.
    participant_id : str
        Unique identifier for Participant.  Must exist in experiment.
    experiment : modules.experiment.Experiment
        Experiment the participant is part of.
    config : modules.config.Config
        Hub configuration / Config object.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.participant.Participant
        WebRTC answer that should be sent back to the client and Participant
        representing the client.
    """
    participant = Participant(participant_id, experiment, participant_data)
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
            filter_api,
            record_data
        )
    else:
        answer, connection = await connection_factory(
            offer,
            participant.handle_message,
            log_name_suffix,
            participant_data.audio_filters,
            participant_data.video_filters,
            filter_api,
            record_data
        )

    participant.set_connection(connection)
    return (answer, participant)


async def experimenter_factory(
    offer: RTCSessionDescription, experimenter_id: str, hub: Hub
) -> tuple[RTCSessionDescription, Experimenter]:
    """Instantiate connection with a new Experimenter based on WebRTC `offer`.

    Instantiate new modules.experimenter.Experimenter, handle offer using
    modules.connection.connection_factory and set connection for the Experimenter.

    This sequence must be donne for all experimenters.  Instantiating an Experimenter
    directly will likely lead to problems, since it wont have a Connection.

    Parameters
    ----------
    offer : aiortc.RTCSessionDescription
        WebRTC offer for building the connection to the client.
    experimenter_id : str
        Unique identifier for Experimenter.
    hub : modules.hub.Hub
        Hub the Experimenter will be part of.  Used for api calls.

    Returns
    -------
    tuple with aiortc.RTCSessionDescription, modules.experimenter.Experimenter
        WebRTC answer that should be sent back to the client and Experimenter
        representing the client.
    """
    experimenter = Experimenter(experimenter_id, hub)
    filter_api = FilterAPI(experimenter)
    log_name_suffix = f"E-{experimenter_id}"

    if hub.config.experimenter_multiprocessing:
        answer, connection = await connection_subprocess_factory(
            offer,
            experimenter.handle_message,
            log_name_suffix,
            hub.config,
            [],
            [],
            filter_api,
            (False, '')
        )
    else:
        answer, connection = await connection_factory(
            offer, experimenter.handle_message, log_name_suffix, [], [], filter_api, (False, '')
        )

    experimenter.set_connection(connection)
    return answer, experimenter
