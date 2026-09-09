# Codex Model Mapping

Use only model names and reasoning efforts advertised by the active runtime.
Revalidate metadata at routing decisions. Never infer global availability from
one task, account, or runtime. These roles are local routing preferences.

## Model Roles

- `gpt-5.6-luna`: clear, low-risk work with established patterns and objective
  checks. May own implementation, verification, and completion end to end.
- `gpt-5.6-sol`: everyday judgement, discovery, local design, difficult
  implementation, unclear diagnosis, and routine independent review.
- `gpt-6-astra`: exceptional ambiguity, complex architecture, consequential
  decisions, and high-blast-radius review. Allow direct routing or escalation
  from Sol when the work warrants it.
- `gpt-5.6-terra`: substitute for Sol under low limits. It has no normal
  middle-tier role. Escalate when the work exceeds its capability.

## Reasoning Effort

- Luna starts at `medium`; use `high` for sustained reasoning within clear,
  low-risk boundaries with objective checks.
- Sol and Astra start at `medium`. Increase one advertised level at a time
  only when evidence shows the current effort is insufficient.
- Terra starts at `medium` when substituting for Sol; use `high` when needed
  for difficult but bounded implementation or diagnosis.

If a preferred effort is unavailable, use the closest suitable advertised
effort and state the adjustment. Tune effort when the model fits the task;
change models when the nature of the judgement changes. Do not use higher
effort as a prestige setting.

## Usage Policy

Check usage before substantial work and at routing or handoff decisions using
the runtime's usage tool. Prefer applicable Codex buckets from
`rateLimitsByLimitId`; fall back to legacy `rateLimits` when applicable mapped
data is unavailable. Inspect all reported applicable windows, including
primary and secondary. Exclude unrelated model-specific buckets, such as a
Spark-only bucket when routing Luna, Sol, Astra, and Terra.

Compute remaining percent as `max(0, min(100, 100 - usedPercent))`. Missing or
null values are unknown, not zero. Any known applicable window with **less
than 10% remaining** triggers low-limit routing, even if another is unknown.

- Below 10%: Terra replaces Sol. Ask before selecting or escalating to Astra,
  including independent review and availability fallbacks.
- Exactly 10% or above in every reported applicable window: normal routing.
  Restore it at the next routing decision after limits recover.
- No known low window and missing usage data: retain normal routing and
  disclose the unavailable measurement. Do not invent a remaining percentage.

This is a conservation preference, not evidence of measured Terra savings or
separate model allowances. Do not consume usage-reset credits without explicit
user authorisation.

## Practical Routing Sequence

```text
Clear + low risk + objective checks
    -> Luna medium/high: own, implement, verify, finish

Everyday judgement, discovery, local design, or difficult implementation
    -> Sol medium: clarify, implement, review, or return work to Luna
    -> Terra medium/high instead when any applicable window is below 10%

Exceptional ambiguity, complex architecture, or consequential decisions
    -> Astra medium: route directly or escalate from Sol
    -> Ask before selecting Astra when any applicable window is below 10%
```

No tier is required at both ends of every task. Review follows consequence and
uncertainty; Luna does not require a stronger reviewer solely because it is
Luna. Increase effort or escalate when evidence warrants it, and return work
to Luna when the remaining scope is clear and objectively testable.

## Availability Fallback

- If Luna is unavailable, use Sol, or Terra under low limits, at a suitable
  advertised effort.
- If Sol is unavailable under normal limits, Terra may handle work within its
  capability as an availability fallback. Use Astra when the task needs it.
- If Terra is unavailable or insufficient under low limits, use Sol only if
  available and capable, and disclose that the conservation preference could
  not be followed. If Astra is needed, ask before selecting it.
- If Astra is unavailable, use Sol only when it can reliably own the work
  (Terra under low limits). Otherwise explain the capability gap and seek a
  scope or availability decision; do not silently lower the required standard.
- If no suitable model is available, report the limitation. Keep scope,
  permissions, and acceptance criteria unchanged through every fallback.

## Routing Walkthroughs

| Situation | Route |
| --- | --- |
| Clear, low-risk work with objective checks | Luna medium/high |
| Local design; 40% remains | Sol medium |
| Complex architecture; 40% remains | Astra medium, directly if warranted |
| Local design; exactly 10% remains | Sol medium |
| Local design; 9.9% remains | Terra medium |
| Consequential decision; 9.9% remains | Ask before Astra |
| Applicable windows show 50% and 9% | Low-limit routing |
| Codex shows 50%; unrelated Spark bucket shows 1% | Normal routing |
| One window at 9%; another unknown | Low limits; disclose missing data |
| All applicable usage is unavailable | Normal routing; disclose missing data |
| Limits recover from 9% to 10% | Restore normal routing at next decision |
| Terra unavailable; low limits | Suitable Sol; disclose, or ask before Astra |
| Astra unavailable; Sol insufficient | Explain gap; seek a decision |

## Runtime Reference

Codex exposes model metadata, including supported reasoning efforts. Use the
active runtime's advertised options rather than a fixed global model list.
The role assignments and 10% threshold above are user preferences.

- [Codex model metadata API](https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md)
