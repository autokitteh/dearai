---
sidebar_position: 2
sidebar_label: Private OAuth
description: Project-specific configuration
---

# Private OAuth 2.0 Apps

## Overview

OAuth 2.0 allows users to authorize your app to access their Linear workspace data. At the end of the OAuth flow, your app receives an access token that enables interaction with the [Linear GraphQL API](https://linear.app/developers/graphql) and webhook events.

To use the AutoKitteh server's default Linear OAuth 2.0 app, see the [Default OAuth](./default_oauth) guide.

To use personal API keys, see the [API Keys](./api_key) guide.

## Linear Documentation

Background information: [OAuth 2.0 authentication](https://linear.app/developers/oauth-2-0-authentication)

## Create a Linear OAuth App

Follow the instructions in the [Default OAuth guide](./default_oauth#create-a-linear-oauth-app) to create your Linear OAuth application.

Make a note of the following values for the AutoKitteh connection configuration:

- **Client ID**
- **Client Secret**

## AutoKitteh Connections

When you create or edit the connection in an AutoKitteh project:

1. Select the "Linear" connection type, if not selected yet

2. Select the "Private OAuth 2.0 app" authentication type

3. Enter the app details from the previous section:

   - **Client ID** (required)
   - **Client Secret** (required)

4. Click the "Start OAuth Flow" button

5. You'll be redirected to Linear to authorize the application

6. After authorization, you'll be redirected back to AutoKitteh with an active connection
