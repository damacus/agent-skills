---
name: explain
description: >
  Explain a code location, component, command, or user-facing system flow. Use
  when the user asks what code does, why it exists, how a feature works, or
  wants a trace of entry points, branches, dependencies, and side effects.
---

# Explain Code and Flows

Build a working mental model and explain it in one pass. This is explanation,
not code review; identify surprising behavior without turning preferences into
findings.

## Establish Evidence

Start from the named file, symbol, command, feature, or user action. Inspect the
implementation, relevant callers, configuration, tests, and generated or
framework entry points. Consult local Git history when it materially explains
why surprising code exists. Do not fetch remotes merely to add history.

## Explain a Code Location

Cover, in the order that best fits the target:

- what it accomplishes in plain language;
- the meaningful control and data flow;
- important dependencies and implicit framework behavior;
- local conventions or abstractions it relies on; and
- non-obvious behavior a maintainer must preserve.

Skip line-by-line narration of obvious syntax. Include precise file and line
references using the host application's supported format.

## Explain a System Flow

Find every relevant route, event, scheduled task, command, or integration
entry point. Trace success and failure paths through authorization, application
logic, persistence, jobs, notifications, storage, and external systems.
Summarize:

- entry points;
- decisions that change the path;
- state transitions; and
- side effects that outlive the immediate request.

Use a compact diagram only when it makes the lifecycle easier to understand
than prose.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `explain` skill at
revision `f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
