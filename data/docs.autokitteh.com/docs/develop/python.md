---
sidebar_position: 4
description: Python runtime
title: Python
---

The Python runtime allows you to run Python code in AutoKitteh.

:::note
The minimal Python version we support is 3.11.
In order to run Python workflow, you must have Python installed on the machine running the code - where the `ak` command is.
`ak` uses the first Python it finds in the `PATH`.
:::

## Example

So you can jump right ahead.

Write the following two files in a directory.

```yaml title="autokitteh.yaml"
---
version: v1

project:
  name: py_simple
  triggers:
    - name: events
      event_type: post
      call: simple.py:greet
      webhook: {}
  vars:
    - name: USER
      value: Garfield
```

```python title="simple.py"
from os import getenv
import json
import autokitteh


HOME = getenv('HOME')  # From environment
USER = getenv('USER')  # From "vars" section in the manifest


def greet(event: autokitteh.Event): # The type annotation is optional.
    print(f'INFO: simple: HOME: {HOME}')
    print(f'INFO: simple: USER: {USER}')

    print(f'INFO: simple: event: {event!r}')
    body = event.data.body
    print(f'BODY: {body!r}')
    request = json.loads(body)
    print(f'REQUEST: {request!r}')
```

Start AutoKitteh

```
ak up --mode dev
```

Then in the directory where the workflow files are, run the following command:

```shell
$ ak deploy --manifest ./autokitteh.yaml
[plan] project "py_simple": not found, will create
[plan] var "py_simple/USER": not found, will set
[plan] trigger "py_simple:webhook/events": not found, will create
[exec] create_project "py_simple": prj_01jv3wxp0dem39cv3v2xvr29wt created
[exec] set_var "py_simple/USER": prj_01jv3wxp0dem39cv3v2xvr29wt updated
[exec] create_trigger "py_simple:webhook/events": trg_01jv3wxp10erfv1wdm0z4sac9b created
[!!!!] trigger "events" created, webhook path is "/webhooks/01jv3wxp10esctj7b0c085enfy"
[plan] project "prj_01jv3wxp0dem39cv3v2xvr29wt": found, id="prj_01jv3wxp0dem39cv3v2xvr29wt"
[exec] create_build: created "bld_01jv3wxp6mf1gvkfdn3arqx49q"
[exec] create_deployment: created "dep_01jv3wxp6ve54r6b3jxzp2m10f"
[exec] activate_deployment: activated
```

Look for the line containing `webhook path is` and write down the path (`/webhooks/01jv3wxp10esctj7b0c085enfy` is this case)

:::tip

If you forgot the webhook path, you can run `ak trigger list` to find it.
:::

Now you can run the workflow by making an HTTP request to the webhook:

```shell
curl -i -X POST -d '{"user": "joe", "event": "login"}' http://localhost:9980/webhooks/01jv3wxp10esctj7b0c085enfy
```

AutoKitteh captures `print` statements from Python and stores them in the session logs.

Use the `session prints` command to view:

```shell
ak session prints py_simple
```

## Overview

The Python runtime can receive events from configured [connection triggers](/glossary/trigger.md).
It _cannot_ use the connection for outgoing messages, you'll need to use a Python library to do that.

### Handler Functions

