from __future__ import annotations

from filters import FilterDict
from group_filters import GroupFilter, group_filter_utils

from hub.exceptions import ErrorDictException


def create_group_filter(
    group_filter_config: FilterDict, participant_id: str
) -> GroupFilter:
    group_filter_name = group_filter_config["name"]

    group_filters = group_filter_utils.get_group_filter_dict()

    if group_filter_name not in group_filters:
        raise ErrorDictException(
            code=404,
            type="UNKNOWN_FILTER_TYPE",
            description=f"Unknown group filter type {group_filter_name}.",
        )

    return group_filters[group_filter_name](group_filter_config, participant_id)
