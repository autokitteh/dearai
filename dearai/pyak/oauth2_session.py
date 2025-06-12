import requests
from os import getenv
from .connections import refresh_oauth
from .connections import check_connection_name
from .errors import ConnectionInitError


class OAuth2Session(requests.Session):
    """Encapsulates arequests session, based on an AutoKitteh connection.

    - Automatically sets the Authorization header with an OAuth token.
    - Automatically refreshes an OAuth token if a refresh token is
      initialized in the connection.
    """
