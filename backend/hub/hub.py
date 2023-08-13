"""Provide the `Hub` class, which is the center of the experiment hub."""

from typing import Literal, Optional
from aiortc import RTCSessionDescription
import asyncio
import logging
import json

from custom_types.message import MessageDict
from session.data.participant.participant_summary import ParticipantSummaryDict

from experiment import Experiment
from hub.util import generate_unique_id
from hub.exceptions import ErrorDictException
from hub.util import get_system_specs

from filters.filter import Filter

import experiment.experiment as _experiment
import session.session_manager as _sm

from server import Config, Server
from users import Experimenter, experimenter_factory, participant_factory


class Hub:
    """Central piece of the experiment hub backend.

    Attributes
    ----------
    TODO: document.  Some might be private.
    """

    experimenters: list[Experimenter]
    experiments: dict[str, _experiment.Experiment]
    session_manager: _sm.SessionManager
    server: Server
    config: Config
    _logger: logging.Logger

    def __init__(self):
        """Parse config and instantiate new Hub instance.

        Raises
        ------
        ValueError
            If a key in `backend/config.json` is missing or has the wrong type.
        FileNotFoundError
            If one of the files refereed to by ssl_cert, ssl_key or logging_file is not
            found.
        """
        self.config = Config()

        # Setup logging
        logging.basicConfig(
            level=logging.getLevelName(self.config.log),
            format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
            filename=self.config.log_file,
        )
        self._logger = logging.getLogger("Hub")
        self._logger.debug("Initializing Hub")
        self._logger.debug(f"System: {get_system_specs()}")

        # Set logging level for libraries
        dependencies_log_level = logging.getLevelName(self.config.log_dependencies)
        logging.getLogger("aiohttp").setLevel(dependencies_log_level)
        logging.getLogger("aioice").setLevel(dependencies_log_level)
        logging.getLogger("aiortc").setLevel(dependencies_log_level)
        logging.getLogger("PIL").setLevel(dependencies_log_level)

        self._logger.debug(f"Successfully loaded config: {str(self.config)}")

        self.get_filters_config()

        self.experimenters = []
        self.experiments = {}
        self.session_manager = _sm.SessionManager("sessions")
        self.server = Server(self.handle_offer, self.config)

    async def start(self):
        """Start the hub.  Starts the server."""
        await self.server.start()

    async def stop(self):
        """Stop the hub, close all connection and stop the server."""
        self._logger.info("Stopping Hub")
        for experiment in self.experiments.values():
            try:
                await experiment.stop()
            except ErrorDictException:
                pass
            experiment.session.creation_time = 0
        tasks = [self.server.stop()]
        for experimenter in self.experimenters:
            tasks.append(experimenter.disconnect())

        await asyncio.gather(*tasks)

    def remove_experimenter(self, experimenter: Experimenter):
        """Remove an experimenter from this hub.

        Should be used when a experimenter connection is closed or failed.

        Does not close the connection on the experimenter or remove it from experiments.

        Parameters
        ----------
        experimenter : hub.experimenter.Experimenter
            Experimenter that will be removed from the hub

        Raises
        ------
        ValueError
            If the given `experimenter` is not part of this experiment.
        """
        self.experimenters.remove(experimenter)

    async def handle_offer(
        self,
        offer: RTCSessionDescription,
        user_type: Literal["participant", "experimenter"],
        participant_id: str | None,
        session_id: str | None,
        experimenter_password: str | None,
    ) -> tuple[RTCSessionDescription, ParticipantSummaryDict | None]:
        """Handle incoming offer from a client.

        This function is intended to be passed down to the hub.server.Server, which
        will call it after checking and parsing an incoming offer.

        Parameters
        ----------
        offer : aiortc.RTCSessionDescription
            WebRTC offer.
        user_type : str, "participant" or "experimenter"
            Type of user that wants to connect.
        participant_id : str or None
            ID of participant.
        session_id : str or None
            Session ID, defining what session a participant wants to connect to (if
            user_type is "participant").
        experimenter_password : str or None
            Experimenter password to authenticate experimenter.  Can be set in config.

        Returns
        -------
        tuple of aiortc.RTCSessionDescription and either
        custom_types.participant_summary.ParticipantSummaryDict or None
            Second variable in tuple is None if user_type is not participant.

        Raises
        ------
        ErrorDictException
            If user_type is not "participant" or "experimenter".
            In case the user_type is participant: If the session or participant was not
            found or the participant is banned.
        """
        if user_type == "participant":
            return await self._handle_offer_participant(
                offer, participant_id, session_id
            )

        elif user_type == "experimenter":
            # Check authentication
            if (
                experimenter_password is None
                or experimenter_password != self.config.experimenter_password
            ):
                raise ErrorDictException(
                    code=401,
                    type="INVALID_REQUEST",
                    description="Invalid or missing experimenter password.",
                )

            experimenter_id = "E" + generate_unique_id(
                [e.id for e in self.experimenters]
            )
            answer, experimenter = await experimenter_factory(
                offer, experimenter_id, self
            )
            self.experimenters.append(experimenter)

            # Remove experimenter from hub when experimenter disconnects
            experimenter.add_listener("disconnected", self.remove_experimenter)
        else:
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Invalid user_type."
            )

        return answer, None

    async def _handle_offer_participant(
        self,
        offer: RTCSessionDescription,
        participant_id: Optional[str],
        session_id: Optional[str],
    ) -> tuple[RTCSessionDescription, ParticipantSummaryDict]:
        """Handle incoming offer for a participant.

        Parameters
        ----------
        offer : aiortc.RTCSessionDescription
            WebRTC offer.
        participant_id : str, optional
            ID of participant.  Will raise an ErrorDictException if missing.
        session_id : str, optional
            Session ID, defining what session a participant wants to connect to (if
            user_type is "participant").  Will raise an ErrorDictException if missing.

        Returns
        -------
        tuple of aiortc.RTCSessionDescription and
        custom_types.participant_summary.ParticipantSummaryDict

        Raises
        ------
        ErrorDictException
            if session_id or participant_id are not defined, the session or participant
            was not found or the participant is banned.

        Notes
        -----
        participant_id and session_id are only optional to allow this function to be
        called in handle_offer without extra checks.  In case one of them is missing,
        this function will raise the exception with a fitting error message.
        """
        if participant_id is None:
            self._logger.warning("Missing participant_id in offer handler")
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Missing participant_id."
            )

        if session_id is None:
            self._logger.warning("Missing session_id in offer handler")
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Missing session_id."
            )

        if session_id not in self.experiments:
            self._logger.warning(
                f"No experiment for session ID {session_id} found. "
                f"Participant {participant_id} failed to join"
            )
            raise ErrorDictException(
                code=400, type="UNKNOWN_SESSION", description="Session not found."
            )

        experiment = self.experiments[session_id]
        participant_data = experiment.session.participants.get(participant_id)
        if participant_data is None:
            self._logger.warning(
                f"Participant {participant_id} not found in session: {session_id}"
            )
            raise ErrorDictException(
                code=400,
                type="UNKNOWN_PARTICIPANT",
                description="Participant not found in the given session.",
            )

        if participant_data.banned:
            raise ErrorDictException(
                code=400,
                type="BANNED_PARTICIPANT",
                description=(
                    "You have been banned and can no longer join the experiment."
                ),
            )

        if participant_id in experiment.participants:
            raise ErrorDictException(
                code=409,
                type="PARTICIPANT_ALREADY_CONNECTED",
                description=(
                    "You are already connected to the experiment. Participants can not "
                    "have multiple simultaneous connections."
                ),
            )

        answer, _ = await participant_factory(
            offer, participant_id, experiment, participant_data, self, self.config
        )

        return answer, participant_data.as_summary_dict()

    async def create_experiment(self, session_id: str) -> Experiment:
        """Create a new Experiment based on existing session data.

        Also send a `EXPERIMENT_CREATED` message to all experimenters, if experiment was
        successfully created.

        Parameters
        ----------
        session_id : str
            ID for session data the experiment should be based on.

        Raises
        ------
        ErrorDictException
            If experiment already exists or there is no session with `session_id`.
        """
        # Check if experiment already exists
        if session_id in self.experiments:
            raise ErrorDictException(
                code=409,
                type="INVALID_REQUEST",
                description="Experiment already exists.",
            )

        # Load session data for experiment
        session = self.session_manager.get_session(session_id)
        if session is None:
            raise ErrorDictException(
                code=400,
                type="UNKNOWN_SESSION",
                description="No session with the given ID found.",
            )

        # Create Experiment
        experiment = Experiment(session)
        self.experiments[session_id] = experiment

        # Notify all experimenters about the new experiment
        message = MessageDict(
            type="EXPERIMENT_CREATED",
            data={
                "session_id": session_id,
                "creation_time": experiment.session.creation_time,
            },
        )
        await self.send_to_experimenters(message)

        return experiment

    async def send_to_experimenters(
        self, data: MessageDict, exclude: Experimenter | None = None
    ):
        """Send `data` to all connected experimenters.

        Can be used to inform experimenters about changes to sessions.

        Parameters
        ----------
        data : custom_types.message.MessageDict
            Message for the experimenters.
        exclude : hub.experimenter.Experimenter, default None
            Optional `Experimenter` that will be ignored.
        """
        for experimenter in self.experimenters:
            if experimenter is not exclude:
                await experimenter.send(data)

    def get_filters_config(self):
        filters_config = {"filters": []}
        # TODO: add get_config_json in all filters files
        for filter in Filter.__subclasses__():
            filter_name = filter.name(filter)
            if (
                filter_name == "ROTATION"
                or filter_name == "FILTER_API_TEST"
                or filter_name == "AUDIO_SPEAKING_TIME"
            ):
                filters_config["filters"].append(filter.get_config_json(filter))

        # Syntax of write JSON data to file
        # TODO: change path to frontend file
        path = "./frontend/src/data.json"
        with open(path, "w") as outfile:
            # json_data refers to the above JSON
            json.dump(filters_config, outfile)

        return filters_config
