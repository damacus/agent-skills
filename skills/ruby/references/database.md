# Databases, Active Record, and Migrations

Detect the actual database adapter and topology before giving database advice.
Do not apply PostgreSQL-specific indexing, SQL, or operational guidance to
SQLite, MySQL, Trilogy, or another adapter.

When the detected adapter is PostgreSQL and the task concerns configuration,
queries, schema, migrations, or performance, also load
[postgresql-rails.md](postgresql-rails.md).

## Establish Evidence

Inspect adapter gems, `config/database.yml`, environment configuration, schema
format, migrations, model queries, logs, and container services. Account for
multiple databases, replicas, sharding, tenancy, and connection proxies when
present.

For a slow query, prefer runtime evidence over static guesses:

- capture the actual SQL and bind values safely;
- inspect query counts and timing;
- use the adapter's query plan tools; and
- compare representative row counts and selectivity.

`EXPLAIN ANALYZE` executes the statement. Do not use it casually on writes or
production data. Follow repository procedures and use a safe representative
environment.

## N+1 and Loading Behavior

Association access inside iteration is a lead, not proof. Confirm whether the
association is already loaded and whether the call (`count`, `size`, `exists?`,
or iteration) issues SQL. Choose `includes`, `preload`, `eager_load`, joins,
batching, or a counter cache based on query semantics and measured behavior.

## Indexes and Constraints

Recommend an index from real query predicates, ordering, joins, cardinality,
and write cost. Check existing composite, partial, expression, and unique
indexes before adding one. Treat foreign keys, uniqueness, nullability, and
check constraints as data-integrity decisions, not merely model validations.

## Migration Safety

Match the locked Rails migration API, adapter, safety gems, deployment process,
and production data size. Consider locks, table rewrites, backfills,
transactions, replication, rollback behavior, and mixed-version deployments.

Separate schema change from large data migration when that reduces operational
risk. Concurrent index and constraint-validation techniques are adapter- and
version-specific; consult current primary documentation before generating code.

Verify migrations through the repository's container-aware task and test both
the resulting schema and affected application behavior.
