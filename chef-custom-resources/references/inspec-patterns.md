# InSpec Patterns

## Table of Contents

- [InSpec Patterns](#inspec-patterns)
	- [Table of Contents](#table-of-contents)
	- [Profile Structure](#profile-structure)
	- [inspec.yml Profile File](#inspecyml-profile-file)
		- [Depending on shared profiles](#depending-on-shared-profiles)
	- [Controls Structure](#controls-structure)
		- [Control naming convention](#control-naming-convention)
	- [Shared Helpers](#shared-helpers)
	- [Kitchen Configuration](#kitchen-configuration)
		- [YAML anchors for attribute reuse](#yaml-anchors-for-attribute-reuse)
		- [kitchen.dokken.yml for CI](#kitchendokkenyml-for-ci)
	- [Common InSpec Resources](#common-inspec-resources)
		- [systemd\_service](#systemd_service)
		- [port](#port)
		- [file](#file)
		- [directory](#directory)
		- [package](#package)
		- [command](#command)
		- [user and group](#user-and-group)
	- [Test Cookbook Recipes](#test-cookbook-recipes)
	- [Migration: Stale Reference Audit](#migration-stale-reference-audit)
		- [What to search for](#what-to-search-for)
		- [Common stale patterns](#common-stale-patterns)
		- [Cross-validation checklist](#cross-validation-checklist)

## Profile Structure

Every integration test suite uses the full InSpec profile structure:

```text
test/
├── cookbooks/
│   └── test/
│       ├── metadata.rb
│       └── recipes/
│           ├── default.rb        # Primary smoke test recipe (required)
│           └── client.rb
└── integration/
    ├── default/                   # Required — matches the default kitchen suite
    │   ├── inspec.yml
    │   └── controls/
    │       └── default_spec.rb
    ├── client/
    │   ├── inspec.yml
    │   └── controls/
    │       └── client_spec.rb
    └── common/
        ├── inspec.yml
        └── controls/
            └── common_spec.rb
```

**Every cookbook must have a `default` suite.** The `default` suite exercises the
primary workflow (install, configure, start, verify) and is the first suite that
must pass before expanding to additional suites.

## inspec.yml Profile File

Every suite directory needs an `inspec.yml`:

```yaml
# test/integration/smoke/inspec.yml
---
name: smoke
title: Smoke Tests
maintainer: Sous Chefs
license: Apache-2.0
summary: Smoke tests for the cookbook
version: 1.0.0
supports:
  - platform-family: debian
  - platform-family: rhel
  - platform-family: fedora
  - platform-family: suse
```

### Depending on shared profiles

```yaml
# test/integration/smoke/inspec.yml
---
name: smoke
title: Smoke Tests
version: 1.0.0
depends:
  - name: common
    path: test/integration/common
```

Then in controls:

```ruby
# test/integration/smoke/controls/smoke_spec.rb
include_controls 'common'
```

## Controls Structure

Controls go in `controls/` subdirectory, not loose in the suite directory:

```ruby
# test/integration/smoke/controls/smoke_spec.rb
# frozen_string_literal: true

title 'Smoke Tests'

control 'myapp-service-01' do
  impact 1.0
  title 'Service is running'
  desc 'The myapp service should be enabled and running'

  describe systemd_service('myapp') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
  end
end

control 'myapp-config-01' do
  impact 0.7
  title 'Configuration file exists'

  describe file('/etc/myapp/my.cnf') do
    it { should exist }
    its('mode') { should cmp '0600' }
    its('owner') { should eq 'myapp' }
    its('group') { should eq 'myapp' }
  end
end
```

### Control naming convention

Use `<cookbook>-<area>-<number>` format:

- `mysql-service-01`
- `mysql-config-01`
- `mysql-client-01`
- `mysql-database-01`

## Shared Helpers

For shared helper methods across suites, use a common file:

```ruby
# test/integration/spec_helper.rb
# frozen_string_literal: true

def myapp_bin
  '/usr/bin/myapp'
end

def myapp_config_dir
  '/etc/myapp'
end

def myapp_query(query, database = 'myapp')
  "#{myapp_bin} --defaults-extra-file=#{myapp_config_dir}/.my.cnf -D #{database} -e \"#{query}\""
end
```

Reference from controls:

```ruby
# test/integration/smoke/controls/smoke_spec.rb
require_relative '../../spec_helper'
```

## Kitchen Configuration

### YAML anchors for attribute reuse

```yaml
# kitchen.yml

# Reusable YAML anchors for run_lists
x-run_lists:
  smoke: &smoke_run_list
    - recipe[test::smoke]
  client: &client_run_list
    - recipe[test::client]

# Reusable YAML anchors for attributes
x-attributes:
  version_lts: &lts_attrs
    myapp_test:
      version: "8.4"
  version_latest: &latest_attrs
    myapp_test:
      version: "9.0"

# Reusable YAML anchors for verifiers
x-verifiers:
  smoke: &smoke_verifier
    inspec_tests:
      - path: test/integration/smoke

suites:
  - name: smoke-lts
    run_list: *smoke_run_list
    attributes: *lts_attrs
    verifier: *smoke_verifier

  - name: smoke-latest
    run_list: *smoke_run_list
    attributes: *latest_attrs
    verifier: *smoke_verifier

  - name: client
    run_list: *client_run_list
    attributes: *lts_attrs
    verifier:
      inspec_tests:
        - path: test/integration/client
```

### kitchen.dokken.yml for CI

Contains **only** driver and platform definitions — no suites:

```yaml
# kitchen.dokken.yml
---
driver:
  name: dokken
  privileged: true
  chef_image: chef/chefworkstation
  chef_version: current

transport:
  name: dokken

provisioner:
  name: dokken

platforms:
  - name: almalinux-9
    driver:
      image: dokken/almalinux-9
  - name: debian-12
    driver:
      image: dokken/debian-12
  - name: ubuntu-24.04
    driver:
      image: dokken/ubuntu-24.04
```

Suites are inherited from `kitchen.yml`.

## Common InSpec Resources

### systemd_service

```ruby
describe systemd_service('myapp') do
  it { should be_installed }
  it { should be_enabled }
  it { should be_running }
end
```

### port

```ruby
describe port(3306) do
  it { should be_listening }
  its('protocols') { should include 'tcp' }
end
```

### file

```ruby
describe file('/etc/myapp/my.cnf') do
  it { should exist }
  it { should be_file }
  its('mode') { should cmp '0600' }
  its('owner') { should eq 'myapp' }
  its('content') { should match(/bind-address/) }
end
```

### directory

```ruby
describe directory('/var/lib/myapp') do
  it { should exist }
  its('mode') { should cmp '0750' }
  its('owner') { should eq 'myapp' }
end
```

### package

```ruby
describe package('myapp-server') do
  it { should be_installed }
  its('version') { should match(/8\.4/) }
end
```

### command

```ruby
describe command('myapp --version') do
  its('exit_status') { should eq 0 }
  its('stdout') { should match(/8\.4/) }
end
```

### user and group

```ruby
describe user('myapp') do
  it { should exist }
  its('group') { should eq 'myapp' }
end
```

## Test Cookbook Recipes

Test recipes live in `test/cookbooks/test/recipes/` and exercise the cookbook's resources:

```ruby
# test/cookbooks/test/metadata.rb
name 'test'
depends 'myapp'
```

```ruby
# test/cookbooks/test/recipes/smoke.rb

# Always include apt_update at the top of every test recipe.
# Dokken containers have stale apt caches — without this, package installs
# fail with exit code 100. The resource is a no-op on non-Debian platforms.
# No name argument or platform guard needed.
apt_update

myapp_service 'default' do
  version node['myapp_test']['version']
  port 3306
  action [:create, :start]
end

myapp_config 'default' do
  instance 'default'
  source 'my.cnf.erb'
  action :create
  notifies :restart, 'myapp_service[default]'
end
```

Use `node['<cookbook>_test']` attributes so values can be set from `kitchen.yml`.

## Migration: Stale Reference Audit

After deleting `recipes/`, `attributes/`, or removing global helper includes (Phase 3), existing
test files may reference code that no longer exists. **Before writing new tests**, audit all files
under `test/` for stale references.

### What to search for

```bash
# Removed helper methods (e.g. splunk_dir, server?, default_config_dir)
rg 'helper_method_name' test/

# Deleted recipe includes
rg 'include_recipe' test/cookbooks/

# Old node attributes from deleted attributes/ directory
rg "node\['cookbook'" test/

# Stale version strings in integration tests
rg 'version.*match|should match' test/integration/
```

### Common stale patterns

| Pattern                                                | Cause                                           | Fix                                                  |
|--------------------------------------------------------|-------------------------------------------------|------------------------------------------------------|
| `splunk_dir` or similar helper calls in test recipes   | Global `Chef::DSL::Universal.include` removed   | Replace with hardcoded path for the test context     |
| `include_recipe 'cookbook::recipe'` in test recipes    | `recipes/` directory deleted                    | Replace with direct resource calls                   |
| `node['cookbook']['attribute']` in test recipes        | `attributes/` directory deleted                 | Use resource properties or test cookbook attributes  |
| Version assertions (`should match(/8.0.6/)`) in InSpec | Test recipe now installs a different version    | Update to match the version the test recipe installs |
| App/file path assertions in InSpec                     | Test recipe changed which resources it installs | Update assertions to match new recipe output         |

### Cross-validation checklist

For **each** kitchen suite, verify alignment between the test recipe and InSpec profile:

1. **Packages**: Does the InSpec `package` assertion match the package the recipe installs?
2. **Versions**: Does the InSpec version regex match the version the recipe installs?
3. **Services**: Does the InSpec `service` name match the `service_name` in the recipe?
4. **Files/configs**: Do InSpec `file` and `ini` paths match the paths the recipe writes?
5. **Config keys**: Do InSpec `ini` section/key assertions match the template or resource output?
6. **Users/groups**: Do InSpec `user`/`group` assertions match the resource properties?

Fix any mismatches before running `kitchen test`.
