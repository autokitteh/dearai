---
sidebar_position: 3
description: Server address, namespace, and deployment guides
---

# Temporal

The AutoKitteh server depends on [Temporal](https://temporal.io).

## Installation

Option 1: set up a Local Development Environment

- [Go](https://learn.temporal.io/getting_started/go/dev_environment/)
- [Java](https://learn.temporal.io/getting_started/java/dev_environment/)
- [TypeScript](https://learn.temporal.io/getting_started/typescript/dev_environment/)
- [Python](https://learn.temporal.io/getting_started/python/dev_environment/)

Option 2: [production deployment](https://docs.temporal.io/production-deployment)

- [Temporal Cloud](https://docs.temporal.io/cloud)
- [self-hosted](https://docs.temporal.io/self-hosted-guide)

## Server Address

The default Temporal server address is `localhost:7233`.

You may configure AutoKitteh to use a different one:

```shell title="(Temporary)"
ak up --config temporalclient.hostport=<HOST>:<PORT>
```

Or:

```shell title="(Persistent, next time you run 'ak up')"
ak config set temporalclient.hostport <HOST>:<PORT>
```

## Database

In AutoKitteh's ["dev" mode](/get_started/start_server#dev-mode), AutoKitteh
may start its own Temporal
[dev server](https://pkg.go.dev/go.temporal.io/sdk/testsuite#StartDevServer)
as a subprocess, if it can't find an already available one.

If that happens, AutoKitteh will configure its Temporal dev server to use a
[SQLite](https://www.sqlite.org/) file as a persistent database.

By default, this file is named `temporal_dev.sqlite`, and is located in
AutoKitteh's data home directory. The exact path is determined by the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

:::tip

Run this command to find out where AutoKitteh stores this file:

```shell
ak config where
```

:::

## Namespace

By default, the AutoKitteh server uses the Temporal namespace `"default"`.

You may configure a different one:

```shell title="(Temporary)"
ak up --config temporalclient.namespace=<CUSTOM>
```

Or:

```shell title="(Persistent, next time you run 'ak up')"
ak config set temporalclient.namespace <CUSTOM>
```

## Deployment Guides

Information about deploying and managing Temporal in production:

- [Self-hosted guide](https://docs.temporal.io/self-hosted-guide)
- [Temporal Cloud guide](https://docs.temporal.io/cloud)
