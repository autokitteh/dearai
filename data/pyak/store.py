from collections.abc import MutableMapping
from enum import StrEnum
from typing import Any
_local_dev_store = {}


class Store(MutableMapping):
    """Store it a dict like interface to ak store.

    Note that read-modify-write operations are not atomic.

    Values must be pickleable, see
    https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled

    Works both for durable and non-durable sessions.
    """


store = Store()


class Op(StrEnum):
    """Enum for operation types."""
    SET = 'set'
    GET = 'get'
    DEL = 'del'
    ADD = 'add'
    CHECK_AND_SET = 'check_and_set'


def mutate_value(key: str, op: Op, *args: list[Any]) ->Any:
    """Mutate a stored value.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to mutate.
        op: Operation to perform on the value.
        args: Additional arguments for the operation.

    Returns:
        Any: Result of the operation, if applicable.

    Raises:
        AutoKittehError: Value is too large.
    """
    ...


def get_value(key: str) ->Any:
    """Get a stored value.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to retrieve.

    Returns:
        Any: The stored value, or None if not found.
    """
    ...


def check_and_set_value(key: str, expected_value: Any, new_value: Any) ->bool:
    """Check and set a stored value.

    This operation is atomic.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to set.
        expected_value: Expected current value.
        new_value: New value to store if the current value matches the expected value.
    Returns:
        bool: True if the value was set, False otherwise.
    """
    ...


def set_value(key: str, value: Any) ->None:
    """Set a stored value.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to set.
        value: Value to store. If Value is None, it will be deleted. Value must be serializable.

    Returns:
        None.

    Raises:
        AutoKittehError: Value is too large.
    """
    ...


def add_values(key: str, value: (int | float)) ->(int | float):
    """Add to a stored value.

    This operation is atomic.

    If key is not found, its initial value is set to the provided value.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to set.
        value: Value to add. Value must be serializable.

    Returns:
        New result value. Always the same type as the value stored under the key.
    """
    ...


def del_value(key: str) ->None:
    """Delete a stored value.

    Works both for durable and non-durable sessions.

    Args:
        key: Key of the value to set.

    Returns:
        None.
    """
    ...


def list_values_keys() ->list[str]:
    """List all stored keys.

    Works both for durable and non-durable sessions.

    Returns:
        list[str]: Sorted list of all keys in the store.
    """
    ...
