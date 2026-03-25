# ChefSpec Patterns

## Table of Contents

- [spec_helper.rb Setup](#spec_helperrb-setup)
- [step_into Pattern for Custom Resources](#step_into-pattern-for-custom-resources)
- [Testing Rendered Config Files](#testing-rendered-config-files)
- [Testing Package Installations](#testing-package-installations)
- [Testing Service Actions](#testing-service-actions)
- [Testing systemd_unit Resources](#testing-systemd_unit-resources)
- [Multi-Platform Specs](#multi-platform-specs)
- [Helper Module Unit Specs](#helper-module-unit-specs)
- [Spec Directory Structure](#spec-directory-structure)

## Running Specs

Always run ChefSpec tests with:

```bash
chef exec rspec
```

This uses the Chef Workstation embedded Ruby and gems, ensuring correct ChefSpec/Berkshelf versions.

## spec_helper.rb Setup

```ruby
# spec/spec_helper.rb
# frozen_string_literal: true

require 'chefspec'
require 'chefspec/berkshelf'

RSpec.configure do |config|
  config.color = true
  config.formatter = :documentation
  config.log_level = :error
end
```

## step_into Pattern for Custom Resources

Use `step_into` with inline `recipe do` blocks. This converges the resource and lets you
assert on the inner resources it declares.

```ruby
# spec/unit/resources/myapp_server_spec.rb
# frozen_string_literal: true

require 'spec_helper'

describe 'myapp_server' do
  step_into :myapp_server
  platform 'ubuntu', '24.04'

  context 'with default properties' do
    recipe do
      myapp_server 'default'
    end

    it { is_expected.to install_package('myapp-server') }
    it { is_expected.to create_directory('/etc/myapp') }
    it { is_expected.to create_template('/etc/myapp/my.cnf') }
  end

  context 'with custom version' do
    recipe do
      myapp_server 'custom' do
        version '8.4'
        port 3307
      end
    end

    it { is_expected.to install_package('myapp-server').with(version: '8.4') }
  end
end
```

### Key points

- `step_into :resource_name` — tells ChefSpec to converge the resource's inner resources
- `platform 'os', 'version'` — sets the Fauxhai platform for the spec
- `recipe do ... end` — inline recipe block, no test cookbook needed
- Assertions use `is_expected.to` with resource matchers

## Testing Rendered Config Files

```ruby
describe 'myapp_config' do
  step_into :myapp_config
  platform 'ubuntu', '24.04'

  context 'renders default config' do
    recipe do
      myapp_config 'default' do
        port 3306
        bind_address '0.0.0.0'
      end
    end

    expected_content = <<~CFG
      [mysqld]
      port = 3306
      bind-address = 0.0.0.0
    CFG

    it { is_expected.to create_template('/etc/myapp/my.cnf') }
    it { is_expected.to render_file('/etc/myapp/my.cnf').with_content(expected_content) }
  end
end
```

### Partial content matching

```ruby
it { is_expected.to render_file('/etc/myapp/my.cnf').with_content(/bind-address = 0\.0\.0\.0/) }
it { is_expected.to render_file('/etc/myapp/my.cnf').with_content(/port = 3306/) }
```

## Testing Package Installations

```ruby
describe 'myapp_client' do
  step_into :myapp_client
  platform 'debian', '12'

  context 'installs client packages' do
    recipe do
      myapp_client 'default' do
        version '8.0'
      end
    end

    it { is_expected.to install_package('myapp-client-8.0') }
    it { is_expected.to install_package('libmyappclient-dev') }
  end
end
```

### Platform-specific package assertions

```ruby
describe 'myapp_client' do
  step_into :myapp_client

  context 'on debian' do
    platform 'debian', '12'

    recipe do
      myapp_client 'default'
    end

    it { is_expected.to install_package('myapp-client') }
  end

  context 'on almalinux' do
    platform 'almalinux', '9'

    recipe do
      myapp_client 'default'
    end

    it { is_expected.to install_package('myapp-community-client') }
  end
end
```

## Testing Service Actions

```ruby
describe 'myapp_service' do
  step_into :myapp_service
  platform 'ubuntu', '24.04'

  context 'action :create' do
    recipe do
      myapp_service 'default' do
        action :create
      end
    end

    it { is_expected.to create_systemd_unit('myapp.service') }
    it { is_expected.to enable_systemd_unit('myapp.service') }
    it { is_expected.to start_systemd_unit('myapp.service') }
  end

  context 'action :stop' do
    recipe do
      myapp_service 'default' do
        action :stop
      end
    end

    it { is_expected.to stop_systemd_unit('myapp.service') }
  end
end
```

## Testing systemd_unit Resources

ChefSpec matchers for `systemd_unit`:

- `create_systemd_unit`
- `delete_systemd_unit`
- `enable_systemd_unit`
- `disable_systemd_unit`
- `start_systemd_unit`
- `stop_systemd_unit`
- `reload_systemd_unit`
- `restart_systemd_unit`

```ruby
it do
  is_expected.to create_systemd_unit('myapp.service').with(
    content: {
      Unit: {
        Description: 'My Application',
        After: 'network.target',
      },
      Service: {
        Type: 'notify',
        ExecStart: '/usr/sbin/myappd',
        Restart: 'on-failure',
      },
      Install: {
        WantedBy: 'multi-user.target',
      },
    }
  )
end
```

## Multi-Platform Specs

Test the same resource across multiple platforms:

```ruby
describe 'myapp_server' do
  step_into :myapp_server

  %w(
    ubuntu-24.04
    debian-12
    almalinux-9
    fedora-latest
  ).each do |platform_spec|
    os, ver = platform_spec.split('-', 2)

    context "on #{platform_spec}" do
      platform os, ver

      recipe do
        myapp_server 'default'
      end

      it { is_expected.to create_directory('/etc/myapp') }
      it { is_expected.to create_template('/etc/myapp/my.cnf') }
    end
  end
end
```

## Helper Module Unit Specs

Test helper modules as plain Ruby — no Chef convergence needed:

```ruby
# spec/helpers_spec.rb
# frozen_string_literal: true

require 'spec_helper'

describe MyCookbook::Helpers do
  let(:helper_class) do
    Class.new do
      include MyCookbook::Helpers

      # Stub Chef methods used by helpers
      attr_accessor :node

      def platform_family?(family)
        node['platform_family'] == family
      end

      def platform?(name)
        node['platform'] == name
      end
    end
  end

  let(:helper) { helper_class.new }

  before do
    helper.node = {
      'platform' => 'ubuntu',
      'platform_family' => 'debian',
      'platform_version' => '24.04',
    }
  end

  describe '#default_package_name' do
    context 'on debian family' do
      it 'returns the debian package name' do
        expect(helper.default_package_name).to eq 'myapp-server'
      end
    end

    context 'on rhel family' do
      before do
        helper.node = helper.node.merge(
          'platform' => 'almalinux',
          'platform_family' => 'rhel',
          'platform_version' => '9'
        )
      end

      it 'returns the rhel package name' do
        expect(helper.default_package_name).to eq 'myapp-community-server'
      end
    end
  end
end
```

## Spec Directory Structure

```text
spec/
├── spec_helper.rb
├── unit/
│   └── resources/
│       ├── myapp_client_spec.rb
│       ├── myapp_config_spec.rb
│       ├── myapp_server_spec.rb
│       └── myapp_service_spec.rb
├── helpers_spec.rb
└── helpers_sql_spec.rb
```

Alternatively, for smaller cookbooks, flat structure is acceptable:

```text
spec/
├── spec_helper.rb
├── myapp_client_spec.rb
├── myapp_server_spec.rb
└── helpers_spec.rb
```

Match the existing cookbook's convention. The `spec/unit/resources/` structure is preferred
for larger cookbooks.

## Common Pitfalls

### Lazy defaults from run_state

Resources that use `default: lazy { ... }` reading from `node.run_state` will fail when
tested in isolation because only the stepped-into resource executes its action block. The
prerequisite resource (e.g. `system_install`) that populates `run_state` won't execute.

**Fix**: Provide the property explicitly in the spec recipe block:

```ruby
# BAD — root_path lazy default reads run_state, which is empty
rbenv_global '3.4.9'

# GOOD — bypass the lazy default
rbenv_global '3.4.9' do
  root_path '/usr/local/rbenv'
end
```

### User home directory lookups

Resources that call `File.expand_path("~username")` will fail if the user doesn't exist on
the machine running specs.

**Fix**: Provide `home_dir` explicitly or stub `File.expand_path`:

```ruby
# Option 1: provide home_dir to skip the lookup
rbenv_user_install 'vagrant' do
  home_dir '/home/vagrant'
end

# Option 2: stub in a before block
before do
  allow(File).to receive(:expand_path).and_call_original
  allow(File).to receive(:expand_path).with('~vagrant').and_return('/home/vagrant')
end
```

### Helper module specs need require_relative

Helper specs that reference `Chef::MyModule::Helpers` directly need to require the library
file since ChefSpec auto-loading only works during convergence:

```ruby
require 'spec_helper'
require_relative '../libraries/helpers'

describe Chef::MyModule::Helpers do
  # ...
end
```
