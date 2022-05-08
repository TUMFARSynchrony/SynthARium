"""Provide the `Hub` class, which is the center of the experiment hub."""

from typing import Literal, Optional
from aiortc import RTCSessionDescription
import asyncio

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

    def __init__(self, config: Config):
        """Instantiate new Hub instance.

        Parameters
        ----------
        config : modules.config.Config
            Configuration for the hub.
        """
        print("[Hub] Initializing Hub")
        self.experimenters = []
        self.experiments = {}
        self.config = config
        self.session_manager = _sm.SessionManager("sessions")
        self.server = _server.Server(
            self.handle_offer, config.host, config.port, config.environment == "dev"
        )

    async def start(self):
        """Start the hub.  Starts the server."""
        await self.server.start()

    async def stop(self):
        """Stop the hub, close all connection and stop the server."""
        print("[Hub] stopping")
        tasks = [self.server.stop()]
        for experimenter in self.experimenters:
            tasks.append(experimenter.disconnect())
        for experiment in self.experiments.values():
            experiment.stop()

        await asyncio.gather(*tasks)

    async def handle_offer(
        self,
        offer: RTCSessionDescription,
        user_type: Literal["participant", "experimenter"],
        participant_id: Optional[str],
        session_id: Optional[str],
    ):
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

        Raises
        ------
        ErrorDictException
            If user_type is not "participant" or "experimenter".
        """
        if user_type == "participant":
            answer = await self._handle_offer_participant(
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
        return answer

    async def _handle_offer_participant(
        self,
        offer: RTCSessionDescription,
        participant_id: Optional[str],
        session_id: Optional[str],
    ):
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

        Raises
        ------
        ErrorDictException
            if session_id or participant_id are not defined.

        Notes
        -----
        participant_id and session_id are only optional to allow this function to be
        called in handle_offer without extra checks.  In case one of them is missing,
        this function will raise the exception with a fitting error message.
        """
        if participant_id is None:
            print("[Hub] WARNING: Missing participant_id in offer handler")
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Missing participant_id."
            )

        if session_id is None:
            print("[Hub] WARNING: Missing session_id in offer handler")
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Missing session_id."
            )

        if session_id not in self.experiments:
            print(
                f"[Hub] WARNING: session {session_id} not found.",
                f"Participant {participant_id} failed to join",
            )
            raise ErrorDictException(
                code=400, type="UNKNOWN_SESSION", description="Session not found."
            )

        experiment = self.experiments[session_id]
        if not experiment.knows_participant_id(participant_id):
            print(
                f"[Hub] WARNING: participant {participant_id} not found in session:",
                session_id,
            )
            raise ErrorDictException(
                code=400,
                type="UNKNOWN_PARTICIPANT",
                description="Participant not found in the given session.",
            )

        answer, participant = await _participant.participant_factory(
            offer, participant_id, experiment
        )
        experiment.add_participant(participant)

        return answer

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
