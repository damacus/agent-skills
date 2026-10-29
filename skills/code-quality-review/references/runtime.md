# Runtime selection and evidence

Discover before dispatch, and refresh when changing route or reusing an agent.
The parent model, configured model and actually selected reviewer are different
facts. Record requested and observed settings separately.

1. Inspect live delegation tool descriptions for model IDs, effort choices,
   fresh-context semantics, sandbox and service tier. The app-server catalog is
   useful inventory; it does not prove a particular tool can select every field.
2. Resolve latest eligible Sol and Astra using current numeric version metadata
   and descriptions; reject ambiguity and excluded families/releases. Verify
   `low`, `high`, `medium` and `xhigh` on the exact intended models as applicable.
   Never hard-code today's IDs in the workflow.
3. Check normal/default service independently. An inventory listing `priority`
   with a null default does not establish the effective normal service setting.
   Inspect supported configuration/protocol and recorded applied settings.
4. Use fresh context for architecture and blind subjective assessments. With the
   native `agents.spawn_agent` API, use `fork_turns="none"` when supported to set
   model/effort explicitly; inspect current restrictions before passing overrides.
   Do not inherit history containing findings or scores. If the tool only offers
   priority service, do not dispatch through it without specific user approval.
5. The bundled `scripts/review-session.mjs` provides a verified app-server route.
   It starts an ephemeral session, explicitly selects the newest eligible Sol or
   Astra and requested effort, requests `serviceTier: "default"`, checks the
   `thread/start` response for matching model, effort, tier and sandbox, and only
   then sends `turn/start` with `serviceTierForTurn: "default"`. This turn field is
   documented by the local protocol as standard speed. The helper does not create
   a persistent sidebar chat. If these fields are unsupported or mismatched, it
   fails before starting a model turn.
6. A CLI session is another possible fallback only after checking the installed
   `codex exec --help` and configuration schema. Use exact advertised `--model`,
   supported effort and normal service overrides, fresh/ephemeral context and
   `--sandbox read-only`, with output stored outside the source snapshot. Do not
   invent CLI flags or assume an accepted flag proves the applied configuration.
7. Record session/agent ID, timestamp, role, exact model, effort, tier, tool,
   isolation, requested versus applied settings and evidence location. Verify
   settings from runtime/session events where available. Missing evidence is
   `unknown`; capability listing is not proof that a reviewer actually ran.

The discovery helper calls only `initialize`, `model/list` (all pages) and
`skills/list` with `forceReload`. It starts no model turns or review agents and
does not edit Codex configuration. The app-server may write its ordinary runtime
logs outside the target. Use normal sandbox approval for that host access; do not
change authentication or bypass protections. If app-server discovery is absent,
use the host's documented live inventory and disclose the unavailable helper.

## App-server reviewer helper

Call only after authorisation, usage checks and source/output path validation.
Arguments are role, family, effort, scratch working directory, prompt file,
external output prefix, then optional sandbox (`read-only` by default) and
session timeout in seconds (240 by default, permitted range 10–3600).

```fish
rtk proxy node /path/to/code-quality-review/scripts/review-session.mjs architect astra medium /scratch/source-only /scratch/architect-prompt.md /scratch/artifacts/architect
```

Use `sol low` for collection and `sol high` for ownership/subjective assessment.
Only a collector working in a disposable copy should need the optional
`workspace-write` sandbox. The caller must prepare the brief and snapshot, check
quota and keep output outside the target. The helper runs no automatic challenger.
It accepts only `sol`/`astra` and read-only/workspace-write, never priority or
danger-full-access. No prompt should delegate further.

The output prefix must be unused and its parent must exist. The helper writes applied settings,
notifications (JSON and live JSONL), and the final answer. Notifications may contain
reviewed source and tool output; keep them local. It records unsuccessful turns
as failures. For a larger authorised batch, set a suitable finite timeout
deliberately or use the host's managed session interface; never
interpret a timeout as successful review.

## Failure handling

- Exact role unsupported: report it unavailable. Ask for a supported alternative
  only when it is needed; do not silently call another model by the requested name.
- Current owner settings differ from Sol High: disclose them, arrange an actual
  supported owner session if possible, and avoid claiming that instructions
  switched the active model.
- No fresh-context reviewer: independent review cannot be claimed. Safe mechanical
  collection can proceed; mark the workflow partial.
- No verified normal tier: pause dependent delegation. User approval for a specific
  priority reviewer can unblock it; general model approval is insufficient.
- Native review roles are authorised by skill invocation, but creating user-owned
  sidebar chats or messaging existing chats still requires explicit user authority.

## Observed installation environment, 28 October 2026

The local app-server advertised `gpt-6.1-sol` and `gpt-6-astra` with the required
efforts. Local configuration had `service_tier = "priority"`; the catalog listed
priority as an option with a null default. The native spawning API advertised
priority service only. Follow-up validation proved that the local app-server
supports explicit default service in ephemeral sessions and reports the applied
model, effort and tier before a turn starts. Review roles were exercised through
that route on a synthetic fixture. This historical evidence does not replace
live capability discovery on future runs.
