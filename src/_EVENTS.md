# Event Structure

Event handler functions receive a single argument of type `autokitteh.Event`. It is recommended this argument to be called `event`:

```py
from autokitteh import Event

def on_some_trigger(event: Event):
    ...
```

The event contains the `session_id` for the session and the event payload in its `data` field.

Each integration has a different event payload format. See details about each integration format in the `integrations/` folder.

## Which Integrations Support Events?

Before adding `event_type` to a trigger, check this list to verify the integration supports events.

### Integrations WITH Events

- slack
- github
- discord
- linear
- zoom
- jira
- confluence
- googlecalendar
- googleforms
- googledrive
- gmail
- hubspot
- telegram

For event details, see the integration's file in the `integrations/` folder.

### Integrations WITHOUT Events

**API-only integrations - use `type: webhook` or `type: schedule` to trigger, then call their APIs:**

- auth0
- aws
- anthropic
- chatgpt
- asana
- notion
- pipedrive
- reddit
- twilio
- youtube
- kubernetes
- googlegemini
- microsoft_teams
- salesforce

**Example - WRONG:**

```yaml
triggers:
  - name: on_auth0_login
    connection: auth0_conn
    event_type: user.login # ❌ DOES NOT EXIST
```

**Example - CORRECT:**

```yaml
triggers:
  - name: hourly_sync
    type: schedule
    schedule: "0 * * * *"
    call: program.py:sync_auth0_users # Calls auth0 API inside
```

{% include "_data/docs/develop/events/subscription.md" %}

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
