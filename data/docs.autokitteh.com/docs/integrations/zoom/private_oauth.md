---
sidebar_position: 2
sidebar_label: Private OAuth
description: Project-specific configuration
---

# Private OAuth 2.0 Apps

## Overview

A user-managed OAuth app enables you to securely integrate with Zoom APIs and webhooks on behalf of an authorized user.

This connection mode does not require a preexisting AutoKitteh server-wide configuration. Instead, it allows project owners to configure the details of their own apps.

If you want to use the AutoKitteh server's default Zoom OAuth 2.0 app, see the [Default OAuth](./default_oauth) guide.

If you want to use your own Server-to-Server internal app, see the [Server-to-Server](./server_to_server) guide.

:::note

This guide assumes that the AutoKitteh server is already configured with [HTTP tunneling](/config/http_tunneling).

Creating Zoom apps requires being a Zoom workspace admin, or receiving approval from one.

:::

## Zoom Documentation

- [Introduction](https://developers.zoom.us/docs/integrations/)
- [Create an OAuth app](https://developers.zoom.us/docs/integrations/create/)
- [Using webhooks](https://developers.zoom.us/docs/api/webhooks/)
- [OAuth scopes](https://developers.zoom.us/docs/integrations/oauth-scopes-overview/)

## Create an OAuth App

1. Sign into the [Zoom App Marketplace](https://marketplace.zoom.us)

2. Follow the instructions here: [create an OAuth app](https://developers.zoom.us/docs/integrations/create/)

3. Go to the section "Basic Information > OAuth Information", and set the OAuth redirect URL:

   - AutoKitteh public cloud: `https://api.autokitteh.cloud/oauth/redirect/zoom`
   - Dedicated environments: `https://NAME-api.autokitteh.cloud/oauth/redirect/zoom`\
     (where `NAME` is the AutoKitteh server's name)
   - Self-hosted servers: `https://PUBLIC-ADDRESS/oauth/redirect/zoom`\
     (where `PUBLIC-ADDRESS` is the [public tunnel address](/config/http_tunneling))

## Events (Optional)

If you want to receive asynchronous events from Zoom, go to the section "Features > Access > Event Subscriptions", and add one or more subscriptions:

- Method: Webhook

- Event notification endpoint URL:

  - AutoKitteh public cloud: `https://api.autokitteh.cloud/zoom/event`
  - Dedicated environments: `https://NAME-api.autokitteh.cloud/zoom/event`\
    (where `NAME` is the AutoKitteh server's name)
  - Self-hosted servers: `https://PUBLIC-ADDRESS/zoom/event`\
    (where `PUBLIC-ADDRESS` is the [public tunnel address](/config/http_tunneling))

- Authentication Header Option: Default Header Provided by Zoom

## App Details

Basic Information > App Credentials:

- Client ID
- Client Secret

Features > Access:

- Secret Token

## AutoKitteh Connections

When you create, initialize, or edit the connection in an AutoKitteh project:

1. Select the "Zoom" connection type, if not selected yet

2. Select the "Private OAuth 2.0 app" authentication type, if not selected yet

3. Enter the app details from the previous section:

   - Client ID (required)
   - Client secret (required)
   - Secret token (required only if you want to receive events)

4. Click the "Start OAuth Flow" button
