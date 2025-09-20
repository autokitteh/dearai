"""Initialize an Anthropic client, based on an AutoKitteh connection."""
import os
from pipedrive.client import Client
from .connections import check_connection_name
from .errors import ConnectionInitError


def pipedrive_client(connection: str) ->Client:
    """Initialize a Pipedrive client, based on an AutoKitteh connection.

    API reference:
        https://pypi.org/project/pipedrive-python-lib/

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Pipedrive API client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...
