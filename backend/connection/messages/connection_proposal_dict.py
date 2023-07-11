from typing import TypedDict

from session.data.participant.participant_summary import ParticipantSummaryDict


class ConnectionProposalDict(TypedDict):
    """TypedDict for sending a `CONNECTION_PROPOSAL` message to the client.

    Attributes
    ----------
    id : str
        Identifier of this proposal.  Must be used in the
        custom_types.connection.ConnectionOfferDict to identify the offer.
    participant_summary : custom_types.participant_summary.ParticipantSummaryDict or None
        Optional summary for the participant the subconnection is connected to.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#ConnectionProposal
    Connection Protocol Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol
    """

    id: str
    participant_summary: ParticipantSummaryDict | str | None
