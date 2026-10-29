---
name: adaptive-model-routing
description: >-
  Choose and revise Codex model and reasoning effort for engineering work. Use
  when deciding between the Luna, Sol, and Astra families; balancing quality, cost, and
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

Read [references/codex-models.md](references/codex-models.md) for runtime family
resolution, exclusions, effort handling and fallbacks. Resolve the latest
permitted stable model in the chosen family from the target runtime metadata
at each decision; use the checked `scripts/resolve_model.py` helper. Family
labels are not API aliases. Every Terra model and Sol 6.0 are excluded from
normal routing, fallbacks, inherited defaults and reuse of existing agents.
Never send new work to an excluded model, even if it is advertised or cached
in an old instruction. Do not invent a latest alias or fall back to a remembered
ID. An unresolved or ambiguous inventory blocks model selection.

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

- Use **latest permitted Luna** for clear, low-risk work with established
  patterns and objective checks. This includes substantial implementation when
  the work remains well specified and correctness is cheap to verify.
- Use **latest permitted Sol** for everyday engineering judgement: discovery,
  unfamiliar code, local design, difficult implementation, ambiguous
  diagnosis, and routine independent review. It is the value choice when
  Luna's likely retries or review burden would erase its price advantage.
- Use **latest permitted Astra** for exceptional ambiguity, complex
  architecture, consequential decisions, or high-blast-radius review where its
  additional capability is needed to protect quality. Route directly when
  warranted; do not require a cheaper model to fail first.

Luna may own suitable work end to end without a mandatory Sol framing pass or
stronger-model review. Sol can own difficult work without an automatic Astra
handoff. Reserve Astra for a concrete capability need, not routine ceremony.

### Resolve Before Dispatch

Obtain the target tool and host model inventory, resolve the chosen family and
preflight the exact intended ID with `scripts/resolve_model.py --check-model`.
This check also applies before inheriting a parent model or reusing a child.
If the parent is not the resolved latest permitted model, select the exact
resolved ID through the supported tool instead of inheriting. Follow tool fork
constraints. Never treat a policy family name as a real API identifier.

Recheck on later routing decisions; a new advertised stable minor or major
release replaces the previous family version without editing this skill.
Do not reuse dated model IDs, default efforts, prices or benchmark conclusions.
If a running or cached agent uses an excluded model, do not dispatch further
work to it. Change or replace it only within existing task/delegation authority.

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
Use current-version price/performance evidence as an initial
estimate, then judge the actual result. Prefer one advertised effort step at
a time; skip steps when the risk or evidence already warrants it. Do not
exhaust every effort level or default to `max` because a chart used it.

### Service Tier: Normal by Default

Use the normal/default service tier for every model, especially Astra. Model
choice and reasoning effort do not authorise Fast mode. Priority/Fast requires
explicit user approval for the specific work; urgency, a prior Fast session or
an inherited setting is not approval. Do not enable it as a fallback.

Never inherit the caller's speed or service tier. Fast approval for a caller
does not extend to a child agent, reviewer, handoff or reused agent unless the
user explicitly includes that work. For example, a Sol 6.1 caller using Fast
must dispatch an Astra agent on normal/default service unless the user
explicitly requests Fast for that Astra work.

Before dispatch or reuse, inspect the effective tier separately from model and
effort. Select normal/default through the supported mechanism and verify the
recorded setting after dispatch. Do not omit the tier when omission inherits
the caller's speed; explicitly select normal/default instead. A config change
does not retrofit running sessions. If a tool only permits priority or cannot
establish a normal tier,
report that limitation and do not silently start paid-priority work.

Keep session and parent IDs, agent name/path, model, reasoning effort and tier
changes with timestamps in the existing usage record. Use recorded
thread_settings_applied evidence where available; missing tier evidence stays
unknown rather than being inferred from today's global config. Track token
deltas with cached and uncached input separately; cached input is part of input
and reasoning tokens are part of output. Settings and token counts do not prove
actual charges or allowance consumption. Do not sum cumulative snapshots.

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
- Reintroducing Terra or Sol 6.0 through a fallback, inheritance or cached agent.
- Pinning a family role to an old model ID or inventing a latest API alias.
- Inheriting Fast from the caller or extending its Fast approval to other agents.
- Treating missing usage as zero or exactly 10% remaining as low.
- Selecting Astra below 10% without approval, or inferring quota savings from
  API prices.
- Creating agents for overlapping or inherently serial work.

## Completion Check

- Did runtime discovery and the resolver verify the exact latest permitted ID?
- Were Terra, Sol 6.0 and obsolete inherited model choices excluded?
- Did the route meet the same quality and verification requirements?
- Did model choice reflect uncertainty, consequence, and total completion cost?
- Was normal service used, with explicit approval and verified settings for any
  Fast/priority exception covering that agent's specific work, without inheriting
  the caller's speed?
- Were reasoning defaults preserved unless evidence justified an override?
- Did effort changes address a specific problem rather than follow a fixed ladder?
- Were usage, missing data, availability, and Astra approval handled correctly?
- Was review proportionate to risk, with unnecessary handoffs avoided?
- Did new evidence trigger escalation or a worthwhile return to a cheaper model?
