## Tour of AutoKitteh by Projects

All code listings are in txtar format.

### Minimal Projects

```txtar
-- autokitteh.yaml --
version: v2

project:
  name: minimal

-- program.py --
# This can be run using a manual invocation.
def on_trigger(_):
  print("Meow, World!")
```

### Long Running Count

```txtar
-- autokitteh.yaml --
version: v1

project:
  name: minimal

vars:
  - name: N
    value: 10
  - name: T
    value: 1

-- program.py --
from os import getenv
from time import sleep

N = int(getenv("N"))
T = int(getenv("T"))

# This can be run using a manual invocation.
def on_trigger(_):
  for i in range(N):
    print(i)
    # NOTE: Sleep is "hijacked" by AutoKitteh, and if interrupted
    #       (such as by the instance going down), will resume
    #       execution from the same point taking into consideration
    #       the time already spent sleeping.
    sleep(T)
```

### Simple Webhook to Slack

```txtar
-- autokitteh.yaml --
version: v2

project:
  name: webhook_to_slack

  connections:
    - # A single slack connection to authenticate to Slack.
      name: slack_conn
      integration: slack

  triggers:
    - # A webhook to trigger the session.
      # Once applied, AutoKitteh will generate a unique URL for this.
      name: webhook
      type: webhook
      call: program.py:on_webhook

  vars:
    - # Channel to send text to.
      name: CHANNEL
      value: "#general"

-- program.py --
from os import getenv
from autokitteh.slack import slack_client

# `slack_client` returns the official slack client.
# The helper function `slack_client` just initializes the client
# according to the manifest.
#
# NOTE: Since this is done in the global scope, AutoKitteh
#       WILL NOT run this as an activity. This is a feature
#       that allows users to make some things always run, even
#       on replay. Useful for ephemeral client initializations, etc.
client = slack_client("slack_conn")

CHANNEL = getenv("CHANNEL")

# This is triggered when the webhook is hit.
def on_webhook(event):
    # `event.data` always contain the event data as sent from the connection.

    # The following is specific for Webhook payloads:
    payload = event.data.body.json
    channel = payload.get("channel", CHANNEL)
    text = payload.get("text", "Meow, World!")

    # NOTE: This WILL run as an activity, as this is a method called
    #       on an object that was returned from an external package.
    client.chat_postMessage(channel=channel, text=text)
```

### Explicit Activities

```txtar
-- autokitteh.yaml --
version: v1

project:
  name: explicit_activities

  vars:
    - name: SHEET_ID
      value: <some sheet id>

  connections:
    - name: sheets_conn
      integration: googlesheets

-- program.py --
from os import getenv
import autokitteh # The autokitteh module is installed to the default AutoKitteh virtual environment.
from autokitteh.google import google_sheets_client

# google_sheets_client returns the official Google's client.
client = google_sheets_client("sheets_conn").spreadsheets().values()

SHEET_ID = getenv("SHEET_ID")

def on_trigger(_):
  _write()


# The autokitteh.activity decorator allow you to mark a function that must run as activity.
# This allows you to run function with arguments or return values that are not compatible with pickle.
#
# The reason why this is necessary here is that client.update returns
# an object that is not serializable (or "pickleable"), so we cannot have `update`
# and `execute` run in separate activities since the data will need to be serialized
# between their invocations, and thus fail.
@autokitteh.activity
def _write():
   resp = client.update(
        spreadsheetId=SHEET_ID,
        range="Sheet1!A1:B7",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                ["String", "Hello, world!"],
                ["Number", -123.45],
                ["Formula", "=B2*B3"],
            ]
        },
    ).execute()

    print(f"Updated range: {resp['updatedRange']!r}")
```
