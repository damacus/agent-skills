# Codex Model Mapping

Use this reference for Codex model names and reasoning efforts available in the
active runtime. Revalidate tool metadata when models or effort levels change.
Never infer global availability from one task, spawn result, account, or
runtime.

## Model Roles

- `gpt-5.6-luna` is the fastest and most affordable owner. Use it for clear,
  low-risk work, established patterns, bounded implementation, test expansion,
  and routine repository work.
- `gpt-5.6-terra` is the balanced everyday judgment tier. Use it for unfamiliar
  code, local design choices, nontrivial refactors, exploratory diagnosis, and
  routine independent review.
- `gpt-5.6-sol` is the frontier judgment tier. Use it for broad architecture,
  consequential ambiguity, sensitive decisions, and high-blast-radius review.

## Reasoning Effort

Use only effort levels advertised for the selected model by the active runtime.
OpenAI recommends `medium` as a balanced starting point and `low` for
latency-sensitive workloads. This skill uses these practical defaults:

- Luna `medium` for clear, low-risk, objectively testable work.
- Luna `high` for sustained reasoning within clear boundaries.
- Terra `medium` for local judgment, discovery, or unclear diagnosis.
- Terra `high` for difficult but bounded implementation or diagnosis.
- Sol `medium` for frontier judgment, consequential ambiguity, or high risk.
- Increase Sol one level when evidence shows current effort is insufficient.

Tune effort before changing tiers when the model is appropriate but needs more
or less thinking. Change tiers when the nature of the judgment changes. Do not
use `high`, `xhigh`, `max`, or `ultra` as prestige settings.

## Practical Routing Sequence

```text
Clear + low risk + objective checks
    `-- Luna medium/high: own, implement, verify, finish

Local judgment, discovery, or ambiguous failure
    `-- Terra medium/high: clarify, implement, review, or return work to Luna

Consequential ambiguity, broad architecture, or high risk
    `-- Sol medium: judge first; increase effort only with evidence
```

No tier is required at both ends of every task. Add review for risk,
uncertainty, or integration needs, not because a lower-cost model did the work.

## Availability Fallback

If Luna is not advertised, use Terra at the closest suitable advertised
effort. If Terra is not advertised or the task exceeds it, use Sol. Keep the
same scope, permissions, and acceptance criteria when changing models. State
only that the preferred model is unavailable in the active runtime; do not
claim it is globally unavailable.

## OpenAI Guidance

OpenAI describes Luna as the fastest and most cost-efficient tier, Terra as the
balance of intelligence and cost for everyday work, and Sol as the
frontier-capability tier. OpenAI recommends choosing by workload rather than
defaulting to the most capable model, starting reasoning at `medium` for
balance, and testing lower effort where latency matters.

- [Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [GPT-5.6 announcement](https://openai.com/index/gpt-5-6/)
