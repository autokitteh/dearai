# AutoKitteh Overview

AutoKitteh is a "serverless" platform to build and deploy durable workflows.
Durable workflows are long-running processes that automatically resume after interruptions.

Important Sites:

- https://autokitteh.com for general information about AutoKitteh.
- https://autokitteh.cloud, a SaaS deployment of autokitteh that is publicly available.

# Model: Entities & Relationships

- PROJECT has RESOURCEs, CONNECTIONs, TRIGGERs, and VARIABLEs as configuration.
- AutoKitteh supports a number of native INTEGRATIONs.
- an INTEGRATION is a native implementation of an interface to an external system, such as Linear, Slack, etc.
- CONNECTION is a connection to a third-party service using an INTEGRATION, such as Slack, JIRA, Linear, etc.
  a CONNECTION is always associated with an INTEGRATION.
  a CONNECTION can have mutliple TRIGGERs defined on it.
- a DEPLOYMENT is a deployed version of a PROJECT.
- EVENTs are sent by CONNECTIONs. TRIGGERs define what to do with EVENTs. An EVENT consists on JSON formatted data.
- a SESSION starts when a DEPLOYMENT is triggered by a TRIGGER. a SESSION a workflow being run.
- RESOURCE is a source code file, but can be also any file type, like a yaml or json files.
- TRIGGER is a trigger to start a workflow, such as a CONNECTION event, webhook or a SCHEDULE.
  - WEBHOOK and SCHEDULE triggers do not require a CONNECTION.
  - CONNECTION event triggers require a CONNECTION.
- VARIABLE is a key-value pair that is defined in the project and can be used in the workflow.

## Integrations

The following integration names are supported:
- asana
- auth0
- aws
- chatgpt
- confluence
- discord
- github
- gmail
- googlecalendar
- googledrive
- googleforms
- googlegemini
- googlesheets
- height
- hubspot
- jira
- slack
- twilio
- zoom


## Connections

A CONNECTION is created in order to either receive events from an external application (such as Slack, JIRA, etc) or to perform some operation on an external service.

Certain CONNECTIONs need to be initialized after creation in order for them to function. Often, the initialization means establishing authentication with the external application. For example, if creating either a Slack or GitHub connection, the user is expected to initialize the connection using OAuth, which AutoKitteh supplies a UI for for. Another authentication method, in case of Slack or GitHub, can be using a PAT, which AutoKitteh allows to fill in the connection view.

## Triggers

A TRIGGER can be of one of several types.

- Webhook Trigger: when it is created, AutoKitteh generates a unique URL that when it is hit, the trigger will be invoked.
- Schedule Trigger: runs on a schedule, defined by a cronspec.
- Connection Trigger: A third party service sends an event, which when the trigger matches the event - it is invoked.

A TRIGGER can include a FILTER defintion in its `filter` field. The FILTER is specified as a Google CEL expression. The CEL expression takes as input the EVENT payload, under the name `data`. The event type will be under the name `event_type`.

A TRIGGER points to a function execute once is is hit and matches optional filter. The method is specified in the format: "filename:method_name", when `filename` is a name of a RESOURCE in the PROJECT.

### Example: Webhook: Only match with POST JSON requests

```
name: receive_http_post_json
type: webhook
event_type: post
filter: data.headers["Content-Type"].startsWith("application/json")
call: webhooks.py:on_http_post_json
```

### Example: Webhook: Only match with GET or POST requests

```
name: receive_http_get_or_head
type: webhook
filter: data.method in ["GET", "HEAD"]
call: webhooks.py:on_http_get_or_head
```

### Example: Slack: Only match `interaction` from a specific user id

```
name: slack_interaction_from_specific_id
connection: slack_connection
filter: event_type == 'interaction' && data.user.id == 'SOME_SLACK_ID'
```

### Example: Slack: Slack command where its text is "break-glass"

```
name: break_glass_slack_command
connection: slack_connection
event_type: slash_command
call: program.py:on_slack_slash_command
filter: data.text == "break-glass"
```

### Example: GitHub: PR action is either "opened" or "reopened"

```
name: github_pull_request
connection: github_conn
event_type: pull_request
filter: data.action == "opened" || data.action == "reopened"
call: program.py:on_github_pull_request
```

### Example: Schedule Triggers

```
name: weekly
schedule: "0 0 * * 1"
call: program.py:weekly_user_growth
```

```
name: weekly
schedule: @every 1w
call: program.py:weekly_user_growth
```

