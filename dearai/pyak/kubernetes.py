def kubernetes_client(connection: str) ->ModuleType:
    """Initialize a Kubernetes client, based on an AutoKitteh connection.

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Kubernetes API client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: If the connection config is missing or invalid,
            or if an unexpected error occurs during client initialization.

    """
    ...
