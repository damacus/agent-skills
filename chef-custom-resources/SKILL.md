---
name: chef-custom-resources
description: >
  Build, migrate, maintain, and test Chef Infra cookbooks using modern custom resource patterns
  for the sous-chefs organization. Use when: building a new Chef cookbook with custom resources,
  migrating legacy library-based resources to modern resources/, fixing CI failures in a
  sous-chefs cookbook, adding ChefSpec or InSpec tests, restructuring cookbook directories,
  writing resource documentation, converting sysvinit/upstart to systemd, or when the user
  mentions "custom resource", "chef resource", "sous-chefs cookbook", "fix cookbook CI",
  "cookbook structure", or "chef cookbook".
---

# Chef Custom Resources

Build and maintain Chef Infra cookbooks using modern custom resource patterns with full test
coverage and proper documentation.

## Helpers

The `bin/cookbook-helpers` script automates repetitive tasks. Run it from any cookbook directory.

| Command                                  | Purpose                                                 |
|------------------------------------------|---------------------------------------------------------|
| `cookbook-helpers platforms`             | Show current (non-EOL) platforms from endoflife.date    |
| `cookbook-helpers check-platforms [dir]` | Compare metadata.rb against current platform data       |
| `cookbook-helpers check-kitchen [dir]`   | Verify kitchen.yml and kitchen.dokken.yml are in sync   |
| `cookbook-helpers check-structure [dir]` | Validate cookbook directory layout and Ruby conventions |
| `cookbook-helpers generate-metadata`     | Output `supports` lines for metadata.rb                 |
| `cookbook-helpers generate-dokken`       | Output kitchen.dokken.yml platform entries              |
| `cookbook-helpers report [dir]`          | Full report: platforms + structure + kitchen sync       |

Script location: `~/.claude/skills/chef-custom-resources/bin/cookbook-helpers`

## Workflow

Execute these phases in order. Read the referenced file before starting each phase.

### Phase 1: Research

Read [references/research-phase.md](references/research-phase.md).

1. Run `cookbook-helpers platforms` to get current non-EOL platform versions
2. Identify the product being managed (e.g. MySQL, PostgreSQL, Redis)
3. Web-search vendor repositories for supported platforms and architectures
4. Note package availability per platform (apt vs dnf/yum)
5. Check for compiled/source installation requirements
6. Output findings to `LIMITATIONS.md` at the cookbook root

**Done when**: `LIMITATIONS.md` exists and documents vendor platform support, package availability, and any kernel/container limitations

### Phase 2: Structure

Read [references/cookbook-structure.md](references/cookbook-structure.md).

1. Run `cookbook-helpers check-structure` to validate the directory layout
2. Verify or create the required directory layout. Fix any structural issues
3. Run `cookbook-helpers generate-metadata` and `cookbook-helpers generate-dokken` to generate platform entries
4. Run `cookbook-helpers check-kitchen` to verify kitchen files are in sync

**Done when**: `cookbook-helpers check-structure` and `cookbook-helpers check-kitchen` both pass with no errors. No `recipes/` or `attributes/` directories exist. All test recipes start with bare `apt_update`

### Phase 3: Build / Migrate Resources

Read [references/custom-resource-patterns.md](references/custom-resource-patterns.md).

- **New cookbook**: Write custom resources in `resources/` using `unified_mode true`
- **Migration**: Convert class hierarchy in `libraries/` to flat resources in `resources/`
- **Maintenance**: Fix issues in existing resources, ensure patterns are current
- Extract shared properties into **resource partials** (`resources/_partial/`)
- Keep shared helper methods in `libraries/` modules, include via `action_class`
- Use `systemd_unit` for all service management — see [references/systemd-patterns.md](references/systemd-patterns.md)

**Done when**: All resources have `unified_mode true`, `provides`, and `frozen_string_literal: true`. No legacy LWRP/HWRP classes remain in `libraries/`. `cookstyle` passes with no offenses

### Phase 4: ChefSpec Tests

Read [references/chefspec-patterns.md](references/chefspec-patterns.md).

