"""Provide utility functions used by different parts of the software."""

import uuid
from typing import Any, Type, TypedDict

# typing_extensions.TypedDict is required for compatibility. E.g. SessionDict uses
# typing_extensions.TypedDict, because of support for NonRequired / Required Keys.
# Support will come to typing in python 3.11. See PEP 655.
from typing_extensions import TypedDict as TypedDictExt

import custom_types.session as _session_dict


def generate_unique_id(existing_ids: list[str]):
    """Generate an unique id without collision with `existing_ids`.

    Parameters
    ----------
    existing_ids : list of str
        Existing ids which may not include the new, generated id.

    Returns
    -------
    str
        Unique id generated.

    See Also
    --------
    SessionManager._generate_unique_session_id : Generate an unique session
        id.
    """
    id = uuid.uuid4().hex[:10]
    while id in existing_ids:
        id = uuid.uuid4().hex[:10]
    return id


def check_valid_typeddict_keys(
    data: Any, type: Type[TypedDict] | Type[TypedDictExt]
) -> bool:
    """Check if `data` is a valid dict according to `type`.

    Checks if all required and only required or optional keys from `type` exist in
    `data`.

    Does not check the data type of values in `data`!  Full checks, including data type
    checks, should be included within the TypedDicts modules.  These checks should
    include this function.

    Parameters
    ----------
    data : dict
        Dictionary to perform key check on.
    type: typing.TypedDict or typing_extensions.TypedDict
        Target TypedDict with optional and / or required keys.

    Returns
    -------
    bool
        True if all required and only required or optional keys exist in `data`, else
        False.
    """
    if not isinstance(data, dict):
        return False

    # Note: Pyright does not seem to know __required_keys__ and __optional_keys__,
    # which is why the "type: ignore" are here.
    return check_dict(
        data,
        type.__required_keys__,  # type: ignore
        type.__optional_keys__,  # type: ignore
    )


def check_dict(data: dict, required_keys: list[str], optional_keys: list[str]):
    """Check if `data` has all required and only required or optional keys.

    Parameters
    ----------
    data : dict
        Dictionary to perform key check on.
    required_keys : list of str
        Keys that must be present in `data`.
    optional_keys : list of str
        Keys that may be present in `data`, but are not required.

    Returns
    -------
    bool
        True if all required and only required or optional keys exist in `data`, else
        False.
    """
    # Check if required keys exist in data
    for key in required_keys:
        if key not in data:
            print("[check_dict] missing key:", key)
            return False

    # Check that only required & optional keys exist in data
    for key in data.keys():
        if key not in required_keys and key not in optional_keys:
            print(
                f"[check_dict] non allowed key: {key}. Required keys:",
                f"{required_keys}, optional keys: {optional_keys}.",
            )
            return False

    return True


def get_participant_ids(session_dict: _session_dict.SessionDict) -> list[str | None]:
    """Get all participant IDs from session_dict. Missing IDs will be None.

    Parameters
    ----------
    data : custom_types.session.SessionDict
        Session data with participants.

    Returns
    -------
    list of str and/or None
        Participant IDs in `session_dict` with None for missing/empty IDs.

    See Also
    --------
    get_filtered_participant_ids : Get IDs without None values for missing IDs.
    """
    return [p.get("id") for p in session_dict.get("participants", [])]


def get_filtered_participant_ids(session_dict: _session_dict.SessionDict) -> list[str]:
    """Get all participant IDs from session_dict. Missing IDs will be filtered out.

    Parameters
    ----------
    data : custom_types.session.SessionDict
        Session data with participants.

    Returns
    -------
    list of str
        Participant IDs in `session_dict` without missing/empty IDs.

    See Also
    --------
    get_participant_ids : Get IDs with None values for missing IDs.
    """
    p_ids = get_participant_ids(session_dict)
    return [id for id in p_ids if id is not None]
