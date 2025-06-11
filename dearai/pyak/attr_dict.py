"""Helper class to allow attribute access to dictionary keys."""


class AttrDict(dict):
    """Allow attribute access to dictionary keys.

    >>> config = AttrDict({'server': {'port': 8080}, 'debug': True})
    >>> config.server.port
    8080
    >>> config.debug
    True
    """
