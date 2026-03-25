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

## Workflow

Execute these phases in order. Read the referenced file before starting each phase.

## Enforcement

- **Phase 0 is blocking**: You MUST NOT modify files, create commits, or open a PR until the user has explicitly confirmed whether the work is a **full custom resource migration** or **incremental modernization**
- **No silent scope downgrades**: If the cookbook is too large, risky, or messy to follow the structural rules in the chosen scope, stop and ask the user how to proceed. Do not quietly switch to an in-place or partial refactor
- **Every phase needs explicit evidence**: At the end of each phase, output a markdown checklist for that phase's "Done when" items and state how each item was verified in the current session (for example `ls`, `rg`, `cat`, `cookstyle`, `chef exec rspec`, `kitchen test`)
- **Verification gates action**: You MUST NOT invoke `@github-pr` until the outputs of `cookstyle`, `chef exec rspec`, and `kitchen test` have been shown in the current session
- **Structural audit before PR**: Before proposing or opening a PR, run a final structural audit and report the results, including `ls -R` output and confirmation that `recipes/` and `attributes/` are absent when the scope is Full Migration

### Phase 0: Scope

Before starting, clarify the scope with the user:

> "Should I do a **full custom resource migration** (delete recipes/, attributes/, rewrite as resources/) or **incremental modernization** (update existing patterns in place)?"

This avoids mid-session rework. If the user says "modernize", confirm which they mean.

Do not edit any files until the user has answered this question explicitly.

**Done when:** The user has explicitly confirmed `Full Migration` or `Incremental Modernization`, and you have repeated that scope back before making changes.

### Phase 1: Research

Read [references/research-phase.md](references/research-phase.md).

1. Identify the product being managed (e.g. MySQL, PostgreSQL, Redis)
2. Web-search vendor repositories for supported platforms and architectures
3. Note package availability per platform (apt vs dnf/yum)
4. Check for compiled/source installation requirements
5. Output findings to `LIMITATIONS.md` at the cookbook root

**Done when:** `LIMITATIONS.md` exists at cookbook root with vendor platform/arch data.

**Report before moving on:**

- [ ] `LIMITATIONS.md` exists at cookbook root
- [ ] Vendor platform and architecture support is captured
- [ ] Package/source-install constraints are captured

### Phase 2: Structure

Read [references/cookbook-structure.md](references/cookbook-structure.md).

Verify or create the required directory layout. Fix any structural issues.

**Done when:** Directory layout matches the reference, `metadata.rb` has correct `chef_version` and `supports`, `Berksfile` resolves cleanly (`berks install` exits 0), and any legacy `recipes/` or `attributes/` directories are removed (if full migration scope).

**Report before moving on:**

- [ ] Directory layout matches the reference
- [ ] `metadata.rb` has correct `chef_version` and `supports`
- [ ] `Berksfile` resolves cleanly
- [ ] `recipes/` is removed if Full Migration
- [ ] `attributes/` is removed if Full Migration

### Phase 2b: Platform Modernization

