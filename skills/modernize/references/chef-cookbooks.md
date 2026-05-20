# Chef Cookbook Modernization

Use this for Chef Infra cookbooks, cookbook dependencies, Test Kitchen platforms,
ChefSpec, InSpec, and cookbook CI.

## Detect

- Cookbook metadata: `metadata.rb`, `Berksfile`, `Policyfile.rb`.
- Runtime/platforms: `kitchen*.yml`, `.github/workflows/`, Docker images.
- Cookbook code: `resources/`, `recipes/`, `libraries/`, `attributes/`.
- Tests: `spec/unit/`, `test/integration/`, `test/cookbooks/`.

Use `eol-api.md` for platform and Chef Infra Client lifecycle checks.

## Architecture Rules

- Prefer custom resources over recipe-based APIs in the main cookbook.
- Test cookbooks under `test/cookbooks/` may use recipes to exercise resources; do
  not remove them just because recipes are discouraged in the main cookbook.
- Extract common properties shared across three or more resources into
  `resources/_partial/` and include them with `use`.
- Centralize platform-specific logic in `libraries/helpers.rb`.
- Minimize node attributes; prefer resource properties.

## Native Resources

Prefer built-in Chef resources over cookbook dependencies:

| Instead of | Prefer |
|------------|--------|
| `ark` cookbook | `remote_file` plus `archive_file` |
| Template for systemd units | `systemd_unit` |
| `poise-service` | native `service` or `systemd_unit` |

Service accounts should use `shell '/usr/sbin/nologin'` and `system true` unless the
service genuinely needs an interactive shell.

## Test Kitchen

- Define `suites:` in `kitchen.yml` only.
- Let `kitchen.dokken.yml` override driver, transport, provisioner, and platforms.
- Use Dokken images with systemd via `pid_one_command: /usr/lib/systemd/systemd`.
- Do not delete test recipes or Kitchen suites; suites usually map to recipes, such
  as suite `source-28` to `recipe[test::source_28]`.

Supported platform targets commonly include:

```yaml
platforms:
  - name: almalinux-8
  - name: almalinux-9
  - name: amazonlinux-2023
  - name: centos-stream-9
  - name: debian-12
  - name: fedora-latest
  - name: rockylinux-8
  - name: rockylinux-9
  - name: ubuntu-22.04
  - name: ubuntu-24.04
```

CI matrix names may use `ubuntu-2204` and `ubuntu-2404` depending on existing
workflow conventions.

## Documentation

- Create `documentation/<resource_name>.md` for each custom resource.
- Include actions, properties, and examples.
- Update `README.md` links to resource documentation.

## Testing

- ChefSpec: test each resource in `spec/unit/resources/`; use `step_into` for
  resource internals.
- Kitchen: integration suites use test cookbook recipes in `test/cookbooks/`.
- InSpec: keep controls focused on externally visible behavior after convergence.
- Run the repo's existing task runner, Cookstyle, ChefSpec, and Kitchen commands when
  proportional to the change.

## Dependency Management

- Minimize external cookbook dependencies.
- Remove version pins unless they protect known compatibility constraints.
- Prefer cookbooks that expose custom resources over recipe-only cookbooks.
