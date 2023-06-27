from dataclasses import dataclass, field
from typing import Any

from pyee import AsyncIOEventEmitter


@dataclass(slots=True)
class BaseData(AsyncIOEventEmitter):
    """Base dataclass with update recognition and handling.

    When data is changed and `_emit_updates` is true, a `update` event is emitted with
    self as data.
    """

    _emit_updates: bool | None = field(repr=False, init=False, default=False)
    """If true, a `update` event is emitted on changes to class variables.

    Only disable temporarily for bulk updates.
    """

    def __post_init__(self):
        """Initialize AsyncIOEventEmitter and set `_emit_updates` to true."""
        super(BaseData, self).__init__()
        self._emit_updates = True

    def __setattr__(self, _name: str, _value: Any) -> None:
        """Recognize changes to variables in this class and call `_emit_update_event`.

        Ignores updates to private variables, including `_emit_updates` and private
        variables in parent class.
        """
        object.__setattr__(self, _name, _value)
        if _name[0] != "_":
            self._emit_update_event()

    def _emit_update_event(self, _=None):
        """Emit an `update` event if `_emit_updates` is true."""
        try:
            if self._emit_updates:
                self.emit("update", self)
        except AttributeError as e:
            pass

