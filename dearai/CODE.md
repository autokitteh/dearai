

# Code

An AutoKitteh project contains configuration (as described by a manifest) and code.
The code is Python 3 code.

By default, AutoKitteh makes available the following packages for the program:
"""
anthropic ~= 0.54.0
asana ~= 5.0
atlassian-python-api ~= 3.41
auth0-python ~= 4.7
azure-identity ~= 1.19
boto3 ~= 1.35
discord.py ~= 2.5
google-api-python-client ~= 2.155
google-auth-httplib2 ~= 0.2
google-auth-oauthlib ~= 1.2
google-generativeai ~= 0.8
gspread ~= 6.2
gspread-formatting ~= 1.2
hubspot-api-client ~= 11.1
kubernetes ~= 31.0
msgraph-sdk ~= 1.18
notion_client ~= 2.0
openai ~= 1.57
pipedrive-python-lib ~= 1.2
praw ~= 7.8
pyairtable ~= 3.1
PyGithub ~= 2.6
python-telegram-bot ~= 22.0
simple-salesforce ~= 1.12
slack-sdk ~= 3.33
twilio ~= 9.4
beautifulsoup4 ~= 4.12
grpcio ~= 1.68
grpcio-reflection ~= 1.68
PyYAML ~= 6.0
requests ~= 2.32
requests-toolbelt ~= 1.0
tenacity ~= 9.0
"""

**IMPORTANT**: NEVER add the above mentioned packages into the project's requirements.txt! These will be already automatically installed by the AutoKitteh runtime. Avoid using different package versions than what is already explicitly specified above.

If the additional packages are required, they can be specified in a `requirements.txt` file.

The following integration names are supported:
anthropic
asana
auth0
autokitteh
aws
chatgpt
confluence
discord
github
githubcopilot
gmail
googlecalendar
googledrive
googleforms
googlegemini
googlesheets
height
hubspot
jira
linear
notion
pipedrive
slack
telegram
twilio
youtube
zoom


These are the ONLY integrations supported.
NEVER specifiy any integration that does not appear above as an integration.

## Pitfalls

## Function Return Value Must Be Pickleable

In durable mode, we use pickle to pass function arguments back to AutoKitteh to run as an activity. See What can be pickled and unpickled? for supported types. Most notably, the following can't be pickled:

- Open file handlers (when open returns)
- lambdas
- Dynamically generated functions (e.g. os.environ.get)

```txtar
-- bad.py --
import db

def handler(event):
    mapper = lambda n: n.lower()
    db.apply(mapper)  # BAD

-- good.py --
import db

def mapper(n):
    return n.lower()

def handler(event):
    db.apply(mapper)  # GOOD
```

NOTE: You can use copyreg.pickle in order to support more types.

## Function Timeout

In durable mode, if a function that runs in a workflow context (not in an activity) takes a long time, it might cause a timeout.

Say you have the following code:

```py
from collections.abc import Sequence


class Response(Sequence):
    def __init__(self, count):
        self.count = count

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        if index >= self.count:
            raise IndexError

        print("calling server")  # network call, takes time
        return {
            'id': index,
            'level': 'INFO',
            'message': f'log #{index+1}',
        }


def get_logs(env: str) -> Response:
    # TODO: Actual code
    return Response(3)


def on_event(event):
    logs = get_logs(event.data.env)
    logs = sorted(logs, key=lambda log: log['id'])  # timeout
    ...  # More code
```

When the workflow runs, `sorted(logs)` is not in an activity, and will cause a timeout due to network calls in `__getitem__`.

The solution is to place long running code in an activity:

```py
@autokitteh.activity
def on_event(event):
    logs = get_logs(event.data.env)
    logs = sorted(logs, key=lambda log: log['id'])  # timeout
    ...  # More code
```

## SDK

The AutoKitteh SDK is automatically available for import.
Its documentation can be found at https://autokitteh.readthedocs.io/en/latest/.

### Explicit Activities using the `autokitteh.activity` Decorator

The autokitteh.activity decorator allow you to mark a function that must run as activity. This allows you to run function with arguments or return values that are not compatible with pickle. This is mostly useful when performing IO.

NOTE: The autokitteh module is installed to the default AutoKitteh virtual environment.

Say you have the following code in your handler:

