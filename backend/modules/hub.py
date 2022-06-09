"""Provide the `Hub` class, which is the center of the experiment hub."""

from typing import Literal, Optional
from aiortc import RTCSessionDescription
import asyncio
import logging

from custom_types.message import MessageDict
from custom_types.participant_summary import ParticipantSummaryDict

from modules.experiment import Experiment
from modules.config import Config
from modules.util import generate_unique_id
from modules.exceptions import ErrorDictException

import modules.server as _server
import modules.experiment as _experiment
import modules.experimenter as _experimenter
import modules.participant as _participant
import modules.session_manager as _sm


class Hub:
    """Central pice of the experiment hub backend.

    Attributes
    ----------
    TODO: document.  Some might be private.
    """

    experimenters: list[_experimenter.Experimenter]
    experiments: dict[str, _experiment.Experiment]
    session_manager: _sm.SessionManager
    server: _server.Server
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
            format="%(levelname)s:%(name)s: %(message)s",
            filename=self.config.log_file,
        )
        self._logger = logging.getLogger("Hub")
        self._logger.debug("Initializing Hub")

        # Set logging level for libraries
        dependencies_log_level = logging.getLevelName(self.config.log_dependencies)
        logging.getLogger("aiohttp").setLevel(dependencies_log_level)
        logging.getLogger("aioice").setLevel(dependencies_log_level)
        logging.getLogger("aiortc").setLevel(dependencies_log_level)
        logging.getLogger("PIL").setLevel(dependencies_log_level)

        self._logger.debug(f"Successfully loaded config: {str(self.config)}")

        self.experimenters = []
        self.experiments = {}
        self.session_manager = _sm.SessionManager("sessions")
        self.server = _server.Server(self.handle_offer, self.config)

    async def start(self):
        """Start the hub.  Starts the server."""
        await self.server.start()

    async def stop(self):
        """Stop the hub, close all connection and stop the server."""
        self._logger.info("Stopping Hub")
        for experiment in self.experiments.values():
            await experiment.stop()
        tasks = [self.server.stop()]
        for experimenter in self.experimenters:
            tasks.append(experimenter.disconnect())

        await asyncio.gather(*tasks)

    def remove_experimenter(self, experimenter: _experimenter.Experimenter):
        """Remove an experimenter from this hub.

        Should be used when a experimenter connection is closed or failed.

        Does not close the connection on the experimenter or remove it from experiments.

        Parameters
        ----------
        experimenter : modules.experimenter.Experimenter
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
        participant_id: Optional[str],
        session_id: Optional[str],
    ) -> tuple[RTCSessionDescription, ParticipantSummaryDict | None]:
        """Handle incoming offer from a client.

        This function is intended to be passed down to the modules.server.Server, which
        will call it after checking and parsing an incoming offer.

        Parameters
        ----------
        offer : aiortc.RTCSessionDescription
            WebRTC offer.
        user_type : str, "participant" or "experimenter"
            Type of user that wants to connect.
        participant_id : str, optional
            ID of participant.
        session_id : str, optional
            Session ID, defining what session a participant wants to connect to (if
            user_type is "participant").

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
            id = generate_unique_id([e.id for e in self.experimenters])
            answer, experimenter = await _experimenter.experimenter_factory(
                offer, id, self
            )
            self.experimenters.append(experimenter)

        else:
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Invalid user_type."
            )

        return (answer, None)

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
        participant = experiment.session.participants.get(participant_id)
        if participant is None:
            self._logger.warning(
                f"Participant {participant_id} not found in session: {session_id}"
            )
            raise ErrorDictException(
                code=400,
                type="UNKNOWN_PARTICIPANT",
                description="Participant not found in the given session.",
            )

        if participant.banned:
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

        answer, _ = await _participant.participant_factory(
            offer, participant_id, experiment, participant
        )

        return (answer, participant.as_summary_dict())

    def create_experiment(self, session_id: str) -> Experiment:
        """Create a new Experiment based on existing session data.

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

        experiment = Experiment(session)
        self.experiments[session_id] = experiment
        return experiment

    async def send_to_experimenters(self, data: MessageDict):
        """Send `data` to all connected experimenters.

        Can be used to inform experimenters about changes to sessions.

        Parameters
        ----------
        data : custom_types.message.MessageDict
            Message for the experimenters.
        """
        for experimenter in self.experimenters:
            await experimenter.send(data)
