from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hub.hub import Hub

from aiortc import RTCSessionDescription

from filter_api import FilterAPI
from connection.connection import connection_factory
from connection.connection_subprocess import connection_subprocess_factory

from users.experimenter import Experimenter


async def experimenter_factory(
    offer: RTCSessionDescription, experimenter_id: str, hub: Hub
) -> tuple[RTCSessionDescription, Experimenter]:
    """Instantiate connection with a new Experimenter based on WebRTC `offer`.

    Instantiate new hub.experimenter.Experimenter, handle offer using
    hub.connection.connection_factory and set connection for the Experimenter.

    This sequence must be donne for all experimenters.  Instantiating an Experimenter
    directly will likely lead to problems, since it won't have a Connection.

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
    tuple with aiortc.RTCSessionDescription, hub.experimenter.Experimenter
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
            [],
            [],
            filter_api,
            (False, ""),
        )
    else:
        answer, connection = await connection_factory(
            offer,
            experimenter.handle_message,
            log_name_suffix,
            [],
            [],
            [],
            [],
            filter_api,
            (False, ""),
        )

    experimenter.set_connection(connection)
    return answer, experimenter
