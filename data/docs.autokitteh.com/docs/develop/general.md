---
sidebar_position: 3
description: Explanation about what are Runtimes, which Runtimes we support, how to add runtimes etc.
title: Introduction - SDKs
---

AutoKitteh server can support various SDKs and languages, each with its pros and cons.

The code developed using an SDK is executed on a "Runtime". A Runtime is an engine that seamlessly converts the code, during runtime, to a durable code execution, and provides other services such as access to variables and secrets, execution from triggers and more.

Under the hood, the runtime converts the code to a workflow and functions with side effects to activities in Temporal. This assures after system restart, the workflow code will continue from the same spot.

_NOTE_: AutoKitteh is designed to work as an orchestration platform. Executing workflows with heavy CPU or Memory consumption is not recommended.

Autokitteh supports the following SDKs:

- [Python](./python.md) - develop workflows in Python code, with some restrictions.
  - Pros: Ability to use Python libraries, validate Python code in local environment, and deploy in AutoKitteh to make it durable
  - Cons: For security reasons Python runtime needs to be isolated. This comes with some performance penalty
- [TypeScript](./typescript.md) - Coming soon

** Adding Runtimes**
It is also possible to add runtimes to AutoKitteh. There is a clear interface between the AutoKitteh services and the Runtime.
