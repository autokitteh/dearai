---
sidebar_position: 1
---

# CI/CD and DevOps

DevOps and CI/CD processes often require long running workflows. For example, tasks that require long execution (e.g. when building big projects or running tests, creating cloud environments etc.) or workflows that require manual intervention.

Such use cases typically work asyncrounisly and built using events, queues and state machines.
AutoKitteh enables writing such use cases relatively easily.

## Never Miss a Pull Request Review Reminder (PuRRR)

PuRRR streamlines code reviews, to cut down the turnaround time for merging pull requests.

- Integrates GitHub and Slack seamlessly and efficiently
- Provides real-time, relevant, informative, and bidirectional updates
- Enables better collaboration and faster execution

Bases use case:
Trigger:

- PR in Github
  Workflow:
- Notify groups Slack Channel on ne PR
- As long as the PR is open:
  - Update PR status upon any change
  - If after X hours PR is not closed: notify the team lead
  - If after Y days the PS is not closed: send an email to the manager

This workflow can be easily extended or modified to fit your team work of policy.

Code sample: [PuRRR](https://github.com/autokitteh/kittehub/tree/main/purrr)
