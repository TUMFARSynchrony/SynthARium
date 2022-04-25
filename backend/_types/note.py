"""Provide the `NoteDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from typing import TypedDict


class NoteDict(TypedDict):
    """TypedDict for notes in _types.session.SessionDict.

    Attributes
    ----------
    time : int
        Time the note was saved in milliseconds since January 1, 1970, 00:00:00 (UTC).
    speakers : list of str
        List of Participant IDs for participants speaking when the note was saved.
    content : str
        Text content of the note, written by a experimenter.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#note
    """


    time: int
    speakers: list[str]
    content: str
