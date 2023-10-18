from typing import TypedDict


class GetFiltersTestStatusRequestDict(TypedDict):
    """TypedDict for `GET_FILTERS_TEST_STATUS` requests.

    Attributes
    ----------
    participant_id : str
        Participant ID for the requested endpoint. Can be either id of one participant
        or 'all' for all participants.
    filter_name : str
        Name of the requested filter.
    filter_id : str
        Filter ID of the requested filter. Can be either the id or 'all' for all filters
        with name.
    filter_channel : str
        Filter channel of the requested filter. Can be either 'audio', 'video' or 'both'.

    See Also
    --------
    Data Types Wiki :https://github.com/TUMFARSynchrony/experimental-hub/wiki/Data-Types#getfiltersteststatusrequest
    """

    participant_id: str
    filter_id: str
    filter_name: str
    filter_channel: str
