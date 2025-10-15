---
sidebar_position: 8
description: Synchronous webhooks and HTTP responses
title: Synchronous Webhooks
---

# Synchronous Webhooks

AutoKitteh webhooks can operate in two modes: **asynchronous** (default) and **synchronous**. This page explains how to configure and use synchronous webhooks to return HTTP responses from your workflows.

## Asynchronous vs. Synchronous

### Asynchronous Webhooks (Default)

By default, webhook triggers return an immediate `202 Accepted` response and execute the workflow in the background.

```yaml
triggers:
  - name: webhook
    type: webhook
    call: program.py:handler
    # is_sync: false (default)
```

**Behavior:**
1. HTTP request arrives
2. AutoKitteh returns `202 Accepted` immediately
3. Workflow session starts and runs independently
4. Client receives response before workflow completes

**Use cases:**
- Long-running workflows
- Fire-and-forget operations
- Webhooks from services that don't need responses
- Background processing

### Synchronous Webhooks

With `is_sync: true`, the webhook waits for the workflow to produce a response before replying to the HTTP client.

```yaml
triggers:
  - name: api_endpoint
    type: webhook
    is_sync: true
    call: program.py:api_handler
```

**Behavior:**
1. HTTP request arrives
2. Workflow session starts
3. AutoKitteh streams session outcomes
4. When workflow calls `http_outcome(more=False)`, that outcome becomes the HTTP response
5. Client receives the response
6. Workflow can continue executing after sending response

**Use cases:**
- REST APIs
- Webhooks that require immediate response
- Request/response patterns
- Validation endpoints

## Basic Example

### Configuration

```yaml
version: v2

project:
  name: simple_api

  triggers:
    - name: api
      type: webhook
      is_sync: true
      call: program.py:handle_request
```

### Code

```python
import json
import autokitteh

def handle_request(event):
    # Parse request
    data = json.loads(event.data.body.text)

    # Process
    result = {"message": f"Hello, {data['name']}!"}

    # Send response
    autokitteh.http_outcome(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(result)
    )
```

### Request/Response

```bash
$ curl -X POST http://localhost:9980/webhooks/abc123 \
    -H "Content-Type: application/json" \
    -d '{"name": "Alice"}'

{"message": "Hello, Alice!"}
```

## The `http_outcome()` Function

### Signature

```python
autokitteh.http_outcome(
    status_code: int = 200,
    headers: dict = None,
    body: str = None,
    more: bool = False
) -> None
```

### Parameters

- `status_code` (int): HTTP status code (default: 200)
- `headers` (dict): Response headers as key-value pairs
- `body` (str): Response body content
- `more` (bool): If `True`, workflow continues sending outcomes. If `False` (default), this outcome becomes the final HTTP response

### Examples

**Simple text response:**
```python
autokitteh.http_outcome(
    status_code=200,
    body="Success"
)
```

**JSON response:**
```python
import json

autokitteh.http_outcome(
    status_code=200,
    headers={"Content-Type": "application/json"},
    body=json.dumps({"status": "ok", "data": result})
)
```

**Error response:**
```python
autokitteh.http_outcome(
    status_code=400,
    headers={"Content-Type": "application/json"},
    body=json.dumps({"error": "Invalid input"})
)
```

**Custom headers:**
```python
autokitteh.http_outcome(
    status_code=201,
    headers={
        "Content-Type": "application/json",
        "X-Request-ID": request_id,
        "Location": f"/api/resources/{resource_id}"
    },
    body=json.dumps({"id": resource_id})
)
```

## Streaming Outcomes

The `more` parameter allows workflows to send multiple outcomes before the final response.

```python
def handle_request(event):
    # Send intermediate outcome (more=True)
    autokitteh.http_outcome(
        status_code=200,
        body="Processing...",
        more=True
    )

    # Do work
    result = long_running_operation()

    # Send final outcome (more=False, default)
    autokitteh.http_outcome(
        status_code=200,
        body=f"Result: {result}"
    )

    # Workflow can continue after response is sent
    log_completion(result)
```

:::note

Only the **last outcome with `more=False`** becomes the HTTP response. Intermediate outcomes are logged but not sent to the client.

:::

## Continue After Response

Workflows can continue executing after sending the HTTP response. This is useful for:

- Logging and cleanup
- Triggering follow-up actions
- Updating metrics
- Background processing

```python
def handle_order(event):
    order = validate_order(event.data)

    # Send immediate response to client
    autokitteh.http_outcome(
        status_code=202,
        headers={"Content-Type": "application/json"},
        body=json.dumps({"order_id": order.id, "status": "accepted"})
    )

    # Continue processing after response sent
    process_payment(order)
    update_inventory(order)
    send_confirmation_email(order)
    notify_warehouse(order)
```

## Advanced Examples

### REST API with Validation

```python
import json
import autokitteh

def api_create_user(event):
    try:
        # Parse request
        data = json.loads(event.data.body.text)

        # Validate
        if not data.get("email") or not data.get("name"):
            autokitteh.http_outcome(
                status_code=400,
                headers={"Content-Type": "application/json"},
                body=json.dumps({"error": "Missing required fields"})
            )
            return

        # Create user
        user = create_user(data["email"], data["name"])

        # Success response
        autokitteh.http_outcome(
            status_code=201,
            headers={
                "Content-Type": "application/json",
                "Location": f"/api/users/{user.id}"
            },
            body=json.dumps({
                "id": user.id,
                "email": user.email,
                "name": user.name
            })
        )

    except json.JSONDecodeError:
        autokitteh.http_outcome(
            status_code=400,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"error": "Invalid JSON"})
        )
    except Exception as e:
        autokitteh.http_outcome(
            status_code=500,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"error": "Internal server error"})
        )
```

