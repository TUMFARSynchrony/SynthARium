import logging
from typing import Literal, TypeGuard, get_args
from .filter_dict import FilterDict
from .filters_request_dict import SetFiltersRequestDict
from .delay.delay_filter_dict import is_valid_delay_filter_dict

import custom_types.util as util

logger = logging.getLogger("Filters")

FILTER_TYPES = Literal[
    "MUTE_AUDIO",
    "MUTE_VIDEO",
    "DELAY",
    "ROTATION",
    "EDGE_OUTLINE",
    "FILTER_API_TEST"
]
"""Valid filter types."""


def is_valid_filter_dict(data) -> TypeGuard[FilterDict]:
    """Check if `data` is a valid FilterDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid FilterDict.
    """
    if "type" not in data:
        logger.debug(f"Missing key: type")
        return False

    if not isinstance(data["type"], str):
        logger.debug(f'Filter "type" must be of type str.')
        return False

    if data["type"] not in get_args(FILTER_TYPES):
        logging.debug(f'Invalid filter type: "{data["type"]}".')
        return False

    # Add custom filter dicts here. They do not need to check `type` or `id`.
    # Custom filter TypeGuard functions are expected to call `check_valid_typeddict_keys`.
    valid_filter = False
    match data["type"]:
        case "DELAY":
            valid_filter = is_valid_delay_filter_dict(data)
        case _:
            # Default case, no custom filter
            valid_filter = util.check_valid_typeddict_keys(data, FilterDict)

    return valid_filter and isinstance(data["id"], str)


def is_valid_set_filters_request(
    data, recursive: bool = True
) -> TypeGuard[SetFiltersRequestDict]:
    """Check if `data` is a valid custom_types.filters.SetFiltersRequest.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.
    recursive : bool, default True
        If true, filters will be checked recursively.

    Returns
    -------
    bool
        True if `data` is a valid FilterDict.
    """
    if (
        not util.check_valid_typeddict_keys(data, SetFiltersRequestDict)
        or not isinstance(data["audio_filters"], list)
        or not isinstance(data["video_filters"], list)
        or not isinstance(data["participant_id"], str)
    ):
        return False

    if recursive:
        ids = []
        for filter in data["audio_filters"]:
            if filter["id"] in ids:
                logger.debug(f'Duplicate id: "{filter["id"]}" in SetFiltersRequestDict')
                return False
            ids.append(filter["id"])
            if not is_valid_filter_dict(filter):
                return False

        ids = []
        for filter in data["video_filters"]:
            if filter["id"] in ids:
                logger.debug(f'Duplicate id: "{filter["id"]}" in SetFiltersRequestDict')
                return False
            ids.append(filter["id"])
            if not is_valid_filter_dict(filter):
                return False

    return True