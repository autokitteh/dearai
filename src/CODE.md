{% import "_macros" as macros %}

# Code

An AutoKitteh project contains configuration (as described by a manifest) and code.
The code is Python 3 code.

By default, AutoKitteh makes available the following packages for the program:
{{ macros.quote("_data/requirements.txt") }}

**IMPORTANT**: NEVER add the above mentioned packages into the project's requirements.txt! These will be already automatically installed by the AutoKitteh runtime. Avoid using different package versions than what is already explicitly specified above.

If the additional packages are required, they can be specified in a `requirements.txt` file.

{% include "INTEGRATIONS.md" %}
{% include "_PITFALLS.md" %}
{% include "_SDK.md" %}
{% include "_TOUR.md" %}

## General Guidelines

- Each session is running isolated from other sessions:
  - You cannot, for example, store state in memory and expect another session to access it.
  - Environment variables are not shared among different sessions as well.
- For logging, use `print` functions. Currently the `logging` package is not supported.
- NEVER "invent" new AutoKitteh functions that are not explicitly exist in AutoKitteh's SDK (pyak).
- AutoKitteh will display uncaught exceptions to the user. Only catch and translate the exception if absolutely neccessary for the user to understand it.
- When using `autokitteh.subscribe`, no need to `autokitteh.unsubscribe` at the end of the program. These will be done automatically.
- IMPORTANT: All object names (projects, connections, triggers, vars) must be words which adhere to the following regex: "^[a-zA-Z\_][\w]\*$". To emphasize, do not use dashes, spaces or any other special characters for these.
- Some pyak (AutoKitteh's Python SDK for sessions) can be run only in durable sessions, some only in nondurable sessions and some can run in any mode. Check the function's docstring to know.
