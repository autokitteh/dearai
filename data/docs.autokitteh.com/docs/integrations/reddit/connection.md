---
sidebar_label: Connection
description: Initialize a connection with a Reddit app
---

# Initialize a Reddit Connection

To use the Reddit integration, you'll need to create a Reddit app and configure a connection using your app credentials. Reddit supports two authentication methods: script-based (with username/password) and application-only (without user credentials).

## Prerequisites

1. **Reddit Account:** Create one at [reddit.com](https://www.reddit.com)
2. **Reddit App:** Follow the steps below to create an app

## Create a Reddit App

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)

2. Scroll to the bottom and click **"create another app..."** or **"are you a developer? create an app..."**

3. Fill in the application details:

   - **name:** Choose a name for your app
   - **App type:** Select **"web app"**
   - **description:** (optional) Describe your app
   - **about url:** (optional) Link to more information
   - **redirect uri:** Use `https://api.autokitteh.cloud`

4. Click **"create app"**

5. After creation, you'll see your app credentials:
   - **client_id:** Found under the app name (a short string of characters)
   - **client_secret:** Labeled as "secret"

:::note Rate Limiting
Reddit enforces rate limits on API requests. The recommended practice is to make no more than 60 requests per minute.
:::

## Connection Configuration

You can configure the Reddit connection in two ways:

### Option 1: Application-Only Authentication (Read-Only)

Use this method for read-only access without user context:

- **client_id:** Your Reddit app's client ID
- **client_secret:** Your Reddit app's secret
- **user_agent:** A unique identifier for your app (format: `platform:app_name:version (by u/your_username)`)

Example user agent:

```
autokitteh:my_reddit_bot:v1.0 (by u/myusername)
```

### Option 2: Script Authentication (Full Access)

Use this method for full access including posting, commenting, and voting:

- **client_id:** Your Reddit app's client ID
- **client_secret:** Your Reddit app's secret
- **user_agent:** A unique identifier for your app
- **username:** Your Reddit username
- **password:** Your Reddit password

## Additional Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api)
