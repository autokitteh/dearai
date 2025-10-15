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

## Filter Syntax

Filters use CEL (Common Expression Language) to selectively trigger execution based on event data.

:::tip

Complete CEL reference: https://github.com/google/cel-spec/blob/master/doc/langdef.md

:::

### Event Type Filters

```yaml
# Single event type
filter: event_type == 'issue_created'

# Multiple event types with OR
filter: event_type == 'issue_created' || event_type == 'issue_updated'

# Pattern matching - any issue-related events
filter: event_type.startsWith('issue_')

# Pattern matching - any creation events
filter: event_type.endsWith('_created')

# Substring matching
filter: event_type.contains('comment')
```

### Data Payload Filters

```yaml
# Simple field equality
filter: data.action == 'opened'

# Multiple conditions with AND
filter: data.method == 'POST' && data.url.path.endsWith('/api')

# List membership
filter: data.method in ['GET', 'HEAD']

# Size checks
filter: size(data.items) > 5 || size(data.description) < 100

# Nested field access
filter: data.issue.labels[0].name == 'bug'

# Dictionary access
filter: data.headers['Content-Type'] == 'application/json'
```

### Complex Filter Examples

```yaml
# GitHub: Only PRs to main branch
filter: event_type == 'pull_request' && data.pull_request.base.ref == 'main'

# Slack: Messages in specific channel from non-bots
filter: event_type == 'message' && data.channel == 'C12345' && !data.bot_id

# HTTP: POST requests with JSON to specific endpoint
filter: data.method == 'POST' && data.url.path == '/api/v1/webhook' && data.headers['Content-Type'].startsWith('application/json')

# Gmail: Emails from specific domain with attachments
filter: event_type == 'message_received' && data.from.endsWith('@example.com') && size(data.attachments) > 0
```

:::tip

Using filters in triggers is more efficient than checking conditions in your Python code, because it prevents unnecessary session creation.

:::

See also: [Filter Expressions in Manifest Reference](/develop/manifest#filter-expressions)
