# InSpec Patterns

## Table of Contents

- [Profile Structure](#profile-structure)
- [inspec.yml Profile File](#inspecyml-profile-file)
- [Controls Structure](#controls-structure)
- [Shared Helpers](#shared-helpers)
- [Kitchen Configuration](#kitchen-configuration)
- [Common InSpec Resources](#common-inspec-resources)
- [Verification](#verification)
- [Test Cookbook Recipes](#test-cookbook-recipes)

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
```

> **Do not use `supports` in `inspec.yml`.** The `supports: platform-family:` filter
> silently skips the entire profile in Dokken containers where platform strings
> (e.g. `amazon/2023.10.20260105`) don't match the filter. Omitting `supports`
> ensures InSpec always runs and fails visibly if something is wrong.

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

## Verification

**InSpec profiles must be verified runnable.** Writing controls is not enough — controls
that reference specific config content (JVM flags, proxy settings, file paths) can only
be validated by actually converging Kitchen. Always run at least one `kitchen test` before
considering integration tests complete.

## Test Cookbook Recipes

Test recipes live in `test/cookbooks/test/recipes/` and exercise the cookbook's resources:

```ruby
# test/cookbooks/test/metadata.rb
name 'test'
depends 'myapp'
```

```ruby
# test/cookbooks/test/recipes/smoke.rb
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
