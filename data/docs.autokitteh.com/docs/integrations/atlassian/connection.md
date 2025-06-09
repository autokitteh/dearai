---
sidebar_position: 2
sidebar_label: Connection
description: Initialize a connection with a token
---

# Initialize a Connection With a Token

Follow this guide in order to initialize an AutoKitteh connection with
Atlassian products such as Jira and Confluence - using API tokens, or Personal
Access Tokens (PATs), instead of an [OAuth 2.0 (3LO) app](./config).

:::info

"API tokens" and "Personal Access Tokens" are essentially the same - they both
allow AutoKitteh to impersonate a user. The key difference between them is that
Atlassian Cloud products use the former, whereas on-prem servers use the latter.

:::

:::note

This guide assumes that the AutoKitteh server is already configured with
[HTTP tunneling](/config/http_tunneling).

:::

## Create an Atlassian Token

For Atlassian Cloud products, manage your API tokens here:
https://id.atlassian.com/manage-profile/security/api-tokens

For Atlassian on-prem servers, manage your PATs using these instructions:
https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html

## Initialize the AutoKitteh Connection

Base URLs for Atlassian Cloud products look like:
`https://your-domain.atlassian.net`

If you're using an Atlassian Cloud API token, **do** specify your email
address.

If you're using an Atlassian on-prem server PAT, **do not** specify your email
address.

## Post-Initialization

:::info

When an AutoKitteh Atlassian connection is initialized, AutoKitteh
automatically registers webhooks to receive asynchronous event callbacks from
Atlassian. There is no need to register webhooks on your own.

However, manual updates or unregistrations of webhooks are not detected or
fixed automatically by AutoKitteh - that would require another connection
initialization.

:::
