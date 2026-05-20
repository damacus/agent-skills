# Rust Crate Modernization

Use this for Rust toolchain and crate dependency modernization.

## Detect

- Toolchain: `rust-toolchain`, `rust-toolchain.toml`, CI matrices, Docker tags.
- Dependencies: `Cargo.toml`, workspace manifests, `Cargo.lock`, `.cargo/config.toml`.
- Scope: single crate, workspace member, dependency group, or toolchain edition.

## Inspect

```bash
cargo metadata --format-version 1
cargo tree
cargo tree -d
cargo update --dry-run
```

If installed, `cargo outdated` and `cargo audit` are useful but do not add them as
required project dependencies unless the user asks.

Use `references/eol-api.md` for Rust runtime/toolchain lifecycle checks.

## Update

- Preserve workspace structure and dependency source choices.
- Prefer `cargo update -p <crate>` for focused lockfile updates.
- Edit version requirements in `Cargo.toml` only when the requested target needs it
  or the existing constraint blocks the update.
- Treat Rust edition changes as a separate migration unless explicitly requested.
- For libraries, consider minimum supported Rust version before raising toolchains.

## Validate

Run `cargo fmt --check`, `cargo check`, `cargo test`, and `cargo clippy` when available
and proportional to the change. For workspaces, include `--workspace` when that matches
the repo's existing pattern.
