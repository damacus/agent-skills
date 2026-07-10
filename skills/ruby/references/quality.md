# Quality Tools

Use only the tools configured by the repository or explicitly requested. A
Ruby project may use RuboCop, Standard, RubyCritic, Reek, syntax checks, or
custom tasks, and their responsibilities overlap without being identical.

## RuboCop and Standard

Inspect locked versions, `.rubocop.yml`, inherited configuration, plugins, and
task wrappers. Plugin loading and cop defaults vary by version.

Prefer checking changed files or the affected directory before the whole tree.
When direct execution is the established fallback:

```sh
bundle exec rubocop path/to/changed.rb
bundle exec standardrb path/to/changed.rb
ruby -c path/to/changed.rb
```

Use the repository's configured command when it differs. Inspect offenses
before autocorrecting. Safe correction may still create a large unrelated
diff; unsafe correction needs explicit justification and review.

Do not rewrite style configuration or generate a todo file just to make a task
pass.

## RubyCritic and Reek

Run RubyCritic or Reek only when already configured, explicitly requested, or
materially useful for a refactoring assessment. Do not install them, require a
universal score, or turn every Ruby edit into a metrics exercise.

Interpret results in context:

- complexity can reveal risky decision paths;
- duplication can reveal or merely resemble a missing abstraction;
- churn increases the value of clarity and tests;
- smell reports are hypotheses to inspect, not automatic defects; and
- generated, DSL-heavy, migration, and test code may need different thresholds.

Prefer a before/after comparison for the changed scope over an arbitrary global
grade. Refactor because the code becomes easier to understand or change, not
merely to satisfy a number.

## Completion

Run the quality checks that cover edited files and required project gates. A
full-tree lint is appropriate for broad config or formatter changes, but not
automatically for a tiny isolated edit.
