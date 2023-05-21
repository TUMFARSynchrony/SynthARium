"""Provide the `SessionDict` related utility functions.

Use for type hints and static type checking without any overhead during runtime.
"""
from hub.util import generate_unique_id
from session.data.session.session_dict import SessionDict


def _generate_participant_ids(session_dict: SessionDict) -> None:
    """Generate missing participant IDs in `session_dict`.

    Parameters
    ----------
    session_dict : session.data.session.SessionDict
        Session dictionary where the participant ids will be generated in.
    """
    participant_ids = get_filtered_participant_ids(session_dict)
    for participant in session_dict["participants"]:
        id = participant["id"]
        if id == "":
            # New participant without id
            new_id = generate_unique_id(participant_ids)
            participant_ids.append(new_id)
            participant["id"] = new_id


def get_participant_ids(session_dict: SessionDict) -> list[str]:
    """Get all participant IDs from session_dict.

    Parameters
    ----------
    data : session.data.session.SessionDict
        Session data with participants.

    Returns
    -------
    list of str
        Participant IDs in `session_dict`.

    See Also
    --------
    get_filtered_participant_ids : Get IDs without empty strings for missing IDs.
    """
    return [p["id"] for p in session_dict["participants"]]


def get_filtered_participant_ids(session_dict: SessionDict) -> list[str]:
    """Get all participant IDs from session_dict. Missing (empty string) IDs will be
    filtered out.

    Parameters
    ----------
    data : session.data.session.SessionDict
        Session data with participants.

    Returns
    -------
    list of str
        Participant IDs in `session_dict` without missing/empty IDs.

    See Also
    --------
    get_participant_ids : Get IDs with empty strings for missing IDs.
    """
    p_ids = get_participant_ids(session_dict)
    return [id for id in p_ids if id != ""]


def has_duplicate_participant_ids(session_dict: SessionDict) -> bool:
    """Check if `session_dict` has duplicate session IDs.

    Parameters
    ----------
    session_dict : session.data.session.SessionDict
        Session dictionary that should be checked for duplicates.

    Returns
    -------
    bool
        True if there are duplicate IDs, False if no duplicate IDs where found.
    """
    participant_ids = get_filtered_participant_ids(session_dict)
    return len(participant_ids) != len(set(participant_ids))