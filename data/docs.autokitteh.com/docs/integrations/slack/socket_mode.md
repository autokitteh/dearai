---
sidebar_position: 3
sidebar_label: Socket Mode
description: Project-specific configuration
---

# Private Socket Mode Apps

## Overview

Slack's "Socket Mode" allows your app to use the [Events API](https://api.slack.com/apis/events-api) and [interactive features](https://api.slack.com/interactivity) - without the AutoKitteh server having to expose public HTTP webhooks. Instead, AutoKitteh and Slack use a bidirectional stateful [WebSocket](https://datatracker.ietf.org/doc/html/rfc6455) connection.

Socket Mode helps developers working behind a corporate firewall, or who have other security concerns that don't allow exposing a static HTTP endpoint.

This connection mode does not require a preexisting AutoKitteh server-wide configuration. Instead, it allows project owners to configure the details of their own apps.

If you want to use the AutoKitteh server's default Slack OAuth v2 app, see the [Default OAuth](./default_oauth) guide.

If you want to use your own OAuth v2 app, see the [Private OAuth](./private_oauth) guide.

:::info[ATTENTION]

Socket Mode is available in self-hosted AutoKitteh servers but it is disabled in https://app.autokitteh.cloud/ because WebSockets are not appropriate for production-grade, high-availability use-cases:

- WebSocket connections need to remain open all the time, unlike HTTP requests to a passive webhook:
  - This limits the total number of available connections per server
  - This precludes stateless failover and load balancing across servers
- Ensuring that AutoKitteh doesn't miss Slack events while refreshing a WebSocket connection requires more than one WebSocket connection per AutoKitteh Slack connection
- Supporting high loads of incoming Slack events requires a dynamic pool of WebSocket connections
- Slack allows no more than 10 open WebSocket connections per app at the same time

:::

## Slack Documentation

