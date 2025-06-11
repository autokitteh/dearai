---
sidebar_position: 3
sidebar_label: PAT + Webhook
description: Project-specific configuration
---

# PAT and/or Personal Webhook

## Overview

This connection mode does not require a preexisting AutoKitteh server-wide configuration. Instead, it allows project owners to use Personal Access Tokens (PATs) and personal webhooks.

You may set up an AutoKitteh connection with:

- Only a [PAT](#personal-access-token-pat) (to send API calls from AutoKitteh), or
- Only a [personal webhook](#webhook) (to receive events from GitHub), or
- Both in the same AutoKitteh connection

If you want to use the AutoKitteh server's default GitHub app, see the [Default App](./default_app) guide.

If you want to use your own GitHub app, see the [Private App](./private_app) guide.

## GitHub Documentation

- [Authenticating with a personal access token](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28#authenticating-with-a-personal-access-token)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Personal Access Token (PAT)

Follow the instructions in this section if you want to send API calls from AutoKitteh.

:::note

Some GitHub organizations may have a [policy that restricts PAT access](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization).

:::

1. In a browser, go to: https://github.com/settings/apps

2. In the left sidebar, under "Personal access tokens", select either "Fine-grained tokens" or "Tokens (classic)", and click the "Generate new token" button

3. Follow the instructions for creating a
   [fine-grained token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
   or a [classic token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic):

   - For fine-grained tokens, make sure you select the right resource owner:
     - Yourself (for your personal repositories)
     - An organization you're a member of (which allows PATs)
   - Repository access: either "All repositories", or "Only select repositories"
   - Repository permissions: see the [repository permissions](#repository-permissions) section below
   - Click the green "Generate token" button at the bottom of the page

4. Copy the new PAT string

### Repository Permissions

Your choices in this section depend on a balance between functional and security needs, which GitHub API calls you expect AutoKitteh scripts to make, and which GitHub API events you expect AutoKitteh scripts to respond to.

Here are some common examples:

- [Actions](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-actions)
- [Administration](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-administration)
- [Commit statuses](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-commit-statuses)
- [Contents](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-contents)
- [Issues](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-issues)
- [Metadata](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-metadata) (mandatory)
- [Pull requests](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-pull-requests)

## Webhook

Follow the instructions in this section if you want to receive events from GitHub.

:::note[NOTES]

Only organization and repository owners can create webhooks for them.

This guide assumes that the AutoKitteh server is already configured with [HTTP tunneling](/config/http_tunneling).

:::

1. Decision: where you want the new webhook - a single repository, or an entire organization?

2. Go to the settings page of that repository / organization

   - Click "Webhooks" in the left sidebar
   - Click the "Add webhook" button in the top-right corner of the page

3. Paste the auto-generated webhook URL from the GitHub connection UI

4. Follow the instructions for creating a webhook for a [single repository](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks#creating-a-repository-webhook) or an [entire org](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks#creating-an-organization-webhook):

   - Content type: doesn't matter, AutoKitteh supports both
   - Secret: specify the same string in GitHub and in AutoKitteh
   - Events: select "Send me everything", or only specific ones
   - Click the green "Add webhook" button at the bottom

## AutoKitteh Connections

When you create, initialize, or edit the connection in an AutoKitteh project:

1. Select the "GitHub" connection type, if not selected yet

2. Select the "PAT + webhook" authentication type, if not selected yet

3. Enter the details from the previous sections:

   - PAT (optional, if you want to send API calls from AutoKitteh)
   - Webhook secret (optional, if you want to receive events from GitHub)

4. If your organization uses a [GitHub Enterprise Server (GHES)](https://docs.github.com/en/enterprise-server/admin/overview/about-github-enterprise-server), enter its URL in order to replace the default `https://github.com`

5. Click the "Save Connection" button
