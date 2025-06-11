"""Initialize a Height client, based on an AutoKitteh connection."""


def height_client(connection: str) ->Session:
    """Initialize an Height client, based on an AutoKitteh connection.

    API reference:
    https://height-api.xyz/openapi/

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Requests session object.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...
