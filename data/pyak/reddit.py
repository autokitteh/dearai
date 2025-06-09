"""Initializes a Reddit client, based on an AutoKitteh connection."""
import os
import praw
from .connections import check_connection_name
from .errors import ConnectionInitError


def reddit_client(connection: str) ->praw.Reddit:
    """Initialize a Reddit client, based on an AutoKitteh connection.

    API reference:
    https://praw.readthedocs.io/en/stable/

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Reddit API client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...
