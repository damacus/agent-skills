# Reviewer briefs

Fill placeholders with observed run facts. Include source scope, repository rules,
prohibited actions, accepted output location and the actual role settings in each
brief. Do not include other reviewers' conclusions in blind briefs.

## Collector: Sol Low

Collect mechanical evidence from SOURCE_SNAPSHOT. Do not edit the original
repository. Run the verified `uvx` scan command, save logs, exit codes, versions,
detector coverage and immutable initial scores/state in ARTIFACTS. Inspect native
CI/task definitions and run the agreed safe check-only commands in the snapshot.
Record overlaps and missing detectors; do not infer subjective quality or propose
automated fixes. Preserve existing history separately. Return artifact paths and
failures without inventing clean results.
Use fish or Node built-ins for collection helpers; do not write Python scripts.
Preflight external detector executables and inspect native tool cache/build paths
before starting. A package download or inaccessible cache is a setup failure.

## Subjective reviewer: Sol High, fresh context

Review BATCH_PROMPT and BLIND_PACKET against SOURCE_SNAPSHOT. Follow their exact
rubric and output schema. Read relevant callers and tests beyond supplied seeds.
Assess all assigned dimensions. Do not read scan scores, mechanical conclusions,
old review state or other reviewers' reports. Do not execute repairs, suppress
findings or aim at score targets. Return code evidence, confidence, limitations
and the required structured payload; missing coverage must remain explicit.

## Independent architect: Astra Medium, fresh context

Assess SOURCE_ONLY_SNAPSHOT from product requirements and repository rules.
Do not read `.desloppify`, scan artifacts, review packets, baseline scores or other
reviewers' reports. Describe observed boundaries and dependencies, trace the
profile's required product journeys, and independently assess:

- Architecture: dependency direction, state ownership, lifecycle and real seams.
- Abstractions: benefits, duplication, coupling and needless indirection.
- Error handling: propagation, recovery, cancellation and user-visible failures.
- Maintainability: navigation, local reasoning, tests and cost of likely changes.

For each finding, give source locations, trigger/impact, confidence,
counterevidence and a proportionate alternative. Explain sound trade-offs and
unknowns too. Do not impose a named architecture or additional layers without a
demonstrated problem. Return an initial independent report; reconciliation with
tool findings happens only after this report has been saved and timestamped.

## Challenger: Sol XHigh, only for a qualifying dispute

Resolve DISPUTE using SOURCE_SNAPSHOT, both reviewers' strongest evidence and
COUNTERARGUMENTS. State the exact proposition, inspect implementation/callers/tests,
identify what would falsify it and conclude supported, rejected, narrowed or
unresolved. Explain severity separately from truth. Do not vote by reviewer model
or tool score. Offer the smallest useful remedy and preserve remaining uncertainty.

## Owner: Sol High

Own coverage, capability checks, baseline preservation, blind-context boundaries
and final reporting. Personally verify promoted findings against source and native
tool evidence. Reconcile independent reports only after their initial outputs are
frozen. Escalate qualifying disputes, disclose actual role settings and incomplete
work, and verify the target's commit/status remained unchanged. Keep review-only
authority separate from any later explicitly authorised remediation.