```py
import json
from urllib.request import urlopen


def handler(event):
    login = event['login']
    url = f'https://api.github.com/users/{login}'
    with urlopen(url) as fp:
        resp = json.load(fp)
    print('user name:', resp['name'])
```

Running this handler will fail since the result of urlopen can't be pickled. What you can do is move the code into a function marked as activity:

```py
import json
from urllib.request import urlopen

import autokitteh


def handler(event):
    login = event['login']
    info = user_info(login)
    print('user name:', info['name'])


@autokitteh.activity
def user_info(login):
    url = f'https://api.github.com/users/{login}'
    with urlopen(url) as fp:
        resp = json.load(fp)
    return resp
```

All the code in user_info runs in a single activity. Since user_info accepts a str and returns a dict, both are pickleable, it can run as activity.

### Starting new child sessions using `autokitteh.start`

A session can start a new child session using the `autokitteh.start` function from the SDK.

```
autokitteh.start(loc: str, data: dict = None, memo: dict = None) -> str
```

- `loc` is the code location of the function start, format: "filename:function_name".
- `data` is the payload to pass to that function. The function can access this data via the `event.data` parameter.
- `memo` is a string to string dictionary for general memo fields that will be displayed in the UI.

The function returns the session ID for the newly created session.

Example:

```txtar
-- main.py --

import autokitteh

def on_whatever(_):
    autokitteh.start("main.py:say", {"sound": "meow"})

def say(event):
    print(event.data.sound) # prints "meow"
```

# Event Structure

Event handler functions receive a single argument of type `autokitteh.Event`. It is recommended this argument to be called `event`:

```py
from autokitteh import Event

def on_some_trigger(event: Event):
    ...
```

The event contains the `session_id` for the session and the event payload in its `data` field.

Each integration has a different event payload format. See details about each integration format in the `integrations/` folder.

---
sidebar_position: 1
description: Programmatic event handling
title: Subscription
---

# Programmatic Event Handling

## Overview

Triggers are static definitions in AutoKitteh projects to start sessions that
run Python workflows when certain events are received.

In addition, workflows can receive events programmatically during runtime.
This page describes how this works.

## Initial Subscription

```py
import autokitteh

subscription_id = autokitteh.subscribe(connection_or_trigger_name, filter)
```

### Subscription ID

