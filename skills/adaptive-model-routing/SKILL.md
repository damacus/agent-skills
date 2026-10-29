---
name: adaptive-model-routing
description: >-
  Choose and revise Codex model and reasoning effort for engineering work. Use
  when deciding between GPT-6 Luna, Sol, and Astra; balancing quality, cost, and
  latency; assigning end-to-end work or bounded subtasks; planning a model
  handoff; or escalating after uncertainty, risk, or failed attempts increase.
  Apply at the start of substantial work and whenever its shape changes.
---

# Adaptive Model Routing

Choose the least expensive route that can meet the required quality reliably.
Optimise the cost of a verified result, including retries, latency, briefing,
review, and rework. Keep acceptance criteria and verification intact when
changing models.

This skill governs model choice and handoffs. It does not broaden the user's
authorisation, permit unrequested external actions, or override repository
instructions. A suitable model may own implementation, verification, and the
final report end to end.

Read [references/codex-models.md](references/codex-models.md) for GPT-6 model
identifiers, price/performance evidence, effort handling, and fallbacks. Use
only models and efforts advertised by the active runtime. Terra is retired
from this routing policy, including low-limit and availability fallbacks.

## Core Workflow

### 1. Judge the Work Shape

Before choosing a model, establish:

- How clear are the objective, scope, repository rules, and acceptance criteria?
- How much discovery or design judgement remains?
- What happens if the model makes a plausible but wrong choice?
- Are failures cheap, objective, and reversible? Can checks localise them?
- Does the work involve security, permissions, money, destructive operations,
  concurrency, public contracts, deployments, or irreversible data?

Route from uncertainty, consequence, and verification quality. File count or
task length alone does not justify a stronger model or higher effort.

### 2. Choose the Initial Route

- Use **GPT-6 Luna** for clear, low-risk work with established patterns and
  objective checks. This includes substantial implementation when the work
  remains well specified and correctness is cheap to verify.
- Use **GPT-6 Sol** for everyday engineering judgement: discovery, unfamiliar
  code, local design, difficult implementation, ambiguous diagnosis, and
  routine independent review. It is the value choice when Luna's likely
  retries or review burden would erase its price advantage.
- Use **GPT-6 Astra** for exceptional ambiguity, complex architecture,
  consequential decisions, or high-blast-radius review where its additional
  capability is needed to protect quality. Route directly when warranted;
  do not require a cheaper model to fail first.

Luna may own suitable work end to end without a mandatory Sol framing pass or
stronger-model review. Sol can own difficult work without an automatic Astra
handoff. Reserve Astra for a concrete capability need, not routine ceremony.

### 3. Keep Default Reasoning Unless Evidence Justifies a Change

Start with the selected model's advertised default reasoning effort. Preserve
an explicit user choice. Do not hard-code `medium`, infer defaults from a
benchmark, or inherit an unrelated model's effort accidentally.

Leave effort unset only when the tool documents that omission uses the selected
model's default. Some tools inherit the parent's effort or keep the task's
existing setting; inspect those semantics before choosing arguments. If an
explicit value is required, use the advertised default. If none is exposed,
retain a known supported setting and disclose the uncertainty.

Change effort only for a concrete reason:

- Increase it when the model understands the task but needs more reasoning to
  finish a bounded problem, or representative results justify the increase.
- Lower it when the remaining work is simple and objective checks support the
  same quality with less latency or cost.
- Change models when missing judgement or capability is the issue. Extra
  thinking is not a substitute for the capability the work requires.

Compare a modest effort increase with moving up a model before escalating.
Use relevant price/performance evidence from the reference as an initial
estimate, then judge the actual result. Prefer one advertised effort step at
a time; skip steps when the risk or evidence already warrants it. Do not
exhaust every effort level or default to `max` because a chart used it.

### Usage Policy

Check usage before substantial work and at routing or handoff decisions. Use
applicable Codex buckets in `rateLimitsByLimitId`; fall back to legacy
`rateLimits` when applicable mapped data is unavailable. Inspect all reported
applicable windows and exclude unrelated model-specific buckets. Remaining
percent is `max(0, min(100, 100 - usedPercent))`.

