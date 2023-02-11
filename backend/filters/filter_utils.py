import logging
from typing import TypeGuard

from .filter import Filter
from .filter_dict import FilterDict
from .filters_request_dict import SetFiltersRequestDict

import custom_types.util as util

logger = logging.getLogger("Filters")


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

    filter_type = data["type"]

    if not isinstance(filter_type, str):
        logger.debug(f'Filter "type" must be of type str.')
        return False

    filters = get_filter_dict()

    if filter_type not in filters:
        logging.debug(f'Invalid filter type: "{filter_type}".')
        return False

    return isinstance(data["id"], str) and filters[filter_type].validate_dict(data)


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


def get_filter_list() -> list[str]:
    """Get a list of filter classes.

    Returns
    -------
    A list of filters classes.
    """
    result = []

    for myClass in Filter.__subclasses__():
        result.append(myClass.name(myClass))

    return result


def get_filter_dict() -> dict:
    """Get a dictionary of filters:
    Key: Return value of concrete_filter.name()
    Value: The corresponding filter class

    Returns
    -------
    A dictionary of filters
    """
    filter_dict = {}

    for concrete_filter in Filter.__subclasses__():
        filter_name = concrete_filter.name(concrete_filter)
        if filter_name in filter_dict:
            logger.warning(
                f"Filter name {filter_name} already exists for class {concrete_filter.__name__}"
            )
        else:
            filter_dict[filter_name] = concrete_filter

    return filter_dict
