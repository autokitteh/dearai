## Pitfalls

## Entry Point Functions Must Be Synchronous

Entry point functions (functions called from triggers) MUST be synchronous. AutoKitteh does not support async functions as entry points.

If you need to use async operations in your workflow, create a synchronous wrapper function that uses `asyncio.run()`:

```python
import asyncio

# Entry point function - MUST be synchronous
def on_event(event):
    asyncio.run(handle_event_async(event))

# Actual handler can be async
async def handle_event_async(event):
    result = await some_async_operation()
    await another_async_operation(result)
```

**BAD - This will cause deployment to fail:**

```python
# Entry point is async - WILL FAIL
async def on_event(event):
    result = await some_async_operation()
```

**GOOD - Synchronous entry point:**

```python
def on_event(event):
    asyncio.run(async_handler(event))

async def async_handler(event):
    result = await some_async_operation()
```

## Function Return Value Must Be Pickleable

In durable mode, we use pickle to pass function arguments back to AutoKitteh to run as an activity. See What can be pickled and unpickled? for supported types. Most notably, the following can't be pickled:

- Open file handlers (when open returns)
- lambdas
- Dynamically generated functions (e.g. os.environ.get)

```txtar
-- bad.py --
import db

def handler(event):
    mapper = lambda n: n.lower()
    db.apply(mapper)  # BAD

-- good.py --
import db

def mapper(n):
    return n.lower()

def handler(event):
    db.apply(mapper)  # GOOD
```

NOTE: You can use copyreg.pickle in order to support more types.

## Function Timeout

In durable mode, if a function that runs in a workflow context (not in an activity) takes a long time, it might cause a timeout.

Say you have the following code:

```py
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

When the workflow runs, `sorted(logs)` is not in an activity, and will cause a timeout due to network calls in `__getitem__`.

The solution is to place long running code in an activity:

```py
@autokitteh.activity
def on_event(event):
    logs = get_logs(event.data.env)
    logs = sorted(logs, key=lambda log: log['id'])  # timeout
    ...  # More code
```
