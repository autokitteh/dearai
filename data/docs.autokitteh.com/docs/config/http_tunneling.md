---
sidebar_position: 7
---

# HTTP Tunneling

## Motivation

AutoKitteh integrations hide away the complexities of using third-party
services and APIs:

- Support for the [OAuth 2.0](https://oauth.net/2/) protocol
- Handling external asynchronous events
  - Receiving them without over/under-capacity concerns
  - Relaying them reliably and securely to all interested workflows
  - Acknowledging them in a timely manner

This depends on exposing AutoKitteh's webhooks as publicly-accessible HTTPS
endpoints. There are many options to do this; a popular "freemium" solution is
[_ngrok_](https://ngrok.com/).

## Set-Up _ngrok_

1. Install _ngrok_, according to step 1 here:
   https://ngrok.com/docs/getting-started/

2. Connect your _ngrok_ agent to your ngrok account, according to step 2 in
   the same quickstart guide

3. Create a static domain on your _ngrok_ dashboard:
   https://dashboard.ngrok.com/cloud-edge/domains

4. Run this command to start _ngrok_:

   ```shell
   ngrok http 9980 --domain example.ngrok.dev
   ```

   :::note

   - `9980` is AutoKitteh's local HTTP port
   - `example.ngrok.dev` is the domain you've registered in step 3

   :::

## Configure AutoKitteh

Set this environment variable, based on the step 3 above:

- `WEBHOOK_ADDRESS`

:::tip

Specify just the address, without the `https://` prefix, and without a path
suffix, e.g. `example.ngrok.dev`.

:::
