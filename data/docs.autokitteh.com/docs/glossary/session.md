---
sidebar_position: 9
---

# Session

A session represents an execution of a [workflow](./workflow).

Session states:

- Created - a session is created once a trigger associated with an active integraion is received
- Running - the session is running until its codes completes
- Error - the session terminated with and error
- Completed - the session terminated in success and reached its end

A session is executed as a Temporal workflow and all API calls via connections are implemented as Activities.

A session is identified by a session is that starts with "s:........".

A session can be forcefully terminated.