Each Python handler is a function that receives a single parameter called `event` of type [Event](https://autokitteh.readthedocs.io/en/latest/#autokitteh.Event).
The event has these attributes:

- `data`: This is the "raw" event sent by the trigger. The content of `data` depends on the trigger's integration.
- `session_id`: This is the session id of the workflow.

The event type is a dict-like object, you can access attributes values using the `.` operator or the `[]` operator.
Both of the following lines are valid:

```python
body = event.data.body
body = event['data']['body']
```

:::warning
You can't set event values with attributes.
The following is valid:

```python
event['data']['user'] = 'Garfield'
```

The following raises an exception:

```python
event.data.user = 'Garfield'
```

:::

#### asyncio

We support [async functions](https://docs.python.org/3/library/asyncio.html) (`async def`) as event handlers.
Here's an example:

```python
import autokitteh


async def on_http_start(event):
    print('START:', event)
    await act()
    print('END')


@autokitteh.activity
async def act():
    print('ACT')
```

AutoKitteh will use [asyncio.run](https://docs.python.org/3/library/asyncio-task.html#asyncio.run) to run `on_http_start`.

:::note

AutoKitten runs activities in a thread pool, this can cause issues with asyncio code.

:::

### Module Level Function Calls

Functions called during module import are executed as regular functions (not activities).
Make sure that these function are deterministic, otherwise a replay of your workflow can yield different results.

:::info

A deterministic function is a function that always returns the same results if given the same input values.

:::

For example:

```python
from os import getenv

api_key = getenv('API_KEY')
```

`getenv` will _not_ run as activity.
This is intentional and useful for setting up connections and other global state.

## Third Party Dependencies

AutoKitteh creates a virtual environment using the system Python.
It uses the first `python3` or `python` found in your `PATH` environment variable.

:::note
AutoKitteh creates the virtual environment once on the first time you deploy a Python workflow.
This causes the first time you deploy a Python workflow to take a while.
Next deployments will be faster.

Once the virtual environment is created, AutoKitteh will use the python executable inside it.

To install packages at the virtual environment, see [here](#installing-python-packages).
:::

:::info
You can override which Python executable to use by setting the `AK_WORKER_PYTHON` environment variable.
If you set this environment variable, AutoKitteh will use this Python without creating a virtual environment.

If you want to create your own virtual environment, see [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
To see how you can install other version of Python, see [pyenv](https://github.com/pyenv/pyenv).
:::

AutoKitteh installs the following packages to the virtual environment:

```
# Integrations

atlassian-python-api ~= 3.41
boto3 ~= 1.34
google-api-python-client ~= 2.122
google-auth-httplib2 ~= 0.2
google-auth-oauthlib ~= 1.2
jira ~= 3.8
openai ~= 1.14
PyGithub ~= 2.2
redis ~= 5.0
slack-sdk ~= 3.27
twilio ~= 9.0

# AutoKitteh SDK

autokitteh ~= 0.2

# General

beautifulsoup4 ~= 4.12
PyYAML ~= 6.0
requests ~= 2.31
```

See the update list [here](https://github.com/autokitteh/autokitteh/blob/main/runtimes/pythonrt/py-sdk/pyproject.toml).

### Installing Python Packages

#### Self Hosted

If you want to install other packages, first find out where the virtual environment is.

```shell
ak config where
```

Say the "Data home directory" is `/home/ak/.local/share/autokitteh`,
then the virtual environment is at `/home/ak/.local/share/autokitteh/venv`.

Use the `python` executable from the virtual environment to install packages.
For example:

```shell
/home/ak/.local/share/autokitteh/venv/bin/python -m pip install pandas
```

#### Web Platform

- Create a `requirements.txt` file in your project

![Create req](/img/requirements_walkthrough/create_req.png)

- List the required libraries in `requirements.txt`

![req walkthrough](/img/requirements_walkthrough/req_file_example.png)

- Deploy and run the project

## Local Development

## Setting Up Your IDE

If you want to debug your code and get autocompletion,
you need to tell your IDE to use the Python from the AutoKitteh virtual environment.
This way, the IDE runs your code in the same environment that AutoKitteh uses to run it.

If you don't have AutoKitteh virtual environment, you can create a virtual environment yourself.

Download [pyproject.toml][req] to your machine.
The in a terminal, run:

```
python -m virtualenv venv
venv/bin/python -m pip install .[all]
```

This will create a virtual environment called `venv`, point your IDE Python to `/path/to/venv/bin/python`.

[req]: https://raw.githubusercontent.com/autokitteh/autokitteh/refs/heads/main/runtimes/pythonrt/py-sdk/pyproject.toml

### Visual Studio Code

Copy the interpreter path (see above) to the clipboard.

Open the command pallet and write `Python: Select Interpreter` and paste the interpreter path.
For more information, see the [official Visual Studio Code documentation][vscode].

Also, don't forget to install the [autokitteh extension][ext] so you'll be able to install and manage workflows.

[ext]: https://marketplace.visualstudio.com/items?itemName=autokitteh.autokitteh
[vscode]: https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter

### PyCharm

In `Settings` pick your project and then `Python Interpreter`.
Click on `Add interpreter` on the top right and select `Add Local Interpreter`.
Click on `System Interpreter` from the list on the left and then enter the interpreter path from autokitteh virtual environment (see above).

For more information, see the [official PyCharm documentation][pycharm].

[pycharm]: https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html

### Isolated Handler Functions

Handler functions are the functions you define in the manifest, they are called by AutoKitteh on new events.
Handler functions are regular Python functions, and you can debug them like you debug other Python code.

If your handler function is using vars or secrets, you need to set the environment before importing the handler module.
See [Working with Secrets](#working-with-secrets) on how to name your environment variables.

For example, say you have a `handler.py` with an HTTP `on_event` handler function:

```python title="handler.py"
def on_event(event):
    print("BODY:", event.data.body.decode())
```

Then you can run the handler function like this:

```python
from autokitteh import AttrDict
import handler

# AutoKitteh events are instances of autokitth.AttrDict
event = AttrDict({"data": {"body": "hello".encode()}})
handler.on_event(event)
```

### Debugging Workflows

Before you run `ak` locally, set up any environment variables for secrets/vars that are required by your workflow.
For example:

```shell
export TOKEN=s3cr3t
```

Another option is to use the `ak var set` command instead of setting environment variables.
You need to run this command _after_ starting `ak`.

The easiest way to run a workflow locally is to add an HTTP trigger.

```yaml title="autokitteh.yaml"
version: v1

project:
  name: hello

  triggers:
    - name: events
      event_type: post
      call: simple.py:greet
      webhook: {}
```

Next, deploy your workflow:

```
ak deploy --manifest ./autokitteh.yaml --file handler.py
```

And now you can trigger your code:

```
curl -d hello http://localhost:9980/webhooks/<webhook_id>
```

You can view the print output using the `ak session prints` command.

Every time you change the handler code, you need to re-deploy the workflow.

## Limitations

:::danger
We try to lift these limitations as we progress, but currently your workflow will fail if you don't follow them.
:::

### Function Return Value Must Be Pickleable

We use [pickle](https://docs.python.org/3/library/pickle.html) to pass function arguments back to AutoKitteh to run as an activity.
See [What can be pickled and unpickled?](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled) for supported types. Most notably, the following can't be pickled:

- Open file handlers (when `open` returns)
- lambdas
- dynamically generate functions (e.g. `os.environ.get`)

```python title="bad.py"
import db

def handler(event):
    mapper = lambda n: n.lower()
    # highlight-next-line
    db.apply(mapper)  # BAD
```

```python title="good.py"
import db

# highlight-start
def mapper(n):
    return n.lower()
# highlight-end

def handler(event):
    # highlight-next-line
    db.apply(mapper)  # GOOD
```

:::note
You can use [copyreg.pickle](https://docs.python.org/3/library/copyreg.html#copyreg.pickle) in order to support more types.
:::



#### Using the `autokitteh.activity` Decorator

The `autokitteh.activity` decorator allow you to mark a function that must run as activity.
This allows you to run function with arguments or return values that are not compatible with `pickle`.
This is mostly useful when performing IO.

:::note
The `autokitteh` module is installed to the default AutoKitteh virtual environment.
If you provide your own Python by setting the `AK_WORKER_PYTHON` environment variable,
you will need to install the `autokitteh` module.

`python -m pip install autokitteh`.

You can see the API documentation [here](https://autokitteh.readthedocs.io/en/latest/).
The `autokitteh` module also contains common operation for connection to various services.
:::

Say you have the following code in your handler:

```python
import json
from urllib.request import urlopen


def handler(event):
    login = event['login']
    url = f'https://api.github.com/users/{login}'
    with urlopen(url) as fp:
        resp = json.load(fp)
    print('user name:', resp['name'])
```

Running this handler will fail since the result of `urlopen` can't be pickled.
What you can do is move the code into a function marked as activity:

```python
import json
from urllib.request import urlopen

import autokitteh


def handler(event):
    login = event['login']
    info = user_info(login)
    print('user name:', info['name'])


@autokitteh.activity
def user_info(login):
    url = f'https://api.github.com/users/{login}'
    with urlopen(url) as fp:
        resp = json.load(fp)
    return resp
```

All the code in `user_info` runs in a single activity.
Since `user_info` accepts a `str` and returns a `dict`, both are pickleable, it can run as activity.

### Function Timeout

If a function that runs in a workflow context (not in an activity) takes a long time, it might cause a timeout.

Say you have the following code:

```python
from collections.abc import Sequence


class Response(Sequence):
    def __init__(self, count):
        self.count = count

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        if index >= self.count:
            raise IndexError

        print("calling server")  # network call, takes time
        return {
            'id': index,
            'level': 'INFO',
            'message': f'log #{index+1}',
        }


def get_logs(env: str) -> Response:
    # TODO: Actual code
    return Response(3)


def on_event(event):
    logs = get_logs(event.data.env)
    logs = sorted(logs, key=lambda log: log['id'])  # timeout
    ...  # More code
```

When the workflow runs, `sorted(logs)` is _not_ in an activity, and will cause a timeout due to network calls in `__getitem__`.

The solution is to place long running code in an activity:

```python
@autokitteh.activity
def on_event(event):
    logs = get_logs(event.data.env)
    logs = sorted(logs, key=lambda log: log['id'])  # timeout
    ...  # More code
```

## How It Works

AutoKitteh first loads your code and then instruments every function call that is external to your module.
Each instrumented call will run as an activity.

## Working with Secrets

AutoKitteh has a secret store. These secrets are exposed to Python via the environment.

For example, if you set a token:

```shell
$ ak var set --secret --env env_01hyg78h31e3yahn2dt4mf9nzz TOKEN s3cr3t
```

:::tip
To get the list of environments (for `--env`), use `ak env list`.
:::

Then in your python code you can write the following to access it:

```python
from os import getenv

def handler(event):
    token = getenv('TOKEN')
    if not token:
        raise ValueError('missing `TOKEN` environment variable')
    # Use token...
```

If you need a secret in a file (e.g. Google's [service account keys][gsvc]),
you can set the secret value to be the file's contents.
Download the file (e.g. to `/tmp/credentials.json`), and run these commands:

```shell
$ ak var set --secret --env env_01hyg78h31e3yahn2dt4mf9nzz GOOGLE_CREDS_DATA < /tmp/credentials.json
$ shred -u /tmp/credentials.json  # Delete local file, optional but recommended
```

Then in your script you can write the file and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```python
import os


def ensure_google_credentials():
    env_key = 'GOOGLE_APPLICATION_CREDENTIALS'
    if os.getenv(env_key):
        return

    creds_file = 'credentials.json'
    data = os.getenv(env_key)
    with open(creds_file, 'w') as out:
        out.write(data)
    os.putenv(env_key, creds_file)


def commit_handler(event):
    ensure_google_credentials()
    ...  # Rest of handler code
```

### Connection Secrets

Connections have their own secrets. You can access them via the environment as well.
The environment variable name is the connection name followed by two underscores and the secret name.

For example: Say you defined an HTTP connection called `http_trigger` and set its bearer token to `s3cr3t`.

You can look at the connection web page to see the environment variable name under the `Vars` section.
In this case, it'll be `auth`. So in your workflow code you can write:

```python

token = getenv('http_trigger__auth')
print(f'HTTP token: {token!r}')
```

Note that the value of token is `Bearer s3cr3t`, not `s3cr3t`.

[gsvc]: https://cloud.google.com/iam/docs/keys-create-delete#creating

## Waiting For Events

AutoKitteh triggers a workflow when an event is received.
But, you can also wait for events from inside your workflow using `subscribe` and `next_event`.

```python
from datetime import timedelta

import autokitteh


def on_http_get_meow(event):
    """This workflow is triggered by a predefined HTTP GET request event."""
    print("Got a meow, waiting for a woof")

    # Wait (up to 1 minute) for a subsequent webhook
    # event where the URL path ends with "woof".
    filter = "data.url.path.endsWith('/woof')"
    sub = autokitteh.subscribe("meow_webhook", filter)
    delta = timedelta(minutes=1)
    next = autokitteh.next_event(sub, timeout=delta)

    if next:
        print("Got a woof:", next)
    else:
        print("Timeout!")
```

You can read more about events in [Programmatic Event Handling](/develop/events/subscription).
