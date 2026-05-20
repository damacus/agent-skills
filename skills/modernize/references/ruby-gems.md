# Ruby Gem Modernization

Use this for Ruby runtime and gem dependency modernization.

## Detect

- Runtime: `.ruby-version`, `Gemfile` `ruby`, CI matrices, Docker tags.
- Dependencies: `Gemfile`, `Gemfile.lock`, `*.gemspec`, gem groups, source blocks.
- Tooling: Bundler version in `Gemfile.lock`, `bin/`, `.rubocop.yml`, RSpec files.

## Inspect

```bash
bundle outdated
bundle outdated --groups
bundle info <gem>
gem info <gem> --remote
```

Use `references/eol-api.md` for Ruby runtime EOL checks.

## Update

- Keep Gemfile constraints intentional; avoid widening constraints unless required by
  the target version or requested by the user.
- Prefer `bundle update <gem>` or a small related group over broad lockfile churn.
- For applications, preserve Rails and framework compatibility boundaries.
- For libraries, update gemspec runtime constraints and test against the declared
  supported Ruby versions.
- Keep the Bundler version unless the project already requires changing it.

## Validate

Run the repo's existing commands, typically `bundle exec rspec`, `bundle exec rubocop`,
`bundle exec rake`, or the configured task runner. If dependencies cannot be installed,
report the blocker and the commands that remain.
