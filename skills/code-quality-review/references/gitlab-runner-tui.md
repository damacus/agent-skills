# Reference example: gitlab-runner-tui

This is an invocation example, not a repository-specific rule in the workflow.
Observed read-only on 28 October 2026 at commit
`cb0e0ace9484fc409005f65259a84e8c0346e105`.

The local checkout was `/Users/damacus/repos/damacus/gitlab-runner-tui`. Its
`AGENTS.md` requires `mise run <task>` for local Rust checks and prohibits direct
Cargo/rustup invocation. `mise.toml` defines these existing commands:

| Task | Purpose | Review handling |
| --- | --- | --- |
| `mise run fmt` | rustfmt `--check` | Safe format check in snapshot |
| `mise run lint` | Clippy, locked, all targets/features, deny warnings | Compare warnings with mechanical candidates |
| `mise run test` | Locked all-feature tests | Use isolated fixtures; keep build output outside target |
| `mise run security` | cargo-deny advisories | Record advisory database freshness and setup failures |
| `mise run workflow:lint` | actionlint | Relevant when workflow files are in scope |
| `mise run workflow:security` | offline zizmor | Relevant workflow security evidence |

Do not use `fmt:fix`, dependency updates, hook installation or a broad `check`
task without inspecting its current definition. Do not add tasks to this example
repository during a review; report missing safe commands instead. Repository
publication instructions do not grant permission to push audit work.

Existing `.desloppify/` state was present as an untracked directory. Preserve it
as existing baseline evidence before a fresh scan, never overwrite it or add it
to `.gitignore`. That dirty status must be distinguished from tracked source.

Suggested invocation:

> Use $code-quality-review on gitlab-runner-tui with the standard profile.
> Keep the checkout read-only, preserve its existing scan baseline and save the
> report outside the repository.

The independent architect should trace a real fetch/display journey and error/
cancellation/terminal cleanup paths based on current source. This suggests where
to inspect; it is not a claim that these paths are defective. Recheck current
repository instructions and tasks before use. No application scan, test or model
review was performed as part of installing this skill.
