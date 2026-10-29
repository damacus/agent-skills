# Runtime Model Families

Resolve roles against the model inventory advertised by the actual target tool
and host at each routing decision. Family names below are policy labels, not
API model identifiers. Never send an invented `sol-latest` or similar alias.

| Family role | Use when |
| --- | --- |
| Latest permitted Luna | Clear, low-risk work with objective checks |
| Latest permitted Sol | Discovery, design, implementation and diagnosis |
| Latest permitted Astra | Exceptional ambiguity, architecture or consequence |

## Excluded Models

- **Every Terra model**, regardless of generation, alias or availability.
- **Sol 6.0**, including `gpt-6-sol`, `gpt-6.0-sol` and any alias or pinned
  release whose underlying model is Sol 6.0.
- Models labelled retired, deprecated, legacy, previous-generation or older.
- Preview, experimental and beta releases are excluded by this stable-family
  resolver.

These exclusions apply to normal routing, low-limit routing, reviews,
fallbacks, inherited defaults and reuse of existing agents. Availability does
not make an excluded model eligible. Never use an unverified alias to bypass
the exclusions. If no permitted model can meet the task's quality requirement,
report the routing blocker instead of silently selecting an older model.

## Resolve the Latest Permitted Release

1. Read the target tool's current advertised model IDs, descriptions, release
   status, versions, availability and supported/default reasoning efforts.
   Do not use this document, a previous session, an old benchmark or another
   host's inventory as a model registry.
2. Filter out excluded and unavailable candidates. Retain the requested family.
3. Prefer the newest stable generation/version within that family. Compare
   version components numerically, never model strings lexicographically.
   A later supported stable minor or major release replaces its predecessor
   automatically; no change to this skill is required.
4. Treat contradictory latest/version metadata or indistinguishable versions
   as ambiguous. Resolve that metadata before selecting; do not guess a model ID.
5. Pass the exact permitted ID returned by the resolver to the tool. A runtime
   alias is usable only when its concrete target is advertised and verified;
   prefer that concrete target so the exclusion check is explicit.

The deterministic helper accepts a JSON inventory on stdin:

```text
python3 scripts/resolve_model.py --family sol
```

Its input is `{"models": [...]}`. Each entry requires an advertised `id` and
may include `description`, `status`, `available`, `is_latest`,
`default_reasoning_effort` and `supported_reasoning_efforts`. Copy these fields
from current runtime metadata; do not invent availability, versions or defaults.
The helper supports canonical numeric GPT family IDs. Other naming schemes
require verified canonical metadata and a resolver update, not an assumed match.

Before using an explicit or inherited ID, check it against the same inventory:

```text
python3 scripts/resolve_model.py --check-model ACTUAL_ADVERTISED_MODEL_ID
```

The helper rejects excluded IDs and permitted-but-outdated versions. It returns
no replacement model on failure. It does not invoke models, alter account
limits, consume resets or change any running agent.

If model discovery is unavailable, report that latest resolution is unverified.
Do not silently fall back to a remembered identifier or to inheritance from an
unverified parent. Continue independent authorised work where possible.

## Reasoning Defaults and Tool Semantics

Use the selected permitted model's current advertised default unless the owner
chooses otherwise or evidence warrants an adjustment. Do not retain a dated
snapshot of model defaults in this skill. Missing effort metadata is unknown.

- Some tools inherit both the parent's model and effort when omitted. Omit
  model only after verifying that the parent is the resolved latest permitted
  model for the chosen role. Verify the effort separately.
- When selecting a different model, follow the tool's fork constraints and
  pass the resolved exact ID. Use its advertised default effort if omission
  would inherit an unrelated value.
- Existing agents retain their selected model. Check before reusing them;
  do not send new work to an excluded or superseded model. A permitted switch
  or replacement requires the normal task/delegation authority.
- If the tool cannot switch a model and replacement is not authorised, report
  the limitation. Updating this skill does not retrofit running agents.

## Value, Usage and Fallbacks

Optimise the total cost of a verified result while preserving quality. Model
family roles guide initial judgement; actual current-version evidence should
inform cost/performance comparisons. Do not transfer a predecessor's pricing,
benchmarks or default effort to its successor. Consult current primary sources
when a routing choice depends on those figures.

Apply the main skill's usage policy to every model decision. Below 10% in any
applicable allowance window, conserve usage and ask before Astra. Exactly 10%
uses normal routing; missing usage is unknown. API prices do not establish
Codex allowance consumption or separate model allowances.

- Luna unavailable: use latest permitted Sol when suitable; Astra only when
  required or the only suitable family, subject to the low-limit approval rule.
- Sol unavailable: use latest permitted Luna only when quality remains adequate;
  otherwise use latest permitted Astra, subject to the same approval rule.
- Astra unavailable: use latest permitted Sol only when it can reliably meet
  the requirement. Otherwise explain the capability gap.
- No suitable permitted model: report the blocker. Exclusions stay in force.

Changing family, effort or ownership does not itself authorise delegation,
external messages, another task, or a change to running sessions.

## Service Tier Evidence

Normal service is the default for every family, especially Astra. Select the
recorded `default` tier; `priority` means Fast and requires explicit approval for
the specific work. Inspect tool capabilities before dispatch. A priority-only
tool cannot satisfy normal routing; do not launch an agent through it silently.
Verify `thread_settings_applied.thread_settings.service_tier` after dispatch.
Missing settings remain unknown. Global `service_tier = "default"` is a new-session
default and cannot prove or change an existing session tier.
