---
sidebar_position: 5
sidebar_label: Python
description: Language-specific interfaces and tips
---

# Python Support

## Client Initialization

Use this helper function from the
[AutoKitteh Python SDK](https://pypi.org/project/autokitteh/):

```python
from autokitteh.slack import slack_client

slack = slack_client("autokitteh_connection_name")
```

This helper function is documented [here](https://autokitteh.readthedocs.io/en/latest/#autokitteh.slack.slack_client).

<details>
  <summary>
    The code above uses the AutoKitteh connection's authentication details
    automatically, and is equivalent to this code snippet
  </summary>

```python
from slack_sdk.web.client import WebClient

client = WebClient(bot_token)
client.auth_test().validate()
```

</details>

## Other Helper Functions

- `normalize_channel_name`
  ([documentation](https://autokitteh.readthedocs.io/en/latest/#autokitteh.slack.normalize_channel_name),
  [source code](https://github.com/autokitteh/autokitteh/blob/629ca3f3d083b7d203dec7b0d51d77d34c65b686/runtimes/pythonrt/py-sdk/autokitteh/slack.py#L49))\
  Convert arbitrary text into a valid Slack channel name, based on [Slack's channel naming rules](https://api.slack.com/methods/conversations.create#naming)

## References

- [Web API](https://api.slack.com/methods) (Slack method calls)
- [Events API](https://api.slack.com/events?filter=Events)
- [Python client API](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html)

## Code Samples

- [All AutoKitteh projects that use Slack](https://github.com/search?q=repo%3Aautokitteh%2Fkittehub+path%3A%2FREADME.md+slack&type=code)
