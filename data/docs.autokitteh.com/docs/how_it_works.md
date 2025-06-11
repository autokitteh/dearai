---
sidebar_position: 3
---

# How It Works

AutoKitteh is a platform that can be easily deployed on-prem, in the cloud, or on a PC (see supported platforms). It provides an API for the creation, deployment, and management of projects, each potentially comprising multiple workflows. The API is accessible to a user via CLI, VS Code extension, and cloud UI (coming soon).

Essentially, AutoKitteh receives user-provided configuration and code, executes the code within its secure environment, and implements the features mentioned above. A project's configuration specifies:

- **Connections** (adapters) to various services (e.g., Slack, GitHub) that the project can leverage during execution.
- **Triggers** connect between events on connections (e.g. event received in webhook) and an entry function in the code that initiates workflow execution.
- **Optional variables** usable within the code.

The code, written using one of the supported languages, can interact with external applications through provided connector APIs and use various code utilities such as sharing information between workflows, setting API call retry policy, and more.

Once prepared, a deployment (encompassing both configuration and code) is created and pushed to the server for execution. Each workflow execution instance is referred to as a **session**.

![AutoKitteh flow](/img/how_it_works.png)

AutoKitteh is powered by [Temporal](https://temporal.io) as a durable execution engine. Sessions are executed as Temporal [workflows](https://docs.temporal.io/workflows) and calls to external APIs are executed in a session, seamlessly, as [activities](https://docs.temporal.io/activities) in Temporal.
Developers and operators can readily retrieve session status information and perform management actions like stopping a session, activating or deactivating a deployment, and more. They also have access to detailed statistical data about sessions and deployments, covering metrics like execution time, success/failure rates, and other indicators.
