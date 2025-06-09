---
sidebar_position: 1
description: Connecting to PostgreSQL databases in AutoKitteh workflows
---

# PostgreSQL

## Overview

PostgreSQL is a powerful, open-source relational database system. This guide shows how to connect to PostgreSQL databases from within AutoKitteh workflows using Python.

## Prerequisites

- PostgreSQL server running and accessible
- `psycopg2` Python library installed ([see installation guide](/develop/python#installing-python-packages))
- DSN

## Connection Example

```python
import os
import autokitteh
import psycopg2

DSN = os.getenv("DSN")

@autokitteh.activity
def on_trigger(event):
    conn = psycopg2.connect(DSN)

    try:
        with conn.cursor() as cur:
            # Your database operations here.
            cur.execute("SELECT * FROM users")
            results = cur.fetchall()
            print(results)
    finally:
        conn.close()
```

## Important Requirements

### Activities Only

**All database operations and connections must be created within the same AutoKitteh activity.** Database connections and queries cannot be executed outside of activities in AutoKitteh workflows. This includes the `psycopg2.connect()` call itself.

### Short Operations

PostgreSQL connections in AutoKitteh should be **short-lived operations**. They are not durable and should be used for:

- Quick data retrieval
- Simple insert/update operations
- Brief transactions

### Durability Limitations

Database connections are **not persistent across workflow replays**. During replay scenarios:

- Database connections cannot be reopened
- Connection state is not maintained
- Operations may fail during replay

For this reason, keep database operations simple and atomic within each activity.

## Best Practices

1. **Always use activities** for database operations
2. **Keep operations short** and focused
3. **Use try/finally blocks** to ensure connections are properly closed

## Connection Parameters

The `psycopg2.connect()` function accepts various parameters:

- `host`: Database server hostname or IP address
- `port`: Database server port (default: 5432)
- `database`: Database name
- `user`: Database username
- `password`: Database password
- `sslmode`: SSL connection mode (optional)
- `connect_timeout`: Connection timeout in seconds (optional)

For production deployments, consider using environment variables or AutoKitteh's secret management for sensitive connection details. See [Working with Secrets](/develop/python#working-with-secrets) for more information.
