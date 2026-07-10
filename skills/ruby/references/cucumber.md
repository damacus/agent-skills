# Cucumber and Gherkin

Use Cucumber when the repository treats executable product examples as part of
its test strategy. Do not introduce it solely as another end-to-end test
runner.

## Detect the Suite

Inspect:

- `features/**/*.feature`;
- `features/step_definitions/` and `features/support/`;
- `config/cucumber.yml` or `cucumber.yml` profiles;
- `cucumber`, `cucumber-rails`, Capybara, and driver gems; and
- tags, hooks, World modules, database cleanup, and CI sharding.

Step definitions are matched by their expressions, not by which feature file
they sit beside. Search existing expressions before adding a new step to avoid
duplicates or ambiguity.

## Focused Execution

Prefer the repository's Mise, Task, or Rake entry point and configured profile.
When direct Cucumber execution is the established fallback, narrow by feature,
scenario line, name, or tag:

```sh
bundle exec cucumber features/path/example.feature
bundle exec cucumber features/path/example.feature:LINE
bundle exec cucumber --name 'scenario text'
bundle exec cucumber --tags '@tag'
```

Preserve required profiles and `--require` paths. Do not silently replace the
browser driver or execution environment.

## Gherkin Guidance

- Describe business behavior and outcomes in domain language.
- Prefer declarative steps over UI mechanics such as button selectors.
- Keep scenarios independent and understandable without reading step code.
- Use `Background` only for context shared by every scenario in the feature.
- Use Scenario Outlines for meaningful examples, not as a data-dump mechanism.
- Use tags for intentional selection or hooks; avoid an uncontrolled tag
  taxonomy.

## Step Definitions and State

- Reuse domain-level steps when their meaning is truly the same.
- Keep regex and Cucumber Expressions specific enough to avoid ambiguity.
- Store scenario state on the World instance or established helpers, never in
  globals shared between scenarios.
- Keep page objects, API clients, and setup helpers below the Gherkin layer when
  the repository already uses those abstractions.
- Diagnose undefined, ambiguous, pending, and flaky steps separately; adding a
  broad catch-all step usually makes the suite worse.
