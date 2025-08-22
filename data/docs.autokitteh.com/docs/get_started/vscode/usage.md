---
sidebar_position: 2
sidebar_label: Usage
description: Using the AutoKitteh extension in VS Code
---

import ReactPlayer from 'react-player'

# Using the VS Code Extension

AutoKitteh [projects](/glossary/project) must have a working directory, which contains:

- The project's YAML manifest file
- Source code in one or more `*.py` files

To set the project's working directory:

1. Open the project's YAML manifest file
2. In the VS Code command palette, run: `AutoKitteh: Apply Manifest`
3. A notification with an error or success result shall appear

This will run a set of commands that create the project, including its
[connections](/glossary/connection) and [triggers](/glossary/trigger). See all
the details in the OUTPUT panel.

## Build and Deploy the Project

Once the project is configured:

1. Click the sidebar AutoKitteh icon
2. Click the project name
3. Click the `Deploy` button
   - You may click `Build` first, to check that the code compiles
   - Either way, `Deploy` includes and implicit [build](/glossary/build)

You're all set! Once the project is [deployed](/glossary/deployment), its
triggers will start the execution of [workflows](/glossary/workflow) in
runtime [sessions](/glossary/session).

<ReactPlayer playing controls url='/vscode_ext_run_project.mp4' />

## Management and Monitoring

In the AutoKitteh window you can see the deployments (versions) of your
project, and the sessions that are/were running for each deployment.

You can see the logs of a selected session in the OUTPUT panel.

:::info

AutoKitteh has two output tabs:

- `autokitteh-session-logs` - the logs of the selected session
- `autokitteh-log` - all inteactions with the AutoKitteh server

:::

## Actions

1. Build - checks that the code compiles, and has all the expected dependencies
2. Deploy - creates and activates a new version of the project, ready to start
   sessions based on the defined triggers
3. Per deployment:
   1. Deactivate
   2. Activate - deactivates the previous deployment, if one exists, and sets
      the selected deployment as active
