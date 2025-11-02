---
sidebar_position: 2
sidebar_label: Private User Apps
description: Project-specific configuration
---

# Private User-Delegated (OAuth 2.0) Apps

## Overview

User-delegated authentication uses OAuth 2.0 to allow users to authorize your app to access their Microsoft data on their behalf. At the end of the OAuth flow, your app receives an access token that enables interaction with Microsoft APIs (Microsoft Graph, Teams, Outlook, etc.).

To use the AutoKitteh server's default Microsoft user-delegated OAuth 2.0 app, see the [Default User App](./default_user) guide.

To use daemon (non-interactive) authentication, see the [Daemon Apps](./daemon) guide.

## Microsoft Documentation

Background information:

- [Microsoft identity platform and OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
- [Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

## Create a Microsoft App Registration

Follow the instructions in the [Default User App guide](./default_user#create-a-microsoft-app-registration) to create your Microsoft app registration.

Make a note of the following values for the AutoKitteh connection configuration:

- **Application (client) ID**
- **Client Secret** value
- **Directory (tenant) ID**

## AutoKitteh Connections

When you create or edit the connection in an AutoKitteh project:

1. Select the "Microsoft" connection type, if not selected yet

2. Select the "Private user-delegated (OAuth 2.0) app" authentication type

3. Enter the app details from the previous section:

   - **Client ID** (required) - the Application (client) ID
   - **Client Secret** (required) - the client secret value
   - **Tenant ID** (optional) - the Directory (tenant) ID (use `common` for multi-tenant apps, or leave blank for default)

4. Click the "Start OAuth Flow" button

5. You'll be redirected to Microsoft to authorize the application

6. Review and accept the requested permissions

7. After authorization, you'll be redirected back to AutoKitteh with an active connection
