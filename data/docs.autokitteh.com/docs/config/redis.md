---
sidebar_position: 5
description: Server URL, and deployment guides
---

# Redis

## Server URL

By default, the AutoKitteh server uses an ephemeral, in-memory
[Miniredis](https://pkg.go.dev/github.com/alicebob/miniredis/v2) cache which
disappears when the process is terminated.

You may configure AutoKitteh to use a real [Redis](https://redis.io/) server:

```shell title="(Temporary)"
ak up --config store.server_url=redis://<HOST>:<PORT>[/<DB>]
```

Or:

```shell title="(Persistent, next time you run 'ak up')"
ak config set store.server_url redis://<HOST>:<PORT>[/<DB>]
```

## Deployment Guides

Information about deploying and managing Redis in production:

- [Local install guides](https://redis.io/docs/install/)
- [Administration guides](https://redis.io/docs/management/)
- [Redis Enterprise Software documentation](https://docs.redis.com/latest/rs/)
- [Redis Enterprise for Kubernetes documentation](https://docs.redis.com/latest/kubernetes/)
- [Redis Cloud documentation](https://docs.redis.com/latest/rc/)
