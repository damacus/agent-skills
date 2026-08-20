---
name: wtf
description: >-
  Use when the user says "wtf", asks what a previous answer means, or says an
  immediately preceding assistant response was unclear, dense, or hard to
  follow.
disable-model-invocation: true
---

# WTF

Re-explain the immediately previous assistant response in plain, precise UK
English. This is a clarification, not a new task.

## Procedure

1. Read the immediately previous assistant response.
2. Identify its conclusion, decisions, conditions, warnings, and any remaining
   uncertainty.
3. If a specialist term matters, look for the repository's relevant glossary or
   context document. Use it only to preserve the term's meaning.
4. Explain the same answer with clearer structure and simpler wording.
5. Stop after the clarification.

If the previous response is unavailable, ask the user to paste it. Do not guess
at it.

## Boundaries

- Preserve technical facts, constraints, examples, values, and uncertainty.
- Keep the explanation about the previous response. Do not answer a different
  question that happens to be adjacent to it.
- Do not browse, run commands, edit files, create plans, call tools, or start
  work as part of the clarification.
- Do not add information that the previous response did not contain.
- Do not invent a glossary or introduce new terminology.

## Writing Rules

- Use active voice and plain UK English.
- Put conditions and warnings before the action they qualify.
- Use the same term for the same concept throughout.
- Replace vague pronouns with the relevant file, command, component, or value.
- Prefer short sentences and one main action per sentence.
- Define an uncommon abbreviation when it first appears.
- Prefer accurate wording over a shorter but ambiguous explanation.

## Completion Check

- Does this explain the previous response rather than continue the task?
- Are its facts and uncertainty unchanged?
- Is jargon defined or removed where possible?
- Did this clarification make no external or filesystem change?

## Attribution

Adapted for Codex from Adam Bulmer's MIT-licensed `wtf` skill. This version
adds Codex tool and mutation boundaries and removes Claude-specific framing.
See [source notes](references/source-notes.md) and [LICENSE](LICENSE).
