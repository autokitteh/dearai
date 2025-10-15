---
sidebar_position: 2
description: Complete manifest (autokitteh.yaml) reference
title: Manifest Reference
---

# Manifest Reference

The manifest file (`autokitteh.yaml`) is the configuration file that defines your AutoKitteh project. It specifies connections, triggers, variables, and other project settings.

## File Structure

```yaml
version: v2

project:
  name: project_name

  connections:
    - name: connection_name
      integration: integration_type
      # Additional connection-specific configuration

  triggers:
    - name: trigger_name
      type: webhook | schedule
      event_type: event_type_name
      connection: connection_name
      call: file.py:function_name
      filter: CEL_expression

  vars:
    - name: VAR_NAME
      value: var_value
```

## Top-Level Fields

### `version`

**Required**. Specifies the manifest schema version.

**Supported values:**

- `v2` - Current recommended version (default)
- `v1` - Legacy version (deprecated)

**Example:**

```yaml
version: v2
```

### `project`

**Required**. Contains all project configuration.

## Project Fields

### `name`

**Required**. The unique name of your project.

**Type:** String

**Example:**

```yaml
project:
  name: my_workflow
```

### `connections`

**Optional**. List of connections to external services.

Each connection requires:

- `name` - Unique identifier for this connection (used in code)
- `integration` - One of the [supported integrations](/glossary/integration#supported-integrations)
- Additional fields depend on the integration type

**Example:**

```yaml
connections:
  - name: my_slack
    integration: slack

  - name: my_github
    integration: github
```

See the [integrations documentation](/integrations) for integration-specific configuration.

### `triggers`

**Optional**. List of triggers that start workflow sessions.

Each trigger can have:

| Field        | Required | Type    | Description                                         |
| ------------ | -------- | ------- | --------------------------------------------------- |
| `name`       | Yes      | String  | Unique trigger identifier                           |
| `type`       | No       | String  | `webhook` or `schedule`                             |
| `event_type` | No       | String  | Event type provided by the integration              |
| `connection` | No\*     | String  | Connection name (required for integration triggers) |
| `call`       | Yes      | String  | Entry point in format `file.py:function_name`       |
| `filter`     | No       | String  | CEL expression to filter events                     |
| `is_sync`    | No       | Boolean | For webhooks: return HTTP response from workflow    |

\* `connection` is required for integration-based triggers but not for standalone webhooks.

**Example - Webhook Trigger:**

```yaml
triggers:
  - name: http_endpoint
    type: webhook
    call: program.py:handle_webhook
```

**Example - Integration Event Trigger:**

```yaml
triggers:
  - name: on_github_issue
    connection: my_github
    event_type: issues
    filter: data.action == 'opened'
    call: program.py:handle_issue
```

**Example - Scheduled Trigger:**

```yaml
triggers:
  - name: daily_report
    type: schedule
    schedule: "0 9 * * *" # Daily at 9 AM
    call: program.py:generate_report
```

**Example - Synchronous Webhook:**

```yaml
triggers:
  - name: api_endpoint
    type: webhook
    is_sync: true
    call: program.py:api_handler
```

### `vars`

**Optional**. List of environment variables available to your code.

Each variable requires:

- `name` - Variable name (accessible via `os.getenv()`)
- `value` - Variable value

**Example:**

```yaml
vars:
  - name: CHANNEL_ID
    value: "C12345678"

  - name: API_ENDPOINT
    value: "https://api.example.com"
```

Variables can also be set as secrets using the CLI:

```bash
ak var set --secret --env <env_id> TOKEN s3cr3t
```

See [Working with Secrets](/develop/python#working-with-secrets) for more information.

## Filter Expressions

Filters use CEL (Common Expression Language) to selectively trigger executions.

### Event Type Filtering

```yaml
# Single event type
filter: event_type == 'issue_created'

# Multiple event types
filter: event_type == 'issue_created' || event_type == 'issue_updated'

# Pattern matching
filter: event_type.startsWith('issue_')
filter: event_type.endsWith('_created')
filter: event_type.contains('comment')
```

### Data Filtering

```yaml
# Simple field check
filter: data.action == 'opened'

# Multiple conditions
filter: data.method == 'POST' && data.url.path.endsWith('/api')

# List membership
filter: data.method in ['GET', 'HEAD']

# Size checks
filter: size(data.items) > 5

# Nested fields
filter: data.issue.state == 'open'
```

See the [CEL specification](https://github.com/google/cel-spec/blob/master/doc/langdef.md) for complete syntax.

## Complete Examples

### Simple HTTP Webhook

```yaml
version: v2

project:
  name: simple_webhook

  triggers:
    - name: incoming
      type: webhook
      call: program.py:on_request
```

### GitHub Integration

```yaml
version: v1

project:
  name: github_notifier

  connections:
    - name: github_conn
      integration: github

  triggers:
    - name: on_pr
      connection: github_conn
      event_type: pull_request
      filter: data.action == 'opened'
      call: program.py:handle_pr

  vars:
    - name: SLACK_CHANNEL
      value: "#github-notifications"
```

### Multi-Integration Project

```yaml
version: v1

project:
  name: workflow_automation

  connections:
    - name: slack_conn
      integration: slack

    - name: gmail_conn
      integration: gmail

    - name: sheets_conn
      integration: googlesheets

  triggers:
    - name: slack_command
      connection: slack_conn
      event_type: slash_commands
      call: program.py:handle_command

    - name: new_email
      connection: gmail_conn
      event_type: message_received
      filter: data.from.contains('@example.com')
      call: program.py:process_email

    - name: daily_sync
      type: schedule
      schedule: "0 0 * * *"
      call: program.py:daily_sync

  vars:
    - name: SPREADSHEET_ID
      value: "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
```

## Best Practices

1. **Use descriptive names** for projects, connections, and triggers
2. **Leverage filters** to reduce unnecessary session creation
3. **Keep secrets out of the manifest** - use the CLI's secret management instead
4. **Use environment variables** for values that change between deployments
5. **Document your triggers** with clear, descriptive names

## See Also

- [Project Glossary](/glossary/project)
- [Trigger Glossary](/glossary/trigger)
- [Connection Glossary](/glossary/connection)
- [Python Development Guide](/develop/python)
- [Event Subscription](/develop/events/subscription)
