---
sidebar_position: 2
description: Aggregated reference of supported integration events
title: Types
---

# Event Types

This is a summary of all the events reference pages in the
[Integrations](/integrations) documentation section.

## Atlassian

AutoKitteh automatically manages push and pull notifications, and dispatches
them to all the relevant projects. All you have to do is declare in your
project which events you want to receive, and how to handle them.

### Confluence

- Everything in:
  - https://developer.atlassian.com/cloud/confluence/modules/webhook/#confluence-webhook-events
  - https://confluence.atlassian.com/doc/managing-webhooks-1021225606.html

### Jira

- Everything in:
  - Atlassian Cloud: https://developer.atlassian.com/cloud/jira/platform/webhooks/
  - On-prem servers: https://developer.atlassian.com/server/jira/platform/webhooks/

## Discord

## GitHub

- Everything in https://docs.github.com/en/webhooks/webhook-events-and-payloads

## Google

### Gmail

- `mailbox_change`

### Google Calendar

- `event_created`

- `event_updated`

- `event_deleted` (one or all instances of an event were deleted)

> [!NOTE]
> For details about event data, see:
> https://developers.google.com/calendar/api/v3/reference/events#resource

#### Not Implemented Yet

- `event_starting_in_10_minutes`

- `event_starting_in_5_minutes`

- `event_started_now`

- `event_ended_now`

- https://developers.google.com/calendar/api/v3/reference/calendarList/watch

- https://developers.google.com/calendar/api/v3/reference/acl/watch

### Google Drive

### Google Forms

- `responses` (form responses submitted)

- `schema` (changes to form content and settings)

## Slack

- Everything in https://api.slack.com/events?filter=Events

- `interaction` (https://api.slack.com/interactivity/handling)

- `slash_command` (https://api.slack.com/interactivity/slash-commands)
