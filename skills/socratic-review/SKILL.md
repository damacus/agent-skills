---
name: socratic-review
description: >
  Conduct an opt-in Socratic code review or refactoring conversation. Use when
  the user explicitly wants pairing through questions instead of an immediate
  findings report.
---

# Socratic Review

This is a pairing mode. Read the supplied scope and relevant callers, tests,
configuration, and history before asking questions. Keep a private assessment
of concrete risks so the conversation does not miss serious issues.

## Guide the Review

Begin with what the user noticed or found confusing. Ask one question at a time
and follow their reasoning before opening another problem area. Useful lenses
include:

- correctness and unintended behavior;
- data integrity, transactions, concurrency, and error handling;
- authentication, authorization, secrets, and untrusted input;
- public compatibility and change cost;
- test confidence and edge cases;
- query, allocation, blocking, and operational performance;
- responsibility, coupling, naming, and unnecessary abstraction; and
- consistency with healthy repository conventions.

Do not hide a critical security, data-loss, or production-safety finding merely
to preserve the exercise. State urgent risks directly, then continue pairing.

## Move From Diagnosis to Action

Once the important issues are understood, ask what safety net protects the
change and which move should come first. Help name the actual problem and the
smallest useful refactoring. Sequence moves by risk and dependency, and define
where to stop.

Close with the agreed issues, actions in order, and first concrete step. If the
user asks for a conventional review report instead, give direct prioritized
findings rather than forcing Socratic interaction.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `socratic-review` skill at
revision `f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
