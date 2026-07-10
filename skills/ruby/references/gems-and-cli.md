# Gems, Libraries, CLIs, and Non-Rails Ruby

Do not assume every Ruby repository is Rails. Detect gem, library, executable,
Rack application, framework, and monorepo boundaries from the source layout and
locked dependencies.

## Gems and Libraries

Inspect the gemspec, `lib/`, require paths, version constant, public API,
supported Ruby versions, Rake tasks, and release automation. Preserve:

- require and autoload behavior;
- semantic-versioning and compatibility commitments;
- keyword argument and block behavior;
- error classes and return contracts;
- generated files and packaged file lists; and
- supported runtime and dependency ranges.

Use repository tasks for tests, lint, gem building, and packaging. Inspect the
built artifact contents when packaging changes; do not publish or release
without explicit authorization.

## Command-Line Applications

Inspect executables, command framework, option parser, configuration sources,
stdout/stderr contract, exit codes, signal handling, and tests. Keep machine-
readable output stable, avoid leaking secrets, and test failure paths as well as
successful output.

## Other Frameworks

For Sinatra, Hanami, Rack, dry-rb, or another framework, detect the locked
version and consult current primary documentation. Reuse the common project,
testing, quality, security, database, and type references without forcing Rails
conventions onto the application.

## Bundler and Rake

Treat `Gemfile.lock`, gemspec dependencies, Bundler configuration, and existing
Rake tasks as project contracts. Do not update the lockfile, dependency bounds,
or task graph unless the task includes that change. Prefer the repository's
Mise or Task wrapper before invoking Rake directly.
