{% import "_macros" as macros %}

## Manifest

An AutoKitteh manifest is a yaml or json file that defines how a project is configured.
It defines the PROJECT, CONNECTIONs, TRIGGERs, and VARIABLEs.

A manifest is "applied" by the user (via CLI, or automatically by the Web Application). When it is applied, it creates or updates the project configuration accordingly.

A manifest has a version. It is always specified in the `version` field:

- Version `v1` implies that all triggers are creating a durable session by default, unless overridden with "is_durable: false".
- Version `v2` implies that all triggers are creating a non-durable session by default, unless overridden with "is_durable: true".

When authoring new manifests always use `v2` for versioning.

The manifest is defined according to the following schema:

{{ macros.code("_data/autokitteh/manifest.schema.yaml", "json") }}

### Examples

{% set paths = [
    "samples/auth0",
    "ai_agents/langgraph_bot",
    "devops/github_issue_alert",
  ] %}
{% for path in paths %}
{{ macros.code("_data/kittehub/" + path + "/autokitteh.yaml", "yaml") }}
{% endfor %}
