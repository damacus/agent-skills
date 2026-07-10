# Rails

Treat the locked Rails version and the application's configuration as the
source of truth. Rails defaults and APIs change; consult current primary
documentation for the detected version when exact behavior matters.

## Establish the Application Shape

Inspect `Gemfile.lock`, `config/application.rb`, environment files,
initializers, routes, binstubs, and relevant application directories. When the
project's execution wrapper can boot the app safely, `bin/rails about` can
confirm Ruby, Rails, Rack, and database details.

Determine which Rails components are active rather than assuming a full-stack
default:

- Active Record and its database adapter or an alternative persistence layer;
- Action Controller, API-only mode, views, serializers, and responders;
- Active Job and the configured queue adapter;
- Action Mailer, Cable, Mailbox, Text, and Storage;
- Propshaft or Sprockets, import maps, bundlers, Vite, Turbo, and Stimulus;
- caching, session, and deployment adapters; and
- engines, multiple databases, and custom autoload paths.

## Work With Existing Rails Conventions

Follow local naming, namespaces, route shape, rendering, policies, forms,
serializers, jobs, and service boundaries. Do not automatically extract a
service object, concern, callback, presenter, or query object because a generic
style guide prefers one. Choose the smallest abstraction that makes the current
behavior clearer and safer.

When changing framework behavior:

- inspect nearby examples and the generated application configuration;
- preserve authorization and tenancy boundaries;
- account for transactions, callbacks, retries, and `after_commit` timing;
- consider Zeitwerk naming and autoloading for constants and file moves;
- keep request formats, status codes, redirects, and Turbo behavior compatible;
  and
- test the public boundary at the level used by the repository.

## Data and Migrations

Load [database.md](database.md) for query, schema, or migration work. Match the
migration version, schema format, adapter, safety tooling, deployment process,
and data volume. A migration that is valid in a new application can still lock
or rewrite a production table.

## Jobs and External Effects

Detect the Active Job adapter and worker topology. Preserve queue names,
priorities, retry/discard behavior, serialization, idempotency, and transaction
boundaries. Do not replace a repository's direct worker API with Active Job, or
vice versa, without a task-specific reason.

## Frontend and Browser Behavior

Inspect the actual asset and JavaScript stack before editing views or adding
dependencies. Turbo, import maps, bundlers, component systems, and API-only
applications need different solutions. Use the configured system-test driver
and existing browser helpers for verification.

## Related References

- tests: [testing.md](testing.md) plus the configured framework reference
- database and query performance: [database.md](database.md)
- PostgreSQL-specific operation: [postgresql-rails.md](postgresql-rails.md)
- security: [security.md](security.md)
- types: [types.md](types.md)
- semantic impact analysis: [navigation.md](navigation.md)
