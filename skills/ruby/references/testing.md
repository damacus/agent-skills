# Testing Strategy

Use the framework and conventions already present in the repository. Ruby
projects may use RSpec, Minitest, Cucumber, or several of them together.

## Detect Before Writing

Inspect the locked gems, test directories, helper files, task wrappers, and
nearby tests. Also detect supporting tools such as Capybara, FactoryBot,
fixtures, Mocha, WebMock, VCR, time helpers, Shoulda Matchers, test-prof, and
parallel runners.

Match the existing choice of:

- test level and file placement;
- setup, fixtures, factories, and helper modules;
- assertion or expectation style;
- mocking boundaries;
- database cleanup and parallelization; and
- descriptive naming and shared behavior.

Do not introduce a second style merely because it is familiar.

## Choose the Smallest Useful Test

Test observable behavior at the lowest level that provides confidence:

- unit or model tests for focused domain behavior;
- request/integration tests for HTTP and component boundaries;
- job, mailer, channel, or command tests for their public contracts;
- system tests for browser behavior; and
- Cucumber scenarios for executable product behavior when the repository uses
  that collaboration style.

Avoid duplicating the same assertion through every layer without a risk-based
reason.

## Fast Feedback Ladder

Run checks in this order where practical:

1. the failing example, test method, or scenario;
2. its file or nearest subsystem;
3. tests for directly affected callers and boundaries;
4. relevant lint, types, security, and coverage checks; and
5. the full suite only when the change is broad, repository policy requires it,
   or focused checks cannot expose the main regression risk.

Use the repository's Mise, Task, or Rake wrapper and its supported filtering
mechanism. Do not start a suite of thousands of tests merely to validate one
branch of behavior.

## Test Quality

- Assert outcomes and collaborations that form the public contract.
- Prefer deterministic inputs; control time, randomness, network, and jobs at
  established boundaries.
- Use real value objects freely; mock slow or external collaborators, not every
  internal method.
- Add regression tests that fail for the reported defect before relying on the
  fix.
- Preserve useful failure messages and avoid assertions that can pass for the
  wrong reason.
- Reproduce randomized failures with the reported seed.

Watch for four recurring test smells:

- **Obscure tests** hide essential setup or intent far from the assertion.
- **Fragile tests** fail when unrelated shared setup or implementation details
  change.
- **Erratic tests** depend on order, time, asynchronous races, leaked state, or
  uncontrolled external systems.
- **Test hooks** put test-only branches or behavior into production code.

A coverage increase is evidence of execution, not proof that behavior is well
specified. Use [coverage.md](coverage.md) when coverage itself is in scope.
