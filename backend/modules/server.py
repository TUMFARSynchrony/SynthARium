"""Provides the Server class, which serves the frontend and other endpoints."""

import aiohttp_cors
import json
from typing import Any, Callable, Coroutine, Literal, Optional
from aiohttp import web
from datetime import datetime
from aiortc import RTCSessionDescription

from custom_types.message import MessageDict
from custom_types.error import ErrorDict

from modules.exceptions import ErrorDictException


class Server:
    """Server providing the website and an endpoint to establish WebRTC connections."""

    _HANDLER = Callable[
        [
            RTCSessionDescription,
            Literal["participant", "experimenter"],
            Optional[str],
            Optional[str],
        ],
        Coroutine[Any, Any, RTCSessionDescription],
    ]

    _hub_handle_offer: _HANDLER
    _app: web.Application
    _runner: web.AppRunner
    _host: str
    _port: int

    def __init__(
        self, hub_handle_offer: _HANDLER, host: str, port: int, use_cors=False
    ):
        """Instantiate new Server instance.

        Parameters
        ----------
        hub_handle_offer : function
            Handler function for incoming WebRTC offers.
        host : str
            Host address for server.
        port : int
            Port for server.
        use_cors : bool, default False
            If true, cors will be enabled for *.  Should only be used for development.
        """
        self._hub_handle_offer = hub_handle_offer
        self._host = host
        self._port = port

        self._app = web.Application()
        self._app.on_shutdown.append(self._shutdown)
        routes = []
        routes.append(self._app.router.add_get("/", self.get_hello_world))
        routes.append(self._app.router.add_get("/offer", self.handle_offer))

        if not use_cors:
            return

        # Using cors is only intended for development, when the client is not hosted by
        # this server but a separate development server.
        print("[SERVER] WARNING: Using CORS. Only use for development!")

        cors = aiohttp_cors.setup(self._app)  # type: ignore
        for route in routes:
            cors.add(
                route,
                {
                    "*": aiohttp_cors.ResourceOptions(
                        allow_credentials=True,
                        expose_headers=("X-Custom-Server-Header",),
                        allow_methods=["GET"],
                        allow_headers=("X-Requested-With", "Content-Type"),
                    )
                },
            )

    async def start(self):
        """Start the server."""
        print(f"[SERVER] Starting server on http://{self._host}:{self._port}")
        # Set up aiohttp - like run_app, but non-blocking
        # (Source: https://stackoverflow.com/a/53465910)
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, host=self._host, port=self._port)
        await site.start()

    async def _shutdown(self, app: web.Application):
        """TODO document"""
        pass

    async def stop(self):
        """Stop the server."""
        print("[SERVER] Server stopping")
        await self._app.shutdown()
        await self._app.cleanup()

    async def get_hello_world(self, request: web.Request) -> web.StreamResponse:
        """Placeholder for testing if the server is accessible"""
        print("[SERVER] Get hello world")
        return web.Response(
            content_type="application/json",
            text=json.dumps({"text": "Hello World", "timestamp": str(datetime.now())}),
        )

    async def _parse_offer_request(self, request: web.Request) -> dict:
        """Parse a request made to the `/offer` endpoint.

        Checks the parameters in the request and check if the types are correct.

        Parameters
        ----------
        request : aiohttp.web.Request
            Incoming request to the `/offer` endpoint.

        Returns
        -------
        dict
            Parsed offer request.

        Raises
        ------
        ErrorDictException
            If any error occurres while parsing.  E.g. incorrect request parameters or
            missing keys.
        """
        if request.content_type != "application/json":
            raise ErrorDictException(
                code=415,
                type="INVALID_REQUEST",
                description="Content type must be 'application/json'.",
            )

        # Parse request
        try:
            params: dict = await request.json()
        except json.JSONDecodeError:
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Failed to parse request."
            )

        # Check if all required keys exist in params
        required_keys = ["sdp", "type", "user_type"]
        if params["user_type"] == "participant":
            required_keys.extend(["session_id", "participant_id"])

        missing_keys = list(filter(lambda key: key not in params, required_keys))

        if len(missing_keys) > 0:
            raise ErrorDictException(
                code=400,
                type="INVALID_REQUEST",
                description=f"Missing request parameters: {missing_keys}.",
            )

        # Check if user_type is valid
        if params["user_type"] not in ["participant", "experimenter"]:
            raise ErrorDictException(
                code=400, type="INVALID_REQUEST", description="Invalid user type."
            )

        # Successfully parsed parameters
        return params

    async def handle_offer(self, request: web.Request) -> web.StreamResponse:
        """Handle incoming requests to the `/offer` endpoint.

        Parameters
        ----------
        request : aiohttp.web.Request
            Incoming request to the `/offer` endpoint.

        Returns
        -------
        aiohttp.web.StreamResponse
            Response to request from client.
        """
        print(f"[SERVER] Handle offer from {request.host}")
        # Check and parse request.
        try:
            params = await self._parse_offer_request(request)
        except ErrorDictException as error:
            return web.Response(
                content_type="application/json",
                status=error.code,
                reason=error.description,
                text=error.error_message_str,
            )

        # Create session description based on request.
        try:
            offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        except ValueError:
            error_description = "Failed to parse offer."
            error = ErrorDict(
                code=400, type="INVALID_REQUEST", description=error_description
            )
            error_message = MessageDict(type="ERROR", data=error)
            return web.Response(
                content_type="application/json",
                status=400,
                reason=error_description,
                text=json.dumps(error_message),
            )

        # Pass request to handler function in hub.
        try:
            response = await self._hub_handle_offer(
                offer,
                params["user_type"],
                params.get("participant_id"),
                params.get("session_id"),
            )
        except ErrorDictException as error:
            return web.Response(
                content_type="application/json",
                status=error.code,
                reason=error.description,
                text=error.error_message_str,
            )

        # Create response
        answer = MessageDict(type="SESSION_DESCRIPTION", data=response)
        return web.Response(content_type="application/json", text=json.dumps(answer))

    def get_index(self):
        """TODO document"""
        pass

    def get_css(self):
        """TODO document"""
        pass

    def get_javascript(self):
        """TODO document"""
        pass
