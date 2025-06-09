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
from autokitteh.google import google_forms_client

forms = google_forms_client("autokitteh_connection_name")
```

This helper function is documented here:
https://autokitteh.readthedocs.io/en/latest/#autokitteh.google.google_forms_client

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

forms = build("forms", "v1", credentials=creds)
```

</details>

## API Reference

Python:
https://googleapis.github.io/google-api-python-client/docs/dyn/forms_v1.forms.html

Code samples:

- https://github.com/autokitteh/kittehub/tree/main/samples/google/forms
- https://github.com/googleworkspace/python-samples/tree/main/forms

Overview:
https://developers.google.com/forms/api/guides

REST:
https://developers.google.com/forms/api/reference/rest
