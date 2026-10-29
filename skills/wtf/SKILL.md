---
name: wtf
description: >-
  Rewrite an unclear previous answer in plain UK English. Use for wtf or an
  explicit complaint that the explanation is unreadable. On the second
  occurrence in one session, record the failure and run a brief focused retro.
disable-model-invocation: true
---

# WTF

Explain the previous answer clearly first. Preserve its facts, constraints and
uncertainty. If the previous answer is unavailable, ask for it instead of guessing.

## Clarify

1. Identify the answer, practical consequence, remaining uncertainty and next step.
2. Name concrete subjects and use ordinary words, following
   `plain-technical-writing`. Explain necessary technical terms.
3. Remove unnecessary process detail without concealing incomplete work.
4. Correct an exposed factual or reasoning error explicitly rather than
   preserving it for consistency.

This is a clarification request, not permission to start adjacent implementation,
change product scope or perform external actions.

## Count actual clarification failures

Count explicit user invocations or complaints about unclear assistant wording
in this session. A pasted skill, quoted trigger, discussion of this policy or
the same request repeated in a transcript summary does not count. Use turn or
message IDs when available. Never infer missing occurrences.

Retain the count and whether the focused retro ran in the session handoff.
On the first occurrence, clarify and continue the existing task as appropriate.
On the second, perform the procedure below. Later occurrences update the same
incident; do not repeat a whole-session retrospective automatically.

## Second occurrence: record and inspect

Use the [central feedback procedure](references/communication-feedback.md).
Record one sanitised incident in the skills source repository, not the project,
installed skill directory or model memory. This procedure authorises that narrow
local record when the skill is invoked; it does not authorise publication.

Preserve live jobs and the current source checkpoint. Do not cancel a build,
switch model or create a new thread just because the wording was poor.
Run `retro` in its focused communication mode using the recent unclear answers
and user corrections. Inspect for:

- Jargon, missing subjects or excessive detail.
- Stale context, contradictory decisions or lost scope.
- Unsupported assumptions or inability to explain the actual failure.
- Repeated attempts that require reassessment under `adaptive-model-routing`.

Report the likely cause with evidence and distinguish communication from reasoning
failure. Ask one focused question about the proposed improvement, with a concrete
recommendation. Apply already-authorised corrections; wait for consequential
scope, permission or preference decisions. Do not make the owner redesign the
workflow or turn a wording failure into an expensive audit.

## Boundaries

Ordinary clarification needs no tools. On repeated failure, tools may read the
relevant session evidence and write the narrow central incident only. Keep other
work within its existing authority. Do not post transcripts, save model memories,
edit skills, schedule retros or change permissions automatically.

## Attribution

Adapted for Codex from Adam Bulmer's MIT-licensed `wtf` skill.
See [source notes](references/source-notes.md) and [LICENSE](LICENSE).
The damacus revision adds repeated-clarification feedback and a focused retro.
