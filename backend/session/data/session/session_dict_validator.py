from typing import TypeGuard

from custom_types import util
from custom_types.note import is_valid_note
from session.data.participant import is_valid_participant
from session.data.session.session_dict import SessionDict


def is_valid_session(data, recursive: bool = True) -> TypeGuard[SessionDict]:
    """Check if `data` is a valid SessionDict.

    Checks if all required and no unknown keys exist in data as well as the data types
    of the values.

    Parameters
    ----------
    data : any
        Data to perform check on.
    recursive : bool, default True
        If true, participants and notes will be checked recursively.

    Returns
    -------
    bool
        True if `data` is a valid SessionDict.
    """
    if not util.check_valid_typeddict_keys(data, SessionDict):
        return False

    # Check participants and notes
    if not isinstance(data["participants"], list) or not isinstance(
        data["notes"], list
    ):
        return False

    if recursive:
        for entry in data["participants"]:
            if not is_valid_participant(entry, recursive):
                return False
        for entry in data["notes"]:
            if not is_valid_note(entry):
                return False

    # TODO check log

    return (
        isinstance(data["id"], str)
        and isinstance(data["creation_time"], int)
        and isinstance(data["start_time"], int)
        and isinstance(data["end_time"], int)
        and isinstance(data["title"], str)
        and isinstance(data["description"], str)
        and isinstance(data["date"], int)
        and isinstance(data["time_limit"], int)
        and isinstance(data["record"], bool)
    )
