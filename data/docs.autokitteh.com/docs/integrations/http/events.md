---
sidebar_position: 2
sidebar_label: Events
description: Supported event types, event payloads, and trigger definitions
---

# Incoming Events

## Event Types

AutoKitteh webhooks accept the following HTTP request methods (the event type
is the HTTP method in **lowercase**):

- RFC 9110: [get](https://www.rfc-editor.org/rfc/rfc9110#name-get),
  [head](https://www.rfc-editor.org/rfc/rfc9110#name-head),
  [post](https://www.rfc-editor.org/rfc/rfc9110#name-post),
  [put](https://www.rfc-editor.org/rfc/rfc9110#name-put),
  [delete](https://www.rfc-editor.org/rfc/rfc9110#name-delete),
  [options](https://www.rfc-editor.org/rfc/rfc9110#name-options)

- RFC 5789: [patch](https://www.rfc-editor.org/rfc/rfc5789)

## Event Data Payload

Handler functions receive an `event` object as input. This object has a `data`
attribute, which has the following payload:

```python
event.data = {
    "method": "GET",
    "url": {
        "path": "/webhooks/slug",
        "query": [
            "key1": "value1",
            "key2": "value2",
        ],
        "raw_query": "key1=value1&key2=value2",
        "fragment": "",
        "raw_fragment": "",
    },
    "raw_url": "/webhooks/slug?key1=value1&key2=value2",
    "headers": [
        "Accept": "*/*",
        "Content-Length": 123,
        "Content-Type": "...",
        "User-Agent": "curl/x.y.z",
    ],
    "body": {
        "bytes": b"...",   # None if there is no body
        "form":  { ... },  # None if the body is not a URL-encoded form
        "json":  { ... },  # None if the body is not a JSON object
    }
}
```

Note that the fields in `data` are accessible as **dictionary keys** as well
as **object attributes**. For example: `event.data.method` is the same as
`event.data["method"]` and `event.data.get("method")`.

:::tip

The difference between them is that `get()` allows you to specify a default
value in case the field is missing.

:::

## Trigger Definition

Unlike most integrations, webhooks do not depend on predefined AutoKitteh
connections. Instead, you need to specity the trigger's type as `webhook`:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    call: filename.py:handler_function_name
```

In addition, you can limit the trigger to specific confitions.

### Option 1: Single Event Type

Reminder: AutoKitteh webhook event types are HTTP methods in lowercase.

Examples:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    event_type: get
    call: filename.py:handler_function_name
```

```yaml
triggers:
  - name: trigger_name
    type: webhook
    event_type: post
    call: filename.py:handler_function_name
```

### Option 2: CEL Filter Expression

CEL language definition: https://github.com/google/cel-spec/blob/master/doc/langdef.md

#### Example 1

Let a single handler function support multiple HTTP methods:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    filter: data.method == "GET" || data.method == "POST"
    call: filename.py:handler_function_name
```

Or this equivalent-but-simpler filter:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    filter: data.method in ["GET", "POST"]
    call: filename.py:handler_function_name
```

#### Example 2

Start a session only if the URL path has a specific suffix:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    filter: data.url.path.endsWith("/foo")
    call: filename.py:handler_function_name
```

Or this equivalent filter, which uses a
[regular expression](https://github.com/google/re2/wiki/Syntax):

```yaml
triggers:
  - name: trigger_name
    type: webhook
    filter: data.url.path.matches("^/webhooks/.*/foo$")
    call: filename.py:handler_function_name
```

:::tip

Regular expressions may seem more complicated in this case, but they allow
you to define triggers that expect URL patterns containing parameters.

:::

#### Example 3

Start a session only for HTTP POST requests with a JSON body:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    event_type: post
    filter: data.headers["Content-Type"] == "application/json"
    call: filename.py:handler_function_name
```

:::tip

The `filter` expression above doesn't take into account
[optional parameters](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type#syntax)
such as `charset` or `boundary`. The alternative expressions below solve this
issue.

:::

```yaml
triggers:
  - name: trigger_name
    type: webhook
    event_type: post
    filter: data.headers["Content-Type"].startsWith("application/json")
    call: filename.py:handler_function_name
```

Or:

```yaml
triggers:
  - name: trigger_name
    type: webhook
    event_type: post
    filter: data.headers["Content-Type"].matches("application/json(;.*)?")
    call: filename.py:handler_function_name
```

## Configuration and Code Samples

All the concepts above are demonstrated in this AutoKitteh project:
https://github.com/autokitteh/kittehub/tree/main/samples/http
