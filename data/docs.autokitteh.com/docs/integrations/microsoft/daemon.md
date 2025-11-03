---
sidebar_position: 3
sidebar_label: Daemon Apps
description: Non-interactive, project-specific configuration
---

# Private Daemon Apps

## Overview

Daemon authentication (also known as app-only authentication or client credentials flow) allows applications to authenticate without user interaction. This is ideal for background services, automation, and server-to-server scenarios where no user is present to authorize access.

Unlike user-delegated authentication, daemon apps authenticate as themselves using application permissions rather than delegated permissions. This means the app has direct access to resources based on its configured permissions.

To use user-delegated OAuth 2.0 authentication with user interaction, see the [Default User App](./default_user) or [Private User Apps](./private_user) guides.

## Microsoft Documentation

Background information:

- [Microsoft identity platform and OAuth 2.0 client credentials flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)
- [Application permissions vs. delegated permissions](https://learn.microsoft.com/en-us/entra/identity-platform/permissions-consent-overview)
- [Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

## Create a Microsoft App Registration

1. Navigate to the [Azure Portal](https://portal.azure.com/)

2. Go to **Microsoft Entra ID** (formerly Azure Active Directory)

3. In the left sidebar, select **App registrations**

4. Click **New registration**

5. Configure the app registration:

   - **Name**: Choose a descriptive name (e.g., "AutoKitteh Daemon App")
   - **Supported account types**: Select "Accounts in this organizational directory only" (single-tenant)
   - **Redirect URI**: Leave blank (not needed for daemon apps)

6. Click **Register** to create the app registration

7. After creation, you'll see the app's **Overview** page with important details:

   - **Application (client) ID** - copy this value
   - **Directory (tenant) ID** - copy this value

8. Create a client secret:

   - In the left sidebar, select **Certificates & secrets**
   - Click **New client secret**
   - Add a description (e.g., "AutoKitteh daemon secret")
   - Select an expiration period
   - Click **Add**
   - **Important**: Copy the secret **Value** immediately (it won't be shown again)

9. Configure API permissions (application permissions, not delegated):

   - In the left sidebar, select **API permissions**
   - Click **Add a permission**
   - Select **Microsoft Graph**
   - Choose **Application permissions** (not Delegated permissions)
   - Add the permissions your integration needs (e.g., `User.Read.All`, `Mail.Read`, `Calendars.Read`, `Chat.Read.All` for Teams)
   - Click **Add permissions**

10. Grant admin consent (required for daemon apps):
    - Click **Grant admin consent for [Your Organization]**
    - Confirm the consent
    - **Important**: Admin consent is mandatory for application permissions

::::warning[IMPORTANT]

Daemon apps use **Application permissions**, which are more powerful than delegated permissions and require admin consent. Ensure you only grant the minimum necessary permissions for your use case.

::::

## AutoKitteh Connections

When you create or edit the connection in an AutoKitteh project:

1. Select the "Microsoft" connection type, if not selected yet

2. Select the "Private daemon app" authentication type

3. Enter the app details from the app registration:

   - **Client ID** (required) - the Application (client) ID
   - **Client Secret** (required) - the client secret value
   - **Tenant ID** (required) - the Directory (tenant) ID

4. Click **Save** or **Connect**

5. The connection will be established immediately without user interaction

6. Your AutoKitteh workflows can now access Microsoft APIs using application permissions
