# Project Discovery and Command Routing

Discover the repository's contract before editing or running Ruby code. The
goal is to enter the same environment that maintainers and CI use.

## Read First

Look for repository instructions such as `AGENTS.md`, `README.md`, contribution
guides, development docs, and CI workflows. Then inspect the files that define
the Ruby project:

- `.ruby-version`, `.tool-versions`, `mise.toml`, or `.mise.toml`
- `Gemfile`, `Gemfile.lock`, and any `*.gemspec`
- `Rakefile`, `bin/`, `lib/tasks/`, and executable scripts
- Rails configuration under `config/`
- test directories, helper files, and tool configuration
- `Dockerfile*`, Compose files, Procfiles, and development containers

Prefer locked dependency information over memory or global installations.

## Command Precedence

Use the first layer that actually defines the needed operation.

### 1. Mise

Detect `[tasks]` in Mise configuration or scripts under `mise-tasks/`. Inspect
available tasks with `mise tasks`; run a defined task with `mise run NAME`.
Mise tasks carry the project's configured tools and environment.

### 2. Taskfile

Look for `Taskfile.yml`, `Taskfile.yaml`, or included Taskfiles. Use
`task --list` and inspect the selected task before running `task NAME`.

### 3. Rake

When no higher wrapper exists, inspect `Rakefile` and `lib/tasks/`. Use
`bundle exec rake -T` to discover public tasks and run the repository's task
instead of assembling an equivalent command by hand.

### 4. Binstubs and Bundler

Prefer checked-in binstubs such as `bin/rails`, `bin/rspec`, and `bin/rubocop`.
Otherwise use `bundle exec` so the locked gem versions are selected.

Direct host executables are the last resort.

## Preserve Container Boundaries

Mise, Task, or Rake tasks often wrap Docker Compose. If the selected task runs
inside a service container, keep using that path for tests, generators,
database access, and linting. A host command may use the wrong Ruby, gems,
services, environment variables, or filesystem ownership.

Do not replace a wrapper merely because a direct command is shorter. If Docker
is unavailable, report that limitation and use a fallback only when it is both
safe and representative.

## Detect the Active Stack

| Concern | Evidence |
| --- | --- |
| Ruby and Bundler | version files, Mise config, `Gemfile.lock` |
| Rails | locked `rails` gems, `config/application.rb`, `bin/rails` |
| RSpec | `rspec-core` or `rspec-rails`, `.rspec`, `spec/` |
| Minitest | `minitest`, `test/`, `test_helper.rb`, Rails test classes |
| Cucumber | `cucumber` or `cucumber-rails`, `features/`, `cucumber.yml` |
| Database | adapter, `config/database.yml`, schema, Compose services |
| Jobs | `config.active_job.queue_adapter`, job gems, worker processes |
| Frontend | asset/bundler gems and package manager files |
| Types | `sig/`, `rbs_collection.yaml`, `Steepfile`, `sorbet/`, `typeprof` |
| Quality | RuboCop/Standard/Reek/RubyCritic config and locked gems |
| Coverage | `.simplecov`, SimpleCov requires, coverage CI configuration |

Different test frameworks and quality tools can coexist. Route by the files and
behavior being changed, not by assuming one tool owns the whole repository.

## Map Prior Art

Before introducing a new pattern or boundary, search for how the repository
already handles the concern. Identify the dominant approach, meaningful
exceptions, relevant tests, and whether recent Git history shows a settled
convention or an active migration. Extend the established pattern when it fits;
do not copy an inconsistency merely because it already exists.

## Focused Command Discovery

Before running a broad task, determine whether the wrapper accepts a path,
line, scenario, tag, or filter. Inspect task definitions and examples; do not
guess pass-through syntax. If the wrapper offers only a full suite, consider a
lower command layer only when that still preserves the intended environment.
