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
from autokitteh.google import google_drive_client

drive = google_drive_client("autokitteh_connection_name")
```

This helper function is documented here:
https://autokitteh.readthedocs.io/en/latest/#autokitteh.google.google_drive_client

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

drive = build("drive", "v3", credentials=creds)
```

</details>

## API Reference

Python:
https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/

Code samples:
https://github.com/googleworkspace/python-samples/tree/main/drive

Overview:
https://developers.google.com/drive/api/guides/about-sdk

REST:
https://developers.google.com/drive/api/reference/rest/v3
