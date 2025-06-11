---
sidebar_position: 5
description: Guide for deploying AutoKitteh projects in a self-hosted environment
---

# Project Deployment

This guide describes the standard process for deploying AutoKitteh projects on a self-hosted server, using the CLI tool.

## Prepare the AutoKitteh Server

Follow [these instructions](./install) to install a self-hosted AutoKitteh server.

## Deployment Steps

### 1. Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/<project-directory>
```

### 2. Start AutoKitteh Server

```shell
ak up --mode dev
```

:::note

For additional options, see the [start server](./start_server) guide.

:::

### 3. Deploy the Project

```shell
ak deploy --manifest autokitteh.yaml
```

The deployment will output connection IDs that look like this:

```shell
[exec] create_connection "<project>/<connection_name>": con_01j36p9gj6e2nt87p9vap6rbmz created
```

:::tip

Save these connection IDs - you'll need them for the next step.

:::

### 4. Initialize Connections

```shell
ak connection init <connection name or ID>
```

:::note

Some connection authentication modes - especially OAuth 2.0 - require set-up
at the server level. See our [integration-specific guides](/integrations/).

:::

## Next Steps

1. Verify your connections are properly initialized
2. Set/modify any required project variables
3. Test your deployment

:::note

For project-specific configuration and testing details, refer to the project's
`README.md` file.

:::

## Webhook URLs

You can get the full URL of webhook triggers in the AutoKitteh web UI:

1. Go the the project assets page, and then to the triggers tab
2. Hover over the webhook trigger's (i) icon
3. Click the copy icon next to the webhook URL

<img
src={require('/img/webhook_url.png').default}
alt="Screenshot: Webhook URL"
width="700" height="221" border="1" style={{padding: '3px'}} />

Alternatively, get the URL path from the output of the `ak deploy` CLI command:

```
[!!!!] trigger "trigger_name" created, webhook path is "/webhooks/SLUG"
```

Or run this CLI command to get the webhook trigger's slug:

```shell
ak trigger get trigger_name_or_id --project project_name_or_id  -J
```

:::tip

If you expect the webhook to be used by external services, replace the local
server address (`http://localhost:9980`) with a public HTTPS address - see the
[HTTP Tunneling](/config/http_tunneling) page for more details.

Of course, keep the URL path suffix (`/webhooks/slug`) unchanged.

:::

## Getting Help

- Join our [Discord community](https://discord.gg/kQQyxU9UxU)
- File issues on GitHub:
  - AutoKitteh server: https://github.com/autokitteh/autokitteh/issues
  - Kittehub projects: https://github.com/autokitteh/kittehub/issues
