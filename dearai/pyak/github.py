"""Initialize a GitHub client, based on an AutoKitteh connection."""
import os
import time
from urllib.parse import urljoin
from github import Auth, Consts, Github, GithubIntegration
from .connections import check_connection_name, encode_jwt
from .errors import ConnectionInitError


def github_client(connection: str, **kwargs) ->Github:
    """Initialize a GitHub client, based on an AutoKitteh connection.

    API reference and examples: https://pygithub.readthedocs.io/

    Args:
        connection: AutoKitteh connection name.

    Returns:
        PyGithub client.

    Raises:
        ValueError: AutoKitteh connection name or GitHub app IDs are invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...


class AppAuth(Auth.AppAuth):
    """Generate JWTs without exposing the GitHub app's private key.

    Based on: https://github.com/PyGithub/PyGithub/blob/main/github/Auth.py
    """

    def create_jwt(self, expiration: (int | None)=None) ->str:
        ...
