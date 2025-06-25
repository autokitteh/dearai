from typing import Any
from enum import StrEnum
_local_dev_store = {}


class Op(StrEnum):
    """Enum for operation types."""
    SET = 'set'
    GET = 'get'
    DEL = 'del'


def mutate_value(key: str, op: Op, *args: list[Any]) ->Any:
    """Mutate a stored value.

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

    Args:
        key: Key of the value to retrieve.

    Returns:
        Any: The stored value, or None if not found.
    """
    ...


def set_value(key: str, value: Any) ->None:
    """Set a stored value.

    Args:
        key: Key of the value to set.
        value: Value to store. If Value is None, it will be deleted. Value must be serializable.

    Returns:
        None.

    Raises:
        AutoKittehError: Value is too large.
    """
    ...


def del_value(key: str) ->None:
    """Delete a stored value.

    Args:
        key: Key of the value to set.

    Returns:
        None.
    """
    ...


def list_values_keys() ->list[str]:
    """List all stored keys.

    Returns:
        list[str]: Sorted list of all keys in the store.
    """
    ...
