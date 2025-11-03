# Gmail Integration

Reacting on Gmail state change can be done in either of two ways:

- Polling using a schedule trigger and checking the state, or -
- Triggering on Gmail "mailbox_change" events.

The only event available for Gmail in AutoKitteh is "mailbox_change". The event data fields are:

- `publish_time`: the publish time of the message, taken from the X-Goog-Pubsub-Publish-Time header from Gmail notification.
- `email_address`: the Gmail account that owns the mailbox where the change occurred.
- `history_id`: represents a specific point in time in a Gmail mailbox's history. This can be used for incremental syncs.

IMPORTANT: There are no other fields on this event! Do not try to use trigger filters on this events. NEVER set the Trigger filter for GMail.

Common use case for `history_id`:

1. Your app receives a Pub/Sub notification with history_id: 12345
2. You can call Gmail's users.history.list() API with startHistoryId: 12345 to get all changes since that point
3. This gives you exactly what changed (new messages, deletions, label updates) without having to scan the entire mailbox
