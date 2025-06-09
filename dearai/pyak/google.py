"""Initialize Google API clients, based on AutoKitteh connections."""
from datetime import UTC, datetime
import json
import os
import re
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
import google.generativeai as genai
import google.oauth2.credentials as credentials
import google.oauth2.service_account as service_account
from googleapiclient.discovery import build
import gspread
from .connections import check_connection_name, refresh_oauth
from .errors import ConnectionInitError, OAuthRefreshError


def gmail_client(connection: str, **kwargs):
    """Initialize a Gmail client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/google/gmail/python

    Code samples:
    - https://github.com/autokitteh/kittehub/tree/main/samples/google/gmail
    - https://github.com/googleworkspace/python-samples/tree/main/gmail

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Gmail client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def google_calendar_client(connection: str, **kwargs):
    """Initialize a Google Calendar client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/google/calendar/python

    Code samples:
    https://github.com/autokitteh/kittehub/tree/main/samples/google/calendar

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Google Calendar client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def google_drive_client(connection: str, **kwargs):
    """Initialize a Google Drive client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/google/drive/python

    Code samples:
    https://github.com/googleworkspace/python-samples/tree/main/drive

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Google Drive client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def google_forms_client(connection: str, **kwargs):
    """Initialize a Google Forms client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/google/forms/python

    Code samples:
    - https://github.com/autokitteh/kittehub/tree/main/samples/google/forms
    - https://github.com/googleworkspace/python-samples/tree/main/forms

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Google Forms client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def gemini_client(connection: str, **kwargs) ->genai.GenerativeModel:
    """Initialize a Gemini generative AI client, based on an AutoKitteh connection.

    API reference:
    - https://ai.google.dev/gemini-api/docs
    - https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai/GenerativeModel.md

    Code samples:
    - https://ai.google.dev/gemini-api/docs#explore-the-api
    - https://ai.google.dev/gemini-api/docs/text-generation?lang=python
    - https://github.com/google-gemini/generative-ai-python/tree/main/samples
    - https://github.com/google-gemini/cookbook

    Args:
        connection: AutoKitteh connection name.

    Returns:
        An initialized GenerativeModel instance.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
    """
    ...


def google_sheets_client(connection: str, **kwargs):
    """Initialize a Google Sheets client, based on an AutoKitteh connection.

    API documentation:
    https://docs.autokitteh.com/integrations/google/sheets/python

    Code samples:
    - https://github.com/autokitteh/kittehub/tree/main/samples/google/sheets
    - https://github.com/googleworkspace/python-samples/tree/main/sheets

    Args:
        connection: AutoKitteh connection name.

    Returns:
        Google Sheets client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def gspread_client(connection: str, **kwargs) ->gspread.Client:
    """Initialize a gspread client, based on an AutoKitteh connection.

    API documentation:
    https://docs.gspread.org/en/latest/
    https://github.com/burnash/gspread

    Args:
        connection: AutoKitteh connection name.

    Returns:
        gspread client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def youtube_client(connection: str, **kwargs):
    """Initialize a YouTube Data API client, based on an AutoKitteh connection.


    Code samples:
    - https://github.com/youtube/api-samples/tree/master/python

    Args:
        connection: AutoKitteh connection name.

    Returns:
        YouTube Data API client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def google_creds(integration: str, connection: str, scopes: list[str], **kwargs
    ):
    """Initialize credentials for a Google APIs client, for service discovery.

    This function supports both AutoKitteh connection modes:
    users (with OAuth 2.0), and GCP service accounts (with a JSON key).

    Code samples:
    https://github.com/googleworkspace/python-samples

    For subsequent usage details, see:
    https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build

    Args:
        integration: AutoKitteh integration name.
        connection: AutoKitteh connection name.
        scopes: List of OAuth permission scopes.

    Returns:
        Google API credentials, ready for usage
        in "googleapiclient.discovery.build()".

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        OAuthRefreshError: OAuth token refresh failed.
    """
    ...


def google_id(url: str) ->str:
    """Extract the Google Doc/Form/Sheet ID from a URL. This function is idempotent.

    Example: 'https://docs.google.com/.../d/1a2b3c4d5e6f/edit' --> '1a2b3c4d5e6f'
    """
    ...
