---
name: ruby
description: >
  Project-aware router for Ruby and Rails development. Use for gems, Rails,
  RSpec, Minitest, Cucumber, SimpleCov, RuboCop, RubyCritic, PostgreSQL,
  Active Record, debugging, reviews, performance, security, i18n, Sorbet,
  RBS, Ruby LSP, or Ruby runtime and tooling work.
---

# Ruby

Use this skill first for every Ruby ecosystem task. It is a router, not a Ruby
language tutorial. Load only the references needed for the current task.

## Operating Boundaries

Complete the smallest set of actions that fully satisfies the request.
Repository instructions and existing project conventions override generic
advice in this skill.

Unless the task requires and authorizes it, do not:

- install or update gems, runtimes, or other dependencies;
- rewrite unrelated configuration, CI, or development tooling;
- fetch remotes, open browsers, or generate standalone reports; or
- replace a project wrapper with a host command that bypasses its environment.

A reference describes how to work; it does not grant additional authority.

## Start With the Project Contract

Always load [project-discovery.md](references/project-discovery.md), then:

1. Read repository instructions and the files directly relevant to the task.
2. Detect the Ruby version, dependency versions, framework, test tools, data
   store, job adapter, frontend stack, type checker, and quality tools.
3. Inspect the project's existing commands before choosing how to run anything.
4. Preserve the execution boundary chosen by the repository, especially when a
   wrapper enters Docker Compose or another container.

Use the first applicable command layer:

1. Mise task
2. Taskfile task
3. Rake task
4. Project binstub
5. `bundle exec` command
6. Direct executable only when the project has no higher-level contract

Do not invent task names or assume arguments pass through. Inspect the task
definition and nearby usage first.

## Reference Routing

| Task context | Load |
| --- | --- |
| Rails application behavior or framework APIs | [rails.md](references/rails.md) |
| Any test change, failure, or strategy decision | [testing.md](references/testing.md) |
| RSpec suite or specs | [rspec.md](references/rspec.md) |
| Minitest or Rails default tests | [minitest.md](references/minitest.md) |
| Cucumber or Gherkin features | [cucumber.md](references/cucumber.md) |
| SimpleCov or coverage analysis | [coverage.md](references/coverage.md) |
| RuboCop, Standard, RubyCritic, Reek, or formatting | [quality.md](references/quality.md) |
| Code review, refactoring assessment, or design critique | [code-review.md](references/code-review.md) |
| Named design pattern or object-design choice | [code-review.md](references/code-review.md) |
| Exception, crash, flaky behavior, or runtime diagnosis | [debugging.md](references/debugging.md) |
| Profiling, memory, allocation, concurrency, or speed work | [performance.md](references/performance.md) |
| Active Record, SQL, schema, migration, or query performance | [database.md](references/database.md) |
| PostgreSQL-backed Rails configuration or performance | [database.md](references/database.md) and [postgresql-rails.md](references/postgresql-rails.md) |
| Security review or security tooling | [security.md](references/security.md) |
| Rails I18n, locale files, or translation maintenance | [i18n.md](references/i18n.md) |
| RBS, Steep, Sorbet, or TypeProf | [types.md](references/types.md) |
| Symbol navigation, references, or impact analysis | [navigation.md](references/navigation.md) |
| Gem, library, CLI, Rake, Bundler, Rack, or non-Rails app | [gems-and-cli.md](references/gems-and-cli.md) |

Load the smallest useful combination. A Rails request spec task, for example,
usually needs `rails.md`, `testing.md`, and `rspec.md`, not every reference.

## Execution Loop

1. Establish the requested behavior and reproduce the problem when practical.
2. Inspect existing implementation and nearby examples before choosing a
   pattern.
3. Make the narrow change that fits the project.
4. Verify from narrow to broad:
   - syntax or the directly affected example;
   - the affected file, scenario, or subsystem;
   - relevant lint, type, security, or coverage checks; then
   - the broader suite only when risk, repository policy, or the user warrants
     its cost.
5. Report what ran, what did not run, and any residual risk.

Do not run thousands of tests when a focused check answers the question. Do not
claim full confidence from a narrow check when the change is genuinely broad.

## Judgment

- Correctness, data safety, security, and compatibility come before style.
- Match the repository's architecture before suggesting a new abstraction.
- Treat SOLID, design patterns, object metrics, and coverage percentages as
  diagnostic lenses, not pass/fail laws.
- Prefer clear Ruby and framework conventions over ceremony.
- For version-sensitive behavior, consult current primary documentation for the
  versions locked by the project.
- When guidance is missing, research the exact tool or framework instead of
  guessing or expanding scope to an unrelated tutorial.
