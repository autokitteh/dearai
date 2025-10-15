---
sidebar_position: 6
description: Complete AutoKitteh Python SDK API reference
title: SDK API Reference
---

# AutoKitteh SDK API Reference

This page documents all functions available in the `autokitteh` Python SDK module.

## Installation

The `autokitteh` module is automatically installed in AutoKitteh's virtual environment.

For **local development and testing**, you can install it with:

```bash
pip install autokitteh
```

:::warning

Installing the SDK locally is **only useful for**:
- Type hints and IDE autocompletion
- Testing individual handler functions in isolation
- Local syntax checking and linting

The SDK functions **require the AutoKitteh runtime to work**. When run outside of AutoKitteh (e.g., locally with plain Python), SDK functions like `subscribe()`, `next_event()`, `start()`, `http_outcome()`, etc., will not function properly as they depend on the AutoKitteh execution environment.

For actual workflow execution, you must run your code via `ak deploy` on an AutoKitteh server.

:::

Full API documentation is also available at: https://autokitteh.readthedocs.io/

See: [Local Development](/develop/python#local-development) for setting up your IDE and testing workflows.

## Core Functions

### `autokitteh.activity`

Decorator to mark a function as an activity. Activities are the unit of durable execution in AutoKitteh.

**When to use:**
- Functions with non-pickleable arguments or return values (e.g., file handles, database connections)
- Long-running operations
- Functions that perform I/O operations
- When you need to group multiple operations as a single atomic unit

**Example:**
```python
import autokitteh

@autokitteh.activity
def fetch_data(url):
    # This entire function runs as a single activity
    response = requests.get(url)
    return response.json()

def handler(event):
    data = fetch_data("https://api.example.com/data")
    print(data)
```

:::note

You **cannot** use event subscription functions (`subscribe`, `next_event`) or signals inside an activity.

:::

See: [Using the autokitteh.activity Decorator](/develop/python#using-the-autokittehactivity-decorator)

## Session Management

### `autokitteh.start()`

Start a new child session.

**Signature:**
```python
autokitteh.start(loc: str, data: dict = None, memo: dict = None) -> str
```

**Parameters:**
- `loc` (str): Code location in format `"filename:function_name"`
- `data` (dict, optional): Payload to pass to the function (accessible via `event.data`)
- `memo` (dict, optional): String-to-string dictionary for metadata displayed in the UI

**Returns:** Session ID (string) of the newly created session

**Example:**
```python
import autokitteh

def on_webhook(event):
    # Start a child session
    session_id = autokitteh.start(
        "worker.py:process_task",
        data={"task_id": 123, "priority": "high"},
        memo={"triggered_by": "webhook"}
    )
    print(f"Started session: {session_id}")

# In worker.py:
def process_task(event):
    task_id = event.data.task_id
    priority = event.data.priority
    print(f"Processing task {task_id} with priority {priority}")
```

**Use cases:**
- Spawning parallel workflows
- Delegating work to separate sessions
- Creating background jobs

## Event Subscription

### `autokitteh.subscribe()`

Subscribe to events from a connection or trigger.

**Signature:**
```python
autokitteh.subscribe(connection_or_trigger_name: str, filter: str = None) -> str
```

**Parameters:**
- `connection_or_trigger_name` (str): Name of the connection or trigger defined in your manifest
- `filter` (str, optional): CEL expression to filter events

**Returns:** Subscription ID (UUID string)

**Example:**
```python
import autokitteh

def on_trigger(event):
    # Subscribe to Slack messages
    sub_id = autokitteh.subscribe(
        "slack_conn",
        "event_type == 'message_posted' && data.channel == 'C12345'"
    )
    print(f"Subscribed with ID: {sub_id}")
```

See: [Programmatic Event Handling](/develop/events/subscription)

### `autokitteh.next_event()`

Wait for and retrieve the next event from one or more subscriptions.

**Signature:**
```python
autokitteh.next_event(*subscription_ids: str, timeout: timedelta = None) -> Event
```

**Parameters:**
- `*subscription_ids` (str): One or more subscription IDs from `subscribe()`
- `timeout` (timedelta, optional): Maximum time to wait. If not specified, waits indefinitely

**Returns:** Event object containing the event data, or `None` if timeout occurred

**Example - Single subscription:**
```python
from datetime import timedelta
import autokitteh

def on_webhook(event):
    sub_id = autokitteh.subscribe("webhook_trigger", "data.method == 'POST'")

    # Wait up to 5 minutes
    event = autokitteh.next_event(sub_id, timeout=timedelta(minutes=5))

    if event:
        print(f"Received event: {event.data}")
    else:
        print("Timeout - no event received")
```

**Example - Multiple subscriptions:**
```python
def on_trigger(event):
    # Wait for either GitHub or Slack event
    github_sub = autokitteh.subscribe("github_conn", "event_type == 'push'")
    slack_sub = autokitteh.subscribe("slack_conn", "event_type == 'message_posted'")

    # Returns whichever event arrives first
    event = autokitteh.next_event(github_sub, slack_sub, timeout=timedelta(hours=1))
    print(f"Received event from: {event.connection_id}")
```

:::tip

Without a timeout, `next_event()` will block forever and keep the session running until manually stopped.

:::

### `autokitteh.unsubscribe()`

Cancel an event subscription.

**Signature:**
```python
autokitteh.unsubscribe(subscription_id: str) -> None
```

**Parameters:**
- `subscription_id` (str): Subscription ID returned from `subscribe()`

**Example:**
```python
def on_trigger(event):
    sub_id = autokitteh.subscribe("slack_conn")

    # ... process some events ...

    # Clean up when done
    autokitteh.unsubscribe(sub_id)
```

:::note

Calling `unsubscribe()` is recommended but not required. Unused subscriptions don't burden AutoKitteh significantly.

:::

## HTTP Response

### `autokitteh.http_outcome()`

Set the HTTP response for synchronous webhooks.

**Signature:**
```python
autokitteh.http_outcome(status_code: int = 200, headers: dict = None, body: str = None) -> None
```

**Parameters:**
- `status_code` (int): HTTP status code (default: 200)
- `headers` (dict, optional): Response headers
- `body` (str, optional): Response body

**Example:**
```python
import autokitteh

def api_endpoint(event):
    # Process the request
    data = event.data.body.json
    result = process_data(data)

    # Return JSON response
    autokitteh.http_outcome(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps({"result": result})
    )
```

**Use with synchronous webhooks:**
```yaml
triggers:
  - name: api
    type: webhook
    is_sync: true  # Enable synchronous mode
    call: program.py:api_endpoint
```

See: [Synchronous Webhooks Example](/develop/manifest#example---synchronous-webhook)

## Project Value Store

### `autokitteh.set_value()`

Store a value in the project-wide key-value store.

**Signature:**
```python
autokitteh.set_value(key: str, value: Any) -> None
```

**Parameters:**
- `key` (str): Key name
- `value` (Any): Value to store (must be pickleable)

### `autokitteh.get_value()`

Retrieve a value from the project-wide store.

**Signature:**
```python
autokitteh.get_value(key: str, default: Any = None) -> Any
```

**Parameters:**
- `key` (str): Key name
- `default` (Any, optional): Default value if key doesn't exist

**Returns:** Stored value or default

### `autokitteh.del_value()`

Delete a value from the store.

**Signature:**
```python
autokitteh.del_value(key: str) -> None
```

**Parameters:**
- `key` (str): Key name to delete

### `autokitteh.list_values_keys()`

List all keys in the store.

**Signature:**
```python
autokitteh.list_values_keys() -> list[str]
```

**Returns:** List of all keys

**Example:**
```python
from autokitteh import set_value, get_value, del_value, list_values_keys

def on_webhook(event):
    # Store values
    set_value("counter", 0)
    set_value("last_user", event.data.user)

    # Retrieve values
    counter = get_value("counter", default=0)
    counter += 1
    set_value("counter", counter)

    # List all keys
    keys = list_values_keys()
    print(f"Stored keys: {keys}")

    # Delete a value
    del_value("last_user")
```

**Limitations:**
- Values must be pickleable
- Maximum 64 values per project
- Maximum 64KB per value after serialization
- Values are project-scoped (not shared across projects)

See: [Project Values Store](/develop/store)

## Signals

### `autokitteh.signal()`

Send a signal that can be waited on by other sessions.

**Signature:**
```python
autokitteh.signal(signal_name: str, data: dict = None) -> None
```

**Parameters:**
- `signal_name` (str): Name of the signal
- `data` (dict, optional): Data to send with the signal

### `autokitteh.wait_for_signal()`

Wait for a signal to be received.

**Signature:**
```python
autokitteh.wait_for_signal(signal_name: str, timeout: timedelta = None) -> dict
```

**Parameters:**
- `signal_name` (str): Name of the signal to wait for
- `timeout` (timedelta, optional): Maximum time to wait

**Returns:** Signal data or `None` if timeout

**Example:**
```python
from datetime import timedelta
import autokitteh

# Session 1: Wait for approval
def workflow(event):
    print("Waiting for approval...")
    signal_data = autokitteh.wait_for_signal("approval", timeout=timedelta(hours=24))

    if signal_data:
        print(f"Approved by: {signal_data.get('approver')}")
    else:
        print("Timeout - no approval received")

# Session 2: Send approval
def approve(event):
    autokitteh.signal("approval", {"approver": "admin", "timestamp": "2024-01-01"})
```

:::note

Signals cannot be used inside activities.

:::

See: [Signals Module](https://autokitteh.readthedocs.io/en/latest/#module-autokitteh.signals)

## Data Types

### `autokitteh.Event`

Event object passed to handler functions.

**Attributes:**
- `data`: Event payload (dict-like object with attribute access)
- `session_id`: ID of the current session

**Example:**
```python
def handler(event: autokitteh.Event):
    # Access via attributes
    body = event.data.body

    # Access via dict syntax
    body = event['data']['body']

    # Get session ID
    print(f"Session: {event.session_id}")
```

### `autokitteh.AttrDict`

Dictionary with attribute-style access used for event data.

**Example:**
```python
from autokitteh import AttrDict

# For testing event handlers
event = AttrDict({
    "data": {
        "body": "hello",
        "method": "POST"
    },
    "session_id": "ses_123"
})

handler(event)
```

## Integration Helpers

The SDK provides helper functions for initializing clients for various integrations:

### `autokitteh.slack.slack_client()`

Initialize Slack client.

```python
from autokitteh.slack import slack_client

slack = slack_client("slack_conn_name")
slack.chat_postMessage(channel="#general", text="Hello!")
```

### `autokitteh.github.github_client()`

Initialize GitHub client.

```python
from autokitteh.github import github_client

github = github_client("github_conn_name")
repo = github.get_repo("owner/repo")
```

### `autokitteh.google.google_sheets_client()`

Initialize Google Sheets client.

```python
from autokitteh.google import google_sheets_client

sheets = google_sheets_client("sheets_conn_name")
```

See individual [integration documentation](/integrations) for complete details.

## See Also

- [Python Development Guide](/develop/python)
- [Programmatic Event Handling](/develop/events/subscription)
- [Project Values Store](/develop/store)
- [Complete API Documentation](https://autokitteh.readthedocs.io/)