### Webhook with Signature Verification

```python
import hmac
import hashlib
import json
import autokitteh

SECRET = os.getenv("WEBHOOK_SECRET")

def verify_webhook(event):
    # Get signature from headers
    signature = event.data.headers.get("X-Hub-Signature-256", "")
    body = event.data.body.bytes

    # Verify signature
    expected = "sha256=" + hmac.new(
        SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        autokitteh.http_outcome(
            status_code=401,
            body="Invalid signature"
        )
        return None

    # Parse and return payload
    return json.loads(body)

def handle_webhook(event):
    data = verify_webhook(event)
    if not data:
        return  # Response already sent

    # Process webhook
    process_event(data)

    # Send success response
    autokitteh.http_outcome(
        status_code=200,
        body="OK"
    )
```

### Waiting for Events

Synchronous webhooks can wait for other events before responding:

```yaml
triggers:
  - name: first
    type: webhook
    is_sync: true
    call: program.py:on_first

  - name: second
    type: webhook
    # No call - just allocates a webhook URL
```

```python
from datetime import timedelta
from autokitteh import http_outcome, next_event, subscribe

def on_first(event):
    print("First webhook triggered, waiting for second...")

    # Subscribe to second webhook
    sub = subscribe("second")

    # Wait up to 1 minute
    second_event = next_event(sub, timeout=timedelta(minutes=1))

    if second_event:
        # Send response with data from second webhook
        http_outcome(
            status_code=200,
            body=f"Got second webhook: {second_event.data.body.text}"
        )
    else:
        # Timeout
        http_outcome(
            status_code=408,
            body="Timeout waiting for second webhook"
        )
```

See: [kittehub/samples/sync_webhook](https://github.com/autokitteh/kittehub/tree/main/samples/sync_webhook)

## Performance Considerations

### Response Time

Synchronous webhooks block the HTTP connection until the workflow sends a response. Keep workflows fast:

- ✅ Validate and respond quickly
- ✅ Use non-durable mode for speed (see below)
- ✅ Move heavy processing after the response
- ⚠️ Avoid long database queries before response
- ⚠️ Avoid waiting for external APIs before response

### Durability Mode

For synchronous webhooks, consider using **non-durable mode** for better performance:

```yaml
triggers:
  - name: api
    type: webhook
    is_sync: true
    is_durable: false  # Faster, recommended for APIs
    call: program.py:handler
```

**Durable mode** (`is_durable: true`) adds overhead and may cause timeouts during replay. Use only if:
- Response time is not critical
- Workflow has critical operations before response
- You need state persistence during the response phase

See: [Durability Modes](/develop/durability)

### Timeouts

- HTTP clients typically timeout after 30-60 seconds
- Keep response generation under 10 seconds for good user experience
- Use `more=False` to send response quickly
- Continue heavy work after response is sent

## Error Handling

Always handle errors and send appropriate HTTP responses:

```python
def handle_request(event):
    try:
        # Your logic here
        result = process(event.data)

        autokitteh.http_outcome(
            status_code=200,
            body=json.dumps({"result": result})
        )

    except ValueError as e:
        # Client error
        autokitteh.http_outcome(
            status_code=400,
            body=json.dumps({"error": str(e)})
        )

    except Exception as e:
        # Server error
        print(f"Error: {e}")
        autokitteh.http_outcome(
            status_code=500,
            body=json.dumps({"error": "Internal server error"})
        )
```

## Comparison: Async vs. Sync

| Feature | Async (`is_sync: false`) | Sync (`is_sync: true`) |
|---------|-------------------------|------------------------|
| HTTP Response | Immediate `202` | From workflow |
| Response Time | < 1ms | Depends on workflow |
| Durability | Recommended | Use with caution |
| Use Case | Background jobs | APIs, webhooks |
| Client Waits | No | Yes |
| Custom Status | No | Yes |
| Custom Headers | No | Yes |
| Custom Body | No | Yes |

## Best Practices

1. **Use async by default** - only enable sync when needed
2. **Respond quickly** - send response within seconds
3. **Validate early** - check inputs before heavy processing
4. **Use non-durable mode** - for better API performance
5. **Handle errors** - always send appropriate status codes
6. **Set Content-Type** - specify the response format
7. **Continue after response** - move heavy work after `http_outcome()`
8. **Test timeouts** - ensure workflows respond before client timeout
9. **Log outcomes** - track responses for debugging
10. **Document your API** - specify expected request/response formats

## Limitations

- Only works with `type: webhook` triggers
- Cannot change response after `http_outcome(more=False)` is called
- HTTP client must support waiting for response
- Some webhook providers expect immediate `200 OK` (use async mode)

## See Also

- [SDK Reference - http_outcome()](/develop/sdk_reference#autokittehhttp_outcome)
- [Durability Modes](/develop/durability)
- [Webhook Events](/integrations/http/events)
- [Manifest Reference](/develop/manifest)
- [Example Project: sync_webhook](https://github.com/autokitteh/kittehub/tree/main/samples/sync_webhook)
