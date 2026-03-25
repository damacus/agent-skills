# Systemd Patterns

## Table of Contents

- [systemd_unit Resource](#systemd_unit-resource)
- [Unit File as Hash](#unit-file-as-hash)
- [Unit File as String](#unit-file-as-string)
- [Complete Service Resource Example](#complete-service-resource-example)
- [Removing Legacy Init Systems](#removing-legacy-init-systems)
- [InSpec Verification](#inspec-verification)

## systemd_unit Resource

Use Chef's native `systemd_unit` resource instead of `template` + `service` combinations.
This is the **only** supported init system — no sysvinit, no upstart.

### Actions

| Action              | Description                                |
|---------------------|--------------------------------------------|
| `:create`           | Create the unit file                       |
| `:delete`           | Delete the unit file                       |
| `:enable`           | Enable the unit to start on boot           |
| `:disable`          | Disable the unit from starting on boot     |
| `:start`            | Start the unit                             |
| `:stop`             | Stop the unit                              |
| `:restart`          | Restart the unit                           |
| `:reload`           | Reload the unit configuration              |
| `:reload_or_restart`| Reload if supported, otherwise restart     |

### Properties

| Property          | Type          | Default    | Description                    |
|-------------------|---------------|------------|--------------------------------|
| `unit_name`       | String        | name       | Name of the unit file          |
| `content`         | String, Hash  | required   | Unit file content              |
| `triggers_reload` | Boolean       | true       | Daemon-reload on create/delete |
| `verify`          | Boolean       | true       | Verify unit before install     |
| `user`            | String        | nil        | Run under user scope           |

## Unit File as Hash

Preferred approach — structured and easy to generate dynamically:

```ruby
systemd_unit 'myapp.service' do
  content({
    Unit: {
      Description: 'My Application Server',
      After: 'network.target',
    },
    Service: {
      Type: 'notify',
      ExecStart: '/usr/sbin/myappd --defaults-file=/etc/myapp/my.cnf',
      ExecStartPre: '/usr/bin/myapp-pre-start',
      Restart: 'on-failure',
      User: 'myapp',
      Group: 'myapp',
      LimitNOFILE: 65535,
      PIDFile: '/run/myapp/myapp.pid',
    },
    Install: {
      WantedBy: 'multi-user.target',
    },
  })
  action [:create, :enable, :start]
end
```

### Repeatable options (arrays)

For directives that can appear multiple times (e.g. `Environment`):

```ruby
systemd_unit 'myapp.service' do
  content({
    Service: {
      Environment: [
        'MYAPP_HOME=/var/lib/myapp',
        'MYAPP_CONFIG=/etc/myapp',
      ],
    },
  })
  action [:create, :enable]
end
```

## Unit File as String

Use heredoc when you need exact control over the unit file format:

```ruby
systemd_unit 'myapp.service' do
  content <<~UNIT
    [Unit]
    Description=My Application Server
    After=network.target

    [Service]
    Type=notify
    ExecStart=/usr/sbin/myappd --defaults-file=/etc/myapp/my.cnf
    Restart=on-failure
    User=myapp
    Group=myapp

    [Install]
    WantedBy=multi-user.target
  UNIT
  action [:create, :enable, :start]
end
```

## Complete Service Resource Example

A custom resource that manages a service using `systemd_unit`:

```ruby
# resources/myapp_service.rb
# frozen_string_literal: true

provides :myapp_service
unified_mode true

use '_partial/_config'

property :instance, String, name_property: true

action_class do
  include MyCookbook::Helpers

  def service_name
    instance == 'default' ? 'myapp' : "myapp-#{new_resource.instance}"
  end

  def unit_content
    {
      Unit: {
        Description: "#{service_name} service",
        After: 'network.target',
      },
      Service: {
        Type: 'notify',
        ExecStart: "#{mysqld_bin} --defaults-file=#{new_resource.config_dir}/my.cnf",
        Restart: 'on-failure',
        User: new_resource.user,
        Group: new_resource.group,
        LimitNOFILE: 65535,
        PIDFile: "/run/#{service_name}/#{service_name}.pid",
      },
      Install: {
        WantedBy: 'multi-user.target',
      },
    }
  end
end

action :create do
  # Create runtime directory config
  directory "/usr/lib/tmpfiles.d" do
    owner 'root'
    group 'root'
    mode '0755'
    recursive true
  end

  file "/usr/lib/tmpfiles.d/#{service_name}.conf" do
    content "d /run/#{service_name} 0755 #{new_resource.user} #{new_resource.group} -\n"
    owner 'root'
    group 'root'
    mode '0644'
  end

  systemd_unit "#{service_name}.service" do
    content unit_content
    action [:create, :enable]
  end
end

action :start do
  systemd_unit "#{service_name}.service" do
    action :start
  end
end

action :stop do
  systemd_unit "#{service_name}.service" do
    action [:stop, :disable]
  end
end

action :restart do
  systemd_unit "#{service_name}.service" do
    action :restart
  end
end

action :delete do
  systemd_unit "#{service_name}.service" do
    action [:stop, :disable, :delete]
  end
end
```

## Removing Legacy Init Systems

When migrating a cookbook, remove all sysvinit and upstart code:

### Files to delete

- `libraries/mysql_service_manager_sysvinit.rb`
- `libraries/mysql_service_manager_upstart.rb`
- `templates/sysvinit/` or similar
- `templates/upstart/` or similar
- Any `sysvinit` or `upstart` references in service manager selection logic

### Code to remove

Remove service_manager selection for non-systemd:

```ruby
# REMOVE this pattern:
case new_resource.service_manager
when 'sysvinit'
  mysql_service_manager_sysvinit(...)
when 'upstart'
  mysql_service_manager_upstart(...)
end
```

Remove the `service_manager` property or restrict it:

```ruby
# REMOVE:
property :service_manager, %w(sysvinit upstart systemd auto), default: 'auto'

# No replacement needed — systemd is the only option
```

### Verification

After removing legacy init code:

1. Run ChefSpec — all specs should pass with systemd assertions
2. Run InSpec — verify `systemd_service` is running
3. Check that no references to `sysvinit`, `upstart`, or `init.d` remain

## InSpec Verification

```ruby
control 'myapp-service-01' do
  impact 1.0
  title 'Service is managed by systemd'

  describe systemd_service('myapp') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
  end

  describe file('/etc/systemd/system/myapp.service') do
    it { should exist }
    its('content') { should match(/Type=notify/) }
    its('content') { should match(/ExecStart=/) }
  end
end
```
