"""Backend entry point"""

from modules.config import Config
from modules.hub import Hub
import asyncio

_hub: Hub


async def main():
    """Entry point for experiment Hub.

    Creates a modules.config.Config and modules.hub.Hub.  Then waits for ever.
    Close with KeyboardInterrupt.
    """
    global _hub

    try:
        config = Config()
    except ValueError as err:
        print("ERROR: Failed to load config:", err)
        print("Aborting start. Please fix error above.")
        return

    _hub = Hub(config)
    await _hub.start()

    # Run forever
    await asyncio.Event().wait()


async def stop():
    """Stop the experiment hub"""
    global _hub
    await _hub.stop()
    exit()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detected Keyboard Interrupt. Exiting...")
        asyncio.run(stop())
