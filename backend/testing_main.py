"""Backend entry point for testing purposes.

After starting the hub, the connection test experiment (session id: bbbef1d7d0) is
automatically started.  The session ID and all Participant IDs will be printed for use
with the Connection test page.
"""

# import logging
from modules.exceptions import HubException
from modules.data import SessionData
from modules.hub import Hub
import asyncio

from custom_types.session import SessionDict


hub: Hub
session: SessionData | None

EXAMPLE_SESSION: SessionDict = {
    "id": "",
    "title": "TEST SESSION",
    "description": "Test session for testing backend - frontend communication.",
    "date": 1650380763073,
    "time_limit": 300,
    "record": False,
    "start_time": 0,
    "end_time": 0,
    "participants": [
        {
            "id": "",
            "first_name": "Max",
            "last_name": "Mustermann",
            "muted_audio": False,
            "muted_video": False,
            "filters": [],
            "position": {"x": 0, "y": 0, "z": 30},
            "size": {"width": 250, "height": 2000},
            "chat": [],
            "banned": False,
        },
        {
            "id": "",
            "first_name": "Erika",
            "last_name": "Mustermann",
            "muted_audio": False,
            "muted_video": False,
            "filters": [],
            "position": {"x": 100, "y": 200, "z": 300},
            "size": {"width": 100, "height": 100},
            "chat": [],
            "banned": False,
        },
    ],
    "start_time": 0,
    "end_time": 0,
    "notes": [],
    "log": [],
}


async def main():
    """Start the hub and the connection test experiment

    After starting the hub, the connection test experiment (session ID: bbbef1d7d0) is
    automatically started.  The session ID and all Participant IDs will be printed for
    use with the Connection test page.
    """
    global hub, EXAMPLE_SESSION, session

    # Uncomment bellow to get detailed logging from aiortc. You will need to install the
    # logging library.

    # logging.basicConfig(level=logging.DEBUG)
    # print("logger set")

    try:
        hub = Hub()
    except HubException as err:
        print("Failed to start hub. Error:", err)
        return

    await hub.start()

    # Create new Session
    session = hub.session_manager.get_session("bbbef1d7d0")
    if session is None:
        print("[ERROR] Failed to get test session.")
        return

    print("## Test Session Loaded ##")
    print("################################")
    print(f"##     Session ID: {session.id} ##")
    print("################################")

    for p in session.participants.values():
        print(f"## Participant ID: {p.id} ##")

    print("################################")

    hub.create_experiment(session.id)
    print("## Experiment Started - Connect now ##")

    # Run forever
    await asyncio.Event().wait()


async def stop():
    """Stop the experiment hub"""
    global hub, session
    await hub.stop()
    exit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Detected Keyboard Interrupt. Exiting...")
        loop.run_until_complete(stop())
    finally:
        loop.stop()
        print("Program finished.")
