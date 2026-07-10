---
name: challenge
description: >
  Pressure-test an assumption, architecture decision, estimate, or inherited
  constraint. Use when the user asks to challenge a belief, play devil's
  advocate, test reasoning, or find a simpler alternative.
---

# Challenge an Assumption

Treat this as a focused conversation, not an audit. Use the context already
available and ask one useful question at a time. Do not make the user restate
facts you can inspect or already know.

## Explore the Claim

Clarify:

- the exact claim or decision;
- the underlying need, separate from the proposed solution;
- where the belief came from and what evidence supports it;
- what conditions would make it false;
- what evidence would change the decision; and
- the simplest credible alternative.

Distinguish a real constraint from convention, familiarity, speculation, or a
future problem that has not arrived. Test alternatives against the same
requirements rather than presenting novelty as improvement.

## Conclude

Once the reasoning is clear, give a direct verdict: retain, qualify, test, or
reject the assumption. State the strongest evidence, the unresolved risk, and
the next decision or experiment. Do not remain Socratic when the user needs a
clear recommendation.

Conversation does not authorize code changes, external messages, or other
mutations. Take those actions only when the user separately requests them.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `challenge` skill at
revision `f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
