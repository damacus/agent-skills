# JSON report input

Use [the complete example](../examples/example.json). JSON is the sole editable
data source; HTML is generated. Keep both files in the same directory.

## Top-level fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1` |
| `project`, `report` | Nonempty display names |
| `headline` | Short headline |
| `summary` | One short sentence; no history or repeated checklist details |
| `snapshot_at` | ISO 8601 evidence snapshot with UTC offset |
| `snapshot_timezone` | IANA display zone, e.g. `Europe/London` |
| `release_boundary` | First-release boundary and separate acceptance gates |
| `limitations` | Missing proof, scope changes and evidence limitations |
| `slices` | Nonempty array of slice records |
| `evidence` | Object keyed by stable evidence ID |

Snapshot time describes evidence freshness, not when HTML was rendered. Do not
advance it for a formatting-only change. Historical evidence retains its own
observation time. Additional descriptive metadata is allowed; it does not alter
scoring and is not automatically shown.

## Slices and items

Each slice has `id`, `title`, `acceptance`, `acceptance_criteria` and a nonempty
`items` array. Acceptance is a state object with status passed, pending or failed.
Every slice and item ID must be unique across the report and match
`[A-Za-z][A-Za-z0-9_-]*`.

Each item has `id`, `title`, `scope`, `states`, `works`, `remaining` and
`next_action`. Scope is `first-release` or `full-goal`. The final three fields are
nonempty strings or JSON `null`; null means no recorded text, not completion.

The `states` object requires exactly these seven keys:

| Key | Allowed statuses |
| --- | --- |
| `implementation` | complete, in-progress, not-started |
| `local_checks` | passed, pending, failed, not-required |
| `publication` | published, unpublished |
| `hosted_checks` | passed, pending, failed, not-required |
| `acceptance` | passed, pending, failed, not-required |
| `merge` | merged, unmerged |
| `deployment` | deployed, not-deployed |

Every state is an object, for example:

```json
{"status": "passed", "evidence_ids": ["runner-ci"]}
```

All references must resolve in `evidence`. Complete, passed, not-required,
published, merged and deployed require at least one reference. Other states may
use an empty array. A passed slice needs every item to earn a point, plus its
separate acceptance evidence. Do not store a `done` flag or manual score.

## Evidence and prose

Every evidence record requires nonempty `title`, `observed_at`, `revision`,
`source` and `note`. Use ISO 8601 with offset for new observations. When migrating
historical evidence that lacks an exact time, preserve its original observed
text rather than inventing precision; the renderer retains that wording.

Sources may be HTTP/HTTPS links, local paths or file links. No credentials or
temporary signed URLs. Prefer durable references. The note states exactly what
was checked; never reuse an old passing run for changed work without justification.

Prose supports paragraphs, simple lists, bold, inline code and Markdown links.
HTML is escaped. Keep each fact in its item; the template does not repeat item
work/remaining/next prose outside the expandable checklist. Evidence and release
limitations have their own collapsed disclosure.
