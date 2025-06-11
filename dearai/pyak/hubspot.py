"""Initialize a HubSpot client, based on an AutoKitteh connection."""


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
