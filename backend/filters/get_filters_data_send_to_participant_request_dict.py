from typing import TypedDict


class GetFiltersDataSendToParticipantRequestDict(TypedDict):
    """TypedDict for `GET_FILTERS_DATA_SEND_TO_PARTICIPANT` requests.

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
    Data Types Wiki :https://github.com/TUMFARSynchrony/experimental-hub/wiki/Data-Types#getfiltersdatasendtoparticipantrequest
    """

    participant_id: str
    filter_id: str
    filter_name: str
    filter_channel: str
