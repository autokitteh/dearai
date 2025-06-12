"""Initialize a HubSpot client, based on an AutoKitteh connection."""
import os
from hubspot import HubSpot
from .connections import check_connection_name, refresh_oauth
from .errors import ConnectionInitError, OAuthRefreshError


def hubspot_client(connection: str, **kwargs) ->HubSpot:
    """Initialize a HubSpot client, based on an AutoKitteh connection.

    Args:
        connection: AutoKitteh connection name.

    Returns:
        HubSpot SDK client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...
