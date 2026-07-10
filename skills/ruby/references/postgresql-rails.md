# PostgreSQL on Rails

Load this reference only after confirming that the Rails application uses the
PostgreSQL adapter. Match the locked Rails version, PostgreSQL server version,
`pg` gem, deployment topology, and repository tooling before recommending
configuration or migration code.

## Analysis Workflow

1. Define the reported problem: latency, query count, connection pressure,
   locks, schema design, migration safety, or a broader audit.
2. Enter the application's normal Mise, Task, Rake, or Docker Compose boundary.
3. Inspect configuration and collect runtime evidence before proposing changes.
4. Prioritize findings by measured impact, production risk, and effort.
5. Make or recommend the smallest change, then repeat the same measurement and
   relevant application tests.

Do not run imagined analyzer scripts. Use repository tasks, Rails and PostgreSQL
introspection, configured monitoring, logs, and current primary documentation.

## Connection Configuration

Inspect `config/database.yml`, `DATABASE_URL`, Rails credentials or environment
configuration, container services, and any connection proxy such as PgBouncer.
Rails can merge `DATABASE_URL` with `database.yml`, with URL values taking
precedence on conflicts, so inspect the effective configuration rather than one
file in isolation.

Review configuration in the context of every process and database role:

- pool size versus Puma threads, job concurrency, console/runner processes, and
  horizontal replicas;
- the total PostgreSQL connection budget, reserved connections, proxies, and
  failover behavior;
- `checkout_timeout`, connection establishment, reaping, and idle behavior;
- `statement_timeout`, `lock_timeout`, and transaction timeout policy;
- SSL mode and certificate verification;
- prepared-statement behavior and proxy compatibility; and
- primary, replica, shard, and multiple-database configuration.

Increasing the pool can move contention from Rails to PostgreSQL. Estimate the
aggregate connection demand across processes before changing it.

## Query Evidence

Capture the actual SQL, binds, frequency, latency distribution, row counts, and
call path. Useful existing sources include Rails query logs, Active Support
instrumentation, PostgreSQL logs, application telemetry, PgHero, and
`pg_stat_statements`.

Use `EXPLAIN` to inspect the estimated plan. `EXPLAIN ANALYZE` executes the
statement; use representative non-production data or an approved safe method.
For data-changing statements, wrapping analysis in a transaction and rolling it
back avoids persistence but does not eliminate execution cost, locks, triggers,
or other side effects.

When reading a plan, compare estimates with actual rows and loops, then inspect
buffers, scan and join choices, sorts, hashes, memory, spills, and repeated
work. A sequential scan is not automatically wrong; it can be cheaper for a
large fraction of a table or a small relation.

## Rails Query Patterns

Confirm N+1 behavior with query logs, notifications, Bullet when configured, or
a focused test. Choose `includes`, `preload`, `eager_load`, joins, strict
loading, aggregation, batching, or a counter cache according to the access
pattern. `count`, `size`, `exists?`, and association iteration do not have
identical loading behavior.

For large collections, inspect whether `find_each`, `find_in_batches`, bulk
operations, cursors, pagination, or a set-based SQL operation fits the contract.
Preserve ordering, callbacks, validations, timestamps, locking, and error
semantics when replacing row-by-row work.

## Index Analysis

Base an index recommendation on real predicates, joins, ordering, selectivity,
row counts, and frequency. Check existing indexes and constraints first.
Consider:

- column order in composite indexes;
- unique indexes for database-enforced uniqueness;
- partial indexes for stable selective predicates;
- expression indexes for the exact queried expression;
- covering indexes and their write/storage cost;
- foreign-key lookup and delete/update behavior;
- redundant or unused indexes, bloat, and maintenance overhead; and
- whether stale statistics, not a missing index, explain the planner choice.

A boolean column, foreign key, or frequently mentioned field does not
automatically need its own index.

## PostgreSQL Schema Choices

Review data types and constraints against the domain and query workload:

- `jsonb` versus normalized columns, including containment and expression
  queries;
- numeric precision, timestamps and time zones, UUID or integer identifiers,
  arrays, enums, ranges, network types, and generated columns;
- `NOT NULL`, foreign keys, unique constraints, and check constraints; and
- extension ownership and availability across environments.

Do not choose a PostgreSQL-specific type merely because it exists. Account for
validation, serialization, indexing, portability, and migration cost.

## Production-Safe Migrations

Evaluate locks, table rewrites, transaction length, replication lag, backfill
volume, rollback, and mixed application versions. Follow configured migration
safety tooling and deployment runbooks.

PostgreSQL concurrent index creation reduces blocking but has its own rules and
failure modes. Rails concurrent index migrations cannot run inside the normal
DDL transaction and therefore require the version-appropriate transaction
setting. Verify invalid indexes and retry/cleanup behavior after failures.

For large changes, prefer staged expansion and contraction where appropriate:
add compatible schema, deploy code that can handle both states, backfill in
bounded batches, validate constraints, switch reads/writes, and remove obsolete
schema later.

Set migration-local timeouts only with an understood operational policy. Do not
quietly weaken application-wide safety settings to make one migration pass.

## Observability and Reporting

Use configured tools such as `pg_stat_statements`, PgHero, Rails query logs,
database metrics, lock views, slow-query logs, and production traces. Do not
install extensions or monitoring gems without authorization.

For each finding, report:

- the observed evidence and affected workload;
- why it matters now rather than as a generic best practice;
- the proposed change and trade-offs;
- how to verify it; and
- production rollout or rollback concerns.
