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
