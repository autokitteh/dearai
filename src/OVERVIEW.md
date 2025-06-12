# AutoKitteh Overview

AutoKitteh is a "serverless" platform to build and deploy durable workflows.
Durable workflows are long-running processes that automatically resume after interruptions.

Important Sites:

- https://autokitteh.com for general information about AutoKitteh.
- https://autokitteh.cloud, a SaaS deployment of autokitteh that is publicly available.

# Durability

AutoKitteh projects run code in a durable, fault-tolerant manner using Temporal (https://temporal.io) under the hood. Temporal ensures reliability by designating non-deterministic code as ACTIVITIES, which cache their results once completed.

When a project fails due to infrastructure issues—such as instance crashes or network problems—Temporal uses a REPLAY mechanism. It reruns the entire workflow from the beginning, but leverages the cached activity results to skip re-executing those parts, allowing them to return immediately.
AutoKitteh analyzes the Abstract Syntax Tree (AST) of project code to intelligently determine which function calls should run as ACTIVITIES and which should not.

# Operation

There are three ways to configure a project:

1. Using an autokitteh.yaml, which is also known as "the project manifest".
2. Using the CLI.
3. Using the Web UI.

# Documentation Adherence Rules

- Only reference commands, APIs, syntax, or procedures that are explicitly mentioned in the provided documentation
- If specific CLI commands or API calls are not documented, say "the documentation doesn't specify the exact command" rather than inferring or assuming
- When documentation mentions something exists (like "CLI" or "API") but doesn't provide details, acknowledge the gap rather than filling it with assumptions
- If you need to reference external knowledge not in the docs, clearly label it as "based on general knowledge, not the provided documentation"
- Always cite specific sections of the documentation when making claims about how something works
