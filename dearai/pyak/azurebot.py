"""Initialize a AzureBot client, based on an AutoKitteh connection."""
from dataclasses import dataclass
from typing import Any
import os
import requests
from .connections import check_connection_name
from .errors import ConnectionInitError, AuthenticationError
from .activities import activity


@dataclass
class _Credentials:
    app_id: str
    app_password: str
    tenant_id: str


class AzureBotClient:

    @activity
    def send_conversation_activity(self, activity: dict, conversation_id: (
        str | None), service_url: str='https://smba.trafficmanager.net/teams/'
        ) ->Any:
        """Send activity synchronously.

        If this is sent as a reply to an event, use the service_url from that event.

        Raises on non-2xx statuses.

        Returns the HTTP response body as JSON.
        """
        ...


def azurebot_client(connection: str) ->AzureBotClient:
    ...
