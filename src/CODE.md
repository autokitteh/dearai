{% import "_macros" as macros %}

# Code

An AutoKitteh project contains configuration (as described by a manifest) and code.
The code is Python 3 code.

By default, AutoKitteh makes available the following packages for the program:
{{ macros.quote("_data/requirements.txt") }}

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
