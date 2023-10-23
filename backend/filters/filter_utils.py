import logging
from typing import TypeGuard

from .filter import Filter
from .filter_dict import FilterDict
from .set_filters_request_dict import SetFiltersRequestDict
from .get_filters_data_request_dict import GetFiltersDataRequestDict
from .get_filters_data_send_to_participant_request_dict import (
    GetFiltersDataSendToParticipantRequestDict,
)

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
    if "name" not in data:
        logger.debug("Missing key: name")
        return False

    filter_name = data["name"]

    if not isinstance(filter_name, str):
        logger.debug('Filter "name" must be of type str.')
        return False

    filters = get_filter_dict()

    if filter_name not in filters:
        logging.debug(f'Invalid filter type: "{filter_name}".')
        return False

    return isinstance(data["id"], str) and filters[filter_name].validate_dict(data)


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


def is_valid_get_filters_data_dict(data) -> TypeGuard[GetFiltersDataRequestDict]:
    """Check if `data` is a valid custom_types.filters.GetFiltersDataRequestDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.
    Check if filter_name is a valid filter name.
    Check if filter_channel is a valid filter channel.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid FilterDict.
    """
    if (
        not util.check_valid_typeddict_keys(data, GetFiltersDataRequestDict)
        or not isinstance(data["filter_id"], str)
        or not isinstance(data["filter_name"], str)
        or not isinstance(data["filter_channel"], str)
    ):
        return False

    if data["filter_channel"] not in ["audio", "video", "both"]:
        logger.debug(
            f'Invalid filter channel: "{data["filter_channel"]}" in GetFiltersDataRequestDict'
        )
        return False

    for concrete_filter in Filter.__subclasses__():
        filter_name = concrete_filter.name(concrete_filter)
        if filter_name == data["filter_name"]:
            return True

    logger.debug(
        f'Invalid filter name: "{data["filter_name"]}" in GetFiltersDataRequestDict'
    )
    return False


def is_valid_get_filters_data_send_to_participant_dict(
    data,
) -> TypeGuard[GetFiltersDataSendToParticipantRequestDict]:
    """Check if `data` is a valid custom_types.filters.GetFiltersTestStatusRequestDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.
    Check if filter_name is a valid filter name.
    Check if filter_channel is a valid filter channel.

    Parameters
    ----------
    data : any
        Data to perform check on.

    Returns
    -------
    bool
        True if `data` is a valid FilterDict.
    """
    if not util.check_valid_typeddict_keys(
        data, GetFiltersDataSendToParticipantRequestDict
    ) or not isinstance(data["participant_id"], str):
        return False

    check_rest = {
        "filter_name": data["filter_name"],
        "filter_channel": data["filter_channel"],
        "filter_id": data["filter_id"],
    }

    return is_valid_get_filters_data_dict(check_rest)


def get_filter_list() -> list[str]:
    """Get a list of filter by class name.

    Returns
    -------
    A list of filters by class name.
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
                f"Filter name {filter_name} already exists for class"
                f" {concrete_filter.__name__}"
            )
        else:
            filter_dict[filter_name] = concrete_filter

    return filter_dict
