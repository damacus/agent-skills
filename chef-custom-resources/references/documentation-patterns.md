# Documentation Patterns

## File Location and Naming

Every custom resource gets a documentation file at:

```text
documentation/<cookbook_name>_<resource_name>.md
```

Examples:

- `documentation/mysql_client.md`
- `documentation/mysql_config.md`
- `documentation/mysql_service.md`
- `documentation/mysql_database.md`
- `documentation/mysql_user.md`

## Template

````markdown
# <cookbook_name>_<resource_name>

Brief description of what this resource manages.

## Actions

| Action    | Description                          |
|-----------|--------------------------------------|
| `:create` | Creates the resource (default)       |
| `:delete` | Removes the resource                 |
| `:start`  | Starts the service                   |
| `:stop`   | Stops the service                    |

## Properties

| Property       | Type              | Default      | Description                        |
|----------------|-------------------|--------------|------------------------------------|
| `instance`     | String            | name         | Instance name (name property)      |
| `version`      | String            | `'8.0'`      | Product version to install         |
| `port`         | Integer           | `3306`       | Listen port                        |
| `bind_address` | String            | `'127.0.0.1'`| Bind address                       |
| `user`         | String            | `'mysql'`    | System user                        |
| `group`        | String            | `'mysql'`    | System group                       |

## Examples

### Basic usage

```ruby
<cookbook_name>_<resource_name> 'default' do
  version '8.4'
  action :create
end
```

### Custom configuration

```ruby
<cookbook_name>_<resource_name> 'custom' do
  version '8.4'
  port 3307
  bind_address '0.0.0.0'
  action [:create, :start]
end
```

### Multiple instances

```ruby
<cookbook_name>_<resource_name> 'primary' do
  port 3306
  action [:create, :start]
end

<cookbook_name>_<resource_name> 'replica' do
  port 3307
  action [:create, :start]
end
```
````

## Guidelines

- **Actions table**: List all actions with brief descriptions. Mark the default action.
- **Properties table**: Include type, default value, and description for every property.
  - Use backtick-quoted defaults for strings and numbers
  - Note `name property` where applicable
  - Note `sensitive` properties
  - Note `desired_state: false` properties that affect behavior but not idempotency
- **Examples**: Provide at minimum a basic usage example. Add more for common patterns.
- **Keep it concise**: Users should be able to copy-paste examples directly.
- **No internal implementation details**: Document the public API only.

## Generating Documentation from Resources

To document a resource, read its source file and extract:

1. `provides` declaration → resource name
2. `property` declarations → properties table
3. `action` declarations → actions table
4. `default_action` or first action → default action
5. Partial includes (`use '_partial/_name'`) → additional properties from the partial file
