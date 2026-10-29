---
name: progress-report
description: >-
  Create and update a readable HTML progress report for a project, migration or
  multi-agent delivery. Use when the user needs every slice, completed/total
  scores, evidence and concrete next actions. Uses authoritative JSON data and
  a bundled Python renderer with a compact human-facing layout.
---

# Progress Report

Keep one machine-readable JSON source and generate HTML for people. Write plain
UK English. Preserve the bundled visual style, with a very short preamble, an
explicit evidence snapshot time and expandable checklists.

## Create or update a report

1. Read the existing JSON and current evidence. Confirm the full goal and any
   separate first-release boundary. Ask only material unresolved questions.
2. Start from [example.json](examples/example.json) and follow the
   [input format](references/input-format.md). JSON is authoritative; do not
   maintain a second Markdown ledger or hand-edit the generated HTML.
3. Keep slice IDs, item IDs, scopes and boundaries stable. Keep deferred work in
   the full goal. Explain any denominator change in `limitations`.
4. Update delivery states only from evidence, retaining its observation time,
   revision and source. Set the timezone-qualified `snapshot_at` and
   `snapshot_timezone`. Reformatting or rendering does not refresh evidence.
5. Keep `headline` brief and `summary` to one short sentence. Put detailed work,
   remaining tasks and next actions in checklist items, once. Do not add repeated
   “What works”, “What remains”, “What closes this slice” or next-action sections.
6. Render with JSON and HTML beside each other:

   ```sh
   python3 scripts/render.py /absolute/path/report.json /absolute/path/report.html
   ```

7. Open the HTML. Inspect desktop and narrow layouts, expand a checklist and
   inspect print behaviour when supported. State any preview limitation. Keep
   source evidence and limitations in their disclosure, not the preamble.

For an existing Markdown report, convert its records to the documented JSON
shape, preserve IDs and dated evidence, compare scores, then retire Markdown as
an active input. Keep the old file only as a labelled historical archive.

## Scoring and delivery states

An item earns one point only when implementation is complete, publication is
published, and both local and hosted checks passed or are evidenced as not
required. Partial work earns no point. Positive states need evidence references;
not-required checks need an explanation of why the check does not apply.

Record implementation, local checks, publication, hosted checks, acceptance,
merge and deployment separately. Whole-slice acceptance requires its own
evidence, even when every item earns a point. Unknown means pending.

Derive scores and navigation from the JSON records. Never store competing
handwritten totals. Items differ in size: do not average into a percentage or
predict a completion date. Show a separate first-release count from explicit
scope. Deferred full-goal work stays visible; counts do not declare release ready.

## Bundled files and validation

- [Renderer](scripts/render.py): Python standard library; validates required
  fields, IDs, states, snapshot time and evidence references.
- [Template](assets/report.html), [styles](assets/report.css) and
  [checklist styles](assets/checklist.css): sidebar, scores, expandable checklist
  tables, responsive layout and print expansion. Detailed delivery states remain
  inside each checklist. Slice acceptance criteria are nested there too.
- [JSON example](examples/example.json) and [HTML example](examples/example.html):
  fictional data demonstrating the format.
- [Retained historical design](references/medtracker-migration-status.html):
  historical reference only; its verbose sections are not the current template.

Do not add a report-generator test suite or testing project. Render the example
and inspect the result. Check representative invalid inputs with the renderer.
Before publishing skill changes, run repository `task test`, lint this skill's
Markdown, check its local links, render the example and run `git diff --check`.
The repository task alone does not cover all of those checks.
