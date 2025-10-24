---
sidebar_label: Connection
description: Create and configure a Telegram bot via BotFather
---

# Initialize a Telegram Connection

To use the Telegram integration, you'll need to create a Telegram bot using the BotFather - Telegram's official bot for creating and managing bots.

## Prerequisites

1. **Telegram Account**
2. **Telegram bot:** Follow the steps below to create a bot

## Create a Telegram Bot via BotFather

1. Open Telegram and search for **@BotFather** (the official bot for creating and managing Telegram bots).

2. Start a conversation with BotFather by sending `/start`.

3. Create a new bot by sending the `/newbot` command.

4. BotFather will ask you to choose a name for your bot. This is the display name that users will see.

   Example: `AutoKitteh Assistant`

5. Next, choose a username for your bot.

   Example: `autokitteh_assistant_bot`

6. Once your bot is created successfully, BotFather will send you a message containing your bot token. This token looks like:

   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

7. **Save this token securely**. You'll need it to initialize the connection in AutoKitteh.

## Additional Bot Configuration

- [BotFather commands documentation](https://core.telegram.org/bots/features#botfather-commands)
- [Bot privacy settings documentation](https://core.telegram.org/bots/features#privacy-mode)