- Below **10% remaining** in any known applicable window, conserve usage:
  prefer Luna wherever it can meet the same quality standard, retain Sol when
  its judgement is needed, and avoid unnecessary agents and repeated reviews.
  Ask before selecting Astra, including for review or availability fallback.
- At exactly 10% or above in every reported applicable window, use normal
  routing. Restore it at the next routing decision after recovery.
- Missing or null usage means unknown, not zero. Disclose missing measurements.
  Retain normal routing if no known window is low; a known low window still
  triggers conservation when another is unknown.

Never downgrade below the task's quality requirement to save quota. API prices
do not establish Codex allowance consumption or separate model allowances.
Do not consume usage-reset credits without explicit user authorisation.

### 4. Keep Ownership and Review Proportionate

Every owner needs the objective, repository rules, owned scope, prohibited
actions, acceptance criteria, project-native checks, and escalation conditions.
These can come directly from the request and repository; a stronger model does
not need to manufacture a formal handoff for clear work.

Delegate only when authorised and when parallelism or context isolation saves
more than briefing and integration cost. Keep tiny, serial, or tightly coupled
work with the active owner. Assign non-overlapping ownership and retain
responsibility for integration. Delegation does not require a Sol parent.

Independent review follows consequence and uncertainty, not model identity:

- Luna can verify and complete low-risk work without stronger-model review.
- Sol is suitable for a second pass on unfamiliar implementation or local design.
- Astra is appropriate for complex architecture, security, destructive changes,
  sensitive decisions, or compatibility review with a high blast radius.
  Ask before selecting it under low limits.
- Inspect diffs and verification evidence directly. Confidence is not proof.

### 5. Reassess and Escalate

Reassess the model, effort, or need for review when:

- Scope or acceptance criteria change, or repository behaviour contradicts
  the working explanation.
- A public API, schema, migration, permission, or compatibility decision appears.
- Verification is subjective, missing, expensive, or cannot localise failure.
- The same failure survives two evidence-based attempts, or the owner is
  guessing at hidden state and cannot explain the failure.
- Authentication, authorisation, secrets, financial correctness, concurrency,
  destructive operations, deployment control, or irreversible data is involved.
- Integration reveals conflicting edits or a cross-task architectural decision.

Usually move Luna to Sol, Sol to Astra, or adjust effort within the current
model. Identify what the change should resolve and verify that it did. Do not
repeat identical attempts. Ask before Astra under low limits. Return clarified,
objectively testable work to a cheaper model when the saving exceeds handoff
cost. Keep the current owner when switching would add more overhead than value.

## Owner Contract

- Preserve user and repository constraints and unrelated work.
- Inspect current state instead of trusting a stale handoff.
- Run proportionate project-native verification without weakening its standard.
- Report changed files, checks, evidence, and unresolved risks accurately.
- Escalate newly exposed high-impact decisions instead of guessing.

## Anti-Patterns

- Selecting Astra for every substantial task or treating Luna as mechanical-only.
- Keeping a cheaper model after its retries erase the saving or threaten quality.
- Raising effort because of file count, model prestige, or benchmark settings.
- Treating every model's default as `medium` without checking the runtime.
- Requiring a stronger model at both ends of every Luna task.
- Reintroducing Terra as a quota or availability fallback.
- Treating missing usage as zero or exactly 10% remaining as low.
- Selecting Astra below 10% without approval, or inferring quota savings from
  API prices.
- Creating agents for overlapping or inherently serial work.

## Completion Check

- Did the route meet the same quality and verification requirements?
- Did model choice reflect uncertainty, consequence, and total completion cost?
- Were reasoning defaults preserved unless evidence justified an override?
- Did effort changes address a specific problem rather than follow a fixed ladder?
- Were usage, missing data, availability, and Astra approval handled correctly?
- Was review proportionate to risk, with unnecessary handoffs avoided?
- Did new evidence trigger escalation or a worthwhile return to a cheaper model?
