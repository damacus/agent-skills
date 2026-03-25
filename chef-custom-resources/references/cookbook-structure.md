# Cookbook Structure

## Table of Contents

- [Cookbook Structure](#cookbook-structure)
	- [Table of Contents](#table-of-contents)
	- [Required Directory Layout](#required-directory-layout)
		- [Directories NOT used](#directories-not-used)
	- [metadata.rb](#metadatarb)
	- [Berksfile](#berksfile)
	- [kitchen.yml](#kitchenyml)
		- [YAML anchor conventions](#yaml-anchor-conventions)
	- [kitchen.dokken.yml](#kitchendokkenyml)
		- [pid\_one\_command](#pid_one_command)
	- [kitchen.global.yml](#kitchenglobalyml)
	- [Other Config Files](#other-config-files)
		- [chefignore](#chefignore)
		- [.rubocop.yml](#rubocopyml)
		- [.yamllint](#yamllint)

## Required Directory Layout

```text
<cookbook>/
├── documentation/                    # Resource documentation
│   └── <cookbook>_<resource>.md
├── libraries/                        # Helper modules (shared logic only)
│   └── helpers.rb
├── resources/                        # Custom resources
│   ├── _partial/                     # Shared property partials
│   │   └── _config.rb
│   ├── <cookbook>_client.rb
│   ├── <cookbook>_config.rb
│   └── <cookbook>_service.rb
├── spec/                             # ChefSpec unit tests
│   ├── spec_helper.rb
│   ├── unit/
│   │   └── resources/
│   │       ├── <resource>_spec.rb
│   │       └── ...
│   └── helpers_spec.rb
├── templates/                        # ERB templates
│   └── my.cnf.erb
├── test/
│   ├── cookbooks/
│   │   └── test/                     # Test cookbook
│   │       ├── metadata.rb
│   │       └── recipes/
│   │           ├── smoke.rb
│   │           └── client.rb
│   └── integration/                  # InSpec tests
│       ├── spec_helper.rb            # Shared InSpec helpers
│       ├── common/
│       │   ├── inspec.yml
│       │   └── controls/
│       │       └── common_spec.rb
│       └── smoke/
│           ├── inspec.yml
│           └── controls/
│               └── smoke_spec.rb
├── LIMITATIONS.md                    # Platform/arch limitations
├── Berksfile
├── chefignore
├── kitchen.yml                       # Suites + Vagrant driver
├── kitchen.dokken.yml                # Dokken driver + platforms (CI)
├── kitchen.global.yml                # Shared provisioner/verifier
├── metadata.rb
└── README.md
```

### Directories NOT used

- **No `recipes/` directory** — sous-chefs cookbooks provide custom resources, not recipes
- **No `attributes/` directory** — use resource properties, not node attributes
- **No `files/` directory** — prefer `template` or inline `file` content

## metadata.rb

```ruby
# frozen_string_literal: true

name              '<cookbook>'
maintainer        'Sous Chefs'
maintainer_email  'help@sous-chefs.org'
license           'Apache-2.0'
description       'Provides <cookbook>_service, <cookbook>_config, and <cookbook>_client resources'
source_url        'https://github.com/sous-chefs/<cookbook>'
issues_url        'https://github.com/sous-chefs/<cookbook>/issues'
chef_version      '>= 15.3'
version           '1.0.0'

supports 'almalinux', '>= 8.0'
supports 'amazon', '>= 2023.0'
supports 'centos_stream', '>= 9.0'
supports 'debian', '>= 12.0'
supports 'fedora'
supports 'opensuseleap', '>= 15.0'
supports 'oracle', '>= 8.0'
supports 'redhat', '>= 8.0'
supports 'rocky', '>= 8.0'
supports 'ubuntu', '>= 20.04'
```

Key rules:

- **`metadata.rb` is a protected file** — managed by the release system (release-please). Do not modify it directly. Use `cookbook-helpers generate-metadata` to output platform lines for reference only
- `chef_version '>= 15.3'` minimum for `unified_mode` support
- Only list platforms actually tested and supported
- Cross-reference with `LIMITATIONS.md` for vendor support
- Add `depends` for any cookbook dependencies

## Berksfile

```ruby
# frozen_string_literal: true

source 'https://supermarket.chef.io'

metadata

group :integration do
  cookbook 'test', path: 'test/cookbooks/test'
end
```

## kitchen.yml

Contains suites, default driver config, and YAML anchors for reuse:

```yaml
---
driver:
  name: vagrant
  customize:
    memory: 1024

transport:
  max_wait_until_ready: 600
  connection_retries: 10
  connection_retry_sleep: 10

provisioner:
  name: chef_infra
  product_name: chef
  product_version: latest
  channel: stable
  chef_license: accept
  deprecations_as_errors: true

verifier:
  name: inspec
  sudo: true

platforms:
  - name: almalinux-9
  - name: debian-12
  - name: ubuntu-24.04

# Reusable YAML anchors for run_lists
x-run_lists:
  smoke: &smoke_run_list
    - recipe[test::smoke]

# Reusable YAML anchors for attributes
x-attributes:
  version_lts: &lts_attrs
    myapp_test:
      version: "8.4"

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
```

### YAML anchor conventions

- `x-run_lists` — anchors for run_list arrays
- `x-attributes` — anchors for attribute hashes
- `x-verifiers` — anchors for verifier configs
- Prefix custom keys with `x-` (ignored by Kitchen, valid YAML)

## kitchen.dokken.yml

Contains **only** Dokken driver and platform definitions. **No suites** — those come from `kitchen.yml`:

```yaml
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
      pid_one_command: /usr/lib/systemd/systemd
  - name: debian-12
    driver:
      image: dokken/debian-12
      pid_one_command: /bin/systemd
  - name: ubuntu-24.04
    driver:
      image: dokken/ubuntu-24.04
      pid_one_command: /bin/systemd
```

### pid_one_command

Required for systemd support in Dokken containers. Use:

- `/usr/lib/systemd/systemd` for RHEL family
- `/bin/systemd` for Debian/Ubuntu

## kitchen.global.yml

Shared settings across all Kitchen configs:

```yaml
---
provisioner:
  name: chef_infra
  product_name: chef
  product_version: latest
  channel: stable
  chef_license: accept
  deprecations_as_errors: true

verifier:
  name: inspec
  sudo: true
```

## Other Config Files

### chefignore

```text
.git
.gitignore
.kitchen/
.rubocop_cache/
*.swp
*~
Berksfile.lock
spec/
test/
.windsurf/
.claude/
.vscode/
```

### .rubocop.yml

```yaml
inherit_gem:
  cookstyle: config/cookstyle.yml
```

### .yamllint

```yaml
---
extends: default

rules:
  line-length:
    max: 256
    level: warning
  truthy:
    allowed-values: ['true', 'false', 'on']
  comments:
    min-spaces-from-content: 1
  document-start:
    present: true
```
