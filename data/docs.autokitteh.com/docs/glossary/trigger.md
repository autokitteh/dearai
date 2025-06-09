---
sidebar_position: 10
---

# Trigger

Triggers link [events](./event) from external services (via [connections](./connection)) to specific entry-point functions in your [project](./project).

## What is a Trigger?

Triggers automatically run your code when specific events occur, such as receiving a GitHub notification or a scheduled task executing.

A trigger connects:

1. An external event.
2. A specific function in your code.

## How Triggers Work

To set up triggers in AutoKitteh:

1. Write your project's code.
2. Connect to external services (e.g., GitHub, Slack).
3. Configure triggers to run code upon specific events.

For example, a trigger might run your `handle_comment` function whenever someone comments on a GitHub issue.

## Trigger Execution Flow

When an event occurs:

1. The external service sends event data to AutoKitteh.
2. AutoKitteh recognizes the trigger.
3. AutoKitteh calls the linked function.
4. Your function processes the event data as programmed.

## Configuration

Define triggers in your project's YAML manifest using the following configuration options:

:::note

Connections and event-types may be shared across multiple projects. AutoKitteh supports "fan-out," distributing a single event to multiple triggers if needed.

:::

## Configuration Reference

| Field        | Type   | Description                                                   |
| :----------- | :----- | :------------------------------------------------------------ |
| `name`       | String | Unique trigger identifier                                     |
| `type`       | String | `webhook` or `schedule` (optional)                            |
| `event_type` | String | Event provided by the [integration](./integration) (optional) |
| `connection` | String | Connection name                                               |
| `call`       | String | Format: `file_name:function_name`                             |
| `filter`     | String | Filter to selectively trigger execution (optional)            |

## Examples

### Minimal Configuration

```yaml
triggers:
  - name: on_issue_comment
    connection: github_conn
    call: program.py:on_issue_comment
  - name: receive_http_post_json
    type: webhook
    call: webhooks.py:on_http_post_json
```

### Configuration with Event Type and Filter

```yaml
triggers:
  - name: on_issue_comment
    event_type: issue_comment
    connection: github_conn
    call: program.py:on_issue_comment
  - name: receive_http_post_json
    type: webhook
    event_type: post
    filter: data.headers["Content-Type"].startsWith("application/json")
    call: webhooks.py:on_http_post_json
```
