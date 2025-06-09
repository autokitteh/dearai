---
sidebar_position: 1
sidebar_label: Python
description: Client initialization and API reference
---

# Python Workflows

## Client Initialization

Use this helper function from the
[AutoKitteh Python SDK](https://pypi.org/project/autokitteh/):

```python
from autokitteh.google import gmail_client

gmail = gmail_client("autokitteh_connection_name")
```

This helper function is documented here:
https://autokitteh.readthedocs.io/en/latest/#autokitteh.google.gmail_client

<details>
  <summary>
    The code above uses the AutoKitteh connection's authentication details
    automatically, and is equivalent to this code snippet
  </summary>

```python
from google.auth.transport.requests import Request
import google.oauth2.credentials as credentials
import google.oauth2.service_account as service_account
from googleapiclient.discovery import build

scopes = [...]

if json_key:
    info = json.loads(json_key)
    creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
else:
    creds = credentials.Credentials.from_authorized_user_info(...)
    if creds.expired:
        creds.refresh(Request())

gmail = build("gmail", "v1", credentials=creds)
```

</details>

## API Reference

Python:
https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.html

Code samples:

- https://github.com/autokitteh/kittehub/tree/main/samples/google/gmail
- https://github.com/googleworkspace/python-samples/tree/main/gmail

Overview:
https://developers.google.com/gmail/api/guides

REST:
https://developers.google.com/gmail/api/reference/rest
