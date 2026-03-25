---
name: modernize
description: |
  Modernize codebases by checking and updating EOL (end-of-life) versions using endoflife.date API.
  Use when: (1) Updating OS versions in CI/CD, Docker, or Kitchen configs, (2) Checking if dependencies
  are EOL or deprecated, (3) Updating tool versions (Ruby, Python, Node.js, etc.), (4) Modernizing
  application versions (Confluence, HAProxy, databases), (5) Auditing a project for outdated components,
  (6) User asks to "modernize", "update versions", "check EOL", or "upgrade dependencies".
---

# Modernize Skill

Check and update end-of-life versions using the endoflife.date API.

## Workflow

### 1. Identify Version Sources

Scan the codebase for version declarations:

```text
kitchen*.yml          - OS platforms (ubuntu-20.04, centos-7, etc.)
.github/workflows/    - CI matrix OS and tool versions
Dockerfile            - Base images, tool versions
docker-compose*.yml   - Service versions
Gemfile               - Ruby version, gem versions
.ruby-version         - Ruby version
.python-version       - Python version
.nvmrc, .node-version - Node.js version
metadata.rb           - Chef cookbook dependencies
Berksfile             - Cookbook versions
requirements.txt      - Python packages
package.json          - Node.js packages
go.mod                - Go version
```

### 2. Check EOL Status

Use the endoflife.date API to check each product:

```bash
# Check single product
curl -s "https://endoflife.date/api/v1/products/ubuntu" | jq '.releases[] | {name, isEol, eolFrom}'

# Check specific version
curl -s "https://endoflife.date/api/v1/products/ubuntu/releases/20.04" | jq '{name, isEol, eolFrom, latest}'

# Get latest supported release
curl -s "https://endoflife.date/api/v1/products/ubuntu/releases/latest" | jq '{name, isLts, latest}'
```

Or use the bundled script:

```bash
python3 scripts/check_eol.py ubuntu:20.04 ruby:3.1 nodejs:18
python3 scripts/check_eol.py --search postgres
python3 scripts/check_eol.py --list
```

### 3. Determine Upgrade Targets

For each EOL or soon-EOL version:

1. Query supported versions from API
2. Prefer LTS releases when available
3. Consider compatibility constraints
4. Document breaking changes

### 4. Apply Updates

Update version declarations in identified files. Common patterns:

**Kitchen platforms:**

```yaml
platforms:
  - name: ubuntu-24.04  # was ubuntu-20.04
  - name: debian-12     # was debian-10
```

**GitHub Actions matrix:**

```yaml
matrix:
  os: [ubuntu-24.04, ubuntu-22.04]  # drop EOL versions
  ruby: ['3.2', '3.3']              # update to supported
```

**Dockerfile:**

```dockerfile
FROM ruby:3.3-slim  # was ruby:3.0
```

### 5. Validate Changes

After updates:

- Run linters and tests
- Check for deprecation warnings
- Verify CI passes on new versions

## API Quick Reference

