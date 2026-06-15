---
name: github-composite-actions
description: Use when a GitHub composite action has complex YAML steps, shell logic, cross-platform behavior, many outputs, or is hard to test, lint, or debug.
---

# GitHub Composite Actions

## Core Principle

Treat `action.yml` as orchestration and the action's inputs/outputs as a
public API. Put non-trivial behavior in scripts so it can be linted, tested,
and debugged outside GitHub Actions.

## Start With The Contract

Before editing implementation, define:

- Modes or variants, with the safest default.
- Supported OS and architecture for each mode.
- Inputs, including how dynamic values such as `latest` are resolved.
- Outputs consumers need for follow-up steps and debugging.
- Failure behavior for unsupported modes or platforms.

Useful action outputs:

- resolved inputs such as `mode`, `version`, `requested_version`, or `ref`
- `runner_os`, `runner_arch`
- primary results such as `artifact_path`, `executable_path`, or `result_id`
- domain-specific paths or IDs that downstream steps should not rediscover

## Structure

Use this shape unless the repo already has a stronger convention:

```text
.github/actions/<action-name>/
  action.yml
  scripts/
    resolve-inputs.sh
    run-<mode>.sh
    outputs-<platform>.sh
    run-<platform>.ps1
  tests/
    check-script-contracts.sh
```

Do not compose sibling local actions from a published remote action; relative
`uses:` paths resolve from the caller's checkout. Call scripts through
`$GITHUB_ACTION_PATH` instead.

## Testing Requirements

Add tests before or alongside behavior changes:

- `actionlint` for workflow/action YAML.
- `shellcheck` for bash scripts.
- PowerShell parser checks for `.ps1` files.
- Contract tests proving `action.yml` calls the expected scripts.
- Runtime output tests with fake commands and fake `GITHUB_OUTPUT`.
- Fake external CLIs, such as `gh`, when testing dynamic latest resolution.

Outputs are API. Test examples like `outputs.version`,
`outputs.artifact_path`, `outputs.executable_path`, or `outputs.result_id` so
downstream workflows can rely on them.

## Release Assets And Platform Support

When an action downloads release assets, never guess archive names or platform
support. Inspect release assets first with `gh api` or `gh release view`, then
encode OS/arch mapping in one script. If a mode does not support a runner, fail
early with a clear `::error::`.

For `latest`, prefer runtime resolution over hardcoded tags when the runner has
a suitable tool:

```bash
gh release view --repo owner/project --json tagName -q .tagName
```

Provide a version input so callers can pin when reproducibility matters.

## Debuggable Output

Every custom step should print the useful facts:

- resolved inputs
- selected mode, URL, archive, ref, or identifier
- OS and architecture mapping
- discovered paths or IDs
- emitted outputs
- file names being parsed or linted

Group verbose sections with `::group::` / `::endgroup::`.

## Runner Choice

Use `ubuntu-slim` only for orchestration jobs that do not depend on
preinstalled CLI tools. Keep `ubuntu-latest` when the job relies on
runner-provided tools such as `shellcheck`, `pwsh`, package managers, or
third-party actions with unstated tool assumptions. Add comments explaining the
choice.

## Common Mistakes

- Hiding large shell scripts inside YAML.
- Adding implementation before defining outputs.
- Testing only that the action runs, not that outputs are correct.
- Hardcoding `latest` to a tag and forgetting to update it.
- Assuming Linux-only or x64-only support without checking release assets.
- Moving jobs to `ubuntu-slim` without checking tool availability.
