---
sidebar_position: 1
description: 1-pager summary from server installation to project execution
---

# Quickstart

## Install the AutoKitteh CLI Tool

Run this command on macOS:

```shell
brew install autokitteh/tap/autokitteh
```

:::tip

For other operating systems and other methods, see the
[Installation](./install) page.

To enable shell completion, follow [these instructions](./shell_completion).

:::

## Start a Self-Hosted Server

Run this command to start a self-hosted AutoKitteh server in "dev" mode:

```shell
ak up --mode dev
```

:::tip

For a discussion of the different server execution modes, see the
[Start Server](./start_server) page.

:::

## Create and Deploy a Project With the CLI Tool

An AutoKitteh [project](/glossary/project) is a collection of settings and
code that implements [workflows](/glossary/workflow).

Let's use an
[existing project](https://github.com/autokitteh/kittehub/tree/main/quickstart)
from the [Kittehub repository](https://github.com/autokitteh/kittehub) to
create a basic workflow that starts when AutoKitteh receives an HTTP request,
and prints a simple message to AutoKitteh's session log.

1.  Run this command to clone the Kittehub repository, which contains various
    project directories:

    ```shell
    git clone https://github.com/autokitteh/kittehub.git
    ```

    Alternatively, download and extract the repository's
    [zip archive file](https://github.com/autokitteh/kittehub/archive/refs/heads/main.zip)

2.  Run this command:

    ```shell
    ak deploy --manifest kittehub/quickstart/autokitteh.yaml
    ```

    <details>
      <summary>Under the hood</summary>
      <div>
        The `ak deploy` command does the following:

    1.  Create a new Autokitteh [project](/glossary/project)
    2.  Apply the project settings from the
        [YAML manifest file](https://github.com/autokitteh/kittehub/blob/main/quickstart/autokitteh.yaml)
    3.  Build (i.e. lint, compile, and package a snapshot of) the
        [source code](https://github.com/autokitteh/kittehub/blob/main/quickstart/program.py)
    4.  Deploy this [build](/glossary/build)
    5.  Activate this [deployment](/glossary/deployment)
      </div>
    </details>

    <details>
      <summary>Expected output</summary>
      <div>
        ```
        [plan] project "quickstart": not found, will create
        [plan] trigger "quickstart/default:/http_request": not found, will create

        [exec] create_project "quickstart": created "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa"
        [exec] create_trigger "quickstart/default:/http_request": created "trg_bbbbbbbbbbbbbbbbbbbbbbbbbb"

        [!!!!] trigger "http_request" created, webhook path is "/webhooks/cccccccccccccccccccccccccc"

        [exec] create_build: created "bld_dddddddddddddddddddddddddd"
        [exec] create_deployment: created "dep_eeeeeeeeeeeeeeeeeeeeeeeeee"
        [exec] activate_deployment: activated
        ```

      </div>
    </details>

That's it! The project is now waiting for trigger events in order to start
runtime [sessions](/glossary/session) that run
[workflows](/glossary/workflow).

## Trigger the Deployment

1.  Look for the following line in the output of the `ak deploy` command, and
    copy the URL path:

    ```
    [!!!!] Trigger "http_request" created, webhook path is "/webhooks/..."
    ```

    :::tip

    If you don't see the output of `ak deploy` anymore, you can run this
    command instead, and use the webhook slug from the output:

    ```shell
    ak trigger get http_request --project quickstart -J
    ```

    :::

2.  Run this command (use the URL path from step 1 instead of
    `/webhooks/...`):

    ```shell
    curl -i "http://localhost:9980/webhooks/..."
    ```

    <details>
      <summary>Explanation</summary>
      <div>
        The `curl` flag `-i` shows you the server's response.

        `localhost:9980` is the address of the local AutoKitteh server that you
        started (with the [default port number](/config/address)).

        `/webhooks/...` is the URL path of the project's trigger, which is
        defined in the
        [YAML manifest file](https://github.com/autokitteh/kittehub/blob/main/quickstart/autokitteh.yaml),
        and was assigned when you deployed the project for the first time.

      </div>
    </details>

3.  Run this command to check that a runtime session has indeed started and
    ended:

    ```shell
    ak session list -J
    ```

    <details>
      <summary>Expected output</summary>
      <div>
      ```json
      {
          "session_id": "ses_wwwwwwwwwwwwwwwwwwwwwwwwww",
          "event_id": "evt_xxxxxxxxxxxxxxxxxxxxxxxxxx",
          "deployment_id": "dep_ffffffffffffffffffffffffff",
          "build_id": "bld_eeeeeeeeeeeeeeeeeeeeeeeeee",
          "env_id": "env_bbbbbbbbbbbbbbbbbbbbbbbbbb",
          "entrypoint": {
              "path": "program.py",
              "name": "on_http_get"
          },
          "created_at": "2024-03-22T00:12:34.123456Z",
          "updated_at": "2024-03-22T00:12:35.123456Z",
          "state": "SESSION_STATE_TYPE_COMPLETED"
      }
      ```

      </div>
    </details>

4.  Run this command to display all the `print` messages in the latest
    session's log:

    ```shell
    ak session watch <SESSION_ID>
    ```

    ```
    [2025-05-14T13:44:50Z] State: CREATED
    [2025-05-14T13:44:50Z] State: RUNNING
    ```

## Resilience Demo

1. Change `ITERATIONS` in the quickstart program to 50

   :::info

   ```python
   SLEEP_SECONDS = 1
   ITERATIONS = 50


   def quickstart(_):
      for i in range(ITERATIONS):
         print(f"Loop iteration: {i + 1} of {ITERATIONS}")
         time.sleep(SLEEP_SECONDS)
   ```

   :::

2. Run this command:

   ```shell
   ak session list -J
   ```

   :::info Notice

   The current state of the new sessions is `RUNNING` rather than `COMPLETED`.

   :::

3. Run this command:

   ```shell
   ak session watch <SESSION_ID>
   ```

   This command outputs several new `print` messages from the latest session's
   log, while it's still running:

   ```
   Prints:
   Loop iteration: 1 of 50
   Loop iteration: 2 of 50
   Loop iteration: 3 of 50
   Loop iteration: 4 of 50
   ...
   ```

4. Terminate the AutoKitteh server in any way you want, for example:

   ```shell
   pkill -f -Il "ak up"
   ```

   :::info

   A naive server would lose its internal state when this happens, and lose
   the running workflow, or (even worse) abandon it to continue running as a
   zombie process without being able to regain ownership.

   Either way, when you restart it, you would have to manually trigger the
   project deployment again, and the new workflow wouldn't remember its
   previous data or be able to resume without repeating steps that it already
   completed.

   AutoKitteh is smarter than that!

   :::

5. Run this command to start the AutoKitteh server again:

   ```shell
   ak up --mode dev
   ```

6. Run this command again, to see what happens after AutoKitteh restarts:

   ```shell
   ak session list -J
   ```

   :::info Conclusion

   AutoKitteh retains its configuration, history, and internal state across
   restarts!

   :::

7. Run this command again too, after a few seconds:

   ```shell
   ak session log -p
   ```

   :::info Conclusion

   AutoKitteh has automatically resumed the original session, without losing
   runtime state or workflow data!

   :::

8. Lastly, after about 4 minutes, run the last two commands again to see that
   the session has ended successfully

## Appendix: HTTP Tunneling

Integrating third-party services and APIs with AutoKitteh usually requires
AutoKitteh to expose publicly-accessible HTTPS endpoints, in order to support
[OAuth 2.0](https://oauth.net/2/) and to receive asynchronous events.

There are many options to do this; a popular "freemium" solution is
[_ngrok_](https://ngrok.com/):

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

5. Set the environment variable `WEBHOOK_ADDRESS`, based on the step 3 above
   (just the address, without the `https://` prefix, and without a path
   suffix, e.g. `example.ngrok.dev`)

Lastly, after adding/changing/removing server configurations and environment
variables, restart the `ak` server, in order for them to take effect.