# Sessions

SESSIONs are created as a result of a TRIGGER. A session runs the code in the project, according to the TRIGGER defintion. When a SESSION is being ran, a specific function in its code is being invoked. That function receives the EVENT that triggered it via its argument. If the trigger is a schedule trigger, that event is empty.

IMPORTANT: Session invocation is asynchronic. The CONNECTION or TRIGGER invoking the session do not wait for the result of the session. For example, if a WEBHOOK trigger is invoked, it will ALWAYS return a 202 response, regardless what the session does.

NOTE: A Session is running under the hood as a Temporal Workflow. AutoKitteh knows how to break down the project code running in a session into separate Temporal Activities.


# Durability

AutoKitteh projects run code in a durable, fault-tolerant manner using Temporal (https://temporal.io) under the hood. Temporal ensures reliability by designating non-deterministic code as ACTIVITIES, which cache their results once completed.

When a project fails due to infrastructure issues—such as instance crashes or network problems—Temporal uses a REPLAY mechanism. It reruns the entire workflow from the beginning, but leverages the cached activity results to skip re-executing those parts, allowing them to return immediately.
AutoKitteh analyzes the Abstract Syntax Tree (AST) of project code to intelligently determine which function calls should run as ACTIVITIES and which should not.

# Operation

There are three ways to configure a project:

1. Using an autokitteh.yaml, which is also known as "the project manifest".
2. Using the CLI.
3. Using the Web UI.




## Manifest

An AutoKitteh manifest is a yaml or json file that defines how a project is configured.
It defines the PROJECT, CONNECTIONs, TRIGGERs, and VARIABLEs.

A manifest is "applied" by the user (via CLI, or automatically by the Web Application). When it is applied, it creates or updates the project configuration accordingly.

The manifest is defined according to this schema:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://go.autokitteh.dev/autokitteh/internal/manifest/manifest",
  "$ref": "#/$defs/Manifest",
  "$defs": {
    "Connection": {
      "properties": {
        "name": {
          "type": "string"
        },
        "integration": {
          "type": "string"
        },
        "vars": {
          "items": {
            "$ref": "#/$defs/Var"
          },
          "type": "array"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name",
        "integration"
      ]
    },
    "Manifest": {
      "properties": {
        "version": {
          "type": "string"
        },
        "project": {
          "$ref": "#/$defs/Project"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "version"
      ]
    },
    "Project": {
      "properties": {
        "name": {
          "type": "string"
        },
        "connections": {
          "items": {
            "$ref": "#/$defs/Connection"
          },
          "type": "array"
        },
        "triggers": {
          "items": {
            "$ref": "#/$defs/Trigger"
          },
          "type": "array"
        },
        "vars": {
          "items": {
            "$ref": "#/$defs/Var"
          },
          "type": "array"
        }
      },
      "additionalProperties": false,
      "type": "object"
    },
    "Trigger": {
      "properties": {
        "name": {
          "type": "string"
        },
        "event_type": {
          "type": "string"
        },
        "filter": {
          "type": "string"
        },
        "type": {
          "type": "string",
          "enum": [
            "schedule",
            "webhook",
            "connection"
          ]
        },
        "schedule": {
          "type": "string"
        },
        "webhook": {
          "properties": {},
          "additionalProperties": false,
          "type": "object"
        },
        "connection": {
          "type": "string"
        },
        "call": {
          "type": "string"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name"
      ]
    },
    "Var": {
      "properties": {
        "name": {
          "type": "string"
        },
        "value": {
          "type": "string"
        },
        "secret": {
          "type": "boolean"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name",
        "value"
      ]
    }
  }
}
```

### Examples



```yaml
# This YAML file is a declarative manifest that describes the setup
# of an AutoKitteh project that demonstrates integration with Auth0.

version: v1

project:
  name: auth0_sample

  vars:
    - name: ROLE_ID
      value:
    - name: TIME_INTERVAL
      value: 7d

  connections:
    - name: auth_conn
      integration: auth0

  triggers:
    - name: weekly
      schedule: 0 0 * * 1
      call: program.py:weekly_user_growth
    - name: assign_role_webhook
      type: webhook
      event_type: post
      call: program.py:assign_role
```

```yaml
# This YAML file defines a manifest for an AutoKitteh project that
# creates a Langgraph bot.

version: v1

project:
  name: Langgraph_Bot

  connections:
    - name: slack_conn
      integration: slack
    - name: sheets_conn
      integration: googlesheets

  triggers:
    - name: on_message
      event_type: app_mention
      connection: slack_conn
      call: program.py:on_app_mention

  vars:
    - name: GOOGLE_API_KEY
      value: ""
    - name: TAVILY_API_KEY
      value: ""
```

```yaml
# This YAML file is a declarative manifest that describes the setup
# of an AutoKitteh project that monitors comments on GitHub issues.

version: v1

project:
  name: github_issue_alert

  vars:
    - name: SLACK_CHANNEL_NAME_OR_ID
      value: github-issues

  connections:
    - name: slack_conn
      integration: slack
    - name: github_conn
      integration: github

  triggers:
    - name: on_issue_comment
      event_type: issue_comment
      connection: github_conn
      call: program.py:on_issue_comment
    - name: on_issue_event
      event_type: issues
      connection: github_conn
      call: program.py:on_issue_event
```

```yaml
# This YAML file is a declarative manifest that describes the setup
# of an AutoKitteh project that logs messages from Discord to a
# Google Sheets document.

version: v1

project:
  name: discord_to_spreadsheet

  vars:
    - name: RANGE_NAME
      value: Sheet1!A1
    - name: SPREADSHEET_ID
      value:

  connections:
    - name: discord_conn
      integration: discord
    - name: googlesheets_conn
      integration: googlesheets

  triggers:
    - name: on_discord_message
      connection: discord_conn
      event_type: message_create
      call: program.py:on_discord_message
```





# Code

An AutoKitteh project contains configuration (as described by a manifest) and code.
The code is Python 3 code.

By default, AutoKitteh makes available the following packages for the program:
"""
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
hubspot-api-client ~= 11.1
kubernetes ~= 31.0
msgraph-sdk ~= 1.18
openai ~= 1.57
PyGithub ~= 2.6
simple-salesforce ~= 1.12
slack-sdk ~= 3.33
tenacity ~= 9.0
twilio ~= 9.4
beautifulsoup4 ~= 4.12
grpcio ~= 1.68
grpcio-reflection ~= 1.68
PyYAML ~= 6.0
requests ~= 2.32
tenacity ~= 9.0
"""

If the additional packages are required, they can be specified in a `requirements.txt` file.

## Pitfalls

### Function Return Value Must Be Pickleable

We use pickle to pass function arguments back to AutoKitteh to run as an activity. See What can be pickled and unpickled? for supported types. Most notably, the following can't be pickled:

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

### Function Timeout

If a function that runs in a workflow context (not in an activity) takes a long time, it might cause a timeout.

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
- `data` is the payload to present to that function. It could read this from the `event` parameter as `event.data`.
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
event_type == 'issue_created' || event_type == 'issue_updated'

// Any issue-related events (e.g. issue_created / issue_updated),
// but not other entities (e.g. page_created / page_updated)
event_type.startsWith('issue_')

// Any event that relates to a created entity (e.g. issue_created,
// page_created), but not other categories (e.g. issue_updated)
event_type.endsWith('_created')

// More sophisticated string checks
event_type.contains('substring')
event_type.matches('regular expression')
```

In addition to event types, filters can also check event payloads. For
example:

```js
data.method in ['GET', 'HEAD'] && data.url.path.endsWith('/meow')

size(data.collection_value) < 5 || size(data.string_value) > 10

data.list_value[0].bar == 'bar value of first element in foo list'

data.dictionary_value['key'] != 'value'
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
received after the `subscribe` call(s) that generared the given ID(s). You can
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


# TODO


## Tour of AutoKitteh by Projects

All code listings are in txtar format.

### Minimal Projects

```txtar
-- autokitteh.yaml --
version: v1

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
version: v1

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
  name: explicit_activites

  vars:
    - name: SHEET_ID
      value: <some sheet id>

  connections:
    - name: sheets_conn
      integration: googlesheets

-- program.py --
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
# The reason why this is neccessary here is that client.update returns
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


# Documentation Adherence Rules

- Only reference commands, APIs, syntax, or procedures that are explicitly mentioned in the provided documentation
- If specific CLI commands or API calls are not documented, say "the documentation doesn't specify the exact command" rather than inferring or assuming
- When documentation mentions something exists (like "CLI" or "API") but doesn't provide details, acknowledge the gap rather than filling it with assumptions
- If you need to reference external knowledge not in the docs, clearly label it as "based on general knowledge, not the provided documentation"
- Always cite specific sections of the documentation when making claims about how something works
