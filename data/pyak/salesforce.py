"""Initialize a Salesforce client, based on an AutoKitteh connection."""


def salesforce_client(connection: str, **kwargs) ->Salesforce:
    """Initialize a Salesforce client, based on an AutoKitteh connection.

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Salesforce client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        SalesforceApiError: Connection attempt failed, or connection is unauthorized.
    """
    ...
