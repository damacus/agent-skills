# Ruby Code Review

Review the scope the user actually supplied. A method review, working-tree
review, commit review, and pull-request review require different discovery.
Do not fetch remotes, choose a base branch, or create a report unless the task
requires it.

## Establish Scope

- For a snippet or named file, start there and inspect callers only as needed.
- For working-tree changes, include staged and unstaged changes while preserving
  unrelated user work.
- For a commit or branch review, confirm the intended base from repository or
  live review metadata rather than defaulting to `main`.
- Include templates, migrations, configuration, tests, and generated interfaces
  when they participate in the behavior.

## Review Priorities

Assess in roughly this order:

1. correctness and behavior regressions;
2. data loss, migration, concurrency, and transaction risk;
3. authentication, authorization, input handling, and other security concerns;
4. public API and compatibility changes;
5. missing or misleading tests;
6. query, allocation, blocking, and operational performance risk;
7. maintainability and design; then
8. style that is not already enforced mechanically.

A finding should identify a concrete failure mode, the conditions that trigger
it, and the smallest useful remediation. Avoid generic preferences disguised
as defects.

## Design Judgment

Use cohesion, coupling, dependency direction, encapsulation, and change cost as
questions. SOLID principles, Sandi Metz's rules, Law of Demeter, and named
patterns are optional lenses:

- a long class is not defective merely because it crosses a line count;
- an explicit dependency is not automatically a reason to add injection;
- a conditional is not automatically a reason to add polymorphism; and
- a service object or concern is not automatically more idiomatic than the
  repository's existing approach.

Prefer shamelessly clear working code before speculative abstraction. Recommend
a pattern only when it resolves an observed source of change or coupling.

## Tooling

Use configured tests, lint, types, security tools, coverage, and RubyCritic when
they add evidence. Their output supports review judgment; it does not replace
reading the code. Run the narrowest useful checks and state what was not run.

## Output

Lead with actionable findings ordered by severity. Include precise file and
line references in the host application's supported format. Do not require a
standalone `REVIEW.md`, a particular editor URI, positive filler, or a fixed
section template unless the user requests one.
