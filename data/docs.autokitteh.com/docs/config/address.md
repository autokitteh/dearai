---
sidebar_position: 2
description: Server port, service URL for clients
---

# Server Address

## Server Port

The default TCP port number of the AutoKitteh server is **9980**.

The AutoKitteh server uses this port for its gRPC-based API, as well as its
HTTP webhooks and web UI.

You may configure AutoKitteh to start with a different one:

```shell title="(Temporary)"
ak up --config http.addr=[HOST]:<PORT>
```

Or:

```shell title="(Persistent, next time you run 'ak up')"
ak config set http.addr [HOST]:<PORT>
```

Specifically, if you want to pick a random available port:

```shell
ak up --config http.addr=:0
```

## Service URL for Clients

When you run the `ak` CLI tool as a client, the default AutoKitteh server
address is http://localhost:9980.

To communicate with a different server address:

```shell title="(Temporary)"
ak --config http.service_url=http[s]://<HOST>[:<PORT>] <COMMAND> [ARGS] [FLAGS]
```

Or:

```shell title="(Persistent, next time you run 'ak')"
ak config set http.service_url http[s]://<HOST>[:<PORT>]
```
