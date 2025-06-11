---
sidebar_position: 1
slug: /
---

# What is AutoKitteh?

AutoKitteh is an open-source workflow automation and orchestration platform
tailored for developers. It enables the creation, management, and monitoring
of code-centric automations and durable workflows.

It is a developer-first alternative to no-code/low-code platforms (such as
Zapier, Workato, Make.com, etc.), as well as a durable execution platform
which is a complement to [Temporal](https://temporal.io).

It offers tools and simplified abstractions for crafting reliable,
long-running workflows without sacrificing the power and flexibility of
sophisticated code.

## Who Can Benefit From AutoKitteh

AutoKitteh is designed for users ranging from the very sophisticated to the
less technical skilled enthusiast. Typical use cases include:

- **DevOps engineers:** Whether you're setting up CI/CD pipelines, managing cloud resources, or building orchestration workflows, AutoKitteh streamlines your processes and deploys them in a highly reliable manner. AutoKitteh lets you quickly connect to cloud service providers (e.g., AWS, Google, Azure), code repositories (e.g., GitHub, Gitlab), and other popular tools such as Slack, Jira, etc.

- **Backend developers:** For long-running, reliable workflows that link microservices and external APIs, AutoKitteh offers a simplified alternative to platforms such as Temporal, Cadence, Prefect, AWS Step Functions, or Airflow.

<!-- - **Automation engineers and enthusiasts:** If you're seeking an alternative to platforms like Zapier, Make.com, or Workato, AutoKitteh's code-centric approach empowers you to build and manage customized, complex, and long-running automation solutions.
 -->

- **Automation engineers and enthusiasts:** AutoKitteh is for you if you're into building and managing automations but need more control than what other platforms offer (like Zapier, Make.com, or Workato). AutoKitteh’s simple-yet-powerful tools allow you to build and manage workflows ranging from basic to super sophisticated.

:::note

AutoKitteh is more of an orchestration platform for any type of pipeline. It
is less suitable for the actual processing in ETL and big data pipelines.

:::

## Why You Should Try AutoKitteh

AutoKitteh offers a blend of simplicity and power, enabling users to define workflows and automations in code for precise control while providing an easy-to-use abstraction layer and all the boilerplate features required for building and managing workflows.

**If this resonates with your automation challenges, try it out.**

## Core Features

- **Built-in integrations:** Off-the-shelf connections to many services, that takes care of the hassles of secrets management, authentication, and complex API calls.

- **Managed deployments:** Immediate workflow deployment and execution.

- **Event-driven execution:** Versatile triggers to start workflows: cron scheduling, webhooks, and manual commands via the AutoKitteh CLI or User Interface.

- **Durable execution:** Fault tolerance and seamless recovery from server failures,
  powered by [Temporal](https://temporal.io). To learn more about this, see this
  [technical guide](https://assets.temporal.io/durable-execution.pdf).

- **Monitoring:** Rich telemetry and observability for execution states, and performance metrics.

- **Logging and debugging:** Detailed log and event collection for debugging and execution analysis.

- **Security:** Isolation between workflows and users to ensure secure execution.

- **Scalability:** Designed to scale with increasing load.
