

## Manifest

An AutoKitteh manifest is a yaml or json file that defines how a project is configured.
It defines the PROJECT, CONNECTIONs, TRIGGERs, and VARIABLEs.

A manifest is "applied" by the user (via CLI, or automatically by the Web Application). When it is applied, it creates or updates the project configuration accordingly.

A manifest has a version. It is always specified in the `version` field:

- Version `v1` implies that all triggers are creating a durable session by default, unless overridden with "is_durable: false".
- Version `v2` implies that all triggers are creating a non-durable session by default, unless overridden with "is_durable: true".

When authoring new manifests always use `v2` for versioning.

The manifest is defined according to the following schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://go.autokitteh.dev/autokitteh/internal/manifest/manifest",
  "$ref": "#/$defs/Manifest",
  "$defs": {
    "Connection": {
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^\\w+$"
        },
        "integration": {
          "type": "string"
        },
        "vars": {
          "items": {
            "$ref": "#/$defs/Var"
          },
          "type": "array"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name",
        "integration"
      ]
    },
    "Manifest": {
      "properties": {
        "version": {
          "type": "string",
          "enum": [
            "v1",
            "v2"
          ]
        },
        "project": {
          "$ref": "#/$defs/Project"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "version"
      ]
    },
    "Project": {
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^\\w+$"
        },
        "display_name": {
          "type": "string"
        },
        "connections": {
          "items": {
            "$ref": "#/$defs/Connection"
          },
          "type": "array"
        },
        "triggers": {
          "items": {
            "$ref": "#/$defs/Trigger"
          },
          "type": "array"
        },
        "vars": {
          "items": {
            "$ref": "#/$defs/Var"
          },
          "type": "array"
        }
      },
      "additionalProperties": false,
      "type": "object"
    },
    "Trigger": {
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^\\w+$"
        },
        "event_type": {
          "type": "string"
        },
        "filter": {
          "type": "string"
        },
        "is_durable": {
          "type": "boolean",
          "description": "Is handling done as a durable session? Default: true for manifest v1, false for all others."
        },
        "is_sync": {
          "type": "boolean"
        },
        "type": {
          "type": "string",
          "enum": [
            "schedule",
            "webhook",
            "connection"
          ]
        },
        "schedule": {
          "type": "string"
        },
        "webhook": {
          "properties": {},
          "additionalProperties": false,
          "type": "object"
        },
        "connection": {
          "type": "string"
        },
        "call": {
          "type": "string"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name"
      ]
    },
    "Var": {
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^\\w+$"
        },
        "description": {
          "type": "string"
        },
        "value": {
          "type": "string"
        },
        "secret": {
          "type": "boolean"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "name",
        "value"
      ]
    }
  }
}
```

### Examples



```yaml
# This YAML file is a declarative manifest that describes the setup
# of an AutoKitteh project that demonstrates integration with Auth0.

version: v1

project:
  name: auth0_sample

  vars:
    - name: ROLE_ID
      value:
    - name: TIME_INTERVAL
      value: 7d

  connections:
    - name: auth_conn
      integration: auth0

  triggers:
    - name: weekly
      schedule: 0 0 * * 1
      call: program.py:weekly_user_growth
    - name: assign_role_webhook
      type: webhook
      event_type: post
      call: program.py:assign_role
```

```yaml
# This YAML file defines a manifest for an AutoKitteh project that
# creates a Langgraph bot.

version: v1

project:
  name: Langgraph_Bot

  connections:
    - name: slack_conn
      integration: slack
    - name: sheets_conn
      integration: googlesheets

  triggers:
    - name: on_message
      event_type: app_mention
      connection: slack_conn
      call: program.py:on_app_mention

  vars:
    - name: GOOGLE_API_KEY
      value: ""
    - name: TAVILY_API_KEY
      value: ""
```

```yaml
# This YAML file is a declarative manifest that describes the setup
# of an AutoKitteh project that monitors comments on GitHub issues.

version: v1

project:
  name: github_issue_alert

  vars:
    - name: SLACK_CHANNEL_NAME_OR_ID
      value: github-issues

  connections:
    - name: slack_conn
      integration: slack
    - name: github_conn
      integration: github

  triggers:
    - name: on_issue_comment
      event_type: issue_comment
      connection: github_conn
      call: program.py:on_issue_comment
    - name: on_issue_event
      event_type: issues
      connection: github_conn
      call: program.py:on_issue_event
```

