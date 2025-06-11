---
sidebar_position: 1
description: Python runtime
title: Introduction - Model & Tools
---

# Main Components

The main components used in AutoKitteh are:

- **AutoKitteh Service** - manages and executes projects (workflows)
- **CLI** - Command Line Interface for interacting with the AutoKitteh service
- **VS-Code Extension** - UI in VS-Code for interfacing with the AutoKitteh service
- **UI** - web interface for interacting with the AutoKitteh service

# AutoKitteh Project Flow

AutoKitteh enables you to build, deploy and manage automation Projects.

A Project is one or more tasks that have a logical association, such as shared variables, and/or interface with each other to complete a larger task.

As in any code development process, a project has several phases, each of which generates artifacts.

- **Setup - Configuration and Coding**
- **Build**
- **Deploy**
- **Manage and Monitor**
  ![Project lifecycle](/img/project_flow.png)

The image below shows the artifacts created in each phase.
![AutoKitteh flow](/img/dev_flow.png)

# Setup - Configuration and Coding

During the configuration and coding phases, a project requires:

- **Code** that defines the task
- **Resource Files** - (Optional) used in the project like images, JSON, YAML files etc.
- **Connections** - setup and definition of AutoKitteh interfaces with external applications. For example, connecting to Gmail via OAUTH.
- **Triggers** - specification of webhooks or Cron events that will trigger a function in the Project code to start a session.
- **Variables** - (optional) used in the code. For example, variables or secrets used by sessions.

# Build

Once configuration and coding are complete, you can compile, or _build_ your project. During the Build, AutoKitteh checks for syntax errors, and if found, outputs detailed error messages. When a Build succeeds, a Build artifact is created which can then be deployed to the server.

# Deploy

When a Build is deployed to the AutoKitteh server, a Deployment artifact is created. This contains all the elements needed for the project to run. A project can have only one active deployment (active version) that waits for events to start a session at the entry point defined in the trigger.

# Monitor and Manage

When a trigger event occurs, the AutoKitteh server starts a Session.

An AutoKitteh Session is a process triggered by an event (Cron or webhook) and which runs until its completion.

Under the hood, AutoKitteh implements Temporal workflows to enable durability. This means that the state is saved, and if a Session is interrupted and then restarted, execution begins from the point at which it was interrupted.

You can manage sessions: Stop, Delete and View Logs.