Verify all supported platforms are current using [endoflife.date](https://endoflife.date):

1. Check each platform in `metadata.rb` `supports` declarations against endoflife.date
2. Remove EOL platforms (e.g. Ubuntu 20.04, Debian 11, openSUSE Leap 15.5)
3. Add newly current platforms if vendor supports them (cross-reference with `LIMITATIONS.md`)
4. Update platform lists in **all** kitchen files — `kitchen.yml`, `kitchen.dokken.yml`, and CI matrix in `.github/workflows/ci.yml`

> **Keep platform lists in sync.** Changes to platforms in any kitchen file must be
> reflected in all others. Stale entries cause CI failures or silent test gaps.

**Done when:** No EOL platforms in `metadata.rb`, all kitchen files and CI matrix have matching platform lists.

**Report before moving on:**

- [ ] No EOL platforms remain in `metadata.rb`
- [ ] `kitchen.yml`, `kitchen.dokken.yml`, and CI matrix list the same platforms
- [ ] Platform changes are consistent with `LIMITATIONS.md`

### Phase 3: Build / Migrate Resources

Read [references/custom-resource-patterns.md](references/custom-resource-patterns.md).

- **New cookbook**: Write custom resources in `resources/` using `unified_mode true`
- **Migration**: Convert class hierarchy in `libraries/` to flat resources in `resources/`
- **Maintenance**: Fix issues in existing resources, ensure patterns are current
- Extract shared properties into **resource partials** (`resources/_partial/`)
- Keep shared helper methods in `libraries/` modules, include via `action_class`
- Use `systemd_unit` for all service management — see [references/systemd-patterns.md](references/systemd-patterns.md)
- **Run `cookstyle -a` frequently** during this phase to catch deprecations early (e.g. `yum_repository` uses `:remove` not `:delete`)

**Done when:** All resources compile (`chef exec ruby -c resources/*.rb`), `cookstyle` reports 0 offenses, and no legacy `libraries/` class hierarchy remains (if migration scope).

**Report before moving on:**

- [ ] Resources compile
- [ ] `cookstyle` reports 0 offenses
- [ ] Legacy `libraries/` class hierarchy is removed if Migration scope
- [ ] Shared properties moved to partials where appropriate

### Phase 4: ChefSpec Tests

Read [references/chefspec-patterns.md](references/chefspec-patterns.md).

- Write `step_into` specs for every custom resource
- Write unit specs for helper modules in `libraries/`
- All specs live in `spec/`
- Run specs with `chef exec rspec`

**Done when:** Every resource has at least one spec, `chef exec rspec` passes with 0 failures.

**Report before moving on:**

- [ ] Every resource has at least one spec
- [ ] Helper modules have unit coverage where needed
- [ ] `chef exec rspec` passes with 0 failures

### Phase 4b: Verify Unit Tests (MANDATORY)

Run verification before proceeding. **Do not skip this step.**

```bash
cookstyle
chef exec rspec --format documentation
```

Both commands must exit 0 with no failures. Fix any issues before moving on.
Use `cookstyle -a` to auto-correct style offenses, then re-run `chef exec rspec`.

**Done when:** `cookstyle` reports 0 offenses and `chef exec rspec` reports 0 failures.

**Report before moving on:**

- [ ] `cookstyle` output shared in the session
- [ ] `cookstyle` reports 0 offenses
- [ ] `chef exec rspec --format documentation` output shared in the session
- [ ] `chef exec rspec` reports 0 failures

### Phase 5: Integration Tests

Read [references/inspec-patterns.md](references/inspec-patterns.md).

- Write InSpec profiles in `test/integration/<suite>/`
- Use full profile structure with `inspec.yml` + `controls/` — **do not** use `supports` in `inspec.yml`
- Write test cookbook recipes in `test/cookbooks/test/recipes/`
- Configure `kitchen.yml` with YAML anchors for attribute reuse

**Done when:** Integration profiles exist for the required suites, test cookbook recipes exist under `test/cookbooks/test/recipes/`, and kitchen suites point at the matching test profiles.

**Report before moving on:**

- [ ] Required integration profiles exist
- [ ] Test cookbook recipes exist under `test/cookbooks/test/recipes/`
- [ ] Kitchen suites and verifier paths match the profiles

### Phase 5b: Verify Integration Tests (MANDATORY)

Run at least the default suite against one platform to confirm convergence and InSpec pass.

```bash
KITCHEN_LOCAL_YAML=kitchen.dokken.yml kitchen test default-ubuntu-2404 --destroy=always
```

If Docker/Dokken is not available, run with Vagrant:

```bash
kitchen test default-ubuntu-2404 --destroy=always
```

The suite must converge idempotently (two converges, zero updated resources on second) and all InSpec controls must pass. Fix any failures before moving on.

**Done when:** At least one suite passes `kitchen test` with idempotent convergence and all InSpec controls green.

**Report before moving on:**

- [ ] `kitchen test` output shared in the session
- [ ] At least one default suite passes
- [ ] Second converge is idempotent
- [ ] All InSpec controls are green

### Phase 6: Documentation

Read [references/documentation-patterns.md](references/documentation-patterns.md).

Write `documentation/<cookbook_name>_<resource_name>.md` for every custom resource.

**Done when:** Every resource in `resources/` has a corresponding doc file in `documentation/`.

**Report before moving on:**

- [ ] Every resource has documentation
- [ ] Documentation filenames match the expected pattern

### Phase 7: Propose Pull Request

All phases are complete. Ask the user:

> "All phases are done — resources modernized, tests passing, docs written. Would you like me to open a pull request now?"

Before asking, run a final structural audit:

```bash
ls -R
```

Use that audit to confirm the directory layout still matches the intended scope. In Full Migration mode, explicitly confirm that `recipes/` and `attributes/` are gone. Also confirm that the outputs of `cookstyle`, `chef exec rspec`, and `kitchen test` have already been shown in the current session.

If the user confirms, invoke the `@github-pr` skill to create the PR.

**Done when:** PR is opened with passing CI.

## Rules

- **TDD**: Write failing test first, then implement
- **Scope confirmation before edits**: Never modify files before the user explicitly confirms Full Migration or Incremental Modernization
- **Verify after every phase**: Run `cookstyle` and `chef exec rspec` after Phase 4. Run `kitchen test` after Phase 5. Never skip verification.
- **Report every "Done when" item**: At the end of each phase, output a markdown checklist showing each criterion and how it was verified in-session
- **Escalate complexity instead of drifting**: If following the declared scope would be too risky, too broad, or too expensive, ask the user for guidance instead of quietly reducing the scope
- **systemd only**: No sysvinit or upstart — remove if present
- **`unified_mode true`** on every resource
- **`provides :<resource_name>`** on every resource
- **Partials** for shared properties across resources
- **`frozen_string_literal: true`** at top of every Ruby file
- Chef version `>= 15.3` minimum (for `unified_mode` support)
- **Default suite required**: Every cookbook must have a `default` kitchen suite that exercises the primary workflow. The suite name must be `default`, run `recipe[test::default]`, and verify with `test/integration/default/`
- **Delete undoes create**: A resource's `:delete` (or `:remove`) action must remove **every** artifact that `:create` (or `:install`/`:start`) produces — files, directories, symlinks, systemd units, templates, and packages. Shared resources (users, groups) that other instances may depend on should not be removed
- **No `attributes/` directory**: Custom resource cookbooks use resource properties, not node attributes. During migration, delete `attributes/` entirely and convert attribute-driven logic to resource properties
- **No `recipes/` directory**: Custom resource cookbooks provide resources, not recipes. During migration, delete `recipes/` and move usage into test cookbook recipes (`test/cookbooks/test/recipes/`)
- **CI aligns with kitchen.yml**: The `.github/workflows/ci.yml` integration matrix must match every suite × platform combination defined in `kitchen.yml`. When suites or platforms change in `kitchen.yml`, update the CI matrix to match
- **Platform lists in sync**: `kitchen.yml`, `kitchen.dokken.yml`, and `.github/workflows/ci.yml` must all list the same platforms. When you change one, update all three
- **Run cookstyle early and often**: Run `cookstyle -a` after every batch of resource changes. It catches deprecations (e.g. `yum_repository :delete` → `:remove`) that are easy to miss
- **No `supports` in InSpec `inspec.yml`**: The `supports: platform-family:` filter silently skips profiles in Dokken containers. Omit it entirely
- **No lazy shell_out at compile time**: If a resource action needs `shell_out`, wrap it in a `lazy` block or move it inside a sub-resource's property. ChefSpec will reject compile-time `shell_out` calls
- **Diplomat resources**: Resources that depend on external gems (e.g. `diplomat`) should NOT use `step_into` in ChefSpec — test resource declaration only, not inner convergence
- **No PR before evidence**: Never invoke `@github-pr` until `cookstyle`, `chef exec rspec`, `kitchen test`, and the final structural audit have all been shown in the current session
