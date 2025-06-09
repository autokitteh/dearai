---
sidebar_position: 2
sidebar_label: Events
description: Supported event types
---

# Incoming Events

Supported event types:

- `file_change` - Triggered when a file is created, opened, modified, or deleted
- `file_remove` - Triggered when a file is deleted or when permissions are revoked

:::note

For complete event data structure and fields, refer to:
https://developers.google.com/drive/api/v3/reference/changes#resource

:::

:::warning

Due to `drive.file` scope restrictions, events are only triggered for files created or
managed through the AutoKitteh app.

:::
