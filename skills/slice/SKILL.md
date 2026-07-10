---
name: slice
description: >
  Break a feature, epic, migration, or capability into independently valuable
  and verifiable delivery slices. Use when work is too large, vague, layered,
  risky, or needs sequencing around user value and learning.
---

# Slice Work Vertically

Understand the outcome before decomposing the implementation. Establish:

- the specific person or system that benefits;
- the situation that creates the need;
- the observable outcome that marks success;
- launch or contractual requirements that cannot be deferred; and
- the largest uncertainty or risk.

## Shape Slices

Prefer vertical slices that cross the necessary layers and produce observable
value. A useful slice can ship, be demonstrated, and be verified independently.
Infrastructure-only work may be necessary, but it is a dependency or enabler,
not automatically a user-valued slice.

For each candidate, test:

- Can it ship without the remaining candidates?
- Can a user or stakeholder observe the result?
- Does it include its happy path, important boundary, and failure behavior?
- Does it reduce a meaningful product or technical risk?
- Is it one outcome rather than several joined by “and”?

Slicing delivery does not redefine the requested launch, silently discard
quality, or relabel mandatory work as a later phase.

## Sequence and Deliver

Order slices by value, learning, risk, and dependency rather than ease alone.
For each slice provide a short name, user or system outcome, completion signal,
acceptance criteria, dependencies, and risk or learning objective. Use a job
story only when that format helps the team.

Finish by checking whether the first slice is genuinely independently useful
and whether the complete sequence still satisfies the full requested outcome.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `slice` skill at revision
`f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
