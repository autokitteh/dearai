---
sidebar_position: 7
description: Understanding durable and non-durable execution modes
title: Durability Modes
---

# Durability Modes

AutoKitteh supports two execution modes for workflows: **durable** and **non-durable**. Understanding the difference helps you choose the right mode for your use case.

## Overview

| Mode            | Default For | Fault Tolerance | Replay | Performance | Use Case                                    |
| --------------- | ----------- | --------------- | ------ | ----------- | ------------------------------------------- |
| **Durable**     | Manifest v1 (legacy) | High            | Yes    | Slower      | Long-running workflows, critical operations |
| **Non-Durable** | Manifest v2 (recommended) | Basic retry     | No     | Faster      | Short-lived operations, simple webhooks     |

## Non-Durable Mode

**Default for manifest v2 and later.**

In non-durable mode, AutoKitteh runs the entire session as a single activity. If the workflow fails due to infrastructure issues (instance crashes, network problems), AutoKitteh simply retries the entire workflow from the beginning.

### Characteristics

- ✅ **Faster execution** - no overhead from activity tracking
- ✅ **Simpler behavior** - entire workflow runs as one unit
- ⚠️ **Basic retry only** - restarts from scratch on failure
- ⚠️ **No replay mechanism** - cannot resume from checkpoint
- ⚠️ **Limited durability** - suitable for short operations only

### When to Use Non-Durable Mode

- **Short-lived workflows** (seconds to minutes)
- **Idempotent operations** that are safe to retry completely
- **Simple API calls** or webhooks
- **High-throughput scenarios** where speed matters
- **Stateless operations** without side effects

### Example

```yaml
version: v2

project:
  name: simple_webhook

  triggers:
    - name: webhook
      type: webhook
      # is_durable defaults to false for v2
      call: program.py:handler
```

```python
def handler(event):
    # This entire function runs as a single activity
    data = event.data.body.json
    result = process(data)
    send_notification(result)
```

## Durable Mode

**Default for manifest v1 (legacy). Can be explicitly enabled for v2.**

