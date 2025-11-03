# Webhook

- Webhooks are special case: There is no such thing as a "webhook connection". Webhooks are defined only as triggers.
- The webhook endpoint is "https://api.autokitteh.cloud/webhooks/<trigger_id>".
- A session created due to a webhook can specify what the caller will get as a response. For that to work, specify "is_sync: true" on the trigger. Then use the `http_outcome` function from pyak to specify the response. The webhook service streams all session outcomes until it receives one with `more=False`, which it converts into the HTTP response. The session can continue running after the response is sent.

## Example: Returning a custom HTTP response

```python
from autokitteh import http_outcome

def on_webhook(event):
    # Process the webhook...
    result = process_data(event.data)

    # Return HTTP response with more=False to end streaming
    http_outcome(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body={"result": result},
        more=False  # This signals that no more outcomes will follow
    )

    # Code here will continue running after the response is sent
    log_to_database(result)
```
