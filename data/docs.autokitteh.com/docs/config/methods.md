---
sidebar_position: 1
sidebar_label: Methods
description: Command-line, files, and environment variables
---

# Configuration Methods

## Command-Line

You may specify the `--config` flag multiple times in the `ak` command-line:

```shell
ak <COMMAND> [ARGS] [FLAGS] \
   --config <KEY1>=<VALUE1> [--config <KEY2=VALUE2> [...]]
```

## `config.yaml` File

You may store persistent configuration details in a `config.yaml` file, which
the `ak` CLI tool reads every time it starts running, either in the server
mode (i.e. with the `up` command) or in the client mode.

The location of this file is determined by the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

For production safety reasons, it's preferable to update this file via the
`ak` CLI tool instead of editing it directly:

```shell
ak config set <KEY> <VALUE>
```

:::tip

Run this command to find out where AutoKitteh stores its configuration and
data files:

```shell
ak config where
```

:::

:::tip

As defined in the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html),
you may set the `XDG_CONFIG_HOME` environment variable in order to override
the default path. Either way, AutoKitteh stores its configuration files in a
subdirectory named `autokitteh`.

:::

## Environment Variables

You may prefer to inject sensitive details via environment variables instead
of exposing them in AutoKitteh's command-line or its `config.yaml` file, in
order to maximize the secrecy of these sensitive details.

Stay tuned for implementation details!

## `.env` File

For ease-of-use in non-production environments, you may also set environment
variables with a `.env` file, located in the same directory as AutoKitteh's
`config.yaml` file.
