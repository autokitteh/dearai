"""AutoKitteh connection-related utilities."""
from datetime import UTC, datetime
import re


def check_connection_name(connection: str) ->None:
    """Check that the given AutoKitteh connection name is valid.

    Args:
        connection: AutoKitteh connection name.

    Raises:
        ValueError: The connection name is invalid.
    """
    ...


def encode_jwt(payload: dict[str, int], connection: str, algorithm: str) ->str:
    """Mock function to generate JWTs, overridden by the AutoKitteh runner."""
    ...


def refresh_oauth(integration: str, connection: str) ->tuple[str, datetime]:
    """Mock function to refresh OAuth tokens, overridden by the AutoKitteh runner."""
    ...
