"""Initialize Microsoft Graph SDK clients, based on AutoKitteh connections."""
DEFAULT_REFRESH_BUFFER_TIME = timedelta(minutes=5)


def teams_client(connection: str, **kwargs) ->GraphServiceClient:
    """Initialize a Microsoft Teams client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/microsoft/teams/python

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Microsoft Graph client.

    Raises:
        ValueError: AutoKitteh connection name or auth type are invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


class OAuthTokenProvider(credentials.TokenCredential):
    """OAuth 2.0 token wrapper for Microsoft Graph clients."""

    def get_token(self, *scopes: str, **kwargs) ->credentials.AccessToken:
        ...
