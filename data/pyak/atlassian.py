"""Initialize an Atlassian client, based on an AutoKitteh connection."""
__TOKEN_URL = 'https://auth.atlassian.com/oauth/token'


def jira_client(connection: str, **kwargs) ->Jira:
    """Initialize an Atlassian Jira client, based on an AutoKitteh connection.

    API reference:
    https://atlassian-python-api.readthedocs.io/jira.html

    Code samples:
    https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/jira

    Args:
        connection: AutoKitteh connection name.
        **kwargs: Additional keyword arguments passed to the Jira client.
            Common options include:
            - 'url': URL of the Jira instance.
            - 'username': Username for Jira authentication.
            - 'password': Password for Jira authentication.
            - 'token': API token for Jira authentication.
            - 'verify_ssl': Boolean to verify SSL certificates.
            For a full list of accepted arguments, see:
            https://github.com/atlassian-api/atlassian-python-api/blob/master/atlassian/rest_client.py#L48

    Returns:
        Atlassian-Python-API Jira client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        EnvVarError: Required environment variable is missing or invalid.
    """
    ...


def confluence_client(connection: str, **kwargs) ->Confluence:
    """Initialize an Atlassian Confluence client, based on an AutoKitteh connection.

    API reference:
    https://atlassian-python-api.readthedocs.io/confluence.html

    Code samples:
    https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/confluence

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Atlassian-Python-API Confluence client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        EnvVarError: Required environment variable is missing or invalid.
        AtlassianOAuthError
    """
    ...


def get_base_url(connection: str) ->(str | None):
    """Get the base URL of an AutoKitteh connection's Atlassian server.

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Base URL of the Atlassian connection, or None if
        the AutoKitteh connection was not initialized yet.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
    """
    ...
