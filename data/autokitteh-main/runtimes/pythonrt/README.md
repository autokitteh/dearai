# Python Runtime

Implementation of Python runtime. 
See [Python runtime](https://linear.app/autokitteh/project/python-runtime-be87fe4c4d7d) for list of issues.

Currently, we don't support 3rd party packages (e.g. `pip install`) for the user code.
See [ENG-538](https://linear.app/autokitteh/issue/ENG-538/support-python-dependencies) for more details.
For a realistic POC/demo, we'll pre-install the packages the user code requires (e.g. `slack-sdk`).

## Python Handler Function