**Always use v1**: `https://endoflife.date/api/v1` (docs: https://endoflife.date/docs/api/v1/)

> **Note**: v1 responses wrap data in a `result` key. Use `.result` in jq queries.

| Endpoint                                | Description               |
|-----------------------------------------|---------------------------|
| `GET /products`                         | List all products         |
| `GET /products/{name}`                  | Product with all releases |
| `GET /products/{name}/releases/latest`  | Latest release cycle      |
| `GET /products/{name}/releases/{cycle}` | Specific release          |

```bash
# All non-EOL releases for a product
curl -s "https://endoflife.date/api/v1/products/haproxy" | jq '.result.releases[] | select(.isEol == false) | {name, latest: .latest.name, eolFrom}'

# Latest release (check isLts for LTS)
curl -s "https://endoflife.date/api/v1/products/haproxy/releases/latest" | jq '.result | {name, latest: .latest.name, isLts, eolFrom}'

# Specific cycle
curl -s "https://endoflife.date/api/v1/products/ubuntu/releases/22.04" | jq '.result | {name, isEol, eolFrom, isLts}'
```

Key response fields: `isEol`, `eolFrom`, `isLts`, `latest.name`, `releaseDate`

## Common Product IDs

See [references/common-products.md](references/common-products.md) for full list.

**OS:** `ubuntu`, `debian`, `rhel`, `centos-stream`, `rocky-linux`, `almalinux`, `amazon-linux`

**Languages:** `ruby`, `python`, `nodejs`, `go`, `php`, `java`

**Databases:** `postgresql`, `mysql`, `mariadb`, `redis`, `mongodb`

**Tools:** `chef-infra-client`, `ansible`, `terraform`, `kubernetes`, `docker-engine`

**Apps:** `confluence`, `jira-software`, `haproxy`, `nginx`, `apache`

## Chef Cookbook Modernization Rules

When modernizing Chef cookbooks, follow these best practices:

### Architecture

- **Custom Resources over Recipes**: Prefer custom resources over recipe-based approaches in the main cookbook (`./recipes/`). Test cookbooks under `test/cookbooks/` use recipes to exercise resources — these are expected and should NOT be removed
- **Resource Partials**: Extract common properties shared across 3+ resources into `resources/_partial/` files using the `use` directive
- **Helpers Module**: Centralize platform-specific logic in `libraries/helpers.rb`
- **No Node Attributes**: Minimize reliance on node attributes; use resource properties instead

### Resource Design

```ruby
# resources/_partial/_common_properties.rb
property :install_path, String,
         default: lazy { default_install_path },
         description: 'Installation directory'

# resources/install.rb
use '_partial/_common_properties'
```

### Native Resources

Prefer built-in Chef resources over cookbook dependencies:

| Instead of           | Use                                |
|----------------------|------------------------------------|
| `ark` cookbook       | `remote_file` + `archive_file`     |
| Template for systemd | `systemd_unit` resource            |
| `poise-service`      | Native `service` or `systemd_unit` |

### Service Accounts

```ruby
user 'myapp' do
  shell '/usr/sbin/nologin'  # NOT /bin/bash
  system true
end
```

### Test Kitchen Configuration

- Define `suites:` in `kitchen.yml` only (not duplicated in `kitchen.dokken.yml`)
- `kitchen.dokken.yml` should only override driver/transport/provisioner and platforms
- Use Dokken images with systemd: `pid_one_command: /usr/lib/systemd/systemd`

### Platform Support

Check EOL status for all platforms in `kitchen*.yml` and `metadata.rb`:

```yaml
# kitchen.dokken.yml - supported platforms
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

### CI/CD Matrix

Expand platform coverage in `.github/workflows/ci.yml`:

```yaml
matrix:
  os:
    - almalinux-8
    - almalinux-9
    - amazonlinux-2023
    - centos-stream-9
    - debian-12
    - fedora-latest
    - rockylinux-8
    - rockylinux-9
    - ubuntu-2204
    - ubuntu-2404
  suite:
    - default
    - standalone
```

### Documentation

- Create `documentation/<resource_name>.md` for each custom resource
- Include: Actions, Properties table, Examples
- Update `README.md` to link to resource documentation

### Testing

- **RSpec**: Test each resource in `spec/unit/resources/`
- **ChefSpec**: Use `step_into` to test resource internals
- **Kitchen**: Integration tests use test cookbook recipes in `test/cookbooks/test/recipes/`
- **NEVER delete test recipes or kitchen suites** — they exercise the cookbook's resources in different configurations (source builds, config variations, SSL, Lua, etc.)
- Each kitchen suite maps to a test recipe: suite `source-28` → `recipe[test::source_28]`
- ChefSpec tests unit-level behaviour; kitchen suites test real convergence — both are needed

### Dependency Management

- Minimize external cookbook dependencies
- Remove version pins unless absolutely necessary
- Prefer cookbooks that use custom resources over recipe-based ones