The `subscribe` function call returns a UUID string that represents a specific
event source and the exact time of the `subscribe` call. AutoKitteh queues all
the events from the given event source, starting at this point in time. This
UUID is used later as a handle to [consume these events](#consuming-events).

### Connection/Trigger Name

Connection and trigger names are defined in the AutoKitteh project. This name
identifies the desired event source: a specific third-party connection, or an
HTTP webhook.

### Filter

The filter string is a single-line CEL (Common Expression Language)
expression. This is identical to the `filter` field in project triggers.

:::tip

Complete reference:
https://github.com/google/cel-spec/blob/master/doc/langdef.md

:::

CEL conditions may reference `event_type` (same as in project triggers).
Unlike the `event_type` field in project triggers, a `filter` conditions may
check more than simple equality, and filters may contain more than a single
condition. For example:

```js
// Either 'issue_created' or 'issue_updated' events
event_type == "issue_created" || event_type == "issue_updated";

// Any issue-related events (e.g. issue_created / issue_updated),
// but not other entities (e.g. page_created / page_updated)
event_type.startsWith("issue_");

// Any event that relates to a created entity (e.g. issue_created,
// page_created), but not other categories (e.g. issue_updated)
event_type.endsWith("_created");

// More sophisticated string checks
event_type.contains("substring");
event_type.matches("regular expression");
```

In addition to event types, filters can also check event payloads. For
example:

```js
data.method in ["GET", "HEAD"] && data.url.path.endsWith("/meow");

size(data.collection_value) < 5 || size(data.string_value) > 10;

data.list_value[0].bar == "bar value of first element in foo list";

data.dictionary_value["key"] != "value";
```

:::tip

Data filtering in triggers and subscriptions - when it's possible - is
preferable to Python checks in handler functions, because it prevents the
creation of unnecessary sessions.

:::

## Consuming Events

The `next_event` function receives one or more subscription ID strings, which
were generated by [`subscribe`](#initial-subscription).

This function is blocking, it returns the data of a single event which was
received after the `subscribe` call(s) that generated the given ID(s). You can
call `next_event` any number of times.

Event order is not guaranteed, they are served in the same order they were
received and processed by AutoKitteh.

Example 1 - single subscription ID, without a timeout:

```py
subscription_id = autokitteh.subscribe(connection_or_trigger_name, filter)

event_data = autokitteh.next_event(subscription_id)
```

Example 2 - single subscription ID, with a timeout:

```py
from datetime import timedelta

subscription_id = autokitteh.subscribe(connection_or_trigger_name, filter)

duration = timedelta(seocnds=10)
event_data = autokitteh.next_event(subscription_id, timeout=duration)
```

Example 3 - multiple subscription IDs, without a timeout:

```py
sub_id_1 = autokitteh.subscribe(connection_or_trigger_name, filter)
sub_id_2 = autokitteh.subscribe(connection_or_trigger_name, filter)
sub_id_3 = autokitteh.subscribe(connection_or_trigger_name, filter)

event_data = autokitteh.next_event(sub_id_1, sub_id_2, sub_id_3)
```

Example 4 - multiple subscription IDs, with a timeout:

```py
from datetime import timedelta

sub1 = autokitteh.subscribe(connection_or_trigger_name, filter)
sub2 = autokitteh.subscribe(connection_or_trigger_name, filter)
sub3 = autokitteh.subscribe(connection_or_trigger_name, filter)

duration = timedelta(minutes=1)
event_data = autokitteh.next_event(sub1, sub2, sub3, timeout=duration)
```

### Timeout

This is an optional named parameter.

If you don't specify it, the `next_event` call will block forever and keep the
session running until someone stops the session manually.

When specified, the expected type is a
[timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects)
object.

## Cleanup

When you're no longer interested in receiving events from a specific
subscription, you may call this function:

```py
autokitteh.unsubscribe(subscription_id)
```

:::note

Calling `unsubscribe` is recommended, but not required. Reasonable amounts of
unused event subscriptions do not burden AutoKitteh, especially when the
sessions they were created in have ended.

:::

## Example

```py
from datetime import timedelta

import autokitteh


def on_trigger(_):
    print("Creating an event subscription")
    filter = "data.method == 'GET' && data.url.path.endswith('/meow')"
    get_sub = autokitteh.subscribe("webhook_name", filter)

    print("Waiting for an HTTP GET request without a timeout")
    event_data = autokitteh.next_event(get_sub)
    print(event_data)

    print("Creating another event subscription")
    filter = "data.method == 'POST' && data.url.path.endswith('/meow')"
    post_sub = autokitteh.subscribe("webhook_name", filter)

    print("Waiting for an HTTP GET or POST request with a 1-minute timeout")
    delta = timedelta(minutes=1)
    event_data = autokitteh.next_event(get_sub, post_sub, timeout=delta)
    print(f"Got an HTTP {event_data.method} request: {event_data}")

    print("Canceling all event subscriptions")
    autokitteh.unsubscribe(get_sub)
    autokitteh.unsubscribe(post_sub)

    print("Done")
```

See also this sample project:
https://github.com/autokitteh/kittehub/tree/main/samples/runtime_events


## Waiting for events in programs

In some cases, especially in human-in-the-loop scenarios, a user might want to wait for an event to happen from an execution of another session that started earlier. For that you should use the `autokitteh.next_event`, `autokitteh.subscribe` and `autokitteh.unsubscribe` functions in `pyak`.

### Example

In this example, we trigger a webhook that will wait for another webhook to trigger. Once the second webhook is triggered, the session will end.

manifest.yaml:

```yaml
version: v2

project:
  name: sync_webhook

  triggers:
    - name: first
      type: webhook
      call: program.py:on_first
      is_sync: true

    - name: second
      type: webhook
      # IMPORTANT: No call specified, this is just used to allocate a webhook URL.
      # The script in program.py will just call `next_event` on this
      # to detect that it's triggered.
```

program.py:

```py
from autokitteh import http_outcome, next_event, subscribe


def on_first(_):
    print("First webhook triggered!")

    s = subscribe("second")
    e = next_event(s)

    print("Second webhook triggered!")

    http_outcome(status_code=200, body=e.data.body.text)
```

# TODO


## Tour of AutoKitteh by Projects

All code listings are in txtar format.

### Minimal Projects

```txtar
-- autokitteh.yaml --
version: v2

project:
  name: minimal

-- program.py --
# This can be run using a manual invocation.
def on_trigger(_):
  print("Meow, World!")
```

### Long Running Count

```txtar
-- autokitteh.yaml --
version: v1

project:
  name: minimal

vars:
  - name: N
    value: 10
  - name: T
    value: 1

-- program.py --
from os import getenv
from time import sleep

N = int(getenv("N"))
T = int(getenv("T"))

# This can be run using a manual invocation.
def on_trigger(_):
  for i in range(N):
    print(i)
    # NOTE: Sleep is "hijacked" by AutoKitteh, and if interrupted
    #       (such as by the instance going down), will resume
    #       execution from the same point taking into consideration
    #       the time already spent sleeping.
    sleep(T)
```

### Simple Webhook to Slack

```txtar
-- autokitteh.yaml --
version: v2

project:
  name: webhook_to_slack

  connections:
    - # A single slack connection to authenticate to Slack.
      name: slack_conn
      integration: slack

  triggers:
    - # A webhook to trigger the session.
      # Once applied, AutoKitteh will generate a unique URL for this.
      name: webhook
      type: webhook
      call: program.py:on_webhook

  vars:
    - # Channel to send text to.
      name: CHANNEL
      value: "#general"

-- program.py --
from os import getenv
from autokitteh.slack import slack_client

# `slack_client` returns the official slack client.
# The helper function `slack_client` just initializes the client
# according to the manifest.
#
# NOTE: Since this is done in the global scope, AutoKitteh
#       WILL NOT run this as an activity. This is a feature
#       that allows users to make some things always run, even
#       on replay. Useful for ephemeral client initializations, etc.
client = slack_client("slack_conn")

CHANNEL = getenv("CHANNEL")

# This is triggered when the webhook is hit.
def on_webhook(event):
    # `event.data` always contain the event data as sent from the connection.

    # The following is specific for Webhook payloads:
    payload = event.data.body.json
    channel = payload.get("channel", CHANNEL)
    text = payload.get("text", "Meow, World!")

    # NOTE: This WILL run as an activity, as this is a method called
    #       on an object that was returned from an external package.
    client.chat_postMessage(channel=channel, text=text)
```

### Explicit Activities

```txtar
-- autokitteh.yaml --
version: v1

project:
  name: explicit_activities

  vars:
    - name: SHEET_ID
      value: <some sheet id>

  connections:
    - name: sheets_conn
      integration: googlesheets

-- program.py --
from os import getenv
import autokitteh # The autokitteh module is installed to the default AutoKitteh virtual environment.
from autokitteh.google import google_sheets_client

# google_sheets_client returns the official Google's client.
client = google_sheets_client("sheets_conn").spreadsheets().values()

SHEET_ID = getenv("SHEET_ID")

def on_trigger(_):
  _write()


# The autokitteh.activity decorator allow you to mark a function that must run as activity.
# This allows you to run function with arguments or return values that are not compatible with pickle.
#
# The reason why this is necessary here is that client.update returns
# an object that is not serializable (or "pickleable"), so we cannot have `update`
# and `execute` run in separate activities since the data will need to be serialized
# between their invocations, and thus fail.
@autokitteh.activity
def _write():
   resp = client.update(
        spreadsheetId=SHEET_ID,
        range="Sheet1!A1:B7",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                ["String", "Hello, world!"],
                ["Number", -123.45],
                ["Formula", "=B2*B3"],
            ]
        },
    ).execute()

    print(f"Updated range: {resp['updatedRange']!r}")
```


## General Guidelines

- Each session is running isolated from other sessions:
  - You cannot, for example, store state in memory and expect another session to access it.
  - Environment variables are not shared among different sessions as well.
- For logging, use `print` functions. Currently the `logging` package is not supported.
- NEVER "invent" new AutoKitteh functions that are not explicitly exist in AutoKitteh's SDK (pyak).
- AutoKitteh will display uncaught exceptions to the user. Only catch and translate the exception if absolutely neccessary for the user to understand it.
- When using `autokitteh.subscribe`, no need to `autokitteh.unsubscribe` at the end of the program. These will be done automatically.
- IMPORTANT: All object names (projects, connections, triggers, vars) must be words which adhere to the following regex: `^[a-zA-Z_]\w*$`. To emphasize, do not use dashes, spaces or any other special characters for these.
- Some pyak (AutoKitteh's Python SDK for sessions) can be run only in durable sessions, some only in non-durable sessions and some can run in any mode. Check the function's docstring to know.
