"""Provide the `ErrorDict` TypedDict and valid `ERROR_TYPES`.

Use for type hints and static type checking without any overhead during runtime.
"""

from __future__ import annotations

from typing import TypedDict, Literal


class ErrorDict(TypedDict):
    """TypedDict for error api response.

    When an API call fails, an ErrorDict is send as response, informing the client of
    the error.

    Attributes
    ----------
    code : int
        HTTP response status code.
    type : custom_types.error.ERROR_TYPES
        Unique error type.
    description : str
        Error description.  Intended to be displayed to the enduser.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#error
    """

    code: int
    type: ERROR_TYPES
    description: str


# TODO define valid types
ERROR_TYPES = Literal[
    "TO_BE_DEFINED",  # Placeholder
    "INTERNAL_SERVER_ERROR",
    "INVALID_REQUEST",
    "UNKNOWN_SESSION",
    "UNKNOWN_EXPERIMENT",
    "UNKNOWN_PARTICIPANT",
]
"""Possible error types for custom_types.error.ErrorDict.

See Also
--------
Data Types Wiki :
    https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#error
"""
