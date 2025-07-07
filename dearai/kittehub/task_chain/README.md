# Task Chain

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=task_chain)

This project runs a sequence of tasks with fault tolerance.

The workflow is resilient to errors in each step (with the ability to retry
each failing step on-demand via Slack), as well as server-side failures
(thanks to AutoKitteh's durable execution).