In durable mode, AutoKitteh uses [Temporal](https://temporal.io) under the hood to provide fault-tolerant, resumable execution. AutoKitteh automatically analyzes your code to determine which operations should run as separate activities.

### How It Works

1. **Activity Detection**: AutoKitteh analyzes the Abstract Syntax Tree (AST) of your code to identify which function calls should be activities
2. **Result Caching**: Each activity's result is cached when it completes
3. **Replay on Failure**: If the workflow fails, Temporal replays the entire workflow from the start
4. **Cache Utilization**: During replay, cached activity results are used instead of re-executing them

### Characteristics

- ✅ **High fault tolerance** - survives infrastructure failures
- ✅ **State persistence** - maintains state across crashes
- ✅ **Smart replay** - resumes from cached activity results
- ✅ **Long-running support** - workflows can run for days/weeks
- ⚠️ **Slower execution** - overhead from activity tracking and caching
- ⚠️ **Determinism required** - code must be deterministic

### When to Use Durable Mode

- **Long-running workflows** (hours, days, weeks)
- **Critical operations** that must complete reliably
- **Multi-step processes** with external API calls
- **Workflows with human-in-the-loop** (approvals, manual steps)
- **Complex orchestration** across multiple services
- **Workflows that must survive server restarts**

### Example

```yaml
version: v2

project:
  name: critical_workflow

  triggers:
    - name: important_task
      type: webhook
      is_durable: true # Explicitly enable durable mode
      call: program.py:handler
```

```python
import autokitteh

def handler(event):
    # Step 1: External API call (automatic activity)
    user = fetch_user(event.data.user_id)

    # Step 2: Database operation (automatic activity)
    record = create_record(user)

    # Step 3: Long operation (explicit activity)
    result = process_large_dataset(record)

    # Step 4: Notification (automatic activity)
    send_email(user.email, result)
```

If this workflow crashes after Step 2, Temporal will:

1. Replay the workflow from the beginning
2. Use cached results from Steps 1 and 2 (no re-execution)
3. Continue from Step 3

## Automatic Activity Detection

In durable mode, AutoKitteh automatically treats these as activities:

- **External function calls** from imported modules
- **API client methods** (e.g., `slack.chat_postMessage()`)
- **Database operations** (e.g., `cursor.execute()`)
- **File I/O operations** (when called from external modules)
- **HTTP requests** via libraries like `requests`

**Not treated as activities:**

- **Built-in Python functions** (e.g., `len()`, `print()`)
- **Module-level code** executed during import
- **Operations within the same file** unless explicitly marked

### Explicit Activity Marking

Use the `@autokitteh.activity` decorator to explicitly mark a function as an activity:

```python
import autokitteh

@autokitteh.activity
def complex_operation(data):
    # Entire function runs as single activity
    # Useful for:
    # - Non-pickleable return values
    # - Grouping multiple operations
    # - Long computations
    result = process_step1(data)
    result = process_step2(result)
    return result
```

See: [Using the autokitteh.activity Decorator](/develop/python#using-the-autokittehactivity-decorator)

## Choosing Between Modes

### Use Non-Durable When:

```python
# Simple webhook handler
def handle_webhook(event):
    data = event.data.body.json

    # Quick validation and response
    if not validate(data):
        return

    # Single API call
    slack.chat_postMessage(
        channel="#alerts",
        text=f"Received: {data['message']}"
    )
```

### Use Durable When:

```python
# Complex multi-step workflow
def process_order(event):
    order_id = event.data.order_id

    # Step 1: Validate with payment service
    payment = validate_payment(order_id)

    # Step 2: Reserve inventory (may take time)
    items = reserve_inventory(order_id)

    # Step 3: Wait for warehouse confirmation
    confirmation = wait_for_warehouse(order_id, timeout=hours(24))

    # Step 4: Send to shipping
    tracking = create_shipment(order_id, items)

    # Step 5: Notify customer
    send_confirmation_email(order_id, tracking)
```

## Configuration

### Per-Trigger Configuration

Control durability on a per-trigger basis:

```yaml
triggers:
  # Durable trigger
  - name: critical_process
    type: webhook
    is_durable: true
    call: program.py:critical_handler

  # Non-durable trigger
  - name: simple_webhook
    type: webhook
    is_durable: false
    call: program.py:simple_handler
```

### Version Defaults

```yaml
# Manifest v1 (legacy) - durable by default
version: v1
project:
  name: my_project
  triggers:
    - name: task
      # is_durable: true (implicit)
      call: program.py:handler

# Manifest v2 (recommended) - non-durable by default
version: v2
project:
  name: my_project
  triggers:
    - name: task
      # is_durable: false (implicit)
      call: program.py:handler
```

## Durability and Sync Webhooks

When using synchronous webhooks (`is_sync: true`), consider the durability mode carefully:

```yaml
# Non-durable sync webhook (fast response)
triggers:
  - name: api_endpoint
    type: webhook
    is_sync: true
    is_durable: false  # Recommended for APIs
    call: program.py:api_handler

# Durable sync webhook (careful - may timeout)
triggers:
  - name: complex_api
    type: webhook
    is_sync: true
    is_durable: true  # Use only if response can wait
    call: program.py:complex_handler
```

:::warning

Synchronous webhooks with durable mode may timeout if the workflow takes too long or requires replay. For HTTP APIs, prefer non-durable mode or use asynchronous webhooks with callback mechanisms.

:::

See: [Synchronous Webhooks](/develop/sync_webhooks)

## Limitations and Considerations

### Durable Mode Limitations

1. **Code must be deterministic** - same inputs must produce same outputs
2. **Non-pickleable values** - some objects cannot be passed between activities
3. **Performance overhead** - activity tracking adds latency
4. **Replay behavior** - code runs multiple times during replay

See: [Function Return Value Must Be Pickleable](/develop/python#function-return-value-must-be-pickleable)

### Non-Durable Mode Limitations

1. **No state persistence** - workflow state lost on failure
2. **Complete retry only** - cannot resume from checkpoint
3. **Not suitable for long workflows** - risk of timeout or abandonment
4. **Limited reliability** - depends on completion before infrastructure issues

## Best Practices

1. **Default to non-durable** for new projects (use v2)
2. **Enable durable mode** only when needed
3. **Keep durable workflows idempotent** to handle replays safely
4. **Use explicit activities** for complex operations in durable mode
5. **Test replay behavior** for durable workflows
6. **Monitor execution times** to catch performance issues
7. **Document durability choice** in your project README

## See Also

- [Durable Execution Concept](/glossary/durable_execution)
- [Python Development Guide](/develop/python)
- [Activities Documentation](/develop/python#using-the-autokittehactivity-decorator)
- [Synchronous Webhooks](/develop/sync_webhooks)
- [Temporal Documentation](https://docs.temporal.io/workflows)
