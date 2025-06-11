---
sidebar_position: 2
description: PostgreSQL relational database
---

# PostgreSQL

## Setup

1. Install, configure, and start [PostgreSQL](https://www.postgresql.org/):

   - [Download](https://www.postgresql.org/download/)
   - Advanced and optional:
     - [Server administration](https://www.postgresql.org/docs/current/admin.html)
     - [Performance optimizations](https://wiki.postgresql.org/wiki/Performance_Optimization)

2. Create a new database for AutoKitteh:

   - CLI
     ```shell
     createdb -e <DB NAME>
     ```
   - SQL
     ```sql
     CREATE DATABASE <DB NAME>;
     ```

3. Configure AutoKitteh to use it:

   ```shell title="(Temporary)"
   ak up --config db.type=postgres --config db.dsn="dbname=<DB NAME>"
   ```

   Or:

   ```shell showLineNumbers title="(Persistent, next time you run 'ak up')"
   ak config set db.type postgres
   ak config set db.dsn "dbname=<DB NAME>"
   ```

:::tip

The Data Source Name (DSN) is a string with one or more `key=value` pairs with
space(s) between them.

All the recognized parameter keys are listed
[here](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

:::

## Reset

If you want to reset all the data in the database:

```shell showLineNumbers title="CLI"
dropdb -efi <DB NAME>
createdb -e <DB NAME>
```

Or:

```sql showLineNumbers title="SQL"
DROP DATABASE <DB NAME>;
CREATE DATABASE <DB NAME>;
```
