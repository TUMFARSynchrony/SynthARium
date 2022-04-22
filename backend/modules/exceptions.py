"""Custom Exceptions for experimental hub"""

import json

from _types.error import ErrorDict, ERROR_TYPES
from _types.message import MessageDict


class ErrorDictException(Exception):
    """Exception used to pass a ErrorDict.

    Custom exception for an ErrorDict that can be send as a response to
    an api request.

    Note
    ----
    Since the intended purpose is to send the information to the user, no
    private/classified information should be included.
    """

    code: int
    type: ERROR_TYPES
    description: str

    def __init__(
        self, code: int, type: ERROR_TYPES, description: str, *args: object
    ) -> None:
        """Construct a new ErrorDictException.

        Parameters
        ----------
        code : int
            HTTP response status code.
        type : _types.error.ERROR_TYPES
            unique error type.
        description : str
            error description.

        Note
        ----
        Since the intended purpose is to send the information to the user, no
        private/classified information should be included.
        """
        self.code = code
        self.type = type
        self.description = description
        super().__init__(description, *args)

    @property
    def error_dict(self) -> ErrorDict:
        """Get a ErrorDict dictionary detailing the exception.

        Returns
        -------
        _types.error.ErrorDict
            ErrorDict dictionary containing the exception information.

        See Also
        --------
        __iter__ : Get the error dictionary using e.g.
                   `dict(ErrorDictException)`
        """
        return ErrorDict(code=self.code, type=self.type, description=self.description)

    @property
    def error_message(self) -> MessageDict:
        """Get a MessageDict containing the ErrorDict detailing the exception.

        The MessageDict can be send as a response to a user request. Avoids the
        need to construct a MessageDict in every try, except clause.

        Returns
        -------
        _types.message.MessageDict
            MessageDict dictionary with type = `ERROR` and data = the ErrorDict
            detailing the exception.

        See Also
        --------
        error_dict : Get the error dictionary.
        __iter__ : Get the error dictionary using e.g.
                   `dict(ErrorDictException)`.  Alternative to `error_dict`.
        """
        return MessageDict(type="ERROR", data=self.error_dict)

    @property
    def error_message_str(self) -> str:
        """Get a MessageDict string containing the ErrorDict detailing the
        exception.

        The MessageDict string can be send as a response to a user request.
        Avoids the need to construct and parse a MessageDict in every try,
        except clause.

        Internally, this simply dumps (stringifies) the `error_message`
        property.

        Returns
        -------
        str
            String containing a MessageDict dictionary with type = `ERROR`
            and data = the ErrorDict detailing the exception.

        See Also
        --------
        error_message : Get the source MessageDict dictionary.
        """
        return json.dumps(self.error_message)

    def __iter__(self):
        """Yield error code, type and description.

        Note:
        ----
            This is intended to be used for dict(ErrorDictException).
        """
        yield "code", self.code
        yield "type", self.type
        yield "description", self.description
