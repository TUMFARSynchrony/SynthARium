import logging
from typing import TypeGuard

from group_filters import GroupFilter
from filters.filter_dict import FilterDict
from group_filters.group_filters_request_dict import SetGroupFiltersRequestDict

import custom_types.util as util
from socket import socket


logger = logging.getLogger("GroupFilters")


def is_valid_filter_dict(data) -> TypeGuard[FilterDict]:
    if "type" not in data:
        logger.debug("Missing key: type")
        return False

    group_filter_type = data["type"]

    if not isinstance(group_filter_type, str):
        logger.debug('GroupFilter "type" must be of type str.')
        return False

    group_filters = get_group_filter_dict()

    if group_filter_type not in group_filters:
        logging.debug(f"Invalid filter type: {group_filter_type}.")
        return False

    return isinstance(data["id"], str) and group_filters[
        group_filter_type
    ].validate_dict(data)


def get_group_filter_dict() -> dict:
    group_filter_dict = {}

    for concrete_group_filter in GroupFilter.__subclasses__():
        group_filter_name = concrete_group_filter.name()
        if group_filter_name in group_filter_dict:
            logger.warning(
                f"GroupFilter name {group_filter_name} already exists for class"
                f" {concrete_group_filter}"
            )
        else:
            group_filter_dict[group_filter_name] = concrete_group_filter

    return group_filter_dict


def is_valid_set_group_filters_request(
    data, recursive: bool = True
) -> TypeGuard[SetGroupFiltersRequestDict]:
    if (
        not util.check_valid_typeddict_keys(data, SetGroupFiltersRequestDict)
        or not isinstance(data["audio_group_filters"], list)
        or not isinstance(data["video_group_filters"], list)
    ):
        return False

    if recursive:
        ids = []
        for filter in data["audio_group_filters"] + data["video_group_filters"]:
            if filter["id"] in ids:
                logger.debug(
                    f'Duplicate id: "{filter["id"]}" in SetGroupFiltersRequestDict'
                )
                return False
            ids.append(filter["id"])
            if not is_valid_filter_dict(filter):
                return False

    return True


def get_group_filter_list() -> list[str]:
    result = []

    for myClass in GroupFilter.__subclasses__():
        result.append(myClass.name())

    return result


def find_an_available_port(addr: str = "") -> int:
    with socket() as s:
        s.bind((addr, 0))
        return s.getsockname()[1]
