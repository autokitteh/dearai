"""Slack client initialization, and other helper functions."""
import os
import re
from slack_sdk.web.client import WebClient
from .connections import check_connection_name
from .errors import ConnectionInitError


def slack_client(connection: str, **kwargs) ->WebClient:
    """Initialize a Slack client, based on an AutoKitteh connection.

    API reference:
    https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html

    This function doesn't initialize a Socket Mode client because the
    AutoKitteh connection already has one to receive incoming events.

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Slack SDK client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        SlackApiError: Connection attempt failed, or connection is unauthorized.
    """
    ...


def normalize_channel_name(name: str) ->str:
    """Convert arbitrary text into a valid Slack channel name.

    See: https://api.slack.com/methods/conversations.create#naming

    Args:
        name: Desired name for a Slack channel.

    Returns:
        Valid Slack channel name.
    """
    ...
