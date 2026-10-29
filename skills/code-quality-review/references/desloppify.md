# Desloppify execution

Verified against the PyPI `desloppify` 1.0 CLI and installed runner source on
28 October 2026. Recheck help at use time; do not rely on a moving upstream guide
over the installed version. Record the resolved version, then pin it for the run
and any comparable rescan. `uvx` isolates the Python tool; it does not make
Desloppify itself read-only.

## External workspace

Create one external run directory containing `source/` (the disposable snapshot),
`artifacts/`, `baseline-existing/`, `baseline-mechanical/` and `architecture/`.
Use a separate source-only copy for the blind architect when scan outputs might
otherwise be visible. Never point a writable tool at the original source path.
Keep uv cache/tool/Python installation directories outside the target too.

## Preflight detector and build tools

Desloppify 1.0 prefers an installed `jscpd` executable. If absent but `npx` is
present, its adapter executes `npx --yes jscpd` with a 120-second subprocess
timeout. A restricted network/cache can therefore make the duplication phase
appear stalled while npm tries to obtain the package. `uvx --offline` only applies
to uv; it does not make this nested npx invocation offline. Do not mistake that
wait for expensive analysis or silently disable duplication.

Check `jscpd --version` before scanning. If needed and authorised, provision a
pinned jscpd in an **external** tooling directory, verify its version, and prepend
that directory's `node_modules/.bin` to the scan's PATH. For example, validation
used `npm install --prefix /scratch/tools --cache /scratch/npm-cache --no-audit
--no-fund --ignore-scripts jscpd@5.4.2`. Resolve an appropriate current version
when creating a new tool environment; record/pin it for comparable scans. Never
install into the target, rely on an uncontrolled implicit download, or change the
target's package files. If provisioning is unavailable, record incomplete
duplication coverage and the setup blocker.

Inspect native tool output/cache configuration too. In Rust, `CARGO_TARGET_DIR`
alone may not control the user-configured `build.build-dir`. Set
`CARGO_BUILD_BUILD_DIR` to an external scratch intermediates path when supported
by that Cargo version. Pass both overrides to Desloppify's child checks and the
native checks. Verify their actual paths from command evidence; do not change
global Cargo configuration. Preserve failed setup logs before a corrected fresh
scan and explain the environment/configuration difference in score comparisons.

Inspect help before using the command sequence. These are fish examples; set
`review_run` to the external run directory and `review_version` to the observed
version. Apply RTK prefixes where installed; it is a local convention, not a
dependency of Desloppify.

```fish
rtk proxy uvx --from desloppify desloppify --version
rtk proxy uvx --from "desloppify==$review_version" desloppify scan --help
rtk proxy uvx --from "desloppify==$review_version" desloppify review --help
```

After moving into the disposable source root, run for each coherent project,
using a verified language override if auto-detection would mix projects:

```fish
rtk proxy uvx --from "desloppify==$review_version" desloppify scan --path . --profile objective --no-badge
rtk proxy uvx --from "desloppify==$review_version" desloppify status --json > "$review_run/artifacts/mechanical-status.json"
rtk proxy uvx --from "desloppify==$review_version" desloppify review --prepare --path . --no-retrospective
rtk proxy uvx --from "desloppify==$review_version" desloppify review --run-batches --runner codex --dry-run --path . --no-retrospective
```

Capture stdout, stderr and exit codes separately for every command. Preserve the
first state and status before generating/importing reviews. If a scan gate blocks
fresh collection, investigate copied history and use a fresh isolated run; do not
silently force completion or falsely attest that a queue was drained. `ci` omits
subjective work and cannot replace the steps below. Do not use `--skip-slow` by
default. Disclose skipped/unsupported/failed detectors and missing optional tools.
Set a finite per-command timeout appropriate to the profile before execution.
Track the exact owned process/session; stop only that process tree on timeout,
save partial logs and mark the affected detector/scan incomplete. Do not leave a
stalled scan running or silently replace it with a reduced scan called complete.

## Complete the subjective batches without hidden model routing

The verified 1.0 built-in Codex runner constructs `codex exec --ephemeral` with a
reasoning effort environment override, but **does not set a model or service tier**.
Its defaults include Low effort and workspace-write sandbox. Consequently,
`--runner codex` alone does not meet this skill's model/tier or read-only guarantees.
There is no verified `DESLOPPIFY_CODEX_MODEL` control in that runner. Do not invent
one, or start automatic batches hoping they inherit the desired settings.

Use `--dry-run` to generate the installed version's prompts and immutable blind
packet without launching its runner. Read the generated run manifest/prompt
locations. Dispatch **every** batch through capability-checked fresh Sol High
sessions, using the actual prompt, blind packet, output schema and source copy.
Withhold score history and the owner's mechanical conclusions from these reviewers.
The generated blind packet may include mechanical navigation signals by design;
retain its original schema and treat those signals only as source-reading leads.
The independent architect receives neither the packet nor those signals. Track all
batches and dimensions, including failed/timed-out ones; preparation is not execution.

Merge using the installed version's generated contract. Preserve per-batch outputs
and packet identity; resolve duplicate findings with source evidence. Do not
invent zero scores, fill missing dimensions or invent provenance to pass validation.
Preflight `review --validate-import <merged.json>` with the same intended trust
flags as import, then import into scratch state only.
Preserve dismissed concern records too: the generated schema may allow a minimal
`concern_verdict: "dismissed"`, fingerprint and reasoning object without the full
defect fields. Validate it using that version's concern contract rather than
discarding it as a malformed defect. Keep dismissals in the false-positive ledger.

For manually dispatched sessions, ordinary imports may accept findings without
trusting scores. Keep scores untrusted if no supported provenance route exists.
If the installed version requires `--manual-override --attest` to import those
assessment scores, use it only with a truthful description of how the blind
reviews actually ran and label the resulting scores **provisional/manual**. They
can expire on the next scan. Never assert a trusted internal or Claude external
session happened when it did not. Do not use `--allow-partial` to disguise missing
coverage. Keep validated full raw assessments in the report even if score import
is unavailable; label the import/score limitation clearly.

Capture post-import status and copy post-review state to a separate artifact.
Do not automatically rescan after import: it can invalidate provisional scores
and obscures comparison with the saved mechanical baseline. Rescans require the
same scope/version/configuration and a separately recorded purpose.

## Sources

- [Upstream README](https://github.com/peteromallet/desloppify/blob/main/README.md)
- [Upstream Codex overlay](https://github.com/peteromallet/desloppify/blob/main/docs/CODEX.md)
- [Codex batch runner source](https://github.com/peteromallet/desloppify/blob/main/desloppify/app/commands/runner/codex_batch.py)
- [PyPI package](https://pypi.org/project/desloppify/)

Prefer installed `--help` and the matching version's source when upstream changes.
