import os
import discord
from .connections import check_connection_name
from .errors import ConnectionInitError


def discord_client(connection: str, intents=None, **kwargs) ->discord.Client:
    """Initialize a Discord client, based on an AutoKitteh connection.

    API reference:
    https://discordpy.readthedocs.io/en/stable/api.html

    Args:
        connection: AutoKitteh connection name.
        intents: An object representing the events your bot can receive.

    Returns:
        Discord client.

    Raises:
        ValueError: AutoKitteh connection name is invalid.
        ConnectionInitError: AutoKitteh connection was not initialized yet.
        DiscordException: Connection attempt failed, or connection is unauthorized.
    """
    ...


def bot_token(connection: str):
    ...
