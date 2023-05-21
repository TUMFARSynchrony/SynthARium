"""Backend entry point for testing purposes.

After starting the hub, the connection test experiment (session id: bbbef1d7d0) is
automatically started.  The session ID and all Participant IDs will be printed for use
with the Connection test page.
"""

# import logging
from session.data.session import SessionData
from hub.hub import Hub
import asyncio

from session.data.session import SessionDict


hub: Hub
session: SessionData | None


async def main():
    """Start the hub and the connection test experiment

    After starting the hub, the connection test experiment (session ID: bbbef1d7d0) is
    automatically started.  The session ID and all Participant IDs will be printed for
    use with the Connection test page.
    """
    global hub, session

    try:
        hub = Hub()
    except (ValueError, FileNotFoundError) as err:
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

    experiment = await hub.create_experiment(session.id)
    await experiment.start()

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
