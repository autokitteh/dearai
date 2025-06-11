---
sidebar_position: 3
---

# Project

A collection of settings:

- A unique name
- Zero or more [connections](./connection)
- Zero or more workflow [triggers](./trigger)
- Zero or more execution environments
- Zero or more environment [variables](./variable)

In addition to these settings, each project is also associated with one or
more files: source code, and optional assets (e.g. data, images, etc.).

These settings and files define a shared goal, and implement one or more
[workflows](./workflow) that address it.

Project [builds](./build) are immutable snapshots of a project's source and
compiled files, which are decoupled from its settings.

---

Project has 3 stages:

1. **Configuration:** aggregation of all the resources required for the project to be executed. A project must have one or more files containing the execution code, assets (such is images, data etc.) and a set of configurations:

- Triggers
- Connections
- Variables (optional)

2. **Deployments:** A project contains a set of [deployments](./deployment). Only one deployment can be active simultaneously. An active deployment is typically waiting for trigger to start running the code.

3. **Execution:** a [trigger](./trigger) will start the execution on the code at the triggered function. Once activated, a [session](./session) is starts execution. Sessions contain information about the execution, the trigger, events it might receive and logs and statistics.

![AutoKitteh flow](/img/Project-states.png)

The user can:

- Build a project - creating a deployment from configuration
- Activate / Deactivate a deployment
- Delete deployment
- Delete project
