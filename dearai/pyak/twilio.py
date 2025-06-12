"""Initialize a Twilio client, based on an AutoKitteh connection."""
import os
from twilio.rest import Client
from .connections import check_connection_name
from .errors import ConnectionInitError


def twilio_client(connection: str) ->Client:
    """Initialize a Twilio client, based on an AutoKitteh connection.

    API reference:
    https://www.twilio.com/docs/libraries/python

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Twilio client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...
