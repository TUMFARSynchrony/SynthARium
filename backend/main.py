"""Backend entry point"""

from hub.hub import Hub
import asyncio

_hub: Hub


async def main():
    """Entry point for experiment Hub.

    Creates a hub.hub.Hub.  Then waits forever.
    Close with KeyboardInterrupt.
    """
    global _hub

    try:
        _hub = Hub()
    except (ValueError, FileNotFoundError) as err:
        print("Failed to start hub. Error:", err)
        return

    await _hub.start()

    # Run forever
    await asyncio.Event().wait()


async def stop():
    """Stop the experiment hub"""
    global _hub
    await _hub.stop()
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
