---
sidebar_position: 1
description: Usage overview, and default SQLite file
---

# Overview

The AutoKitteh server requires a relational database as its primary means of
state management and data storage.

## AutoKitteh "Dev" Mode

By default, AutoKitteh uses a [SQLite](https://www.sqlite.org/) file named
`autokitteh.sqlite`, located in AutoKitteh's data home directory. The exact
path is determined by the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

:::tip

Run this command to find out where AutoKitteh stores this file:

```shell
ak config where
```

:::

You may specify a different SQLite file path for development and testing
purposes:

```shell title="(Temporary)"
ak up --config db.type=sqlite --config db.dsn="path/filename.sqlite"
```

## AutoKitteh "Prod" Mode

In ["dev" mode](/get_started/start_server#dev-mode), you may configure
AutoKitteh to use a more robust RDBMS, in order to support data durability
with better failover, recovery, and performance.

In ["prod" mode](/get_started/start_server#prod-mode), this is a requirement
rather than a recommendation.

Either way, see the next page for more details.
