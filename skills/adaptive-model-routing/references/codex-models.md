# Codex Model Mapping

Use only models and reasoning efforts advertised by the active runtime.
Revalidate metadata at routing decisions. Availability in one task or account
does not establish global availability. Roles below are local routing policy.

## GPT-6 Roles

| Model identifier | Use when |
| --- | --- |
| `gpt-6-luna` | Clear, low-risk work with objective checks |
| `gpt-6-sol` | Discovery, design, difficult implementation, or diagnosis |
| `gpt-6-astra` | Exceptional ambiguity, architecture, or consequence |

Terra has no role in this policy, including under low limits. Do not silently
substitute GPT-5.6 identifiers for GPT-6.

## Price and Performance Evidence

Source: OpenAI's [GPT-6 Sol and Luna announcement][announcement], checked
22 September 2026. These are published evaluation points, not measurements of
this user's repositories or Codex quota consumption.

| GPT-6 model | Input per million tokens | Output per million tokens |
| --- | ---: | ---: |
| Luna | $0.10 | $0.50 |
| Sol | $2 | $10 |

Sol's input and output rates are half its GPT-5.6 rates. At equal token counts,
Luna costs one twentieth as much as Sol. Actual completion costs depend on
token use, caching, reasoning, retries, tools, and review.

Selected points from the announcement's price/performance comparisons:

| Evaluation | Published result |
| --- | --- |
| AutomationBench: Sol `xhigh` | 33.2%, $0.27/task |
| AutomationBench: Astra `low` | 30.3%, 3.9 times Sol's cost |
| DeepSWE 1.1 | Sol `max`: 68.8%; Luna `max`: 66.6% |

These results support considering higher-effort Sol before lower-effort Astra,
and keeping Luna eligible for substantial coding. They do not establish that
Sol always beats Astra or that Luna matches Sol on every task. Different
benchmarks, tools, and effort settings are not interchangeable.

[announcement]: https://openai.com/index/introducing-gpt-6-sol-and-luna/

## How to Use the Cost/Performance Curve

Treat the published curve as an initial estimate. Select a candidate that can
meet the task's quality requirement, then choose the lowest expected total
cost among suitable candidates. Do not maximise score per dollar by accepting
a result below that requirement.

- Use Luna when objective verification makes it a reliable owner.
- Use Sol when its judgement avoids likely retries, rework, or extra review.
- Compare more effort on a suitable model with a stronger model at its default.
  The AutomationBench comparison makes this worthwhile; it is not a universal
  crossover threshold for coding or other work.
- Use Astra directly when the consequence or ambiguity requires it.
- For repeated workloads, compare representative completions using the same
  acceptance checks. Include failures, retries, latency, and review costs.
  Do not create a benchmark project for a one-off routing choice.

## Reasoning Defaults and Tool Semantics

Use the selected model's advertised default unless a user choice or concrete
task evidence justifies an override. Do not infer defaults from the effort
used in published evaluations.

Runtime snapshot on 22 September 2026: the sub-agent tool advertises `medium`
as the default for all three GPT-6 models. Luna supports `low`, `medium`,
`high`, `xhigh`, and `max`; Sol and Astra additionally support `ultra`.
This snapshot is not a permanent default or a global API support claim.

Check the actual tool before setting or omitting effort:

- The sub-agent tool can inherit parent model and effort when omitted. If an
  authorised delegation needs a different model, follow its fork constraints
  and explicitly select the advertised default effort when inheritance would
  carry over an inappropriate setting.
- Existing-task tools may keep current settings on omission. Preserve an
  explicit user choice; do not describe retained effort as a model default.
- If the tool uses the selected model's default on omission, omit effort.
- If a required default is unknown, retain a known supported setting, state
  the uncertainty, and avoid inventing metadata.

A routing recommendation does not itself change the running model. Use a
supported selection mechanism only within the user's authorised workflow.
Do not create another task solely to enact a routing recommendation.

## Usage and Availability

Apply the main skill's usage policy to direct selection, delegation, review,
and fallback. Below 10% in any known applicable Codex window, prefer Luna only
where quality remains adequate, retain Sol where needed, and ask before Astra.
Exactly 10% is normal routing; missing values are unknown. API pricing does
not prove separate allowances or measured Codex usage savings.

- Luna unavailable: use Sol if suitable; Astra only if needed or the only
  suitable option, subject to the low-limit approval rule.
- Sol unavailable: use Luna only if the actual work remains within its
  capability; otherwise use Astra, subject to the same approval rule.
- Astra unavailable: use Sol only if it can reliably meet the requirement.
  Otherwise explain the capability gap and seek a scope or availability decision.
- No suitable model: report the limitation. Keep permissions, scope, and
  acceptance criteria unchanged through every fallback.

## Routing Walkthroughs

| Situation | Route |
| --- | --- |
| Clear multi-file change with objective checks | Luna, default effort |
| Unfamiliar code and local design | Sol at its advertised default |
| Sol fits but needs more reasoning | Consider one effort step before Astra |
| Consequential ambiguity; weak verification | Astra directly when warranted |
| Local design; exactly 10% remains | Sol, normal routing |
| Local design; 9.9% remains | Keep Sol if Luna cannot meet required quality |
| Clear task; 9.9% remains | Luna; avoid redundant agents and reviews |
| Astra needed; 9.9% remains | Ask before selecting Astra |
| Applicable windows show 50% and 9% | Conserve usage; ask before Astra |
| Codex shows 50%; unrelated bucket shows 1% | Normal routing |
| One window at 9%; another unknown | Conserve usage; disclose missing data |
| All applicable usage unavailable | Normal routing; disclose unknown usage |
| Limits recover from 9% to 10% | Restore normal routing at next decision |
| Astra unavailable; Sol insufficient | Report gap; preserve required quality |
