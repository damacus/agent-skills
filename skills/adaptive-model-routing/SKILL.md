---
name: adaptive-model-routing
description: >-
  Choose and revise Codex model and reasoning effort for engineering work. Use
  when deciding between Sol, Terra, and Luna; balancing judgment, cost, and
  latency; assigning end-to-end work or bounded subtasks; planning a model
  handoff; or escalating after uncertainty, risk, or failed attempts increase.
  Apply at the start of substantial work and whenever its shape changes.
---

# Adaptive Model Routing

Choose the fastest, most affordable model that can own the work reliably. Route
from uncertainty, blast radius, and verification quality rather than task size
or model prestige. Reassess when the work changes shape; escalation is
evidence-based, not automatic.

This skill governs model choice and handoffs. It does not broaden the user's
authorization, permit unrequested external actions, or override repository
instructions. A model may own a suitable task end to end, including
implementation, verification, and the final report.

Read [references/codex-models.md](references/codex-models.md) for the current
Codex-specific model and reasoning-effort mapping. Use only models and efforts
advertised by the active runtime. If a preferred model is unavailable, use the
next suitable available tier without making a global availability claim.

## Core Workflow

### 1. Judge the Work Shape

Before choosing a model, establish:

- How clear are the objective, scope, repository rules, and acceptance
  criteria?
- How much local design or discovery remains?
- What is the blast radius if the model makes a plausible but wrong choice?
- Are failures cheap, objective, and reversible?
- Does the work touch security, permissions, money, destructive operations,
  concurrency, public contracts, deployments, or irreversible data?

Do not start every substantial task with Sol. A clear task should not pay a
frontier-model tax just because it spans several files. Complexity by volume is
not complexity by judgment.

### 2. Choose the Initial Route

- Use Luna `medium` for clear, low-risk work with established patterns and
  objective checks.
- Use Luna `high` when the same conditions apply but implementation requires
  sustained reasoning or is substantially larger.
- Use Terra `medium` for some discovery, unfamiliar code, local design
  judgment, or unclear failure diagnosis.
- Use Terra `high` for difficult but bounded implementation, refactoring, or
  hypothesis-led debugging.
- Use Sol `medium` for broad architecture, consequential ambiguity, high blast
  radius, or sensitive decisions.
- Increase Sol one effort level at a time when evidence shows that `medium` is
  insufficient.

Luna may own suitable work end to end. It does not require a Sol framing pass
or a Terra or Sol review merely because it is Luna. Multi-file work may remain
with Luna when the pattern and checks are clear. Prefer Luna aggressively when
correctness is cheap to verify.

Terra is the everyday judgment tier. Start there when the task cannot yet be
reduced to mechanical or tightly specified execution. Escalate Luna to Terra
when implementation exposes meaningful design choices, unfamiliar behavior,
or ambiguous failures.

Sol is for frontier judgment, not routine ceremony. When the task genuinely
routes to Sol, start at `medium` and increase effort only when the evidence
warrants it.

### 3. Keep Ownership Proportionate

An end-to-end owner must have:

1. The objective and user-visible outcome.
2. Relevant repository rules, owned scope, and actions that are out of scope.
3. Acceptance criteria and project-native verification.
4. Known risks and escalation conditions.

This can be established directly from the request and repository. Do not
require a stronger model to manufacture a formal judgment packet when the work
is already clear.

Use delegation only when parallelism or context isolation saves more time or
cost than briefing and review add. Keep tiny, tightly coupled, or inherently
serial work with the active owner.

### 4. Review by Risk

Independent review is driven by consequence and uncertainty, not model
identity.

- A Luna owner may run the checks and complete a low-risk task without
  mandatory Terra or Sol review.
- Use Terra for routine independent review when local judgment or unfamiliar
  implementation makes a second pass worthwhile.
- Use Sol for architecture, security, compatibility, destructive changes,
  sensitive decisions, or whole-branch review with a high blast radius.
- Inspect diffs and evidence directly whenever review is required; confidence
  statements are not verification.

Never add a stronger reviewer solely to compensate for choosing Luna. If every
Luna task needs Sol at both ends, the route has lost its speed and cost
advantage.

### 5. Escalate Dynamically

Move up a tier, increase effort, or request review when:

- The task broadens beyond its established scope or acceptance criteria.
- Repository behavior contradicts the working model.
- A public API, schema, migration, permission, or compatibility decision
  appears.
- Verification is subjective, missing, expensive, or cannot localize failure.
- The same failure survives two evidence-based attempts.
- The owner is guessing at hidden state or cannot explain the failure.
- The work touches authentication, authorization, secrets, destructive
  operations, financial correctness, concurrency, deployment control, or
  irreversible data changes.
- Integration exposes conflicting edits or a cross-task architectural
  decision.

Escalation normally means Luna to Terra, Terra to Sol, or one higher reasoning
level. Do not jump straight to maximum effort when a smaller increase addresses
the uncertainty. A stronger model may return the clarified task to Luna when
the remaining work becomes bounded and objectively testable.

## Owner and Worker Contract

Every owner must:

- Preserve the full user and repository constraints relevant to its scope.
- Preserve unrelated work and stay within authorized boundaries.
- Inspect current state rather than relying on a stale handoff.
- Run proportionate project-native verification.
- Report evidence, changed files, checks, and unresolved risks.
- Escalate instead of silently making a newly exposed high-impact decision.

When delegating, assign non-overlapping ownership and retain responsibility for
integration across workers. Delegation does not require the parent to be Sol.

## Anti-Patterns

- Starting every substantial task with Sol, even at `medium`.
- Starting Sol at `high` before evidence shows `medium` is insufficient.
- Treating Luna as mechanical-only when work is clear and objectively testable.
- Requiring Terra or Sol to review every Luna result regardless of risk.
- Choosing models solely by line count; a one-line authorization change can be
  high risk.
- Keeping Luna after ambiguity, design judgment, or sensitive decisions emerge.
- Using Terra merely because a change spans several files.
- Creating many agents for serial or overlapping work.
- Treating escalation as failure rather than the response to new evidence.

## Completion Check

- Was the initial model chosen from uncertainty, blast radius, and verification
  quality?
- Did clear, low-risk work avoid an unnecessary Sol or Terra tax?
- Was Luna allowed to own suitable substantial work end to end?
- Did Terra take over when local judgment or unclear diagnosis emerged?
- If Sol was needed, did it start at `medium` and increase only with evidence?
- Was independent review proportionate to risk rather than model identity?
- Were escalation triggers acted on when the task changed shape?
- Did the route remain worthwhile after latency, cost, briefing, and review
  overhead?
