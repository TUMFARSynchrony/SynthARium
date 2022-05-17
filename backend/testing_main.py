"""Backend entry point for testing purposes."""

from modules.data import SessionData
from modules.config import Config
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
    global hub, EXAMPLE_SESSION, session

    try:
        config = Config()
    except ValueError as err:
        print("ERROR: Failed to load config:", err)
        print("Aborting start. Please fix error above.")
        return

    hub = Hub(config)
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
        # asyncio.run(main())
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Detected Keyboard Interrupt. Exiting...")
        loop.run_until_complete(stop())
    finally:
        loop.stop()
        print("Program finished.")
