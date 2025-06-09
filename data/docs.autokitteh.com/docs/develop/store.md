---
sidebar_position: 4
description: Project values store
title: Project Values
---

AutoKitteh supplies a project-wide cross-session key-value store.

Use this when you need to persist a value between sessions.

## Example

```python title="store.py"
from autokitteh import set_value, get_value, del_value
from time import time

def on_webhook(event):
    match event.data.method:
        case "POST":
            set_value("t", time())
        case "GET":
            print(get_value("t"))
        case "DELETE":
            del_value("t")
```

## Available Operations

- [set_value](https://autokitteh.readthedocs.io/en/latest/#autokitteh.set_value)
- [get_value](https://autokitteh.readthedocs.io/en/latest/#autokitteh.get_value)
- [del_value](https://autokitteh.readthedocs.io/en/latest/#autokitteh.del_value)
- [list_values_keys](https://autokitteh.readthedocs.io/en/latest/#autokitteh.list_values_keys)

## Limitations

- Values must be serializable (pickleable) to be persisted.
- You can store up to 64 values per project.
- Each value can not be more than 64KB in size after serialization.
- Different projects can not access each other values.
