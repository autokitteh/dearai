---
sidebar_position: 7
---

# Event

The API allows you to register for events on a connection and then wait for events
to be received. Under the hood, AutoKitteh waits on a queue and the
`next_event()` function waits until a new event is received.

```python
postSubscription = subscribe(<connection_id>, <event_id>)
event = next_event(postSubscription)
```

[Code sample](https://github.com/autokitteh/kittehub/tree/main/samples/runtime_events)
