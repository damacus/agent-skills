---
name: security-maintenance
description: >
  Find and safely ship one evidence-backed security improvement using an
  approved repository contract. Use when reviewing, hardening, or fixing a
  security issue in an unfamiliar codebase.
argument-hint: "[audit | fix-one | verify]"
---

# Security Maintenance

Find and address at most one security issue or security improvement per run.
Prioritize demonstrable risk and a narrow, well-tested change over broad
hardening or checklist-driven work.

## Scope and Permissions

Read-only repository inspection and proportionate local verification are
implicitly allowed. Do not add dependencies, change public contracts, alter
authentication or authorization semantics, perform a broad refactor, publish
external findings, or open a pull request unless the user has authorized that
action.

Do not add or remove code comments unless the user explicitly asks. Express
security intent through clear code, tests, and review communication instead.

Reference workflows do not grant additional authority; apply them only within
these boundaries.

## Repository Contract Setup

Before the first security scan in a repository, or whenever the existing
contract is absent or stale, explicitly ask the user:

> Before I start, may I set up or refresh this repository's security contract?
> I will inspect local instructions and configuration, identify the approved
> tooling and sensitive areas, and show the contract for your approval. Should
> this run be audit-only, fix one finding, or include a pull request?

Do not start the scan until the user approves discovery. After approval, gather
the contract using only repository-local evidence:

1. Read repository instructions, contribution guidance, and security policy.
2. Identify supported commands from task runners, package manifests, build
   files, CI workflows, and developer documentation.
3. Find the language, framework, test stack, static-analysis tools, and
   supported local runtime.
4. Map high-value assets and boundaries: authentication, authorization,
   tenancy or ownership, secrets, personal or regulated data, APIs, files,
   jobs, webhooks, and external network access.
5. Identify test, lint, build, security-scan, branch, commit, pull-request,
   and disclosure conventions.

Present the proposed contract to the user and wait for approval before changing
repository files, recording durable memory, or creating a pull request. Use
the template in [repository-contract.md](references/repository-contract.md).

When the user approves it, preserve durable, non-sensitive repository-specific
constraints and learnings in the host agent's approved memory system when one
exists and the user has authorized persistence. Memory is routing context, not
live evidence: revalidate commands, branches, policies, and security state in
each run.

## Investigation

Start from evidence in the approved contract, a reported issue, a failing
security check, or a changed sensitive path. Prefer investigating the highest
impact reachable issue in this order:

1. Unauthorized access, privilege escalation, tenant or ownership escape.
2. Secret, token, personal-data, or regulated-data exposure.
3. Injection, unsafe deserialization, SSRF, path traversal, unsafe redirects,
   command execution, and unsafe file handling.
4. Authentication, session, CSRF, rate-limit, and security-header failures.
5. Dependency or configuration risk with a confirmed affected path.
6. Small defense-in-depth improvement with a clear security outcome.

Do not report a theoretical issue as exploitable without a supported path. Do
not turn an unchanged baseline finding into a pull-request regression.

## Implementation

For an authorized fix, keep the change focused on the selected finding.

1. Add or update a behavior-level test that demonstrates the failure before
   the production change, where the repository supports this.
2. Implement the smallest secure change.
3. Verify authorization, ownership, input handling, error handling, and
   sensitive-data behaviour appropriate to the affected path.
4. Refactor only while the focused checks stay green.

Stop and ask the user before adding a dependency, making a breaking change,
changing an authentication or authorization contract, or expanding beyond one
small finding. Never commit secrets, weaken controls to make tests pass, or
publish exploit instructions or sensitive data.

## Verification and Delivery

Run the approved focused checks first, then the contract's required quality and
security gates before publishing. Report blocked or unavailable checks exactly
as they occurred; never claim an unrun check passed.

When a pull request is authorized:

- Follow the repository's branch and commit convention. If no convention is
  established, ask the user before creating the branch or commit.
- Use Conventional Commits only when the contract requires them. Never add
  decorative emojis or role branding to a title.
- Explain the problem, why it matters, and the protection gained in plain
  language. Keep public vulnerability detail proportionate to the repository's
  visibility.
- Push only after the approved quality gates pass, following the repository's
  documented publication flow.

If no small, evidence-backed improvement is available, report that conclusion
and stop without creating a pull request.
