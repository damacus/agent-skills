---
name: start
description: Start new work by checking existing decisions and implementation, investigating the important unknowns, and holding a focused owner Q&A before expensive implementation or verification. Use at the beginning of every new task or materially changed objective. Scale the process to the task; fully specified small work needs no questionnaire. Prevent repeated mistakes, speculative redesign and avoidable rework.
---

# Start

Establish the right outcome before spending time producing the wrong one.
Apply this skill to new work. Continue existing work from its recorded decisions;
repeat only the affected steps when scope, evidence or constraints change.

## 1. Orient

- Read applicable instructions, the current request, existing decisions and any
  relevant handoff or retrospective. Use current evidence to check facts that can drift.
- Preserve the complete objective. Separate a first delivery from eventual completion.
- Identify existing writers, unrelated changes and live jobs before touching shared work.
- Check existing authorisation. Do not ask again for an action already authorised.
- For a small, clear task, make these checks internally and proceed. Do not manufacture
  questions, a large plan, a team or a new tracker.

## 2. Investigate enough to expose the choices

- Find how the project already handles the concern. Inspect the relevant implementation,
  dependency, schema, fixture or operating procedure before proposing a replacement.
- Prefer proven framework and library capabilities, especially for security protocols.
- Discover actual paths, tool capabilities and current documentation. Do not guess APIs.
- Check prerequisites cheaply. Recheck a stale access or environment failure rather than
  carrying it forward as a permanent blocker.
- Bound research by the questions it must answer. If further investigation would merely
  infer an owner preference, move to Q&A instead of investigating indefinitely.

## 3. Hold the owner Q&A before committing to expensive work

For migrations, use `migrate` to check affected areas and `grilling` to resolve
consequential unknowns. Finish based on evidence and agreement, not a question
count. Reuse the same brief and prior answers.

After substantive investigation, give a short account of what exists, what can be reused
and which choices remain. Ask about decisions whose answers could change the outcome,
design or hours of implementation or verification, even when you could make a plausible guess.

Useful questions concern:

- Required behaviour, first delivery and the full completion criteria.
- Compatibility that must survive, and behaviour the owner is willing to remove.
- Migration, reauthentication, rollback and acceptable data-loss boundaries.
- Product defaults or architectural alternatives with materially different costs.
- What observable evidence will prove success, and which external actions are authorised.

Ask only unresolved questions relevant to this task. Use a short batch, normally one to
three questions per round; use another round only when an answer exposes a new decision.
For each choice, state the evidence, recommended option and practical consequences in
plain language. Explain what work the answer avoids. Do not ask the owner for facts you
can cheaply read from the code, or for routine reversible implementation choices.

Use the available question tool when appropriate. Keep dependent implementation and
costly verification pending until material answers arrive. Continue safe independent
work meanwhile. Silence or elapsed time is not an answer. Previously answered questions
need no repeat unless new evidence materially changes the choice.

## 4. Record the agreement once

Update the existing plan or decision record, if one is needed. Do not create duplicate
briefs or progress trackers. Capture:

- The intended outcome, first useful delivery and full remaining scope.
- What to reuse, remove or defer, including deliberate compatibility breaks.
- Owner answers, relevant constraints and any still-unanswered decision.
- Required behaviour and its acceptance evidence.
- The next implementation step, source ownership, prerequisites and actual release gates.

The latest explicit owner decision overrides an older draft. Ensure implementation,
tests and review instructions use that same decision. Do not encode abandoned behaviour
in tests simply because a legacy application or an old plan still contains it.

## 5. Implement and verify without repair loops

- Follow applicable test-first and quality requirements. Test observable behaviour.
- Use canonical fixtures and actual roles, constraints and permissions.
- Separate implementation prerequisites from acceptance and merge gates. Continue safe
  independent work on proved contracts while external gates run, when instructions allow.
- Before a costly check, identify the unresolved question it will settle. Use focused
  evidence first; run all required broader gates before claiming acceptance.
- Reuse valid unchanged images and results. Do not rerun a check already performed by
  preflight unless a change or unresolved question justifies it.
- Diagnose setup, compiler and helper failures before treating them as application failures.
  After two unsuccessful evidence-based fixes, stop guessing and inspect actual runtime
  behaviour, SQL, HTTP or persisted state. Seek stronger judgement where needed.
- Freeze the reviewed and tested candidate. Do not edit source during its verification.
  Refresh the integration base before costly final checks and recheck it before landing.
- Give reviewers the real change, relevant called helpers and contracts, including new
  files. Check findings against current code. Use coherent capability reviews and focused
  correction reviews rather than restarting every review for a tiny repair.
- Keep ownership disjoint. Preserve exact live-job handles; an observation timeout is
  not evidence that a job needs restarting. Activate idle agents only when delegation is
  authorised; this skill does not authorise a team or external sharing.

## 6. Make progress and retros useful

Report a delivered slice or meaningful blocker in plain language: what works, the evidence,
what remains, what blocks delivery and the next action. Distinguish local, reviewed,
published, accepted, merged and deployed work. Avoid invented percentages and ETAs.

Use retrospectives to prevent recurrence, not add ceremony. Leave unchanged or duplicate
scheduled findings quiet. Surface significant failures and owner decisions; never hide
them to make retros appear successful. Apply the smallest useful improvement and evaluate
whether repeated mistakes, setup failures and unnecessary waiting actually decrease.

Read [the collected findings](references/retro-findings.md) when a similar failure appears
or a task needs deeper preparation. Do not load the entire history for every small task.
This skill adds no recurring automation, permission or release bypass.
