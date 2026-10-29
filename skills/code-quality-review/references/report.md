# Report contract

Lead with the verified engineering conclusion and highest-impact findings. Use
plain UK English. Include the following evidence; do not fill unknowns with guesses.

## Run and completeness

- Source root/project scope, commit, branch, timestamp, dirty-source manifest,
  exclusions and any submodule/LFS limitations.
- Profile and effective overrides; read-only/remediation mode and its authority.
- Completion of mechanical scan, every subjective batch/dimension, independent
  architecture, native comparison, source verification and conditional challenge.
- Runtime inventory timestamp/tool; role, requested and observed model/effort/tier,
  agent/session ID and evidence. Report unavailable/unknown roles explicitly.
- Source commit/status before and after; snapshot identity and artifact location.

## Scores and coverage

| Stage | Overall | Objective | Strict | Subjective/dimensions | Trust/staleness | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Existing baseline, if any | | | | | | |
| First mechanical scan | | | | | | |
| After full subjective review | | | | | | |

State version, scope and configuration differences before comparing scores.
Missing or unavailable is not zero. A score change after adding a review is not
evidence of an application improvement. Attach batch/dimension coverage and list
detectors/checks that failed, were unsupported or were not run.

## Findings and native tools

| ID | Claim and impact | Source file:line and path/trigger | Native rule/check and result | Verdict/confidence | Smallest useful action |
| --- | --- | --- | --- | --- | --- |

Use stable run-local IDs, link raw tool IDs, and deduplicate overlapping symptoms.
Verdicts: confirmed, false positive, accepted trade-off, unverified, disputed or
resolved disagreement. Distinguish severity from confidence. Prioritise actual
impact and remediation cost, not the contribution to a score. Include each native
command's version/configuration, exit status, scope and saved evidence.

## Independent assessment and disagreements

Link the frozen initial architect report and give findings on architecture,
abstractions, error handling and maintainability. Explain independent agreement
and additional findings. Keep a false-positive ledger with evidence and rationale.
For disagreements, record both positions, source counterevidence, challenge trigger
and outcome (or why no challenge was needed). Preserve unresolved dissent.

## Limits and next actions

List unverified candidates, incomplete subjective batches, missing tools/settings,
unsafe or unauthorised checks and any contaminated context. State what would
resolve each material uncertainty. Recommend a small ordered set of actions; do
not apply them in review mode. Link raw logs, immutable baselines and coverage.
