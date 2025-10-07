## SDK

The AutoKitteh SDK is automatically available for import.
Its documentation can be found at https://autokitteh.readthedocs.io/en/latest/.

### Explicit Activities using the `autokitteh.activity` Decorator

The autokitteh.activity decorator allow you to mark a function that must run as activity. This allows you to run function with arguments or return values that are not compatible with pickle. This is mostly useful when performing IO.

NOTE: The autokitteh module is installed to the default AutoKitteh virtual environment.

Say you have the following code in your handler:

```py
import json
from urllib.request import urlopen


def handler(event):
    login = event['login']
    url = f'https://api.github.com/users/{login}'
    with urlopen(url) as fp:
        resp = json.load(fp)
    print('user name:', resp['name'])
```

Running this handler will fail since the result of urlopen can't be pickled. What you can do is move the code into a function marked as activity:

```py
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

All the code in user_info runs in a single activity. Since user_info accepts a str and returns a dict, both are pickleable, it can run as activity.

### Starting new child sessions using `autokitteh.start`

A session can start a new child session using the `autokitteh.start` function from the SDK.

```
autokitteh.start(loc: str, data: dict = None, memo: dict = None) -> str
```

- `loc` is the code location of the function start, format: "filename:function_name".
- `data` is the payload to pass to that function. The function can access this data via the `event.data` parameter.
- `memo` is a string to string dictionary for general memo fields that will be displayed in the UI.

The function returns the session ID for the newly created session.

Example:

```txtar
-- main.py --

import autokitteh

def on_whatever(_):
    autokitteh.start("main.py:say", {"sound": "meow"})

def say(event):
    print(event.data.sound) # prints "meow"
```

{% include "_EVENTS.md" %}
{% include "_SIGNALS.md" %}
