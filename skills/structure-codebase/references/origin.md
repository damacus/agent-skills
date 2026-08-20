# Origin and Adaptation Notes

This skill was adapted from Paul Hammond's `structure-codebase` skill in
[`citypaul/.dotfiles`](https://github.com/citypaul/.dotfiles/tree/main/claude/.claude/skills/structure-codebase).
The upstream material is licensed under the MIT License; the license text is included in `../LICENSE`.

Imported from upstream commit `26419a1611f8c203b6154d53feb87a626358c83e` on 2026-07-13.

Local changes:

- Shortened and narrowed the activation contract to reduce accidental triggering.
- Added repository-instruction, evidence, uncertainty, and dirty-worktree guardrails suitable for Codex.
- Made comparison criteria, rejected alternatives, and migration risks explicit deliverables.
- Softened universal claims where enforcement and testing should be proportional to risk.
- Removed hard dependencies on separately installed DDD and hexagonal-architecture skills.
