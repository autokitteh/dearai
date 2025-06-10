# Model: Entities & Relationships

- PROJECT has RESOURCEs, CONNECTIONs, TRIGGERs, and VARIABLEs as configuration.
- AutoKitteh supports a number of native INTEGRATIONs.
- an INTEGRATION is a native implementation of an interface to an external system, such as Linear, Slack, etc.
- CONNECTION is a connection to a third-party service using an INTEGRATION, such as Slack, JIRA, Linear, etc.
  a CONNECTION is always associated with an INTEGRATION.
  a CONNECTION can have mutliple TRIGGERs defined on it.
- a DEPLOYMENT is a deployed version of a PROJECT.
- a SESSION starts when a DEPLOYMENT is triggered by a TRIGGER. a SESSION a workflow being run.
- RESOURCE is a source code file, but can be also any file type, like a yaml or json files.
- TRIGGER is a trigger to start a workflow, such as a CONNECTION event, webhook or a SCHEDULE.
  - WEBHOOK and SCHEDULE triggers do not require a CONNECTION.
  - CONNECTION event triggers require a CONNECTION.
- VARIABLE is a key-value pair that is defined in the project and can be used in the workflow.

## Integrations

## Triggers

A TRIGGER can be of one of several types.

- Webhook Trigger: when it is created, AutoKitteh generates a unique URL that when it is hit, the trigger will be invoked.
- Schedule Trigger: runs on a schedule, defined by a cronspec.
- Connection Trigger: A third party service sends an event, which when the trigger matches the event - it is invoked.

A TRIGGER can include a FILTER defintion in its `filter` field. The FILTER is specified as a Google CEL expression. The CEL expression takes as input the EVENT payload, under the name `data`. The event type will be under the name `event_type`.

A TRIGGER points to a function execute once is is hit and matches optional filter. The method is specified in the format: "filename:method_name", when `filename` is a name of a RESOURCE in the PROJECT.

### Examples

#### Webhook: Only match with POST JSON requests

```
name: receive_http_post_json
type: webhook
event_type: post
filter: data.headers["Content-Type"].startsWith("application/json")
call: webhooks.py:on_http_post_json
```

### Webhook: Only match with GET or POST requests

```
name: receive_http_get_or_head
type: webhook
filter: data.method in ["GET", "HEAD"]
call: webhooks.py:on_http_get_or_head
```

#### Slack: Only match `interaction` from a specific user id

```
name: slack_interaction_from_specific_id
connection: slack_connection
filter: event_type == 'interaction' && data.user.id == 'SOME_SLACK_ID'
```

#### Slack: Slack command where its text is "break-glass"

```
name: break_glass_slack_command
connection: slack_connection
event_type: slash_command
call: program.py:on_slack_slash_command
filter: data.text == "break-glass"
```

#### GitHub: PR action is either "opened" or "reopened"

```
name: github_pull_request
connection: github_conn
event_type: pull_request
filter: data.action == "opened" || data.action == "reopened"
call: program.py:on_github_pull_request
```
