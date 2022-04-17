"""Backend entry point"""

from modules.hub import Hub
import asyncio

_hub: Hub


async def main():
    """TODO document"""
    global _hub
    _hub = Hub("127.0.0.1", 8080)
    await _hub.start()

    # Run forever

    await asyncio.Event().wait()


async def stop():
    """TODO document"""
    global _hub
    await _hub.stop()
    exit()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detected Keyboard Interrupt. Exiting...")
        asyncio.run(stop())
    finally:
        print("Cleanup complete")
        exit()
