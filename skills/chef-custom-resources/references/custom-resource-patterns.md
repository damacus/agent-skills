# Custom Resource Patterns

## Table of Contents

- [Modern Resource Structure](#modern-resource-structure)
- [Resource Partials](#resource-partials)
- [Helper Modules](#helper-modules)
- [Migration from Libraries](#migration-from-libraries)
- [Migration from Recipes and Attributes](#migration-from-recipes-and-attributes)
- [Repository Wrapper Cookbooks](#repository-wrapper-cookbooks)
- [Existing Resource Audit](#existing-resource-audit)
- [Windows Resources](#windows-resources)
- [Property Patterns](#property-patterns)
- [Action Patterns](#action-patterns)

## Modern Resource Structure

Every custom resource lives in `resources/<resource_name>.rb` and follows this pattern:

```ruby
# frozen_string_literal: true

provides :cookbook_resource_name
unified_mode true

property :instance_name, String, name_property: true
property :version,       String, default: '8.0'

action :create do
  # Resource declarations here
  package 'some-package' do
    version new_resource.version
    action :install
  end
end

action :delete do
  package 'some-package' do
    action :remove
  end
end
```

Key requirements:

- `frozen_string_literal: true` at top
- `provides :resource_name` — explicit provider declaration
- `unified_mode true` — required for Chef 15.3+, mandatory for Chef 18+
- No class hierarchy — flat file, no modules wrapping the resource
- Access properties via `new_resource.property_name` inside actions

## Resource Partials

Use partials to DRY up shared properties across multiple resources. Partials contain
**property declarations only** — no actions, no `provides`, no `unified_mode`.

### Partial file

Place in `resources/_partial/_<name>.rb`:

```ruby
# resources/_partial/_config.rb

property :version, String, default: '8.0'
property :config_dir, String, default: '/etc/myapp'
property :user, String, default: 'myapp'
property :group, String, default: 'myapp'
```

### Using a partial

Include at the top of consuming resources with `use`:

```ruby
# resources/myapp_server.rb
# frozen_string_literal: true

provides :myapp_server
unified_mode true

use '_partial/_config'

property :port, Integer, default: 3306

action :create do
  # new_resource.version, new_resource.config_dir, etc. are available
  # from the partial
  directory new_resource.config_dir do
    owner new_resource.user
    group new_resource.group
    mode '0750'
  end
end
```

### When to extract a partial

Extract a partial when **3+ resources** share the same set of properties. Common candidates:

- Connection properties: `host`, `port`, `user`, `password`, `socket`
- Config properties: `version`, `config_dir`, `data_dir`, `log_dir`
- Ownership properties: `user`, `group`
- Service properties: `instance`, `service_name`

## Helper Modules

Keep shared logic (methods, not properties) in `libraries/` as Ruby modules:

```ruby
# libraries/helpers.rb
# frozen_string_literal: true

module MyCookbook
  module Helpers
    def default_package_name
      case node['platform_family']
      when 'debian'
        'myapp-server'
      when 'rhel', 'fedora', 'amazon'
        'myapp-community-server'
      end
    end

    def default_config_dir
      "/etc/#{instance_name}"
    end
  end
end
```

Include in resources via `action_class`:

```ruby
# resources/myapp_server.rb
provides :myapp_server
unified_mode true

action_class do
  include MyCookbook::Helpers
end

action :create do
  package default_package_name do
    action :install
  end
end
```

For `load_current_value` blocks that need helpers, include at the resource level:

```ruby
provides :myapp_server
unified_mode true

include MyCookbook::Helpers

load_current_value do |new_resource|
  # helpers available here
end
```

## Migration from Libraries

Legacy sous-chefs cookbooks use a class hierarchy in `libraries/`:

```text
libraries/
  mysql_base.rb              # Base class < Chef::Resource
  mysql_service_base.rb      # Inherits MysqlBase
  mysql_service.rb           # Inherits MysqlServiceBase
  mysql_service_manager_systemd.rb  # Inherits MysqlServiceBase
  helpers.rb                 # Helper module
```

### Migration steps

1. **Delete `attributes/` directory** — custom resources use properties, not node attributes. Convert any attribute-driven defaults to resource property defaults
2. **Delete `recipes/` directory** — move recipe logic into custom resource actions. Move usage examples into test cookbook recipes (`test/cookbooks/test/recipes/`)
3. **Identify properties** from each class in the hierarchy → extract shared ones into partials
4. **Identify helper methods** → keep in `libraries/helpers.rb` module
5. **Create flat resources** in `resources/` — one file per resource, no inheritance
6. **Use partials** for shared properties instead of class inheritance
7. **Include helpers** via `action_class` blocks
8. **Remove legacy files** from `libraries/` once all resources are migrated
9. **Update tests** — convert from ServerRunner pattern to step_into pattern

### Before (library class)

```ruby
# libraries/mysql_service_base.rb
module MysqlCookbook
  class MysqlServiceBase < MysqlBase
    property :bind_address, String
    property :port, [String, Integer], default: '3306'
    # ... inherited properties from MysqlBase
  end
end
```

### After (modern resource + partial)

```ruby
# resources/_partial/_service_config.rb
property :bind_address, String
property :port, [String, Integer], default: '3306'
property :data_dir, String, default: lazy { default_data_dir }
```

```ruby
# resources/mysql_service.rb
# frozen_string_literal: true

provides :mysql_service
unified_mode true

use '_partial/_service_config'

action_class do
  include MysqlCookbook::Helpers
end

action :create do
  # ...
end
```

## Migration from Recipes and Attributes

Many sous-chefs cookbooks are legacy recipe/attribute cookbooks rather than old
library-provider cookbooks. Treat these as public API migrations, not mechanical file moves.

### Migration steps

1. Inventory every recipe, attribute file, and README example.
2. Group recipe behavior into resources by user intent, usually:
   - `<cookbook>_install`
   - `<cookbook>_config`
   - `<cookbook>_service`
   - `<cookbook>_client`
   - `<cookbook>_server`
3. Convert node attributes to resource properties. Preserve defaults as property defaults or helper
   methods, not `node['cookbook']` reads.
4. Move recipe examples into `test/cookbooks/test/recipes/`.
5. Delete `recipes/` and `attributes/` only for Full Migration scope.
6. Write `migration.md` explaining the breaking API change from recipes/attributes to resources.

### Default mapping

```ruby
# attributes/default.rb
default['myapp']['package_name'] = 'myapp'
default['myapp']['config_dir'] = '/etc/myapp'
```

```ruby
# resources/myapp_install.rb
# frozen_string_literal: true

provides :myapp_install
unified_mode true

property :package_name, String, default: 'myapp'

action :install do
  package new_resource.package_name
end
```

Prefer explicit properties over an escape-hatch `config` hash unless the upstream config surface
is intentionally pass-through.

## Repository Wrapper Cookbooks

For `yum-*`, `apt-*`, or package-repository cookbooks, the custom resource should model the repo
API explicitly instead of preserving node attributes.

### Recommended shape

```ruby
# resources/yum_example_repo.rb
# frozen_string_literal: true

provides :yum_example_repo
unified_mode true

property :repo_name, String, name_property: true
property :description, String, default: lazy { default_description }
property :baseurl, [String, nil], default: lazy { default_baseurl }
property :mirrorlist, [String, nil], default: nil
property :gpgkey, [String, Array], required: true
property :enabled, [true, false], default: true
property :gpgcheck, [true, false], default: true

action :create do
  yum_repository new_resource.repo_name do
    description new_resource.description
    baseurl new_resource.baseurl if new_resource.baseurl
    mirrorlist new_resource.mirrorlist if new_resource.mirrorlist
    gpgkey new_resource.gpgkey
    enabled new_resource.enabled
    gpgcheck new_resource.gpgcheck
    action :create
  end
end

action :remove do
  yum_repository new_resource.repo_name do
    action :remove
  end
end
```

Preserve behavior that users can observe:

- repository IDs and generated file names
- generated base URLs / mirrorlists
- GPG keys and GPG check defaults
- enable/disable defaults
- deletion of stock distro repo files when the legacy recipe did that
- helper-derived platform/release values

For hyphenated cookbook names, resource names use underscores:

- `yum-epel` -> `yum_epel_repo`
- `yum-mysql-community` -> `yum_mysql_community_repo`

## Existing Resource Audit

When a cookbook already has resources, audit them before adding new resources.

Required checks:

- `# frozen_string_literal: true` is the first line
- `provides :resource_name` is present
- `unified_mode true` is present
- no old `load_current_resource`
- no direct `run_action` unless there is no Chef-native alternative and it is justified
- no global `Chef::Resource.include` or `Chef::DSL::Recipe.include`
- no compile-time `shell_out`; use action-time helpers or `lazy` values
- resource reads `new_resource` properties instead of cookbook node attributes
- `:delete` / `:remove` reverses every artifact created by `:create`

If keeping a legacy alias, document it and test both names:

```ruby
provides :new_resource_name
provides :old_resource_name
```

## Windows Resources

Windows-only cookbooks do not use Dokken or systemd. Use native Chef resources and Windows CI.

Common resource choices:

- `windows_package` or `package` for MSI/EXE installers
- `remote_file` for installer downloads
- `archive_file` for ZIP extraction
- `registry_key` for registry state
- `windows_path` or `env` for PATH/environment changes
- `service` for Windows services
- `powershell_script` for operations with no native resource
- IIS resources when the cookbook manages IIS state

Windows resources still require `provides`, `unified_mode true`, explicit properties, ChefSpec
coverage, InSpec coverage, and delete/remove semantics where the installer or platform supports it.

## Property Patterns

### Common property options

```ruby
property :name,     String, name_property: true          # Uses resource name
property :version,  String, default: '8.0'               # Static default
property :data_dir, String, default: lazy { computed }    # Lazy evaluated
property :password, String, sensitive: true               # Hidden from logs
property :port,     [String, Integer], default: 3306      # Multiple types
property :options,  Hash, default: {}                     # Hash with empty default
property :packages, [String, Array], coerce: proc { |m| Array(m) }  # Coerce to array
property :config,   String, desired_state: false          # Excluded from state comparison
```

### Property naming

- Use `snake_case` for all property names
- Prefix with resource context when ambiguous (e.g. `client_package_name` vs `server_package_name`)
- Use `name_property: true` for the primary identifier

## Action Patterns

### Default action

```ruby
default_action :create
```

Or rely on the first declared action being the default (Chef convention).

### Delete must undo create

A `:delete` (or `:remove`) action must remove **every** artifact that `:create`
(or `:install`/`:start`) produces. Audit the create action and ensure the delete
action reverses each resource declaration:

```ruby
action :create do
  directory '/etc/myapp' do           # ← created
    action :create
  end

  template '/etc/myapp/my.cnf' do     # ← created
    action :create
  end

  link '/usr/share/my-default.cnf' do # ← created
    action :create
  end

  systemd_unit 'myapp.service' do     # ← created
    action [:create, :enable, :start]
  end
end

action :delete do
  systemd_unit 'myapp.service' do     # ← removed (stop first)
    action [:stop, :disable, :delete]
  end

  link '/usr/share/my-default.cnf' do # ← removed
    action :delete
  end

  file '/etc/myapp/my.cnf' do        # ← removed (file, not template)
    action :delete
  end

  directory '/etc/myapp' do           # ← removed
    recursive true
    action :delete
  end
end
```

**Exception:** Shared resources (users, groups) that other instances may depend
on should **not** be removed by delete.

### Action class for shared methods

```ruby
action_class do
  include MyCookbook::Helpers

  def config_path
    "#{new_resource.config_dir}/my.cnf"
  end
end
```

### Idempotent actions with load_current_value

```ruby
load_current_value do |new_resource|
  current_value_does_not_exist! unless ::File.exist?(config_path)
  # Load current state from system
end

action :create do
  converge_if_changed :version do
    # Only runs if version changed
  end
end
```
