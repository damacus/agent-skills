---
name: modernize
description: |
  Modernize codebases by checking EOL runtimes/platforms and upgrading dependencies with minimal context.
  Use for "modernize", "upgrade dependencies", "update versions", "check EOL", or ecosystem-specific
  updates for npm/Node, Ruby gems, Chef cookbooks, and Rust crates. For other ecosystems, ask which
  technology-specific guidance to use before loading more.
---

# Modernize Skill

Modernize only the technologies the task needs. Keep the initial pass to detection,
target selection, small edits, and validation.

## Load Policy

1. Identify the requested or discovered technology from filenames and manifests.
2. Read only the matching reference file(s). If a task spans multiple technologies,
   load only those technologies.
3. For unsupported ecosystems, ask the user which technology guidance to apply before
   loading broader context.
4. Use `references/eol-api.md` only when checking runtime, OS, platform, database,
   tool, or application lifecycle status.
5. Use `references/common-products.md` only when product IDs are unclear.
6. Use `scripts/check_eol.py` without reading it unless its behavior needs to change.

## Technology Routing

| Technology | Load when you see | Reference |
|------------|-------------------|-----------|
| npm/Node | `package.json`, `package-lock.json`, `npm-shrinkwrap.json`, `yarn.lock`, `pnpm-lock.yaml`, `.nvmrc`, `.node-version` | `references/npm.md` |
| Ruby gems | `Gemfile`, `Gemfile.lock`, `*.gemspec`, `.ruby-version` | `references/ruby-gems.md` |
| Chef cookbooks | `metadata.rb`, `Berksfile`, `Policyfile.rb`, `kitchen*.yml`, `recipes/`, `resources/`, `cookstyle` | `references/chef-cookbooks.md` |
| Rust crates | `Cargo.toml`, `Cargo.lock`, `rust-toolchain*`, `.cargo/` | `references/rust-crates.md` |
| EOL products | Docker base images, CI matrices, Kitchen platforms, language version files, database/app/tool versions | `references/eol-api.md` |

## Core Workflow

1. Scan for manifests and version declarations.
2. Load only the selected technology reference(s).
3. Check current versions, EOL status, and available supported targets.
4. Prefer small, reviewable upgrades that respect existing constraints and package managers.
5. Update manifests, lockfiles, CI, Docker, or Kitchen files as needed.
6. Run the validation commands appropriate to the changed technology.
