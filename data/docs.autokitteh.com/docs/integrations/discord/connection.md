---
sidebar_label: Connection 
description: Create and install a Discord app for the server
---

# Initialize a Discord connection 

:::info

Background information:
[building your first Discord app (step 1)](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).

:::

## Create a Discord App

1. Click here: [create a new Discord application](https://discord.com/developers/applications?new_application=true)

2. Provide a name for your application, then click "Create". 

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/create.png').default}
      alt="Screenshot 1: Create an application"
      className="setup-image" />
    </div>

3. In the sidebar, navigate to the "OAuth2" menu.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/oauth_link.png').default}
      alt="Screenshot 2: Generate an invite link"
      className="setup-image" />
    </div>

4. Under the section titled "OAuth2 URL Generator," find the "Scopes" area and check the box labeled "bot."

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/scope.png').default}
      alt="Screenshot 3: Select scope for application"
      className="setup-image" />
    </div>

5. Under the "Bot Permissions" section, check the boxes for "View Channels" and "Send Messages."
    
    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/bot_permissions.png').default}
      alt="Screenshot 4: Select bot permissions"
      className="setup-image" />
    </div>

:::warning ATTENTION

Currently, only bot tokens are supported for authentication. Scopes that require an OAuth redirect URL will not function.

:::

6. For "Integration Type," select "Guild Install" (note: "User Install" requires OAuth). Next, click "Copy" to copy the install link.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/install_link.png').default}
      alt="Screenshot 5: Copy install link"
      className="setup-image" />
    </div>

7. Paste the link copied from the previous step into your browser. Select the server where you want to add the bot, then click "Continue."

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/install.png').default}
      alt="Screenshot 6: Select server to install bot"
      className="setup-image" />
    </div>

8. Authorize the selected scopes by clicking "Authorize".

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/authorize.png').default}
      alt="Screenshot 7: Authorize scopes"
      className="setup-image" />
    </div>

9. A success message will appear, confirming that the AutoKitteh bot has been installed on your server.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/success.png').default}
      alt="Screenshot 8: Success message"
      className="setup-image" />
    </div>

## Bot Token

1. In the sidebar, navigate to the "Bot" menu.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/bot.png').default}
      alt="Screenshot 9: Navigate to bot menu"
      className="setup-image" />
    </div>

2. Generate a new token by clicking "Reset Token".

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/reset.png').default}
      alt="Screenshot 10: Generate a new token"
      className="setup-image" />
    </div>

3. Copy the token by clicking "Copy." Save it somewhere secure, as it will not be shown again.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/new_token.png').default}
      alt="Screenshot 11: Copy token"
      className="setup-image" />
    </div>

4. After deploying your project, initialize the connection using the bot token generated in step 3.

5. Although enabling all of these intents isn't strictly required to receive events, it's recommended because it allows you to view event content, and some events may not function properly without them.

    <div class="setup-image-container">
      <img
      src={require('/img/discord_app/message_intent.png').default}
      alt="Screenshot 12: Toggle message intent"
      className="setup-image" />
    </div>

:::note OPTIONAL

If the supported AutoKitteh [events](events.md) meet your needs, you're all set. However, client-side code may require additional permissions. For instance, in the client library [quickstart](https://discordpy.readthedocs.io/en/stable/quickstart.html), you'll find the following line of code:


```python
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
```

If you attempt to run the client with these settings without enabling message content intents in the Discord developer portal (as mentioned in the previous step), you will encounter the following error:

>"discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, consider disabling the privileged intents instead."

This also applies to other intents and permissions.

:::
