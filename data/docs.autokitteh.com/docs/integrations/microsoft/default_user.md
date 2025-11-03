---
sidebar_position: 1
sidebar_label: Default User App
description: One-time server-wide configuration
---

# Default User-Delegated (OAuth 2.0) App

## Overview

User-delegated authentication uses OAuth 2.0 to allow users to authorize your app to access their Microsoft data on their behalf. At the end of the OAuth flow, your app receives an access token that enables interaction with Microsoft APIs (Microsoft Graph, Teams, Outlook, etc.).

To use your own user-delegated OAuth 2.0 app, see the [Private User Apps](./private_user) guide.

To use daemon (non-interactive) authentication, see the [Daemon Apps](./daemon) guide.

## Microsoft Documentation

Background information:

- [Microsoft identity platform and OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
- [Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

## Create a Microsoft App Registration

1. Navigate to the [Azure Portal](https://portal.azure.com/)

2. Go to **Microsoft Entra ID** (formerly Azure Active Directory)

3. In the left sidebar, select **App registrations**

4. Click **New registration**

5. Configure the app registration:

   - **Name**: Choose a descriptive name (e.g., "AutoKitteh Integration")
   - **Supported account types**: Select the appropriate option for your use case:
     - "Accounts in this organizational directory only" for single-tenant
     - "Accounts in any organizational directory" for multi-tenant
     - "Accounts in any organizational directory and personal Microsoft accounts" for widest access
   - **Redirect URI**: Select "Web" and enter `https://PUBLIC-AK-ADDRESS/oauth/redirect/microsoft`

::::warning[IMPORTANT]

You must replace `PUBLIC-AK-ADDRESS` in the redirect URL with the AutoKitteh server's public address:

- AutoKitteh public cloud: `api.autokitteh.cloud`
- Self-hosted servers: the [public tunnel address](/config/http_tunneling)

::::

6. Click **Register** to create the app registration

7. After creation, you'll see the app's **Overview** page with important details:

   - **Application (client) ID** - copy this value
   - **Directory (tenant) ID** - copy this value

8. Create a client secret:

   - In the left sidebar, select **Certificates & secrets**
   - Click **New client secret**
   - Add a description (e.g., "AutoKitteh secret")
   - Select an expiration period
   - Click **Add**
   - **Important**: Copy the secret **Value** immediately (it won't be shown again)

9. Configure API permissions:

   - In the left sidebar, select **API permissions**
   - Click **Add a permission**
   - Select **Microsoft Graph**
   - Choose **Delegated permissions**
   - Add the permissions your integration needs (e.g., `User.Read`, `Mail.Read`, `Calendars.Read`, `Chat.ReadWrite` for Teams)
   - Click **Add permissions**

10. (Optional) Grant admin consent if required by your organization:
    - Click **Grant admin consent for [Your Organization]**

## AutoKitteh Server

Configure the AutoKitteh server with the following environment variables.

Restart the AutoKitteh server for these settings to take effect.

Set this environment variable, based on the AutoKitteh server's
[public tunnel address](/config/http_tunneling):

- `WEBHOOK_ADDRESS`
  - Just the address, without the `https://` prefix, and without a path suffix

Also set these environment variables, based on the values you copied from the Microsoft app registration:

- `MICROSOFT_CLIENT_ID` - the Application (client) ID
- `MICROSOFT_CLIENT_SECRET` - the client secret value
- `MICROSOFT_TENANT_ID` - the Directory (tenant) ID (use `common` for multi-tenant apps)

## AutoKitteh Connections

When you create or edit the connection in an AutoKitteh project:

1. Select the "Microsoft" connection type, if not selected yet

2. Select the "Default user-delegated (OAuth 2.0) app" authentication type

3. Click the "Start OAuth Flow" button

4. You'll be redirected to Microsoft to authorize the application

5. Review and accept the requested permissions

6. After authorization, you'll be redirected back to AutoKitteh with an active connection
