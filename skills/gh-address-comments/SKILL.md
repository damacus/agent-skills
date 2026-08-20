---
name: gh-address-comments
description: Address actionable GitHub pull request review feedback. Use when the user wants to inspect unresolved review threads, requested changes, or inline review comments on a PR, implement selected fixes, reply on every addressed thread, and resolve those threads in GitHub.
---

# GitHub PR Comment Handler

Use this skill when the user wants to work through requested changes on a GitHub pull request. Treat thread-aware review data as a `gh api graphql` problem: the connector comment surface is flat and does not preserve full review-thread state, stable thread IDs, or inline locations.

Run all `gh` commands with elevated network access. If CLI auth is required, check `gh auth status` first and ask the user to authenticate with `gh auth login` if it fails.

## Workflow

### 1. Resolve the PR

- If the user provides a repository and PR number or URL, use that directly.
- If the request is about the current branch PR, use local git context plus `gh pr view --json number,url,headRepositoryOwner,headRepository` to resolve it.
- Confirm the repository, PR number, and current head before making changes.

### 2. Inspect review context with thread-aware reads

- Use the GitHub app for PR metadata and patch context when the repo and PR are known.
- Use the plugin-provided `scripts/fetch_comments.py` workflow when it is installed alongside this skill and the task depends on unresolved review threads, inline review locations, or resolution state. It should fetch each thread's node `id`, `isResolved`, `isOutdated`, path, line anchors, and comments.
- If that script is unavailable, run an equivalent `reviewThreads` GraphQL query through `gh api graphql`. Do not use flat PR comments as a substitute for thread state.
- Keep the exact thread node ID for every selected item; the ID is required for both the reply and resolution mutations.

### 3. Cluster and select actionable threads

- Group comments by file or behavior area.
- Separate actionable change requests from informational comments, approvals, already-resolved threads, outdated duplicates, and general PR conversation.
- Present numbered actionable threads with a one-line summary when the scope is not already explicit.
- If the user asks to fix everything, interpret that as all unresolved actionable threads and call out anything ambiguous.
- Treat one thread as one issue: post one consolidated reply per addressed thread, even when that thread contains several individual comments.

### 4. Implement and verify the selected fixes

- Keep each code change traceable to the thread or feedback cluster it addresses.
- If a comment calls for explanation rather than code, prepare an explanation reply; do not invent a code change.
- Run the repository's relevant tests and checks after the changes.
- Do not reply to or resolve a thread until the corresponding fix or explanation is complete and the verification result is known.

### 5. Reply to and resolve every addressed thread

For each addressed thread, process the exact saved thread ID in this order:

1. Draft a concise reply stating what was changed or clarified and naming the relevant tests or checks. Mention the commit or PR head when useful.
2. Post the reply to that exact review thread with `addPullRequestReviewThreadReply`:

   ```fish
   set reply 'Addressed: <what changed>. Verified with <tests or checks>.'
   gh api graphql -f query='mutation($threadId: ID!, $body: String!) { addPullRequestReviewThreadReply(input: { pullRequestReviewThreadId: $threadId, body: $body }) { comment { id url } } }' -F threadId="$thread_id" -f body="$reply"
   ```

3. Confirm that the mutation returned a created comment ID. If it did not, stop for that thread and leave it unresolved.
4. Only after the reply succeeds, resolve the same thread with `resolveReviewThread`:

   ```fish
   gh api graphql -f query='mutation($threadId: ID!) { resolveReviewThread(input: { threadId: $threadId }) { thread { id isResolved } } }' -F threadId="$thread_id"
   ```

5. Verify the returned thread ID matches the selected thread and `isResolved` is `true`. If resolution fails or the returned state is not resolved, report the thread as addressed but still open; do not claim completion.

Never resolve a thread before its reply, resolve a whole PR as a bulk operation, or use a newly fetched comment ID in place of the review thread ID. Do not post duplicate replies when retrying: re-fetch the thread and check its comments before retrying a failed operation.

### 6. Summarize the result

Report, per selected thread:

- the issue addressed and the resulting change;
- the reply that was posted, or the reason it was not posted;
- the verification performed; and
- whether the exact thread is resolved.

List any ambiguous, informational, outdated, or intentionally skipped threads separately. A thread is complete only when its reply was created and its `isResolved` state was verified as `true`.

## Write Safety

- When the user authorizes addressing or fixing review threads, replying to each addressed thread and resolving it afterward is part of this workflow. Honor an explicit request to draft only, avoid GitHub writes, or leave threads open.
- If review comments conflict with each other or would cause a behavioral regression, surface the tradeoff before making changes.
- If a comment is ambiguous, ask for clarification or draft a proposed response instead of guessing or resolving it.
- Do not treat flat PR comments from the connector as a complete representation of GitHub review-thread state.
- If `gh` hits auth or rate-limit issues mid-run, stop GitHub writes, report the blocker, and ask the user to re-authenticate or retry.
- If a reply succeeds but resolution fails, preserve the reply, report the exact thread as still open, and retry resolution only after re-fetching current thread state.

## Fallback

If neither the connector nor `gh` can resolve the PR cleanly, tell the user whether the blocker is missing repository scope, missing PR context, or CLI authentication, then ask for the missing repo or PR identifier or for a refreshed `gh` login.
