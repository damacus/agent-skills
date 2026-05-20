---
name: tui-expert
description: Expert guidance for building professional, responsive, and beautiful Terminal User Interfaces (TUIs) in Rust (Ratatui) and Ruby (TTY, cli-ui). Covers architectural patterns (Conductor/Model/App), async client reuse, parallelisation, secure authentication, and modern visual aesthetics. Use when building, refactoring, or styling TUI applications in any language.
---

# TUI Expert

This skill provides the architectural and aesthetic foundation for building world-class TUIs and agent-first CLIs across Rust, Ruby, Go, and other ecosystems.

## Unified CLI/TUI Command Surface

When a tool has both a CLI and a TUI, design the plain command as the first-class interface. The TUI is an explicit interactive mode, not the default path and not a replacement for a stable scriptable command surface.

Use this command grammar for new tools:

1. `<tool>` starts the default agent-first interaction.
2. `<tool> tui` starts the full TUI.
3. `<tool> <resource> <verb>` runs stable scriptable commands.
4. `<tool> raw` provides a break-glass escape hatch for API-backed tools.
5. `<tool> auth`, `<tool> completion`, and `<tool> version` remain explicit support commands.

For API-backed CLIs, organize resources around predictable verbs:

- Use `list`, `get`, `create`, `update`, and `delete` for core CRUD.
- Add domain verbs only when they match user intent better than CRUD, such as `send`, `approve`, `transition`, or `attach-receipt`.
- Prefer positional IDs for `get`, `update`, and `delete`; accept full URLs when the domain naturally exposes resources as URLs.
- Keep support commands separate from domain resources so agents and users can discover the command tree quickly.

Do not make `--json` the hidden agent path or a compatibility alias. Define a first-class output contract:

- Human terminal output defaults to readable tables, summaries, and confirmations.
- Agent and automation calls use a documented structured output path, such as `--format json`, `--output json`, or an explicit agent mode.
- Long-running jobs and event streams use newline-delimited JSON, such as `--format ndjson`, with one complete JSON object per line.
- Structured output must be stable, documented, and covered by tests.

For a FreeAgent-style CLI, this means top-level API resources such as `contacts`, `invoices`, `bank`, `bills`, `projects`, `tasks`, and `users`; support commands such as `auth`, `raw`, `completion`, and `version`; and domain workflows such as invoice `send`, bank `approve`, resource `transition`, and receipt attachment.

## Core Architectural Pattern: The "Orchestrated State"

Regardless of the language, modern TUIs follow a state-driven approach where the UI is a pure function of the application state.

1. **Models:** Raw data structures and domain logic.
2. **Client:** Low-level wrapper for I/O (HTTP, SSH, File System) with connection pooling.
3. **Conductor/Orchestrator:** Handles the lifecycle of data, parallelisation, and caching.
4. **App State:** Manages user interaction (selections, filtering, modes).
5. **UI/View:** Transforms the `App State` into terminal frames.

### Language-Specific Selection
- **For Rust (Ratatui)**: Use the [rust_ratatui.md](references/rust_ratatui.md) for layout engine and widget patterns.
- **For Ruby (TTY/cli-ui)**: See [ruby_tui.md](references/ruby_specific.md) for modular gems and framing patterns.

### Domain-Specific Patterns
- **Monitoring (System/Network)**: See [monitoring.md](references/monitoring.md)
- **Data & DB Management**: See [data_management.md](references/data_management.md)
- **File Management**: See [file_management.md](references/file_management.md)
- **Media & Entertainment**: See [media_entertainment.md](references/media_entertainment.md)

## Expert TUI Workflow (General)

1. **Research:** Understand the data source. TUIs are "windows into data".
2. **Strategy:** Plan the layout segmentation (Header / Content / Status).
3. **Act:** Build in layers: Data Client -> State Manager -> UI Components.
4. **Validate:** Test resizing, edge cases (empty lists), and error states.

## Getting to "Good" Faster

When the team builds multiple Rust TUIs, optimize for a shared foundation instead of repeating screen patterns:

1. **Shared app shell:** Standardize header, footer, status line, hotkey help, loading, and error states.
2. **Small component kit:** Reuse list, detail pane, inspector, confirmation dialog, toast/banner, and empty state widgets.
3. **Real design system:** Define spacing, borders, color roles, emphasis, and icon rules so each app feels related without copy-paste layouts.
4. **Consistent navigation model:** Use the same modes everywhere, such as browse, filter, inspect, edit, and confirm.
5. **Conductor/state layer:** Keep async loading, caching, refresh, and error handling out of the view layer.
6. **Graceful empty/error/loading states:** Treat these as first-class screens, not afterthoughts.
7. **Terminal UX tests:** Add snapshot coverage for common screen recipes and verify narrow, tall, empty, and error states.
8. **Screen recipes:** Maintain reusable patterns like list + detail, table + inspector, dashboard + drilldown, and command palette.

Practical guidance:

- Make modals the exception, not the default detail view.
- Prefer side panels or inspectors for drilldown when space allows.
- Keep keyboard shortcuts consistent across apps so users do not relearn the same actions.
- Build one polished shared layout first, then let each app supply only its domain data and screen-specific widgets.

## Text Input and Hotkeys

Text input focus must override global printable-key hotkeys. When a search box, command palette, URL field, or free-form editor is focused, printable keys are inserted into the input instead of being handled as global actions.

Required behavior:

- Global hotkeys such as `a`, `c`, `q`, `/`, and `?` only fire outside text-entry mode, unless combined with an explicit modifier such as `Ctrl`.
- `Esc` exits input mode or clears focus before returning to normal navigation.
- `Ctrl+C` or the configured emergency quit remains available even while editing text.
- Tests must cover typing words that contain hotkey letters, such as `query`, `account`, and URL-like strings.

## Global TUI Aesthetics (The "Beautiful TUI" Checklist)

- [ ] **Gradients & Colour:** Use high-contrast gradients for titles. E.g., Light Blue to Purple.
- [ ] **Hotkey Discoverability:** Always show shortcut keys in brackets or a distinct colour (e.g., `[q] quit`).
- [ ] **Icons & Symbols:** Use UTF-8 symbols (●, ✓, ✗, ⚠) to represent status without taking up much space.
- [ ] **Adaptive UI:** Collapse panels or switch views based on terminal width/height.
- [ ] **Muted Meta:** Dim secondary data (timestamps, hashes) to reduce cognitive load.

## Side-Quest: The Power of Colour
Every top-tier TUI uses colour strategically. It's not just decoration; it's a **UI primitive** for:
- **Status Perception:** Red/Yellow/Green for health.
- **Hierarchy:** Highlighting the "active" item in a list with a distinct background.
- **Focus:** Greying out inactive sections.
