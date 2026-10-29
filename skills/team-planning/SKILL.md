---
name: team-planning
description: >-
  Coordinate ownership, dependencies and shared resources for work that needs
  several contributors. Use after scope and slices are defined; skip for work
  one owner can complete without coordination.
---

# Team Planning

Use this skill only when work needs coordination between contributors,
dependencies or scarce environments. A single-owner slice does not need a
separate team plan. Do not implement or dispatch a writer while planning.

## Reuse the agreed work

Read repository instructions, settled decisions and the current handoff.
Use `slice` for decomposition and `migrate` for migration discovery and
preservation requirements. Do not repeat either process or create a second
acceptance document.

Apply `adaptive-model-routing` for all model, effort, usage and escalation
decisions. Team titles do not determine models. Existing charter role names
describe responsibilities, not a mandatory standing team.

## Resolve coordination

Update the existing brief with only what execution needs:

- One accountable owner through integration, review fixes and delivery.
- One source writer per active slice, with owned paths and read-only context.
- Dependencies, integration order and ownership of shared files and interfaces.
- Available checkouts, databases, runners and scarce test capacity.
- The agreed acceptance evidence, required review and project-native checks.
- Unresolved decisions, stopping conditions and the next implementation action.
- A place for delegated session IDs, live jobs, results and completion state.

Parallel work must be independent in ownership and verification. Keep tightly
coupled API, UI and integration work together. Do not manufacture work to occupy
agents. The coordinator can also implement; extra roles must justify their cost.

For migrations, pass the established reference and approved differences to
every contributor. The owner should not have to redescribe the existing app.
Resolve material contradictions before dependent implementation.

## Hand off

Read-only help needs a bounded question, retained evidence and existing
delegation authority. External sharing requires its own authority. Planning
does not grant permission to dispatch anyone.

Check that the brief can accept the complete journey. Require independent
review for non-trivial migrations and security work, plus repository gates.
Do not duplicate reviews of unchanged work.

Use `team-slice-development` to execute and follow delegated work to a result.
Use `plain-technical-writing` for the brief and updates. Preserve the existing
owner until the receiver acknowledges a transfer.
