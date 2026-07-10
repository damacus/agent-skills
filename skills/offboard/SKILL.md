---
name: offboard
description: >
  Plan and work through project, client, vendor, or team offboarding. Use for
  handovers, access removal, ownership transfer, documentation, credential
  rotation, data cleanup, and knowledge-transfer checklists.
---

# Offboard an Engagement

Build a checklist that fits the actual engagement. Inspect available context
and ask about missing systems, owners, deadlines, regulatory obligations, and
the destination team before proposing actions.

## Areas to Cover

- source repositories, branches, releases, and code ownership;
- architecture notes, runbooks, setup instructions, and known risks;
- infrastructure, domains, stores, devices, and third-party services;
- chat, email, project-management, design, and document systems;
- password-manager entries, API keys, SSH keys, service accounts, and tokens;
- client or production data retained on personal or company devices;
- unfinished work, open incidents, support obligations, and named owners;
- knowledge-transfer sessions and recorded decisions; and
- credential rotation and verification after access changes.

For each item, record owner, target date, status, evidence, and blocker. Separate
what can be inspected read-only from actions that change access, ownership, or
data.

## Safety

Never delete data, revoke access, rotate credentials, transfer ownership,
archive communication, or contact another person without explicit confirmation
for that action. Show the exact target and consequence before irreversible or
externally visible steps. Preserve an audit trail required by the organization.

Finish with unresolved risks, remaining owners, and the next concrete handover
action. Do not generate a separate document unless the user asks for one.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `offboard` skill at
revision `f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
