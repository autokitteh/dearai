---
sidebar_position: 4
---

# Connection

A "connection" is a contextualizied instance of an [integration](./integration)...... with the set of required authentication properties, allowing to connect and use to the external APIs.

A connection is configured and used in the [session](./session) execution for calling APIs.

## Definition

Each connection has:

- name - to be used in the code when using the connection
- type - one of the [integrations](./integration)
- token - a token created by AutoKitteh that binds between the actual API token, stored in secret store, and an id used in sessions during execution

Additional configuration required per integration.
