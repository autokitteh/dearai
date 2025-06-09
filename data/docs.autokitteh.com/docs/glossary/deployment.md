---
sidebar_position: 5
---

# Deployment

A "many-to-many" association between project [builds](./build) and execution
environments of that same project (or `"default"` if no environment is
specified).

Once a deployment is created, i.e. a specific build is associated with a
specific environment, you can "activate" that deployment. This means that
future workflow runs in that environment will use this deployment's build.

The AutoKitteh server keeps a historical record of all builds and deployments,
for auditing and provenance purposes.

---

A deployment is an object in AutoKitteh contains all elements required for an execution of a project:

- Code
- Triggers
- Connection definitions
- Variables (optional)

The lifecycle of a deployment:

- Creation of deployment is implemented by building a project and deploying it
- Activation of a deployment, will cause the code to be executed and create a [session](./session) upon a trigger
- De-activation of a deployemnt, will stop triggering new sessions
- Deletion of a deployment, only no running sessions

Stated of a deployment:

- Active
- Inactive
- Draining - new events will not trigger new sessions but running sessions will continue running until complete or stopped
- Testing - only test events from the system will trigger a session, external events will not trigger new sessions
