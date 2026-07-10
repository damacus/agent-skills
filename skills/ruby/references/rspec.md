# RSpec

Use this reference only when RSpec is configured or the task explicitly asks
for RSpec guidance. Read `.rspec`, `spec_helper.rb`, `rails_helper.rb`, support
files, and nearby examples before writing a spec.

## Focused Execution

Prefer the project's wrapper. When direct RSpec execution is the established
fallback, useful selectors include:

```sh
bundle exec rspec spec/path/example_spec.rb
bundle exec rspec spec/path/example_spec.rb:LINE
bundle exec rspec -e 'example description'
bundle exec rspec --tag focus
```

Confirm configured formatters, profiles, tags, and parallel runners before
adding flags. Re-run randomized failures with their seed.

## Writing Specs

- Describe behavior and context, not the implementation sequence.
- Follow local choices for `subject`, `let`, hooks, shared examples, aggregate
  failures, factories, and fixtures.
- Keep setup visible enough that the failure is understandable.
- Use request specs for HTTP behavior and system specs for browser behavior
  when that matches the repository; do not convert test types gratuitously.
- Prefer verifying doubles such as `instance_double` when a real interface is
  available.
- Avoid `allow_any_instance_of`, `expect_any_instance_of`, and long
  `receive_message_chain` stubs unless constrained legacy code leaves no safer
  boundary.
- Prefer asserting a returned value or state transition over expecting every
  internal message.

## Rails Integration

Detect `rspec-rails` and the repository's inferred spec types. Preserve its
authentication helpers, Active Job adapter, database cleaning strategy,
Capybara driver, and metadata hooks. A generic RSpec recipe must not override
Rails application configuration.

## Failure Diagnosis

Read the first meaningful failure, including shared-context and hook output.
Run that example alone, inspect its fixture/factory state, then widen only if
the failure depends on order, global state, or suite configuration.
