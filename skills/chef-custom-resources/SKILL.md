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

- **Read-only triage is allowed before Phase 0**: When the user asks to find, rank, or assess
  candidate cookbooks, inspect only. Do not modify cookbook files during triage.
- **Classify before scoping**: For triage work, every cookbook must be classified as
  `MIGRATE`, `DEPRECATE`, or `NEEDS OWNER DECISION` before Phase 0. Use this classification
  to decide whether to start migration planning, write a deprecation recommendation, or ask for
  ownership/product direction.
- **Phase 0 is blocking for cookbook changes**: You MUST NOT modify cookbook files, create commits, or open a PR until the user has explicitly confirmed whether the work is a **full custom resource migration** or **incremental modernization**
- **No silent scope downgrades**: If the cookbook is too large, risky, or messy to follow the structural rules in the chosen scope, stop and ask the user how to proceed. Do not quietly switch to an in-place or partial refactor
- **Every phase needs explicit evidence**: At the end of each phase, output a markdown checklist for that phase's "Done when" items and state how each item was verified in the current session (for example `ls`, `rg`, `cat`, `cookstyle`, `chef exec rspec`, `kitchen test`)
- **Verification gates action**: You MUST NOT invoke `@github-pr` until the outputs of `cookstyle`, `chef exec rspec`, and `kitchen test` have been shown in the current session
- **Structural audit before PR**: Before proposing or opening a PR, run a final structural audit and report the results, including `ls -R` output and confirmation that `recipes/` and `attributes/` are absent when the scope is Full Migration

### Phase -1: Read-only Triage

Use this phase when the user asks which cookbooks should be migrated, deprecated, or assessed.
This phase is non-mutating and can run before Phase 0.

1. Inventory public API surface:
   - `recipes/`
   - `attributes/`
   - `definitions/`
   - `libraries/` providers/resources/classes/helpers
   - `resources/`
   - README-documented recipes, attributes, resources, and examples
2. Audit existing resources for:
   - missing `provides`
   - missing `unified_mode true`
   - missing `# frozen_string_literal: true`
   - old `load_current_resource`
   - direct `run_action`
   - global `Chef::Resource.include` / `Chef::DSL::Recipe.include`
   - node attribute reads inside resources that should become properties
   - compile-time `shell_out`
   - missing `:delete` / `:remove` semantics for artifacts created by `:create`
3. Audit test and CI readiness:
   - resource `step_into` ChefSpec coverage
   - default Kitchen suite
   - test cookbook recipes under `test/cookbooks/test/recipes/`
   - InSpec profiles using `inspec.yml` + `controls/`
   - absence of `supports` filters in InSpec profiles
   - drift between `metadata.rb`, Kitchen files, and CI matrix
4. Classify each cookbook:
   - `MIGRATE`: product/domain remains useful and a custom-resource API is the desired public surface
   - `DEPRECATE`: cookbook is too thin, product is obsolete, upstream packaging is stale, or the
     functionality is better handled directly by built-in Chef resources
   - `NEEDS OWNER DECISION`: product viability, external service ownership, or compatibility goals
     are unclear enough that migration work would encode the wrong public API

**Done when:** Each inspected cookbook has a `MIGRATE`, `DEPRECATE`, or `NEEDS OWNER DECISION`
classification with the evidence that drove it.

**Report before moving on:**

- [ ] Public API surface was inventoried
- [ ] Existing resources were audited for modern custom resource patterns
- [ ] Test and CI readiness was checked
- [ ] Each cookbook was classified as `MIGRATE`, `DEPRECATE`, or `NEEDS OWNER DECISION`
- [ ] Any skill guidance gaps found during triage were listed

### Phase 0: Scope

Before starting, clarify the scope with the user:

> "Should I do a **full custom resource migration** (delete recipes/, attributes/, rewrite as resources/) or **incremental modernization** (update existing patterns in place)?"

This avoids mid-session rework. If the user says "modernize", confirm which they mean.

Do not edit cookbook files until the user has answered this question explicitly.

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
5. **CI vs Local Strategy**:
    - **Default**: Use `kitchen.dokken.yml` (Docker) for both CI and local testing.
    - **Hypervisor Fallback**: If the cookbook requires a hypervisor (Vagrant) for local testing, CI must pivot to the `exec` driver in `kitchen.exec.yml` on `ubuntu-latest`.
    - **Cleanup**: If Dokken is not viable for the cookbook's requirements, remove `kitchen.dokken.yml` entirely to prevent drift.

