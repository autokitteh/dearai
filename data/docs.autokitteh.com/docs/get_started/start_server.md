---
sidebar_position: 3
sidebar_label: Start Server
description: Dev mode, prod mode, and Docker
---

# Starting a Self-Hosted Server

:::note

This tutorial assumes that you've already [installed `ak`](./install).

:::

There are several ways to start a self-hosted `ak` server. Choose the optimal
one, depending on your needs and constraints:

- ["Dev" mode](#dev-mode): the quickest way to start a local server without
  installing or configuring any dependencies

- [Docker](#docker): includes some prepackaged dependencies and configurations
  that make AutoKitteh more robust

- ["Prod" mode](#prod-mode): requires configuring and tuning, to tailor it to
  your reliability and performance needs

## Dev Mode

Simply run this command:

```shell
ak up --mode dev
```

<details>
  <summary>Under the hood</summary>
  <div>
    "Dev" mode does the following when the server starts:

    - Check whether a [Temporal](https://temporal.io) server is ready - if
      not, start a Temporal
      [dev server](https://pkg.go.dev/go.temporal.io/sdk/testsuite#StartDevServer)
      as a subprocess
    - Initialize an in-memory SQLite database
      ([`file::memory:`](https://www.sqlite.org/inmemorydb.html))
    - Initialize an in-memory
      [Miniredis](https://pkg.go.dev/github.com/alicebob/miniredis/v2) cache

    The downside of this mode is that it's less reliable, less efficient,
    and doesn't have failover or load-balancing options.

    It exists mainly for personal experimentation purposes.

  </div>
</details>

## Docker

Run these commands:

```shell showLineNumbers
git clone https://github.com/autokitteh/autokitteh.git
cd autokitteh
docker-compose up -d
```

:::info

The [default compose file](https://github.com/autokitteh/autokitteh/blob/main/compose.yaml)
starts AutoKitteh in "dev" mode.

:::

:::tip

See the comments in the
[default compose file](https://github.com/autokitteh/autokitteh/blob/main/compose.yaml)
for examples of optional customizations of Temporal, using a PostgreSQL database, etc.

:::

## Prod Mode

For the `ak up` command to work without the `--mode dev` flag, `ak` requires
at least a [Temporal](https://temporal.io) server - see the
[configuration page](/config/temporal) for details.

See also other pages in the [configuration section](/config), to
productionize and tune the AutoKitteh server, especially:

- Persistent storage with a [relational database](/config/storage/postgresql)
- Caching with a [Redis](/config/redis) server
- [HTTP tunneling](/config/http_tunneling) - to enable OAuth-based
  integrations, and incoming events
