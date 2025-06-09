---
sidebar_position: 1
sidebar_label: Private OAuth
description: Project-specific configuration
---

# Private OAuth 2.0 Apps

## Overview

A user-managed OAuth app enables you to securely integrate with Salesforce APIs and webhooks on behalf of an authorized user.

This connection mode does not require a preexisting AutoKitteh server-wide configuration. Instead, it allows project owners to configure the details of their own OAuth apps.

:::note

This guide assumes that the AutoKitteh server is already configured with [HTTP tunneling](/config/http_tunneling).

:::

:::info

AutoKitteh does not support **default** OAuth apps for Salesforce, unlike many other AutoKitteh integrations.

:::

## Salesforce Documentation

- [External client apps and connected apps](https://help.salesforce.com/s/articleView?id=xcloud.external_integrations.htm)
- [OAuth scopes](https://help.salesforce.com/s/articleView?id=xcloud.remoteaccess_oauth_tokens_scopes.htm)

## Create an OAuth App

1. Sign into your [Salesforce developer account](https://login.salesforce.com/)

2. Follow the instructions at:

   - [Create an external client app](https://help.salesforce.com/s/articleView?id=xcloud.create_a_local_external_client_app.htm)
   - [Create a connected app](https://help.salesforce.com/s/articleView?id=xcloud.connected_app_create_api_integration.htm)

3. From Setup, navigate to "Platform Tools" > "Apps" and then:

   - "App Manager" (for connected apps)
   - "External Client Apps" > "External Client Apps Manager" (for external client apps)

4. Navigate to the OAuth configuration page:

   - For connected apps: click the dropdown arrow (⌵) next to your app and select "Edit"
   - For external client apps: click the dropdown arrow (⌵) next to your app and select "Edit Settings" and then expand the "OAuth Settings" section

5. Configure the OAuth callback URL:

   - AutoKitteh public cloud: `https://api.autokitteh.cloud/oauth/redirect/salesforce`
   - Dedicated environments: `https://NAME-api.autokitteh.cloud/oauth/redirect/salesforce`\
      (where `NAME` is the AutoKitteh server's name)
   - Self-hosted servers: `https://PUBLIC-ADDRESS/oauth/redirect/salesforce`\
      (where `PUBLIC-ADDRESS` is the [public tunnel address](/config/http_tunneling))

6. Click "Save"

## App Details

### External Client Apps

External Client App Manager > Settings > OAuth Settings:

- Consumer Key = Client ID
- Consumer Secret = Client Secret

### Connected Apps

App Manager > View > Manage Consumer Details:

- Consumer Key = Client ID
- Consumer Secret = Client Secret

## AutoKitteh Connections

When you create, initialize, or edit the connection in an AutoKitteh project:

1. Select the "Salesforce" connection type, if not selected yet

2. Enter the app details from the previous section:

   - Client ID (required)
   - Client Secret (required)
