"""TODO document"""

import json
from typing import Any, Callable, Coroutine, Literal
from aiohttp import web
from datetime import datetime
from aiortc import RTCSessionDescription

from _types.message import MessageDict
from _types.error import ErrorDict


class Server():
    """TODO document"""
    _HANDLER = Callable[
        [RTCSessionDescription, Literal["participant", "experimenter"]],
        Coroutine[Any, Any, RTCSessionDescription | ErrorDict]]

    _hub_handle_offer: _HANDLER
    _app: web.Application
    _runner: web.AppRunner
    _host: str
    _port: int

    def __init__(self, hub_handle_offer: _HANDLER, host: str, port: int):
        """TODO document"""
        self._hub_handle_offer = hub_handle_offer
        self._host = host
        self._port = port

        self._app = web.Application()
        self._app.on_shutdown.append(self._shutdown)
        self._app.router.add_get("/", self.get_hello_world)
        self._app.router.add_get("/offer", self.handle_offer)

    async def start(self):
        """TODO document"""
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
        """TODO document"""
        print("[SERVER] Server stopping")
        await self._app.shutdown()
        await self._app.cleanup()

    async def get_hello_world(self, request: web.Request) -> web.StreamResponse:
        """Placeholder for testing if the server is accessible"""
        print("[SERVER] Get hello world")
        return web.Response(content_type="application/json", text=json.dumps({
            "text": "Hello World",
            "timestamp": str(datetime.now())
        }))

    async def _parse_offer_request(self, request: web.Request) -> dict:
        """TODO document"""
        if request.content_type != "application/json":
            error = ErrorDict(
                code=400, type="EXAMPLE_TYPE",  # TODO adjust type
                description="Content type must be 'application/json'")
            raise _OfferParserException(error)

        # Parse request
        try:
            params: dict = await request.json()
        except json.JSONDecodeError:
            error = ErrorDict(code=400,
                              type="EXAMPLE_TYPE",  # TODO adjust type
                              description="Failed to parse request")
            raise _OfferParserException(error)

        # Check if all required keys exist in params
        required_keys = ["sdp", "type", "user_type"]
        missing_keys = list(
            filter(lambda key: key not in params, required_keys))
        if len(missing_keys) > 0:
            error_description = f"Missing request parameters: {missing_keys}"
            error = ErrorDict(code=400,
                              type="EXAMPLE_TYPE",  # TODO adjust type
                              description=error_description)
            raise _OfferParserException(error)
        # Successfully parsed parameters
        return params

    async def handle_offer(self, request: web.Request) -> web.StreamResponse:
        """TODO document"""
        print(f"[SERVER] Handle offer from {request.host}")
        try:
            params = await self._parse_offer_request(request)
        except _OfferParserException as error:
            error_message = MessageDict(type="ERROR", data=error.args[0])
            return web.Response(content_type="application/json",
                                text=json.dumps(error_message))

        # Try to parse request
        try:
            offer = RTCSessionDescription(
                sdp=params["sdp"], type=params["type"])
        except ValueError:
            error = ErrorDict(code=400,
                              type="EXAMPLE_TYPE",  # TODO adjust type
                              description="Failed to parse offer")
            error_message = MessageDict(type="ERROR", data=error)
            return web.Response(content_type="application/json",
                                text=json.dumps(error_message))

        response = await self._hub_handle_offer(offer, params["user_type"])

        # Create answer according to response
        if type(response) == RTCSessionDescription:
            answer = MessageDict(type="SESSION_DESCRIPTION", data=response)
        elif type(response) == ErrorDict:
            answer = MessageDict(type="ERROR", data=response)
        else:
            print("ERROR: unrecognized response type from hub_handle_offer")
            error = ErrorDict(
                code=500, type="EXAMPLE_TYPE",  # TODO adjust type
                description="Internal server error: failed to handle offer")
            answer = MessageDict(type="ERROR", data=error)

        return web.Response(content_type="application/json",
                            text=json.dumps(answer))

    def get_index(self):
        """TODO document"""
        pass

    def get_css(self):
        """TODO document"""
        pass

    def get_javascript(self):
        """TODO document"""
        pass


class _OfferParserException(Exception):
    """Custom exception for Server._parse_offer_request().
    Should contain an ErrorDict that can be send as a response.
    """
    pass