- [Socket Mode](https://api.slack.com/apis/socket-mode)
- [Exploring HTTP vs Socket Mode](https://api.slack.com/apis/event-delivery)

## Create a Slack App

1. Click here: [create a Slack app](https://api.slack.com/apps?new_app=1)

2. Select the option "From a manifest"

3. Pick a workspace to develop the app in, and click the green "Next" button

4. Switch from JSON to YAML

   <img
   src={require('/img/slack_app/manifest.png').default}
   width="468" height="390" border="1" style={{padding: '3px'}} />

5. Replace the default app manifest with this:

```yaml
display_information:
  name: AutoKitteh Demo App
features:
  bot_user:
    display_name: AutoKitteh
    always_online: true
  slash_commands:
    - command: /COMMAND-NAME
      description: Send command to AutoKitteh
      should_escape: true
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - bookmarks:read
      - bookmarks:write
      - channels:history
      - channels:manage
      - channels:read
      - chat:write
      - chat:write.customize
      - chat:write.public
      - commands
      - dnd:read
      - groups:history
      - groups:read
      - groups:write
      - im:history
      - im:read
      - im:write
      - mpim:history
      - mpim:read
      - mpim:write
      - reactions:read
      - reactions:write
      - usergroups:read
      - usergroups:write
      - users.profile:read
      - users:read
      - users:read.email
settings:
  event_subscriptions:
    bot_events:
      - app_home_opened
      - app_mention
      - app_uninstalled
      - channel_archive
      - channel_created
      - channel_deleted
      - channel_id_changed
      - channel_left
      - channel_rename
      - channel_shared
      - channel_unarchive
      - channel_unshared
      - group_archive
      - group_deleted
      - group_left
      - group_rename
      - group_unarchive
      - member_joined_channel
      - member_left_channel
      - message.channels
      - message.groups
      - message.im
      - message.mpim
      - reaction_added
      - reaction_removed
      - tokens_revoked
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

Edit these details within the app manifest:

- `display_information.name`
- `features.bot_user.display_name`

::::warning[IMPORTANT]

You must also replace the string `COMMAND-NAME` within the app manifest with the app's actual slash command name:

- `features.slash_commands[*].command`

:::danger[WARNING]

Slash command names must be unique within a Slack workspace, do not install
more than one Slack app with the same slash command name!

This is because Slack sends slash command events only to the
**last-installed** app which declared that slash command, not all of them.

:::

::::

:::tip[TIPS]

**Slash commands** are an optional feature - you may remove the one in the template, or add multiple ones.

**Scopes** are permissions that your app requires:

- The template above includes a wide range of them - you may add and remove any based on your functional and security needs
- However, do not remove the [`users:read`](https://api.slack.com/scopes/users:read) scope! (AutoKitteh requires it during connection initializations)
- Also, do not remove the [`commands`](https://api.slack.com/scopes/commands) scope if you use slash commands!
- For more details on Slack scopes, see: [granular bot permission scopes](https://api.slack.com/scopes?filter=granular_bot)

**Bot events** are asynchronous notifications that your app subscribes to receive:

- The template above includes a wide range of them - you may remove any based on your functional needs
- [Contact us](/contact) if you need to add new events that AutoKitteh does not support yet

:::

6. Click the green "Next" button

7. Click the green "Create" button

   <img
   src={require('/img/slack_app/review.png').default}
   width="469" height="442" border="1" style={{padding: '3px'}} />

## Install the Slack App

1. Click the green "Install to Workspace" button

   <img
   src={require('/img/slack_app/install.png').default}
   width="469" height="360" border="1" style={{padding: '3px'}} />

2. Click the green "Allow" button

   <img
   src={require('/img/slack_app/allow.png').default}
   width="484" height="533" border="1" style={{padding: '3px'}} />

## Post-Creation Settings

1. In the app's "Basic Information" page, scroll down to the "App Credentials" section

   <img
   src={require('/img/slack_app/creds.png').default}
   width="627" height="611" border="1" style={{padding: '3px'}} />

2. In the app's "Basic Information" page, scroll down to the "App-Level Tokens" section

   <img
   src={require('/img/slack_app/app_tokens.png').default}
   width="600" height="297" border="1" style={{padding: '3px'}} />

3. Click the "Generate Token and Scopes" button

   <img
   src={require('/img/slack_app/generate_token.png').default}
   width="468" height="443" border="1" style={{padding: '3px'}} />

   - Type a name for the token
   - Click the "Add Scope" button
   - Select the [connections:write](https://api.slack.com/scopes/connections:write) scope
   - Click the green "Generate" button

4. Click the "Copy" button to copy the app-level token (`xapp`) for later, and click the "Done" button

   <img
   src={require('/img/slack_app/copy_token.png').default}
   width="468" height="410" border="1" style={{padding: '3px'}} />

5. Click "Install App" under "Settings" in the left sidebar, and then click the "Copy" button to copy the bot token (`xoxb`) for later

   <img
   src={require('/img/slack_app/bot_token.png').default}
   width="647" height="333" border="1" style={{padding: '3px'}} />

6. Click "App Home" under "Features" in the left sidebar

   <img
   src={require('/img/slack_app/app_home.png').default}
   width="468" height="154" border="1" style={{padding: '3px'}} />

7. Scroll down the page to the "Show Tabs" section, and check the checkbox "Allow users to send Slash commands and messages from the messages tab"

   <img
   src={require('/img/slack_app/enable_slash.png').default}
   width="643" height="482" border="1" style={{padding: '3px'}} />

   This is optional, but recommended for a better user experience.

## AutoKitteh Connections

When you create, initialize, or edit the connection in an AutoKitteh project:

1. Select the "Slack" connection type, if not selected yet

2. Select the "Private Socket Mode app" authentication type, if not selected yet

3. Enter the app details from the previous section:

   - Bot token (`xoxb`, required)
   - App-level token (`xapp`, required)

4. Click the "Save Connection" button
