# AutoKitteh Overview

AutoKitteh is a "serverless" platform to build and deploy durable workflows.
Durable workflows are long-running processes that automatically resume after interruptions.

Important Sites:

- https://autokitteh.com for general information about AutoKitteh.
- https://autokitteh.cloud, a SaaS deployment of autokitteh that is publicly available.

{% include "_MODEL.md" %}

# Durability

AutoKitteh projects run code in a durable, fault-tolerant manner using Temporal (https://temporal.io) under the hood. Temporal ensures reliability by designating non-deterministic code as ACTIVITIES, which cache their results once completed.

When a project fails due to infrastructure issues—such as instance crashes or network problems—Temporal uses a REPLAY mechanism. It reruns the entire workflow from the beginning, but leverages the cached activity results to skip re-executing those parts, allowing them to return immediately.
AutoKitteh analyzes the Abstract Syntax Tree (AST) of project code to intelligently determine which function calls should run as ACTIVITIES and which should not.

{% include "_OPERATION.md" %}

{% include "_MANIFEST.md" %}
