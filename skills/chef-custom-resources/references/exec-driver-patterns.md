# Exec Driver Patterns

## When to Use the Exec Driver

Some cookbooks manage kernel-level features that **cannot run inside Docker/Dokken containers**.
Use the kitchen exec driver for these cookbooks:

- **apparmor** — requires kernel apparmor module
- **selinux** — requires kernel SELinux support
- **firewall / ufw** — requires netfilter/iptables kernel modules
- **Any cookbook that starts a systemd service requiring kernel features**
- **Windows-only cookbooks** — use `windows-latest` runners instead of Dokken

The exec driver runs Chef directly on the GitHub Actions runner host, which is a real
runner VM. Linux exec jobs usually run on Ubuntu; Windows exec jobs run on Windows.

## kitchen.exec.yml

```yaml
---
driver:
  name: exec

transport:
  name: exec

provisioner:
  name: chef_infra
  product_name: chef
  product_version: <%= ENV['CHEF_VERSION'] || 'latest' %>
  chef_license: accept-no-persist
  multiple_converge: 2
  enforce_idempotency: true
  deprecations_as_errors: true
  log_level: <%= ENV['CHEF_LOG_LEVEL'] || 'auto' %>

verifier:
  name: inspec

platforms:
  - name: ubuntu-22.04
  - name: ubuntu-24.04
```

Only list Ubuntu platforms for Linux exec jobs because the Linux GitHub Actions runner host is
Ubuntu. For Windows exec jobs, use a separate Kitchen file and list Windows runner platforms.

## Windows Exec Driver

Windows-only cookbooks should use a Windows runner and native Windows resources. Do not force these
cookbooks through Dokken or Linux platform parity.

```yaml
---
driver:
  name: exec

transport:
  name: exec

provisioner:
  name: chef_infra
  chef_license: accept-no-persist
  multiple_converge: 2
  enforce_idempotency: true
  deprecations_as_errors: true

verifier:
  name: inspec

platforms:
  - name: windows-latest
```

In GitHub Actions, run these jobs on `windows-latest` and pass the normalized Kitchen instance name
used by the cookbook's Windows Kitchen file.

## Instance Name Gotcha

Kitchen normalises dots in platform names when building instance IDs:

- Platform `ubuntu-24.04` → instance name `default-ubuntu-2404` (dots stripped)

The `actionshub/test-kitchen` action passes the `os` parameter directly to `kitchen test <suite>-<os>`.
So the CI matrix must use the **normalised** form:

```yaml
# Correct — matches kitchen instance name
os: ubuntu-2404

# Wrong — kitchen won't find this instance
os: ubuntu-24.04
```

## Split CI Workflow

Use two integration jobs: Dokken for container-safe suites, exec for kernel-dependent suites.

```yaml
jobs:
  integration-dokken:
    needs: lint-unit
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os:
          - debian-12
          - ubuntu-2204
          - ubuntu-2404
        suite:
          - disable  # suites that work in Docker
      fail-fast: false
    steps:
      - uses: actions/checkout@v5
      - uses: actionshub/chef-install@main
      - uses: actionshub/test-kitchen@main
        env:
          CHEF_LICENSE: accept-no-persist
          KITCHEN_LOCAL_YAML: kitchen.dokken.yml
        with:
          suite: ${{ matrix.suite }}
          os: ${{ matrix.os }}

  integration-exec:
    needs: lint-unit
    runs-on: ubuntu-latest
    strategy:
      matrix:
        suite:
          - default       # suites that need kernel features
          - policy-add
          - policy-remove
      fail-fast: false
    steps:
      - uses: actions/checkout@v5
      - uses: actionshub/chef-install@main
      - uses: actionshub/test-kitchen@main
        env:
          CHEF_LICENSE: accept-no-persist
          KITCHEN_LOCAL_YAML: kitchen.exec.yml
        with:
          suite: ${{ matrix.suite }}
          os: ubuntu-2404

  final:
    needs: [integration-dokken, integration-exec]
    runs-on: ubuntu-latest
    steps:
      - run: echo "done"
```

## InSpec and sudo

The exec driver runs InSpec as the unprivileged `runner` user on GitHub Actions.
Commands that require root (e.g. `apparmor_status`, `aa-status`, `iptables -L`) must
use `sudo` explicitly in InSpec controls:

```ruby
# Correct — works with exec driver (non-root user)
describe command('sudo apparmor_status') do
  its('stdout') { should match(/my_profile/) }
end

# Wrong — returns incomplete output without root
describe command('apparmor_status') do
  its('stdout') { should match(/my_profile/) }
end
```

This also works in Vagrant (sudo is a no-op when already root).
