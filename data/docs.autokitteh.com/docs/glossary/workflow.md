---
sidebar_position: 12
---

# Workflow - AKA Temporal workflow

A [session](./session) in a deployment is created once it is [triggered](./trigger) and runs the code of the workflow until completion.

Under the hood, a session runs as a [temporal workflow](https://docs.temporal.io/workflows) which provides AutoKitteh durable execution.
Hence, to achieve durable execution there are deterministic constraints on workflows.

To better understand how temporal works [see](https://docs.temporal.io/temporal).
