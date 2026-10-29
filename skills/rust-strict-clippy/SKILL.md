---
name: rust-strict-clippy
description: Apply a strict Clippy lint policy to a Rust codebase and drive it to zero warnings. Use when asked to tighten lints, enable pedantic/nursery/restriction lint groups, enforce unwrap/cast/indexing discipline, or replicate a strict lint setup in a Rust project.
---

# Rust strict Clippy rollout

Adopt a maximal lint policy while keeping the diff tractable. The strategy: enable everything, fix the crash-surface lints for real, and write documented exemptions where a lint fights the architecture.

## Workflow

1. **Measure first.** Run `cargo clippy --all-targets --message-format json` and group warnings by lint and by file. The distribution decides the plan, not guesswork.
2. **Add crate attributes.** Copy `assets/crate-attrs.rs` into the top of every crate root: `src/lib.rs`, `src/main.rs`, and every file in `tests/` (integration tests are separate crates — `cfg(test)` does not reach them).
3. **Write `clippy.toml`.** Start from `assets/clippy.toml`. Identify the project's config loader(s) and its deliberate process-exit point(s), then add `#[allow(clippy::disallowed_methods)]` with a one-line reason at those sites only.
4. **Scope `indexing_slicing` per module.** In files dominated by `serde_json::Value` object indexing (`payload["field"]` returns Null, never panics), add this header after any `//!` doc comments:

   ```rust
   // JSON object indexing returns Null for absent keys rather than panicking;
   // array-index sites remain to be audited.
   #![allow(clippy::indexing_slicing)]
   ```

   Fix indexing everywhere else (`get()`, `first()`, `let [x] = slice` patterns).
5. **Auto-fix, then triage.** Run `cargo clippy --fix`, review the diff, then fix in this order: `disallowed_methods` → `unwrap_used`/`expect_used` → `as_conversions`/cast lints → mechanical style. Site-level recipes are in `references/fix-patterns.md`.
6. **Documented allow > ugly code.** When a lint fights a deliberate design (mutex held across an await, `map_err` adapter owning its error), add `#[allow(clippy::<lint>)]` with a one-line reason at the smallest scope that works. Never allow silently.
7. **Verify.** `cargo fmt --all`, `cargo clippy --all-targets --locked -- -D warnings` (zero warnings), `cargo test` fully green. Commit separately from feature work; the diff should be lint-driven only.

## Policy summary

Warn: `pedantic`, `nursery`, `cargo`, plus restriction lints `unwrap_used`, `expect_used`, `panic`, `indexing_slicing`, `exit`, `dbg_macro`, `todo`, `unimplemented`, `unreachable`, `undocumented_unsafe_blocks`, `as_conversions`.

Allow globally, with a comment each: `multiple_crate_versions` (transitive deps), `missing_errors_doc`/`missing_panics_doc` (module docs carry intent on internal crates), `too_many_lines` (complexity lint covers it), `cargo_common_metadata` (license is a maintainer decision).

Allow under `cfg(test)`: `unwrap_used`, `expect_used`, `panic`, `indexing_slicing`, `unreachable`, `disallowed_methods`, `future_not_send`, `assert_is_empty`.

## Hard rules

- Never weaken semantics to silence a lint. Auth/crypto paths fail closed (return false/empty, never panic). Map unrepresentable sizes to "too large" (`usize::try_from(n).map_or(true, ...)`) rather than truncating.
- `write!`/`format_args!` into a `String` is infallible — end the statement with `.ok()`, never `.unwrap()`.
- Static regexes on literal patterns: prefer `LazyLock` statics; if an init unwrap remains, annotate `#[allow(clippy::unwrap_used)]` with the "compile-time-verified" reason.
- For trivial fieldless enums flagged by `needless_pass_by_value`, derive `Copy` instead of adding `&` parameters.
- If a lint flags genuinely complex structure (nested `if let` chains), extract a named helper rather than writing unreadable `map_or_else` pyramids.

## Expected scale

On a ~13k-line codebase this produced ~560 initial warnings, ~600 changed lines across 30 files, and a two-commit-sized review burden. Do not promise "fully strict, zero exemptions" — the documented allows are the policy's safety valve. Warn the user if the test suite is weak; it is the only net catching `clippy --fix` collateral.
