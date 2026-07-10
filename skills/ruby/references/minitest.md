# Minitest

Minitest supports class-based tests, spec-style tests, and benchmarks. Detect
which style the repository uses instead of translating RSpec habits into it.
Rails projects commonly build on Minitest through `ActiveSupport::TestCase` and
Rails-specific integration and system test classes.

## Detect the Local Contract

Inspect `test/test_helper.rb`, `test/application_system_test_case.rb`, custom
helpers, fixtures, factories, parallelization, and the test tasks. Identify
whether tests use:

- `Minitest::Test` methods and assertions;
- Minitest spec syntax;
- Rails test classes and fixtures;
- Mocha or another mocking extension; or
- custom reporters, plugins, or parallel runners.

## Focused Execution

Prefer the repository wrapper or Rake task. When a direct fallback is
appropriate, Minitest can run a single file and filter test names:

```sh
bundle exec ruby -Itest test/path/example_test.rb
bundle exec ruby -Itest test/path/example_test.rb --name /pattern/
```

Minitest Rake tasks may expose their own filter variables. Inspect the task or
its help instead of assuming a variable name. Reproduce order-dependent
failures with the reported seed.

## Writing Tests

- Follow the local assertion style and naming pattern.
- Keep `setup` focused; use helper methods or modules for genuinely shared
  behavior.
- Use `assert_changes`, `assert_difference`, job helpers, time helpers, and
  other Rails assertions only when the locked Rails version provides them.
- Prefer a real collaborator when it is cheap and deterministic; stub external
  boundaries using the project's existing mocking library.
- Keep fixtures and factories consistent with the rest of the suite.
- Account for parallel tests when touching global state, files, ports, or
  shared database records.

Do not add RSpec-style DSLs, FactoryBot, or a new mocking gem merely to make a
Minitest test resemble another project.
