---
sidebar_position: 2
sidebar_label: Private App
description: Project-specific configuration
---

# Private GitHub (OAuth 2.0) Apps

## Overview

GitHub Apps are tools that extend GitHub's functionality. GitHub Apps can do things on GitHub like open issues, comment on pull requests, and manage projects. They can also do things outside of GitHub based on events that happen on GitHub. For example, a GitHub App can post on Slack when an issue is opened on GitHub.

This connection mode does not require a preexisting AutoKitteh server-wide configuration. Instead, it allows project owners to configure the details of their own apps.

If you want to use the AutoKitteh server's default GitHub app, see the [Default App](./default_app) guide.

If you want to use a Personal Access Token (PAT) and/or a personal webhook, see the [PAT + Webhook](./pat) guide.

:::note[NOTES]

Only organization and repository owners can install GitHub apps.

This guide assumes that the AutoKitteh server is already configured with [HTTP tunneling](/config/http_tunneling).

:::

## GitHub Documentation

Background information: [about using GitHub apps](https://docs.github.com/en/apps/using-github-apps/about-using-github-apps).

## Create a GitHub App

Depending on your preference, use one of these options:

- The app will be owned by you, i.e. a GitHub **user**:\
  https://github.com/settings/apps/new

- The app will be owned by a GitHub **organization**:\
  `https://github.com/organizations/ORG-NAME/settings/apps/new`\
  (This requires GitHub organization **owner** privileges)

:::tip

If you want the GitHub app to be private, create it in the same GitHub user/organization scope where you intend to install it. If you want multiple GitHub users and organization to install it, create a public GitHub app.

You will make this choice in step 7 below.

:::

1. Required details:

   - GitHub App name
   - Homepage URL

2. Identifying and authorizing users:

   - Callback URL:

     - AutoKitteh public cloud: `https://api.autokitteh.cloud/oauth/redirect/github`
     - Dedicated environments: `https://NAME-api.autokitteh.cloud/oauth/redirect/github`\
       (where `NAME` is the AutoKitteh server's name)
     - Self-hosted servers: `https://PUBLIC-ADDRESS/oauth/redirect/github`\
       (where `PUBLIC-ADDRESS` is the [public tunnel address](/config/http_tunneling))

   - Expire user authorization tokens: **No**

   - Request user authorization (OAuth) during installation: **Yes**

     <img
     src={require('/img/github/2.png').default}
     width="739" height="383" border="1" style={{padding: '3px'}} />

3. Post installation:

   - Redirect on update: **Yes**

     <img
     src={require('/img/github/3.png').default}
     width="739" height="190" border="1" style={{padding: '3px'}} />

4. Webhook:

   - Active: **Yes** (default)

   - Webhook URL:

     - AutoKitteh public cloud: `https://api.autokitteh.cloud/github/webhook`
     - Dedicated environments: `https://NAME-api.autokitteh.cloud/github/webhook`\
       (where `NAME` is the AutoKitteh server's name)
     - Self-hosted servers: `https://PUBLIC-ADDRESS/github/webhook`\
       (where `PUBLIC-ADDRESS` is the [public tunnel address](/config/http_tunneling))

   - Webhook Secret: random and secret string of your choice

     <img
     src={require('/img/github/4.png').default}
     width="487" height="395" border="1" style={{padding: '3px'}} />

5. Permissions:

   Your choices in this section depend on a balance between functional and security needs, which GitHub API calls you expect AutoKitteh scripts to make, and which GitHub API events you expect AutoKitteh scripts to respond to.

   :::info ATTENTION

   Permission changes have to be accepted by owners of existing installations before they become effective.

   :::

   Some common **repository** permission examples:

   - [Actions](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-actions)
   - [Administration](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-administration)
   - [Commit statuses](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-commit-statuses)
   - [Contents](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-contents)
   - [Issues](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-issues)
   - [Metadata](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-metadata) (mandatory)
   - [Pull requests](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-pull-requests)

   Some common **organization** permission examples:

   - [API insights](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps?apiVersion=2022-11-28#organization-permissions-for-api-insights)
   - [GitHub Copilot Business](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps?apiVersion=2022-11-28#organization-permissions-for-github-copilot-business)
   - [Members](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps?apiVersion=2022-11-28#organization-permissions-for-members)

   See also this comprehensive guide: [permissions for GitHub apps](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps?apiVersion=2022-11-28).

6. Subscribe to events:

   Your choices in this section depend on the chosen permissions above, and which GitHub API events you expect AutoKitteh scripts to respond to.

   Some common examples:

   - [Meta](https://docs.github.com/en/webhooks/webhook-events-and-payloads#meta)
   - [Commit comment](https://docs.github.com/en/webhooks/webhook-events-and-payloads#commit_comment)
   - [Issue comment](https://docs.github.com/en/webhooks/webhook-events-and-payloads#issue_comment)
   - [Issues](https://docs.github.com/en/webhooks/webhook-events-and-payloads#issues)
   - [Pull request](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request)
   - [Pull request review](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review)
   - [Pull request review comment](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review_comment)
   - [Pull request review thread](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review_thread)
   - [Push](https://docs.github.com/en/webhooks/webhook-events-and-payloads#push)
   - [Release](https://docs.github.com/en/webhooks/webhook-events-and-payloads#release)
   - [Repository](https://docs.github.com/en/webhooks/webhook-events-and-payloads#repository)
   - [Status](https://docs.github.com/en/webhooks/webhook-events-and-payloads#status)
   - [Workflow dispatch](https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_dispatch)
   - [Workflow job](https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_job)
   - [Workflow run](https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_run)
   - [Sub issues](https://docs.github.com/en/webhooks/webhook-events-and-payloads#sub_issues)

7. Where can this GitHub App be installed?

   Choose one of these options:

   - `Only on this account` (only the GitHub user/org that created this GitHub app)
   - `Any account` (any GitHub user or organization)

8. Click the green button "Create GitHub App"

## App Details

1. Copy the `App ID` and `Client ID` strings at the top of the app settings
   page

   <img
   src={require('/img/github/5.png').default}
   width="676" height="244" border="1" style={{padding: '3px'}} />

2. Click the button "Generate a new client secret", and copy the new string;
   you will not be able to see it again once you leave this page

   <img
   src={require('/img/github/6.png').default}
   width="731" height="251" border="1" style={{padding: '3px'}} />

3. Double-check that the webhook secret was indeed set when you created the
   app; if it's not, set it again, and click the green "Save changes" button

   <img
   src={require('/img/github/7.png').default}
   width="731" height="531" border="1" style={{padding: '3px'}} />

4. Click the "Generate a private key" button at the **bottom** of the app
   settings page

   <img
   src={require('/img/github/8.png').default}
   width="390" height="150" border="1" style={{padding: '3px'}} />

   - This will auto-download a file named `APP-NAME.DATE.private-key.pem`

## AutoKitteh Connections

When you create, initialize, or edit the connection in an AutoKitteh project:

1. Select the "GitHub" connection type, if not selected yet

2. Select the "Private GitHub app" authentication type, if not selected yet

3. Enter the app details from the previous section:

   - App ID (required)
   - App name (required, must exactly match the app name used in the URL format)
   - Client ID (required)
   - Client secret (required, readbale only when re/generated)
   - Webhook secret (required, readable only when re/set)
   - Private key (required, downloadable only when re/generated)

4. If your organization uses a [GitHub Enterprise Server (GHES)](https://docs.github.com/en/enterprise-server/admin/overview/about-github-enterprise-server), enter its URL in order to replace the default `https://github.com`

5. Click the "Start OAuth Flow" button
