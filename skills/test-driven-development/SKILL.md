---
name: test-driven-development
description: >
  Use an opt-in, project-aware test-driven development loop for a feature,
  defect, or behavior change. Detects the repository's test framework and
  commands instead of assuming Rails, RSpec, or a direct host executable.
---

# Test-Driven Development

Use this skill when the user explicitly requests TDD or test-first work. Follow
the repository's framework, test levels, fixtures or factories, command
wrappers, and container boundary.

## Establish the Behavior

Describe one observable behavior and choose the lowest test level that gives
useful confidence. Start at a public boundary when the change spans multiple
components, but do not duplicate the same behavior at every layer without a
risk-based reason.

For an existing defect, first add a focused regression test that reproduces
the failure. For legacy code without protection, characterization tests may be
the safest first step. Never delete or discard existing user code merely
because it was written before a test.

## Red, Green, Refactor

1. Write the smallest test that expresses the next behavior.
2. Run the narrowest supported project command and confirm the test fails for
   the expected reason rather than syntax, setup, or environment failure.
3. Make the smallest production change that satisfies that behavior.
4. Re-run the focused test and directly affected checks.
5. Refactor only while the relevant tests remain green.
6. Repeat, widening verification when shared behavior or project policy
   warrants it.

One method does not automatically require one test. Test meaningful contracts,
branches, boundaries, and failure modes. Prefer real deterministic values;
mock slow or external boundaries according to repository conventions rather
than mocking every collaborator.

Exploratory code can be useful for learning. Treat it as disposable only when
the user agrees and it does not overwrite valuable work. Do not install test
tools, change suite policy, or run a huge suite without task-specific need.

## Completion

Report which tests were observed failing and passing, what wider checks ran,
and what remains unverified. Test-first evidence improves confidence but does
not replace code review, security judgment, or production-safe rollout.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source]
`test-driven-development` skill at revision `f2cb97d`. Distributed under the
accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
