---
sidebar_position: 1
sidebar_label: Configuration
description: Create and install Atlassian apps to enable OAuth 2.0
---

# Configuration

Follow this guide in order to enable AutoKitteh's Atlassian connections to use
an OAuth 2.0 (3LO) app, instead of [API tokens and PATs](./connection).

:::note

This guide assumes that the AutoKitteh server is already configured with
[HTTP tunneling](/config/http_tunneling).

:::

:::info

Background information:
[Atlassian OAuth 2.0 (3LO) apps](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/).

:::

## Create an Atlassian OAuth 2.0 App

1. Click here: [Atlassian developer console](https://developer.atlassian.com/console/myapps/)

2. Click on the "Create" drop-down menu on the right, and select "OAuth 2.0
   integration"

   <img
   src={require('/img/atlassian/1.png').default}
   alt="Screenshot 1: Create OAuth 2.0 integration"
   width="186" height="148" border="1" style={{padding: '3px'}} />

3. Name you app, agree to the developer terms, and click the "Create" button

   <img
   src={require('/img/atlassian/2.png').default}
   alt="Screenshot 2: App name"
   width="460" height="215" border="1" style={{padding: '3px'}} />

4. Select the "Permissions" page in the left panel

   <img
   src={require('/img/atlassian/3.png').default}
   alt="Screenshot 3: Left panel"
   width="228" height="246" border="1" style={{padding: '3px'}} />

   1. Click the "Add" action button for the "User identity API"

      <img
      src={require('/img/atlassian/4.png').default}
      alt="Screenshot 4: User Identity API - add button"
      width="730" height="39" border="1" style={{padding: '3px'}} />

   2. Click the "Configure" action button for the "User identity API"
   3. Click the "Edit Scopes" button

      <img
      src={require('/img/atlassian/5.png').default}
      alt="Screenshot 5: User Identity API - original scopes"
      width="953" height="462" border="1" style={{padding: '3px'}} />

   4. Add this scope, and click the "Save" button:

      - View user profiles (`read:account`)

      <img
      src={require('/img/atlassian/6.png').default}
      alt="Screenshot 6: User Identity API - new scopes"
      width="908" height="482" border="1" style={{padding: '3px'}} />

5. Select the "Permissions" page in the left panel again

   1. Click the "Add" action button for "Jira API" **or** "Confluence API"
   2. Click the "Configure" action button for that row
   3. Click the "Edit Scopes" button
   4. Select **at least** these scopes, and click the "Save" button:

      - View Jira issue data (`read:jira-work`)
      - View user profiles (`read:jira-user`)
      - Create and manage issues (`write:jira-work`)
      - Manage Jira webhooks (`manage:jira-webhook`)
      - ...or...
      - All the Confluence scopes you're interested in

      <img
      src={require('/img/atlassian/7.png').default}
      alt="Screenshot 7: Jira API - new scopes"
      width="908" height="676" border="1" style={{padding: '3px'}} />

6. Select the "Authorization" page in the left panel

   1. Click the "Add" action button
   2. Enter this callback URL: `https://PUBLIC-AK-ADDRESS/oauth/redirect/jira` or `.../confluence`

      (where `PUBLIC-AK-ADDRESS` is the AutoKitteh server's
      [public tunnel address](/config/http_tunneling))

   3. Click the "Save Changes" button

   <img
   src={require('/img/atlassian/8.png').default}
   alt="Screenshot 8: Authorization"
   width="906" height="332" border="1" style={{padding: '3px'}} />

## App Secrets

1. Select the "Settings" page in the left panel

2. Copy the `Client ID` and `Secret` in the "Authentication details" section

   <img
   src={require('/img/atlassian/9.png').default}
   alt="Screenshot 9: App secrets"
   width="728" height="192" border="1" style={{padding: '3px'}} />

## Configure AutoKitteh

There are two equivalent options to configure the AutoKitteh server to
interact with your OAuth app - choose the one most suited for your needs and
constraints.

For more details, see the [Configuration Methods](/config/methods) page.

### `config.yaml` File

Stay tuned!

### Environment Variables

Set this environment variable, based on the AutoKitteh server's address -
either an [HTTP tunnel's public address](/config/http_tunneling), or an
internal address in a Virtual Private Cloud (VPC):

- `WEBHOOK_ADDRESS`
  - Just the address, without the `http[s]://` prefix, and without a path
    suffix

Also set these environment variables, based on the values you were instructed
to copy in the [App Secrets](#app-secrets) section above:

- `JIRA_CLIENT_ID` or `CONFLUENCE_CLIENT_ID`
- `JIRA_CLIENT_SECRET` or `CONFLUENCE_CLIENT_ID`

<details>
  <summary>
    If your organization uses Atlassian Data Center, i.e. self-hosted servers,
    not Atlassian Cloud
  </summary>

Set the environment variable `ATLASSIAN_BASE_URL` to the self-hosted server's URL
**without** a path, i.e. a string that looks like this: `http[s]://host[:port]`.

</details>

Lastly, restart the AutoKitteh server for these settings to take effect.
