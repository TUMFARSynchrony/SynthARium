"""TODO document"""


from typing import Awaitable, Callable, Any
from aiohttp import web
import json
from datetime import datetime


class Server():
    """TODO document"""
    _hub_handle_offer: Callable[[Any], None]
    _app: web.Application
    _runner: web.AppRunner
    _host: str
    _port: int

    def __init__(self, hub_handle_offer: Callable[[Any], None], host: str,
                 port: int):
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

    async def handle_offer(self, request: web.Request) -> web.StreamResponse:
        """TODO document"""
        print("[SERVER] Handle offer")
        self._hub_handle_offer(None)
        return web.Response(content_type="application/json", text=json.dumps({
            "text": "Received your offer",
            "todo": "Implement",
            "timestamp": str(datetime.now())
        }))

    def get_index(self):
        """TODO document"""
        pass

    def get_css(self):
        """TODO document"""
        pass

    def get_javascript(self):
        """TODO document"""
        pass
