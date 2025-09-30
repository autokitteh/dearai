# Event Structure

Event handler functions receive a single argument of type `autokitteh.Event`. It is recommended this argument to be called `event`:

```py
from autokitteh import Event

def on_some_trigger(event: Event):
    ...
```

The event contains the `session_id` for the session and the event payload in its `data` field.

Each integration has a different event payload format. See details about each integration format in the `integrations/` folder.

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

    http_outcome(status_code=200, body=e.body.text)
```
