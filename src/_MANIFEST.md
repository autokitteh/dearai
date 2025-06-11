{% import "_macros" as macros %}

## Manifest

An AutoKitteh manifest is a yaml or json file that defines how a project is configured.
It defines the PROJECT, CONNECTIONs, TRIGGERs, and VARIABLEs.

A manifest is "applied" by the user (via CLI, or automatically by the Web Application). When it is applied, it creates or updates the project configuration accordingly.

The manifest is defined according to this schema:
{{ macros.code("_data/autokitteh/manifest.schema.yaml", "json") }}

### Examples

{% set paths = [
    "samples/auth0",
    "ai_agents/langgraph_bot",
    "devops/github_issue_alert",
    "discord_to_spreadsheet",
  ] %}
{% for path in paths %}
{{ macros.code("_data/kittehub/" + path + "/autokitteh.yaml", "yaml") }}
{% endfor %}
