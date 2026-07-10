---
name: standup
description: >
  Draft a clear standup, end-of-day update, weekly update, or client progress
  note. Use when summarizing completed work, next steps, blockers, risks,
  decisions, and support needed for a team or stakeholder audience.
---

# Draft a Standup Update

Produce an accurate, ready-to-review update without making the reader decode
commit messages. Determine the audience, time window, and desired format first
when they are not evident.

## Gather Evidence

Use supplied context and, when relevant, read-only repository evidence such as
status, recent local commits, diffs, issues, or test results. Do not fetch
remotes or inspect unrelated private activity merely to fill a standup.

Ask only about information the evidence cannot provide, especially:

- work that did not produce a commit;
- decisions or investigation outcomes;
- blockers and who can unblock them;
- risks, uncertainty, or changed expectations;
- what comes next; and
- what the audience needs to decide or know.

## Write the Update

Use the team's established structure. Otherwise organize the message around:

- completed outcomes and why they matter;
- current or next work;
- blockers, risks, and changed expectations; and
- decisions or support needed.

Lead with outcomes rather than file lists. Distinguish completed, in progress,
planned, and blocked work. Do not claim tests, delivery, impact, or certainty
that the evidence does not support. Keep internal detail out of client-facing
updates unless it helps them understand impact or make a decision.

Draft only. Never post or send the update without explicit approval.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `standup` skill at revision
`f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
