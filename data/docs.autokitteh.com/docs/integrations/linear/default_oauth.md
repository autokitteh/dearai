---
sidebar_position: 1
sidebar_label: Default OAuth
description: One-time server-wide configuration
---

# Default OAuth 2.0 App

## Overview

OAuth 2.0 allows users to authorize your app to access their Linear workspace data. At the end of the OAuth flow, your app receives an access token that enables interaction with the [Linear GraphQL API](https://linear.app/developers/graphql) and webhook events.

To use your own OAuth 2.0 app, see the [Private OAuth](./private_oauth) guide.

To use personal API keys, see the [API Keys](./api_key) guide.

## Linear Documentation

Background information: [OAuth 2.0 authentication](https://linear.app/developers/oauth-2-0-authentication)

## Create a Linear OAuth App

1. Navigate to your Linear workspace settings

2. Go to **Settings** → **Security & access** → **OAuth applications**

3. Click **Create new OAuth application**

4. Configure the OAuth application:

   - **Name**: Choose a descriptive name (e.g., "AutoKitteh Integration")
   - **Redirect URL**: Enter `https://PUBLIC-AK-ADDRESS/oauth/redirect/linear`
   - **Description**: Optional description of your integration

::::warning[IMPORTANT]

You must replace `PUBLIC-AK-ADDRESS` in the redirect URL with the AutoKitteh server's public address:

- AutoKitteh public cloud: `api.autokitteh.cloud`
- Self-hosted servers: the [public tunnel address](/config/http_tunneling)

::::

5. Click **Create** to create the OAuth application

6. After creation, you'll see your app's credentials:

   - **Client ID**
   - **Client Secret** (click "Show" to reveal it)

7. Make a note of both values for the AutoKitteh server configuration

## AutoKitteh Server

Configure the AutoKitteh server with the following environment variables.

Restart the AutoKitteh server for these settings to take effect.

Set this environment variable, based on the AutoKitteh server's
[public tunnel address](/config/http_tunneling):

- `WEBHOOK_ADDRESS`
  - Just the address, without the `https://` prefix, and without a path suffix

Also set these environment variables, based on the values you copied from the OAuth app:

- `LINEAR_CLIENT_ID`
- `LINEAR_CLIENT_SECRET`

## AutoKitteh Connections

When you create or edit the connection in an AutoKitteh project:

1. Select the "Linear" connection type, if not selected yet

2. Select the "Default OAuth 2.0 app" authentication type

3. Click the "Start OAuth Flow" button

4. You'll be redirected to Linear to authorize the application

5. After authorization, you'll be redirected back to AutoKitteh with an active connection
