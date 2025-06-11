"""Initialize a Boto3 (AWS SDK) client, based on an AutoKitteh connection."""


def boto3_client(connection: str, service: str, region: str='', **kwargs):
    """Initialize a Boto3 (AWS SDK) client, based on an AutoKitteh connection.

    API reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

    Code samples:
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/examples.html

    Args:
        connection: AutoKitteh connection name.
        service: AWS service name.
        region: AWS region name.

    Returns:
        Boto3 client.

    Raises:
        ValueError: AutoKitteh connection or AWS service/region names are invalid.
        BotoCoreError: Authentication error.
    """
    ...
