def auth0_client(connection: str, **kwargs) ->Auth0:
    """Initialize an Auth0 client, based on an AutoKitteh connection.

    API reference:
    https://auth0-python.readthedocs.io/en/latest/

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Auth0 SDK client.

    Raises:
        ConnectionInitError: If the connection is not initialized.
        ValueError: If the connection name is invalid.
    """
    ...