- Write `step_into` specs for every custom resource
- Write unit specs for helper modules in `libraries/`
- All specs live in `spec/`
- Run specs with `chef exec rspec`

**Done when**: `chef exec rspec` passes with 0 failures. Every resource and helper module has specs

### Phase 5: Integration Tests

Read [references/inspec-patterns.md](references/inspec-patterns.md).
For cookbooks needing kernel features (apparmor, selinux, firewall), read [references/exec-driver-patterns.md](references/exec-driver-patterns.md).

1. **Stale reference audit** (migration only): After Phase 3 deletes code, search `test/` for references to removed helpers, deleted recipes, old node attributes, and stale version strings. Fix or rewrite every file with stale references before writing new tests. Run: `rg 'removed_helper|old_recipe|deleted_attribute' test/`
2. Write test cookbook recipes in `test/cookbooks/test/recipes/` — one per kitchen suite
3. Write InSpec profiles in `test/integration/<suite>/` with `inspec.yml` + `controls/`
4. **Cross-validate**: For each kitchen suite, verify InSpec assertions match what the test recipe actually produces — check package names, versions, file paths, config keys, and service names
5. Configure `kitchen.yml` with YAML anchors for attribute reuse
6. If the cookbook needs kernel features, use the exec driver for those suites — not Dokken
7. Ensure a `default` suite exists that exercises the primary workflow

**Done when**: `kitchen.yml`, `kitchen.dokken.yml` (and `kitchen.exec.yml` if needed) are in sync. CI matrix matches all suite × platform combinations. Every suite has an InSpec profile with controls. No stale references remain in `test/`

### Phase 6: Documentation

Read [references/documentation-patterns.md](references/documentation-patterns.md).

Write `documentation/<cookbook_name>_<resource_name>.md` for every custom resource.

**Done when**: Every custom resource has a documentation file in `documentation/`. `markdownlint-cli2 '**/*.md'` passes

## Rules

- **Protected files**: **NEVER** modify `metadata.rb` or `CHANGELOG.md` — they are managed by the release system (release-please). Revert any changes to these files immediately
- **Conventional Commits**: All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `ci:`, `chore:`. Use `!` suffix for breaking changes (e.g. `feat!:`)
- **TDD**: Write failing test first, then implement
- **systemd only**: No sysvinit or upstart — remove if present
- **`unified_mode true`** on every resource
- **`provides :<resource_name>`** on every resource
- **Partials** for shared properties across resources
- **`frozen_string_literal: true`** at top of every Ruby file
- Chef version `>= 15.3` minimum (for `unified_mode` support)
- **Default suite required**: Every cookbook must have a `default` kitchen suite that exercises the primary workflow. The suite name must be `default`, run `recipe[test::default]`, and verify with `test/integration/default/`. During migration, create the `default` suite early — it is the smoke test that proves the new resources work end-to-end before adding specialized suites
- **Delete undoes create**: A resource's `:delete` (or `:remove`) action must remove **every** artifact that `:create` (or `:install`/`:start`) produces — files, directories, symlinks, systemd units, templates, and packages. Shared resources (users, groups) that other instances may depend on should not be removed
- **No `attributes/` directory**: Custom resource cookbooks use resource properties, not node attributes. During migration, delete `attributes/` entirely and convert attribute-driven logic to resource properties
- **No `recipes/` directory**: Custom resource cookbooks provide resources, not recipes. During migration, delete `recipes/` and move usage into test cookbook recipes (`test/cookbooks/test/recipes/`)
- **CI aligns with kitchen.yml**: The `.github/workflows/ci.yml` integration matrix must match every suite × platform combination defined in `kitchen.yml`. When suites or platforms change in `kitchen.yml`, update the CI matrix to match
- **`apt_update` in every test recipe**: Start every test cookbook recipe with bare `apt_update`. Dokken containers have stale apt caches — without this, package installs fail. No name argument or platform guard needed; the resource handles everything internally
- **Dead code pass after EOL removal**: After removing EOL platform guards, review every simplified method: if it now returns a constant, inline it at call sites and delete the method. If a case/if branch was removed, check if remaining branches collapse. Delete specs that tested removed code paths. Run `chef exec rspec` after each simplification
