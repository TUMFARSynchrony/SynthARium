"""Provide the `SimpleEventHandler` class."""

from typing import Any, Callable, Coroutine, TypeVar, Generic

T = TypeVar("T")


class SimpleEventHandler(Generic[T]):
    """TODO Document"""

    _handlers: list[Callable[[T], Coroutine[Any, Any, None]]]

    def __init__(self) -> None:
        """TODO Document"""
        self._handlers = []

    def on(self, handler: Callable[[T], Coroutine[Any, Any, None]]) -> None:
        """TODO Document"""
        self._handlers.append(handler)

    def off(self, handler: Callable[[T], Coroutine[Any, Any, None]]) -> None:
        """TODO Document"""
        # Raises ValueError if the handler is not present.
        self._handlers.remove(handler)

    async def trigger(self, data: T) -> None:
        """TODO Document"""
        for handler in self._handlers:
            await handler(data)
