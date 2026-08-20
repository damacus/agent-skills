# Origin and Adaptation Notes

This skill was adapted from Paul Hammond's `cli-design` skill in
[`citypaul/.dotfiles`](https://github.com/citypaul/.dotfiles/tree/main/claude/.claude/skills/cli-design).
The upstream material is licensed under the MIT License; the license text is included in `../LICENSE`.

Imported from upstream commit `26419a1611f8c203b6154d53feb87a626358c83e` on 2026-07-13.

Local changes:

- Kept the core language-agnostic and made the TypeScript material explicitly optional.
- Removed hard dependencies on separately installed API, twelve-factor, and hexagonal skills.
- Recast JSON envelopes, `--plain`, sysexits codes, positional arguments, silence on success, and latency numbers as deliberate contracts rather than universal mandates.
- Added explicit CLI/TUI composition and parity guidance.
- Tightened the activation contract for Codex and existing-code compatibility work.
