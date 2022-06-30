import asyncio
import json
from argparse import ArgumentParser
import sys
from typing import Tuple
from aiortc import RTCSessionDescription

from custom_types.connection import (
    is_valid_rtc_session_description_dict,
    RTCSessionDescriptionDict,
)

from modules.connection_runner import ConnectionRunner


def parse_args() -> Tuple[RTCSessionDescription, str]:
    """Parse command line arguments.

    Raises
    ------
    ValueError
        If the offer is invalid
    """
    parser = ArgumentParser()
    parser.add_argument("-o", "--offer", dest="offer", required=True)
    parser.add_argument(
        "-l", "--log_name_suffix", dest="log_name_suffix", required=True
    )
    args = parser.parse_args()

    # Check and parse offer
    try:
        offer_obj: RTCSessionDescriptionDict = json.loads(args.offer)
    except (json.JSONDecodeError, TypeError) as e:
        print(
            f"Failed to parse offer received in command line arguments: {e}",
            file=sys.stderr,
        )
        raise e

    if not is_valid_rtc_session_description_dict(offer_obj):
        print("Offer parsed from command line arguments is invalid.", file=sys.stderr)
        raise ValueError("Invalid offer")

    offer = RTCSessionDescription(offer_obj["sdp"], offer_obj["type"])

    return (offer, args.log_name_suffix)


async def main() -> None:
    offer, log_name_suffix = parse_args()

    runner = ConnectionRunner()
    await runner.run(offer, log_name_suffix)


if __name__ == "__main__":
    asyncio.run(main())
