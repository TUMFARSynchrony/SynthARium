"""Provide utility functions used by different parts of the software."""

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