> **Preserve existing support unless explicitly changed.** For an existing cookbook,
> platform modernization must preserve all currently supported, non-EOL platforms
> unless Phase 1 evidence shows they are no longer supportable or the user
> explicitly approves removing them. Aligning CI with another cookbook means
> matching workflow structure, not copying that cookbook's platform matrix or
> silently narrowing support.

> **Keep platform lists in sync.** Changes to platforms in any kitchen file must be
> reflected in all others. Stale entries cause CI failures or silent test gaps.

**Done when:** No EOL platforms in `metadata.rb`, all kitchen files and CI matrix have matching platform lists.

**Report before moving on:**

- [ ] No EOL platforms remain in `metadata.rb`
- [ ] `kitchen.yml`, `kitchen.dokken.yml`, and CI matrix list the same platforms
- [ ] Platform changes are consistent with `LIMITATIONS.md`
- [ ] CI driver strategy (Dokken vs Exec) aligns with local hypervisor requirements

### Phase 2c: sous-chefs CI Baseline

Normalize GitHub Actions before deep migration work. This avoids red PRs caused by org workflow
contract drift rather than cookbook code.

1. Use `sous-chefs/.github/.github/actions/install-workstation@6.0.0` to install Cinc
   Workstation in CI
2. Do **not** configure `chefworkstation` in Kitchen YAML; use `chef` or leave the provisioner
   install setting blank, depending on the existing cookbook pattern
3. Pin sous-chefs reusable workflows to `@6.0.0` unless the user explicitly asks for `main`
4. For `release-cookbook.yml@6.0.0`, pass all required secrets:
   `token`, `supermarket_user`, `supermarket_key`, `slack_bot_token`, and `slack_channel_id`
5. If reusable workflow validation fails with missing permissions, add the caller-level permissions
   requested by the nested workflow, especially `pull-requests: write` for prevent-file-change
6. Keep lint configuration current: yamllint enabled, markdownlint enabled, markdown lists use `*`,
   `no-multiple-blanks.maximum: 2`, and ignore `.github/copilot-instructions.md` plus `.windsurf/**`

**Done when:** CI workflow files call the current sous-chefs actions/workflows correctly and validate
without missing secret, permission, yamllint, or markdownlint failures.

**Report before moving on:**

- [ ] Cinc Workstation is installed via `install-workstation@6.0.0`
- [ ] Kitchen YAML does not use `chefworkstation`
- [ ] Reusable workflows are pinned to `@6.0.0`
- [ ] Release workflow passes all required secrets
- [ ] Caller workflow permissions satisfy nested workflow requirements
- [ ] yamllint and markdownlint configuration matches sous-chefs conventions

### Phase 3: Build / Migrate Resources

Read [references/custom-resource-patterns.md](references/custom-resource-patterns.md).

- **New cookbook**: Write custom resources in `resources/` using `unified_mode true`
- **Migration**: Convert class hierarchy in `libraries/` to flat resources in `resources/`
- **Recipe/attribute migration**: Convert recipe behavior to resource actions and node attributes
  to resource properties. Do not leave compatibility recipes or attributes in a Full Migration
  unless the user explicitly chooses Incremental Modernization.
- **Repo-wrapper cookbooks**: Convert repository recipes and attribute hashes to explicit resources
  that wrap `apt_repository`, `yum_repository`, or `dnf_module` as appropriate. Preserve public
  repo names, generated URLs, GPG keys, stock repo file deletion, and enable/disable defaults in
  properties or helper methods.
- **Maintenance**: Fix issues in existing resources, ensure patterns are current
- Extract shared properties into **resource partials** (`resources/_partial/`)
- Keep shared helper methods in `libraries/` modules, include via `action_class`
- Use `systemd_unit` for Linux systemd service management — see [references/systemd-patterns.md](references/systemd-patterns.md). For Windows-only cookbooks, use platform-native resources such as `windows_package`, `registry_key`, `windows_path`, `service`, `powershell_script`, and IIS resources as appropriate.
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

For attribute-to-resource migrations, also write `migration.md` at the cookbook root and link it
from `README.md`. The migration guide must explain the breaking change from node attributes and
recipes to resource properties and test cookbook examples.

**Done when:** Every resource in `resources/` has a corresponding doc file in `documentation/`, and
full migrations include a linked `migration.md`.

**Report before moving on:**

- [ ] Every resource has documentation
- [ ] Documentation filenames match the expected pattern
- [ ] Full migrations include `migration.md`
- [ ] `README.md` links to `migration.md`

### Phase 7: Propose Pull Request

All phases are complete. Ask the user:

> "All phases are done — resources modernized, tests passing, docs written. Would you like me to open a pull request now?"

