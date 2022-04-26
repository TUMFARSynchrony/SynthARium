from typing import Any, Type, TypedDict
import uuid


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


def check_valid_typed_dict(data: Any, type: Type[TypedDict]) -> bool:
    """Check if `data` is a valid dict according to `type`.

    Checks if all required and only required or optional keys from `type` exist in
    `data`.

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
            return False

    # Check that only required & optional keys exist in data
    for key in data.keys():
        if key not in required_keys and key not in optional_keys:
            return False

    return True
