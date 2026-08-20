---
name: github-pr
description: Prepare, verify, and publish a scoped GitHub pull request. Use when the user asks to commit local work, push a feature branch, or create or verify a GitHub PR. This workflow always uses main as the PR base branch.
---

# GitHub Pull Request Workflow

> Upstream attribution: Adapted from the original [`github-pr` skill](https://github.com/damacus/skills/blob/b97d545a1099c1096bbaf9e346f833526b849a56/skills/workflow/github-pr/SKILL.md) authored by Dan Webb in `damacus/skills` commit `b97d545`.

Use this skill to take an explicitly selected local change through a conventional commit, push, and GitHub pull request. `main` is always the base branch. Do not discover or substitute another default branch unless the user explicitly overrides this rule.

Run GitHub CLI commands with elevated network access. Check `gh auth status` before the first GitHub write and ask the user to run `gh auth login` if authentication fails.

## Workflow

### 1. Inspect the work and current publication state

- Inspect `git status --short`, `git diff`, and `git diff --cached` before staging anything.
- Identify the exact files that belong to the requested work. Preserve unrelated staged, unstaged, and untracked changes.
- Check whether the current branch already has a PR with `gh pr list --head <branch> --state all`. If it has an open PR, verify and summarize that PR instead of creating a duplicate. If it is closed or merged, do not reuse the branch without explicit user direction.
- Refresh `origin/main` before creating a new feature branch. Do not silently rebase, reset, stash, or rewrite any worktree state.

### 2. Create or verify the feature branch

- Never commit the requested work directly on `main`.
- If starting from `main`, create a branch from refreshed `origin/main` with `git switch -c codex/<type>-<short-slug> origin/main`.
- If the current branch is detached, create an appropriately named branch before committing. If it is an existing feature branch, confirm that it is the intended branch and does not already have a conflicting PR.
- Prefer `codex/` branch names, with an appropriate type such as `feat`, `fix`, `docs`, `chore`, or `refactor`.

### 3. Summarize and stage only the selected changes

- Summarize the selected diff in plain language before writing the commit message.
- Produce a concise conventional commit subject that describes the user-visible intent. Keep it under 50 characters when practical.
- Stage explicit paths only: `git add -- <selected-paths>`. Never use `git add .` or `git add -A` by default.
- Inspect `git diff --cached --stat` and run `git diff --cached --check` before committing. If unrelated files are staged, stop and ask the user which changes belong in the PR.

### 4. Verify the change

- Identify the repository's normal validation commands from its documented project contract, CI configuration, or task runner.
- Run the relevant checks before publishing. For documentation-only work, use focused validation such as repository-provided linting plus `git diff --check` when no runtime test applies.
- Report the exact commands and outcomes. Do not claim tests passed when they were not run.
- If required validation fails because of this change, fix it before publishing. If it is demonstrably pre-existing, report that evidence and ask whether to publish a draft PR.

### 5. Commit and push

- Commit only after the staged diff and validation match the requested scope: `git commit -m "<conventional subject>"`.
- Push the current branch with upstream tracking: `git push -u origin HEAD`.
- After pushing, check again for an existing PR for the exact branch. Do not create a second PR if one already exists.

### 6. Create and verify the PR

- Create a ready PR only when the relevant validation passed. If validation is incomplete or failed for a reason the user accepts, ask whether to create a draft instead.
- Use explicit, non-interactive GitHub CLI arguments:

  ```fish
  gh pr create --base main --head <branch> --title "<conventional subject>" --body "<PR body>"
  ```

- Make the PR body useful to reviewers:
  - `## Summary` with concise behavior-oriented changes.
  - `## Verification` with exact commands and outcomes.
  - `## Risks / follow-ups` only when applicable.
- Verify the created or existing PR with `gh pr view <number> --json number,url,state,isDraft,baseRefName,headRefName,title`.
- Report the PR URL, branch, commit, base (`main`), validation results, and any known follow-up.

## Write Safety

- Invoking this skill to publish authorizes the normal commit, push, and PR-creation sequence. If the user asks only for a draft, analysis, status, or a commit without a PR, stop at that boundary.
- Do not amend existing commits, force-push, rebase, reset, stash, close PRs, or alter unrelated files unless the user explicitly asks.
- Do not create a duplicate PR. Existing PR status is a result to report, not an error to work around.
- Do not add reviewers, labels, assignees, projects, or milestones unless the user requests them.
- If GitHub authentication, repository access, branch push, or PR creation fails, report the precise blocker and leave the local commit intact.

## Completion Criteria

A publication request is complete only when the selected change is committed, pushed to its intended feature branch, represented by one verified PR against `main`, and accompanied by an accurate validation summary.
