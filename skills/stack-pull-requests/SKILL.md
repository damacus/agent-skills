---
name: stack-pull-requests
description: >-
  Decide whether planned implementation work should ship as one pull request, independent pull
  requests, or a stack of small ordered pull requests, then plan, build, review, revise, and land
  the stack safely. Use when a change is too large for effective review, later work must continue
  on an evolving baseline before earlier pull requests merge, AI-generated code needs deliberate
  review boundaries, or the user mentions stacked PRs, PR stacks, dependent PRs, gh-stack,
  bottom-up review, cross-fork stacks, fork-based dependent PRs, or splitting implementation
  across branches.
---

<!-- markdownlint-configure-file {"MD013":{"line_length":100,"code_blocks":false,"tables":false}} -->

# Stack Pull Requests

> Upstream attribution: Adapted from Paul Hammond's MIT-licensed
> [`stack-pull-requests` skill](https://github.com/citypaul/.dotfiles/blob/edf5519aa4bbea03b22217079b3c0e9d303fddd7/claude/.claude/skills/stack-pull-requests/SKILL.md).

Treat stacked pull requests as an optional branch, review, and integration topology. They are not
a substitute for defining a small vertical outcome.

Default a coherent implementation slice to one pull request against the repository's trunk
branch. Use a stack only when ordered branches materially improve review quality or allow useful
dependent work to continue before a lower pull request lands, without weakening verification,
deployability, or comprehension.

GitHub's native stacked pull requests are currently a public preview and use the official
`github/gh-stack` CLI extension. Read [references/source-notes.md](references/source-notes.md) and
check current official documentation plus live `gh stack --help` output before using
preview-specific commands. A portable dependent-branch chain remains an option when native stacks
are unavailable, but its CI, review, and merge behavior differs.

## Keep The Units Separate

| Unit | Question | Rule |
| --- | --- | --- |
| Backlog story | What bounded capability delivers value or learning? | Keep the outcome vertical and fix its acceptance scope before delivery planning. |
| Implementation slice | What smallest increment advances that outcome and leaves a known-good state? | Prefer one pull request and make it safe to land once declared prerequisites are present. |
| Pull request boundary | How should planned work be packaged for focused review? | Usually own one whole slice; use a dependent layer only when it earns its coordination cost. |
| Branch lineage | Which change must be based on which earlier change? | Record hard dependencies and deliberate overlap; do not infer lineage from habitual build order. |

A sequence describes work order; a stack describes branch dependency. Several planned slices are
not automatically a stack. A lower pull request may be independently mergeable, while every upper
pull request targets or is linked to the branch immediately below it.

Use supporting story-splitting or planning skills when they are available and relevant. Their
absence is not a blocker: establish the actor, outcome, approved scope, acceptance evidence, and
safe intermediate states directly before choosing pull request boundaries.

Do not turn `database -> API -> UI -> tests` into backlog stories. If technical layers genuinely
improve review of one selected slice, describe them as dependent pull request boundaries and make
their verification and release states explicit.

## Decide The Delivery Shape

Choose a stack only when all of these hold:

- The scope is one fixed slice or a deliberately ordered sequence of already approved slices.
- A concrete benefit exists: smaller focused diffs, useful overlap while lower review proceeds,
  or correction ownership that justifies propagating lower changes upward.
- The branches have one-way lineage: a hard dependency, or deliberate flow lineage where upper
  work begins before lower merge on the same evolving baseline.
- Fixed lower-first landing is acceptable.
- Each pull request owns one coherent change understandable from its diff and declared context.
- Every cumulative branch can be built, verified, and safely deployed or kept explicitly dormant.
- Every lower slice remains useful and safe if all upper work is abandoned.
- Expected rebase, CI, and re-review cost is lower than the review or lead-time benefit.
- The repository can run trustworthy required checks for every boundary.
- The team and available tooling can support dependent branches and cascading updates.
- Every native stack branch can live in one repository and its owner can push updates there.

Prefer one pull request or independent trunk-based pull requests when any of these hold:

- The whole change is already a quick, coherent review.
- Proposed pull requests can target trunk and merge, reorder, or be dropped independently.
- Later work can wait for its prerequisite to merge without blocking useful progress.
- Splitting would separate tests or evidence from the behavior they protect.
- Reviewers must understand the entire stack to judge every boundary.
- An intermediate merge would expose an unsafe schema, contract, bridge, or half-feature.
- Every layer would repeatedly touch the same cross-cutting code.
- Proposed boundaries are only files, architectural tiers, phases, or team ownership.
- The benefit is merely speculative convenience if an earlier decision changes.
- Restacking and repeated CI would cost more than the smaller diffs save.

### Run Two Counterfactuals

1. **Trunk counterfactual:** Could every proposed pull request start from current trunk and merge,
   reorder, or be dropped without incorporating a sibling? If not, a hard-lineage stack may fit.
2. **Flow counterfactual:** If it could, will upper work actually start before the lower pull
   request lands, is fixed lower-first landing acceptable, and will saved wait time or clear
   correction ownership outweigh restacking and re-review? If not, use independent pull requests.

Record the decision in one sentence:

```text
Delivery: single PR - the end-to-end change is already one focused review.
```

```text
Delivery: 3-PR stack - the dormant migration, tested repository adapter, and sign-in path have
one-way dependencies, and their focused review value exceeds the expected restacking cost.
```

## Design The Stack Before Writing Code

### 1. Fix Scope And Lineage

Record:

- the actor and outcome;
- the fixed union of approved scope;
- whether the stack is within one slice or spans an exact sequence of slices;
- each boundary's observable result or conserved contract;
- hard dependencies and deliberate flow lineage;
- the evidence and release constraint for each boundary; and
- the condition that completes the whole stack.

Do not add acceptance scope by calling a new behavior a pull request layer. If the request still
contains several unrelated outcomes, split or clarify the work before designing the stack.

### 2. Choose Boundaries

Prefer boundaries in this order:

1. **Whole vertical slices** that are useful and known-good, with real hard or flow lineage.
2. **Testable path increments** that advance one fixed slice without adding unrelated outcomes.
3. **Behavior-preserving preparation** that makes the later change reviewable.
4. **Backward-compatible enablement** that is verified, dormant, and directly used next.
5. **Risk isolation** for security-, data-, migration-, or performance-sensitive changes.
6. **Reviewer expertise** when the subsystem boundary still forms a coherent focused diff.

Avoid speculative foundations, a final tests-only pull request, duplicate upstack fixups, or a
lower boundary that needs upper work to compile, pass CI, migrate safely, or remove an unowned
bridge. There is no universal pull request count or line limit. Fold adjacent boundaries that need
the same explanation or evidence.

### 3. Make Intermediate States Safe

Every lower boundary must be one of:

- independently deployable and useful;
- behavior-preserving;
- backward-compatible and dormant;
- hidden behind an established flag;
- an independently verifiable transition with explicit cleanup ownership; or
- intended to land only as part of an approved native stack group, with the reason stated.

Never land an intermediate state that breaks callers, requires an unavailable schema, weakens
security, or exposes incomplete behavior. Expand-and-contract changes may need separate delivery
cycles when cleanup must wait for consumers to move.

### 4. Verify CI And Repository Topology

Before creating branches or pull requests:

- identify the trunk branch and repository branch-naming contract;
- identify whether each head branch is in the target repository or a contributor fork;
- verify who can push, rewrite, and delete every proposed stack branch;
- determine whether native stacked pull requests are available or the chain will be unlinked;
- inspect required workflows, branch filters, rulesets, CODEOWNERS, and merge-queue behavior;
- confirm each boundary produces every required status it needs;
- ensure merge-queue workflows include `merge_group` when GitHub Actions checks are required;
- decide which focused checks run per boundary and which cumulative checks run at the top; and
- account for rebase-triggered reruns, stale approvals, affected-test selection, and caches.

Native linked stacks can apply rules and CI against the stack trunk. Portable dependent pull
requests use ordinary immediate-base semantics. Do not assume a workflow filtered only to trunk
will run for a pull request whose immediate base is another feature branch.

Prefer one pull request when the chosen topology cannot give every boundary trustworthy required
checks without risky CI changes.

## Write The Delivery Plan

Use a compact map before implementation:

```markdown
#### Delivery Shape

**Mode**: Single PR | Independent PRs | Stacked PRs
**Stack scope**: Intra-slice | Cross-slice | N/A
**Repository topology**: Same repository | Fork-based
**Reason**: [Why this shape earns its cost]
**Story scope**: [Fixed actor, outcome, and exclusions]
**Done when**: [Cumulative acceptance or terminal gate]

| # | Boundary | Base | Owns | Depends on | Verification | Release state |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [focused title] | [trunk] | [coherent change] | - | [evidence] | [safe state] |
| 2 | [focused title] | [boundary 1] | [coherent change] | [contract] | [evidence] | [safe state] |
```

For every boundary, also record:

- its focused review question;
- included and excluded scope;
- likely files or subsystem without prescribing unnecessary implementation;
- required specialist reviewer, if any;
- behavior, contract, migration, or mechanical evidence it owns; and
- whether it is draft, review-ready, merge-ready, or blocked by a lower boundary.

Use repository naming conventions. Planning does not authorize branch creation, commits, pushes,
pull requests, rebases, force-pushes, or merges; obtain the user's authorization for those actions.

## Build Bottom To Top

For each boundary:

1. Start from the topmost committed and verified branch in the stack.
2. Confirm the boundary's scope, acceptance evidence, and safe release state.
3. Implement only the owned change.
4. Add each behavior's first meaningful test in the boundary that introduces that behavior.
5. Run focused checks plus the repository's required build, lint, type, security, and test gates.
6. Verify the cumulative branch, because an upper branch includes all lower work.
7. Review the diff against its immediate parent, not only against trunk.
8. Remove work that belongs in another boundary.
9. Commit only when the boundary is coherent and known-good.
10. Create the next branch from that committed tip.

Use the repository's testing, refactoring, security, migration, and mutation-testing contracts when
they exist. Do not invent a universal testing method or require a companion skill that is not
installed. Documentation and mechanical boundaries still need the smallest executable check that
can fail when the change is wrong.

Open unfinished upper boundaries as drafts. Each pull request description should state the stack
position, parent and next boundary, focused review question, owned and deferred scope, verification,
and release state.

## Choose The Operating Mode

### Native GitHub Stack

Use this only when every branch is in the same repository and the official extension is already
installed or the user authorizes installation. Cross-fork stacks are not supported.

1. Check `gh auth status`, `gh extension list`, and `gh stack --help`.
2. Use live help and current official documentation for `init`, `add`, `submit`, `sync`, `rebase`,
   `modify`, `push`, `checkout`, and navigation behavior.
3. Confirm each submitted pull request has the intended branch below it as its base and appears in
   the expected GitHub stack.
4. Use current `gh stack merge` behavior for an approved prefix or full-stack merge. Outside a
   merge queue, the selected merge is all-or-nothing. A merge queue may process the pull requests
   in separate groups, so verify repository rules and queue behavior first.

Do not install extensions, change repository settings, rewrite branches, or merge merely because
this skill is active.

### Fork-Based Contributions

GitHub native stacks cannot contain branches from different repositories. A contributor working
from a fork therefore cannot make a native stack whose pull requests merge into the upstream
repository. Local stack tooling can still manage branch lineage, but it cannot remove this GitHub
server boundary.

Choose a workaround in this order:

1. **One upstream pull request with reviewable commits.** Keep the complete change in one verified
   pull request, make each commit a coherent layer, and ask reviewers to review commit by commit.
   Prefer this when separate merge boundaries are not essential.
2. **Serial upstream pull requests.** Open only the bottom fork pull request against trunk. After
   it lands, rebase or replay only the next boundary onto updated trunk, verify it, and open the
   next pull request. This preserves focused diffs and normal fork security at the cost of overlap.
3. **Maintainer-mirrored branches.** When concurrent native review is materially valuable, an
   authorized maintainer can fetch the contributor's commits and push clearly namespaced branches
   into the upstream repository, then create the native stack there. Preserve commit authorship,
   agree who owns updates, and delete the temporary branches after landing. Do not grant repository
   write access solely to obtain stacked-pull-request UI.
4. **Cumulative fork pull requests.** Open each fork branch against upstream trunk and mark upper
   pull requests as dependent drafts. Their diffs include lower work until earlier boundaries land,
   so provide explicit branch-to-branch comparison instructions and review order. After every lower
   merge, rebuild the next branch from updated trunk with only its owned commits, rerun checks, and
   verify the focused diff before marking it ready.

For parallel focused review without upstream branch writes, pull requests may be opened inside the
contributor's fork between adjacent branches. Treat these as review-only: promote each boundary to
an upstream pull request serially after its prerequisite lands.

Do not assume an upper fork pull request will automatically become focused after a lower pull
request merges. Squash and rebase merge strategies can rewrite ancestry. Explicitly replay only the
upper boundary onto current trunk and inspect the resulting diff.

Every fork workaround must state:

- which pull request is currently eligible to merge upstream;
- the bottom-to-top dependency and review order;
- who owns each branch and may rewrite it;
- how upper branches are rebuilt after lower merges; and
- whether fork-originated CI lacks secrets, write tokens, or automatic workflow approval.

### Portable Dependent Pull Requests

When native stacks are unavailable, manage an explicit branch chain with Git and GitHub pull
requests:

```text
trunk <- boundary-1 <- boundary-2 <- boundary-3
```

Create each pull request with its immediate parent branch as the base so the review diff stays
focused. Verify bases after creation. Document the full order in every pull request because GitHub
will not supply native stack behavior. Confirm CI triggers for feature-base pull requests and plan
manual lower-first landing plus upstack rebases or base retargeting.

## Review And Revise

Review each boundary against its parent for function, intent, maintainability, dependencies,
security, and test integrity. Check for plausible-looking but incorrect generated code. Review
lineage-sensitive boundaries from the bottom upward; independent specialists may work in parallel
when focused diffs are understandable.

When feedback changes a lower boundary:

1. Switch to the branch that owns the contract or behavior.
2. Fix and verify it there.
3. Rebase or restack every branch above it using the selected tool's current workflow.
4. Rerun affected focused and cumulative checks.
5. Re-review upper diffs for duplication, accidental changes, and semantic drift.
6. Push rewritten shared branches only with explicit authorization and safe lease protection.

Do not add an upstack workaround for a downstack defect. Keep new upper-scope discoveries upstack;
use a separate trunk-based fix when the owning lower pull request has already merged. Reshape the
stack when evidence invalidates its boundaries, but require a clean working tree and a recoverable
plan before structural changes.

## Merge And Finish

Before any merge:

- require current checks and approvals for the selected boundary and every boundary below it;
- verify the top branch satisfies the full declared scope and cumulative acceptance evidence;
- verify every possible partially landed state remains safe;
- confirm the repository's merge method and merge-queue behavior; and
- obtain explicit merge authorization if it was not already granted.

For a native GitHub stack, use the current supported GitHub UI, API, or CLI capability to merge an
approved prefix or the whole stack from the bottom upward. For a portable chain, merge the bottom
pull request first, then update, retarget, and recheck the remaining chain. Never merge an upper
pull request without every required dependency below it.

After each partial landing, confirm remaining pull request bases and focused diffs. The whole stack
is complete only when its top boundary lands and all declared cleanup, verification, and release
obligations are satisfied.

## Completion Check

- Did the delivery decision compare single, independent, and stacked pull requests?
- Does every dependency reflect hard lineage or deliberate overlapping flow?
- Is every boundary coherent, verified, and safe in its cumulative state?
- Does each behavior receive its first test in the boundary that introduces it?
- Are native and portable stack semantics explicitly distinguished?
- Was same-repository versus fork topology checked before choosing native stacking?
- Does any fork workaround name branch ownership, merge eligibility, and rebuild procedure?
- Were lower-owned fixes made downstack and propagated upward?
- Are review order, merge order, release state, and authorization explicit?
- Would the stack still be worthwhile after counting rebase, CI, and re-review cost?
