---
name: migrate
description: >-
  Plan and verify a behaviour-preserving application, language or framework
  migration. Discover the existing product, resolve consequential differences
  with grilling, and define acceptance before implementation.
---

# Migrate

Deliver the existing product on the agreed target. Preserve behaviour, data and
presentation unless the owner approves a specific difference. A new framework
does not authorise new product rules, fields, layouts or a component library.

## Establish the reference

Read repository instructions and settled decisions. Apply
`adaptive-model-routing` to the uncertainty and consequence of discovery,
implementation and acceptance separately. Do not assign a fixed leader model.

Inspect source, tests, schemas, API contracts, assets and the running application.
Work out facts yourself. Compare conflicting sources instead of treating one as
automatically correct. The latest explicit owner decision defines approved change.

Build one compact migration record in the existing plan. Cover the affected
areas below, with evidence or a reason they do not apply:

| Area | Establish |
| --- | --- |
| Journeys and roles | Permissions, navigation, success and failure states |
| Business rules | Validation, calculations, timezones and concurrent writes |
| Data | Records, identities, schema, conversions, loss and rollback |
| UI | Layout, fonts, themes, assets, responsive and accessible interactions |
| Contracts | API/native consumers, errors, integrations, imports and exports |
| Background work | Jobs, schedules, retries, notifications and side effects |
| Runtime and cutover | Build, deployment, sessions, operations and rollback |
| Acceptance | Reference revision, fixtures, checks, comparisons and unknowns |

Use the record to expose missing coverage, not to invent work in every category.
Establish the overall boundaries once, then inspect only the next slice in detail.

## Resolve choices with grilling

Invoke `grilling` for contradictions or decisions with meaningful compatibility,
data, security or rework consequences. Present discovered evidence first.
Trace answers into dependent decisions. Separate evidenced facts, approved
differences and unresolved assumptions.

Do not ask the owner to describe working screens or infer approval from a general
"go ahead". Do not silently reproduce a discovered security defect. Bring the
specific conflict to the owner and continue independent work.

## Preserve the UI deliberately

For each visible journey, retain a baseline with source revision, synthetic
fixture, role, locale, timezone, theme and desktop/mobile viewport. Capture
important states: ordinary, empty, invalid, denied, loading and error where
relevant. Keep the evidence with the existing plan or repository screenshots.

Inspect and reuse existing CSS, fonts, icons, images, tokens, spacing, markup and
responsive behaviour. Name any real framework incompatibility before adapting.
Existing approved layouts remain the default. Choosing a UI library does not
approve changes to those layouts.

Derive acceptance from the reference before production code. Reuse equivalent
behavioural scenarios across runtimes with isolated data where practical.
Compare the actual replacement with the reference under equivalent conditions:
layout, hierarchy, content, menus, dialogs, keyboard/focus, validation,
save/cancel, refresh and persisted results.

Inspect side-by-side images or overlays and record the verdict. Capturing images
is insufficient. Fix material differences or obtain explicit approval. Never
rebaseline screenshots or weaken tests merely to accept an unexplained mismatch.

If the reference cannot run, retain available source and historical evidence,
state the missing proof, and continue independent work. Do not claim parity
until the required comparison is possible.

## Deliver through existing workflows

Use `slice` to define complete journeys. Use `team-planning` only for actual
ownership, dependency or resource coordination. Execute through
`team-slice-development`; all stages share the same brief.

Finish in-scope defects before expanding scope. Keep infrastructure prerequisites
separate from product acceptance. Passing tests, published code or a running
foundation does not establish that the migration is complete.

Acceptance requires the agreed journeys, approved differences, data boundaries,
UI comparisons and applicable checks to be evidenced. Preserve separate
authorisation for merging, deployment and destructive cutover.
