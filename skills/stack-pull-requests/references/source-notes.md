<!-- markdownlint-configure-file {"MD013":{"line_length":100,"code_blocks":false,"tables":false}} -->

# Stack Pull Requests Source Notes

Load this reference for provenance, teaching, or preview-specific updates. Ordinary delivery-shape
decisions should use the durable rules in the main skill.

## Upstream

This skill adapts Paul Hammond's
[`stack-pull-requests` skill](https://github.com/citypaul/.dotfiles/blob/edf5519aa4bbea03b22217079b3c0e9d303fddd7/claude/.claude/skills/stack-pull-requests/SKILL.md)
at commit `edf5519aa4bbea03b22217079b3c0e9d303fddd7`.

The upstream material is licensed under the MIT License. The license text is included in
[`../LICENSE`](../LICENSE).

The adaptation preserves the upstream distinctions between stories, implementation slices, pull
request boundaries, hard and flow lineage, per-boundary verification, safe intermediate states,
lower-owned corrections, and bottom-up landing. It removes hard dependencies on companion skills
that may not be installed and separates durable Git behavior from changing GitHub preview behavior.

## Current Official GitHub Sources

GitHub's preview and extension behavior changes quickly. Prefer these current first-party sources:

| Source | Guidance used |
| --- | --- |
| [Creating stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests) | Current preview status, same-repository requirement, CLI and website creation, branch bases, and stack linking. |
| [Stacked pull requests CLI commands](https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands) | Current extension installation, command behavior, flags, merge semantics, safe-lease pushes, and exit codes. |
| [`github/gh-stack`](https://github.com/github/gh-stack) | Extension source and release history. Prefer the main GitHub Docs when repository prose conflicts with them. |
| [GitHub Actions events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) | Ordinary pull request base filters and the `merge_group` trigger required by merge-queue checks. |
| [GitHub Copilot stacking tutorial](https://docs.github.com/en/copilot/tutorials/stack-ai-generated-code-in-pull-requests) | Plan small coherent layers, build and review from the bottom, keep corrections in the owning layer, and propagate changes upward. |
| [Review AI-generated code](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code) | Check context, intent, maintainability, dependencies, test integrity, and plausible-looking wrong code. |

Useful secondary sources retained from upstream:

- [Graphite: How to structure a stack](https://graphite.com/docs/how-to-structure-your-stacks)
- [Graphite: Best practices for reviewing stacks](https://graphite.com/docs/best-practices-for-reviewing-stacks)
- [Graphite: CI optimizations](https://graphite.com/docs/stacking-and-ci)
- [Sapling: Stacks of commits](https://sapling-scm.com/docs/overview/stacks/)

## Verified Adaptation Notes

As of 2026-08-01:

- GitHub describes native stacked pull requests as a public preview and subject to change.
- `gh stack` is supplied by the official `github/gh-stack` extension rather than GitHub CLI core.
- Every branch in a native stack must be in the same repository; cross-fork stacks are unsupported.
- `gh stack push` uses explicit per-branch safe-lease checks in one non-atomic push. Some branches
  can update even when another branch is rejected.
- `gh stack merge` can merge a selected prefix or full stack as one all-or-nothing operation.
- With a merge queue, selected pull requests enter the queue together but may land in separate
  groups as the queue processes them.
- The GitHub UI can merge a selected pull request and the unmerged pull requests below it; current
  documentation should be rechecked before relying on exact partial-merge or queue behavior.
- Portable dependent pull requests remain possible but use ordinary immediate-base CI semantics
  and need manual stack documentation, lower-first landing, and upstack maintenance.

These are observations, not permanent contracts. The main skill therefore requires current official
documentation and live help before preview-specific operations.

## Fork Workaround Synthesis

GitHub's official creation guide states that every native stack branch must be in the same
repository and that cross-fork stacks are unsupported. GitHub does not prescribe one replacement
workflow for external contributors, so the main skill derives proportionate fallbacks from ordinary
pull request and Git branch behavior:

- Use one upstream pull request with coherent commits when separate merge boundaries are optional.
- Serialize upstream pull requests when focused merge boundaries matter more than overlapping work.
- Mirror contributor commits onto maintainer-owned upstream branches when concurrent native stack
  review earns the extra coordination and write responsibility.
- Use cumulative fork pull requests only with explicit dependency notes, comparison instructions,
  and an upper-branch rebuild after every lower merge.
- Use pull requests inside the contributor fork only as review aids, not as upstream merge objects.

These alternatives do not create a native GitHub stack. In particular, local stack tools cannot
bridge the server-side repository boundary, and squash or rebase merges can prevent an upper fork
pull request from shrinking automatically after a lower pull request lands.

## Updating The Skill

When GitHub changes the preview:

1. Re-read the official overview, CLI reference, extension README, and merge guidance.
2. Run `gh --version`, `gh extension list`, and `gh stack --help` in the active environment.
3. Check current availability constraints and the same-repository requirement.
4. Recheck whether cross-fork stacks remain unsupported and update the fallback decision order.
5. Verify submit, push, sync, rebase, modify, merge, and merge-queue behavior.
6. Update operational wording and the dated notes, not the durable scope and lineage rules.
7. Preserve tests with their owning behavior and keep every intermediate branch known-good.
