---
sidebar_position: 2
sidebar_label: Python
description: Client initialization and API reference
---

# Python Workflows

## Client Initialization

Use this helper function from the
[AutoKitteh Python SDK](https://pypi.org/project/autokitteh/):

```python
from autokitteh.salesforce import salesforce_client

client = salesforce_client("autokitteh_connection_name")
```

<details>
  <summary>
    The code above uses the AutoKitteh connection's authentication details
    automatically, and is equivalent to this code snippet
  </summary>

```python
from simple_salesforce import Salesforce

client = Salesforce(
    instance_url="https://<your-domain>.develop.my.salesforce.com",
    session_id="<ACCESS-TOKEN>",
)
```

</details>

## API Reference

Python:

- Documentation: https://simple-salesforce.readthedocs.io/en/latest/
- Source code: https://github.com/simple-salesforce/simple-salesforce

REST:

- https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm
