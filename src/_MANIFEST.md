{% import "_macros" as macros %}

## Manifest

An AutoKitteh manifest is a yaml or json file that defines how a project is configured.
It defines the PROJECT, CONNECTIONs, TRIGGERs, and VARIABLEs.

A manifest is "applied" by the user (via CLI, or automatically by the Web Application). When it is applied, it creates or updates the project configuration accordingly.

The manifest is defined according to this schema:
{{ macros.code("_data/manifest.schema.yaml", "json") }}

### Example: Webhook Trigger

Defines a project with a single webhook trigger.

```yaml
version: v1

project:
  name: webhook_trigger_example
  triggers:
    - name: webhook_trigger
      type: webhook
      call: webhooks.py:on_webhook
```
