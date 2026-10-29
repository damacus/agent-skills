# Findings collected from the MedTracker migration

Collected on 6 October 2026 from the main migration retrospective record and the
owner's corrections. These are workflow lessons, not instructions to resume that migration.
They reflect the available record through the 16:19 UTC checkpoint. Future findings are
not included automatically. Repeated entries are consolidated below.

## Decisions before work

- After a substantial investigation, hold an owner Q&A before implementation. The owner
  can quickly settle choices an LLM could guess but would take time to establish.
- Ask about choices whose implementation or verification would take hours. A short answer
  can eliminate an entire investigation, compatibility layer or repair cycle.
- Confirm first production scope separately from full eventual scope. A smaller first
  delivery does not erase the rest of the objective.
- Record conscious compatibility breaks. The owner chose to drop unsupported Rails
  credential compatibility and accept reauthentication rather than continue researching it.
- Use the latest explicit identity decision in tests and review packets. An obsolete
  password-recovery contract caused work against the wrong requirement.
- Establish rollback and data-loss expectations rather than infer them from legacy code.

## Reuse and actual contracts

- Reuse existing SeaORM transactions, locking, audit and synchronisation logic.
- Use maintained framework and security libraries instead of bespoke protocols.
- Inspect actual schema constraints, indexes, RLS, grants and fixtures before changing
  bootstrap or database roles. A real PostgreSQL 42P10 error concerned a partial email
  index; speculative permission changes would not have repaired that contract.
- Verify reviewer claims against retained policy and current code. Passing tests do not
  justify an unnecessary redesign or custom security implementation.
- Find canonical fixture identities, relationships and roles; names are not proof.

## Delivery and verification

- Eight planned sections became serial stopping points. Implement against locally proved
  dependencies where safe; hosted CI gates acceptance and merging.
- Use focused checks for a small repair, then required broad checks for a coherent frozen
  candidate. Do not run a full application suite for every tooling or report edit.
- Do not repeat the selected test if preflight already ran it and nothing relevant changed.
- One failure can establish a shared missing prerequisite. After repair, still cover every
  distinct behaviour and security requirement.
- A setup, helper or compiler failure is not an application assertion failing. Record the
  exact failure and the limit of the evidence.
- Two unsuccessful evidence-based fixes should trigger diagnosis of real behaviour, SQL,
  HTTP or stored state, rather than another guess.
- A locally green focused test does not explain or eliminate a hosted CI flake.
- Source changes invalidate acceptance evidence for the previous source. Freeze source
  during compilation, review and final acceptance.

## Review quality

- Include tracked and new files in the actual reviewed change; verify Git status and HEAD.
- Include called helpers, permissions, projections, inputs, locks and schema contracts.
  Reviewing an isolated leaf caused unsupported assumptions and extra review rounds.
- Finish focused checks and lint before final review; review the correct source snapshot.
- Resolve a stale narrow finding with the corrected delta and result where sufficient,
  instead of resubmitting the whole change.
- Use a fresh Devin session for a coherent capability; resume it for corrections.
  Supply complete authorised input so unattended review does not stall on missing context.
- Distinguish a review tool's size limit or execution failure from a code finding. Check
  actual required checks before deciding whether acceptance is blocked.

## Resources, ownership and tools

- Cheaply revalidate transient Docker and access failures before calling them blockers.
- Reuse unchanged owned test images; rebuild when dependencies or build inputs change.
- Pin a proven installed runtime and invocation. Shell configuration and stale asdf shims
  caused repeated setup failures; disabling shell config alone did not fix every case.
- Keep one owner per shared target directory or database. Independent isolated resource
  lanes can proceed beside a Docker build without competing over shared state.
- Preserve disjoint file ownership and assign shared seams to the coordinator.
- A message does not activate an idle agent. Use the supported activation operation when
  agent work is authorised. Claim work is running only after observing a live handle.
- Preserve exact live handles across handoffs and capacity failures. Do not restart a job
  merely because observing it timed out.
- Discover paths and tool options rather than repeatedly guessing. Store a proven command
  in the existing handoff rather than creating another runner.

## Integration and publication

- Refresh and integrate the current base before expensive final verification. Record the
  candidate and dependency identity; recheck the base before landing.
- Preserve required merge ancestry. Flattening an upstream merge with plain rebase caused
  hosted registration trouble in the recorded case; choose integration from actual history.
- Check the exact pushed head and actual required checks. Avoid empty trigger commits.
- Avoid restarting full PR CI repeatedly for planning and status-only changes.

## Coordination, reports and retros

- Remove redundant migration runners, demo tabs and routine historical relocation audits
  when they stop helping. Keep historical audits explicit rather than in ordinary CI.
- Keep one authoritative plan and progress record. Do not produce duplicate trackers,
  per-repair briefs or extra planning gates without a concrete need.
- Report at the end of a useful slice and at meaningful blockers. State what shipped,
  what blocks the next delivery and the action being taken. Use readable HTML or Markdown.
- Separate locally passing, reviewed, published, accepted, merged and deployed evidence.
  Do not turn partial proof into a generic claim that everything is done.
- Maintain a reliable retro completion time and next due time. Skip duplicate retros quietly
  and do not interrupt a live test simply because a timer fired.
- A fresh session needs a safe source boundary and a concise handoff retaining the full
  objective, acceptance requirements, owners, permissions and live handles.
- Some failures violated rules already present. Apply the rules consistently before adding
  more rules. Evaluate reduced rework and delivery, not the number of plans or retros.

## Provenance

Collected from the owner's MedTracker migration retrospective on 6 October
2026 and retained from the installed start skill. The temporary transcript is
not distributed with this skill. Treat these as historical workflow lessons;
check current repository decisions before applying project-specific details.