Before asking, run a final structural audit:

```bash
ls -R
```

Use that audit to confirm the directory layout still matches the intended scope. In Full Migration mode, explicitly confirm that `recipes/` and `attributes/` are gone. Also confirm that the outputs of `cookstyle`, `chef exec rspec`, and `kitchen test` have already been shown in the current session.

For full migrations, the PR title and commit subject must use a breaking conventional commit such
as `feat!: migrate <cookbook> to custom resources`. Do not use `refactor:` for attribute-to-resource
migrations because release-please must create a major version bump.

If the user confirms, invoke the `@github-pr` skill to create the PR.

**Done when:** PR is opened with passing CI.

## Rules

- **CI triage for active runs**: When diagnosing a GitHub Actions failure that is still `in_progress`, do not rely on `gh run view ... --log`; it often withholds logs until the run completes. Use `bin/gh-ci-job-logs <run-url-or-id>` to fetch raw job logs via `gh api` instead
- **Check Kitchen instance normalization**: If CI says `No instances for regex ...`, compare the workflow-generated instance names with `kitchen list`. Ubuntu instances are commonly normalized from `ubuntu-22.04` / `ubuntu-24.04` to `ubuntu-2204` / `ubuntu-2404`
- **TDD**: Write failing test first, then implement
- **Scope confirmation before edits**: Never modify files before the user explicitly confirms Full Migration or Incremental Modernization
- **Verify after every phase**: Run `cookstyle` and `chef exec rspec` after Phase 4. Run `kitchen test` after Phase 5. Never skip verification.
- **Local Chef workstation setup**: If local commands cannot find Chef/Cinc binaries, add `.mise.toml` with `[env]` and `_.path = "/opt/chef-workstation/bin"`, then run `mise trust`
- **Report every "Done when" item**: At the end of each phase, output a markdown checklist showing each criterion and how it was verified in-session
- **Escalate complexity instead of drifting**: If following the declared scope would be too risky, too broad, or too expensive, ask the user for guidance instead of quietly reducing the scope
- **No silent support narrowing**: For existing cookbooks, do not remove a currently supported non-EOL platform from `metadata.rb`, Kitchen, CI, docs, or helper logic unless Phase 1 evidence shows it is no longer supportable or the user explicitly approves dropping it
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
- **CI aligns with kitchen.yml**: The `.github/workflows/ci.yml` integration matrix must match every suite × platform combination defined in `kitchen.yml` (or `kitchen.exec.yml` for CI). When suites or platforms change, update the CI matrix to match.
- **CI vs Local Split**: When a hypervisor (Vagrant) is required for local testing, maintain `kitchen.yml` for local use and `kitchen.exec.yml` for CI. Use `ubuntu-latest` for CI.
- **Windows CI Split**: Windows-only cookbooks may use `kitchen.exec.yml` or `kitchen.windows.yml`
  on `windows-latest`. Do not force Dokken or Linux platform parity onto Windows-only cookbooks.
- **Runner Optimization**: In `kitchen.exec.yml`, always set `chef_omnibus_install: false` to use the pre-installed Chef on GitHub runners and avoid `sudo` password prompts. Ensure `sudo: true` is set for resources managing system services.
- **Platform lists in sync**: `kitchen.yml`, `kitchen.dokken.yml` (if used), and `.github/workflows/ci.yml` must all list the same platforms. When you change one, update all three
- **All Kitchen files count**: Include `kitchen.global.yml`, `kitchen.exec.yml`, `kitchen.windows.yml`,
  and any suite-specific Kitchen files in platform and verifier audits when they exist.
- **Run cookstyle early and often**: Run `cookstyle -a` after every batch of resource changes. It catches deprecations (e.g. `yum_repository :delete` → `:remove`) that are easy to miss
- **No `supports` in InSpec `inspec.yml`**: The `supports: platform-family:` filter silently skips profiles in Dokken containers. Omit it entirely
- **No lazy shell_out at compile time**: If a resource action needs `shell_out`, wrap it in a `lazy` block or move it inside a sub-resource's property. ChefSpec will reject compile-time `shell_out` calls
- **Diplomat resources**: Resources that depend on external gems (e.g. `diplomat`) should NOT use `step_into` in ChefSpec — test resource declaration only, not inner convergence
- **No PR before evidence**: Never invoke `@github-pr` until `cookstyle`, `chef exec rspec`, `kitchen test`, and the final structural audit have all been shown in the current session
- **Breaking migration PRs use `feat!`**: Attribute-to-resource migrations remove public node attributes and recipes, so they require a breaking conventional commit/PR title to force a major release
