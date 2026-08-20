# Repository Security Contract

Use this template after the user approves repository-contract discovery. Show
the completed contract to the user for approval before implementation.

## Scope

- Requested mode: audit-only, fix one finding, or pull request.
- In-scope paths, services, environments, and data.
- Explicit exclusions and actions requiring further approval.

## Repository Guidance

- Instruction and contribution files consulted.
- Supported runtime, framework, package manager, and task runner.
- Authoritative test, lint, build, formatting, and security-scan commands.
- CI checks that are the final authority when local verification is unavailable.

## Security Model

- Authentication and session model.
- Authorization, ownership, tenancy, and privileged-action boundaries.
- Sensitive data classes, secret-handling rules, and logging or telemetry limits.
- External inputs, outbound network access, files, jobs, APIs, and webhooks.

## Delivery

- Required focused and full verification.
- Branch, commit, and pull-request conventions.
- Disclosure and reporting limits.
- Whether the user approved durable, non-sensitive contract memory.
