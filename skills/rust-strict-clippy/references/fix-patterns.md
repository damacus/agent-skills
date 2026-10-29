# Strict-Clippy fix recipes

Load this when fixing non-obvious lint sites. Each pattern preserves semantics; do not blindly apply clippy's suggestion when it would weaken error handling.

## unwrap / expect

- **Mutex caches:** recover poisoned guards — `mutex.lock().unwrap_or_else(PoisonError::into_inner)`. Cache data is discardable; a panic in a long-running daemon is not.
- **HMAC/keyed crypto construction** (`Hmac::new_from_slice` returns Result but accepts any key length): switch to `let Ok(mac) = ... else { return false }` (verify paths) or `Option`-returning helpers (issue paths). Fail closed; never panic in auth.
- **Header/cookie parsing on known-ASCII values:** `if let Ok(v) = value.parse() { headers.insert(name, v) }` — skip rather than panic.
- **`chars().next().unwrap()` inside a `while` loop:** `let Some(c) = rest.chars().next() else { break };`
- **`existing.unwrap()` guarded by a boolean flag:** replace the flag-guarded match arm with `let Some(x) = &opt else { return ... };` inside the arm body.
- **Static `Regex::new`:** `LazyLock` statics (also fixes per-call recompilation). Keep `.unwrap()` under `#[allow(clippy::unwrap_used)]` with a "compile-time-verified literal pattern" comment — a static init panic is acceptable fail-fast.

## Casts (`as_conversions`, `cast_*`)

- `n as usize` size limits where n is u64: `usize::try_from(n).map_or(true, |s| s > limit)` — unrepresentable = too large (fail-safe direction).
- `i64 as u64` on clamped values: `u64::try_from(x.max(0)).unwrap_or_default()`.
- `len() as i64`: `i64::try_from(x.len())?` in Result-returning fns.
- `as_secs() as i64` timestamps: `i64::try_from(d.as_secs()).unwrap_or(i64::MAX)`.
- Retry/backoff from DB counts: `u32::try_from(attempts).unwrap_or(u32::MAX)` — corrupt values map to max backoff, matching prior wrap-then-clamp semantics.
- Large literals gain separators: `1_420_070_400_000`.

## Collections / headers

- `collect::<Vec<_>>()` used only for `len() == 1` + `[0]`: iterate — `let token = it.next()?; it.next().is_none().then_some(token)`. This kills `needless_collect`, `indexing_slicing`, and `question_mark` in one move.
- `format!` per item + `.collect::<String>()`: `iter().fold(String::new(), |mut out, x| { write!(out, "...").ok(); out })`.
- `push_str(&format!(...))`: `write!(s, "...").ok()` (`use std::fmt::Write as _;`).
- Hex encoding via `map(|b| format!("{b:02x}")).collect()`: `char::from_digit(u32::from(b >> 4), 16).unwrap_or('0')` in a fold — no per-item alloc, no indexing.

## Control flow

- `map(...).unwrap_or(default)` → `map_or(default, f)`. `or(expensive_call())` → `or_else(|| ...)`. `.unwrap_or(f())` → `.unwrap_or_else(f)`.
- `let x = match r { Ok(v) => v, Err(_) => ... }` → `let Ok(x) = r else { ... };` or `r.unwrap_or_else(|_| ...)`.
- Identical match arms: merge with or-patterns, including tuple arms — `(A, "x" | "y") | (B, "z") => ...`. If one duplicate is `_ =>`, delete the specific arm and list the ignored cases in a comment.
- `Some("known") | _ =>` trips `wildcard_in_or_patterns` — write plain `_` and put the known names in a comment.
- Nested `if let ... else if let ... else` chains (3+ ways with captures): extract a named helper with early returns instead of `map_or_else` pyramids.
- `needless_pass_by_value` on small fieldless enums: derive `Copy` on the enum (semver-visible for public types, but correct for closed 2–4 variant enums). Delete resulting `x.clone()` calls (`clone_on_copy` then applies).
- `needless_pass_by_value` on `map_err` adapters and deliberate API choices: `#[allow]` with a comment; do not churn call sites.
- `items_after_statements`: hoist `use`/`const` items — `const` to the top of the fn or module scope, `use` to file imports.
- `significant_drop_tightening` when the guard is intentionally held across an await (e.g. serialising a fetch): `#[allow]` on the enclosing fn with the reason — the suggestion is a correctness regression.
- `future_not_send` in test code: covered by the `cfg(test)` allow list. In production async code it is a real bug — fix, don't allow.
- `unchecked_time_subtraction`: `Instant::now().checked_sub(d).unwrap()` in tests; `.unwrap_or_else(Instant::now)` in production.
- `assert_is_empty`/`assert!(x.len() == n)` in tests: covered by the test allow list; prefer `is_empty()` anyway when touching the line.

## Config / process boundaries

- `env::var` outside the config loader: move it into the loader, or if a CLI task legitimately needs a minimal env var (e.g. a database URL without full platform config), annotate `#[allow(clippy::disallowed_methods)]` with "tasks intentionally require only X".
- `process::exit` at the deliberate supervision point: annotate on the enclosing statement/fn.
