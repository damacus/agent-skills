---
name: tui-expert
description: >-
  Design, build, review, or refine responsive Terminal User Interfaces (TUIs), especially Rust
  Ratatui and Ruby TTY/cli-ui applications. Use for TUI state and event architecture, terminal
  layout, navigation, keyboard and text-input behavior, async data loading, accessibility,
  rendering, resizing, empty/error/loading states, or visual polish. When the product also exposes
  scriptable commands, use cli-design alongside this skill for the CLI contract.
---

# TUI Expert

This skill provides the architectural and interaction foundation for terminal user interfaces across Rust, Ruby, Go, and other ecosystems. It owns the interactive surface; the separate `cli-design` skill owns scriptable command contracts.

## Compose the TUI with a CLI

When a tool has both interfaces, load `cli-design` and keep them as sibling presentation adapters over shared application behavior.

- Preserve an established bare-command TUI when compatibility requires it; for new automation-first tools, prefer an explicit `<tool> tui` entry.
- Make important TUI reads and mutations available through documented non-interactive commands unless the operation is inherently visual or continuous.
- Keep auth, configuration, validation, permissions, dry-run behavior, and result semantics consistent across both interfaces.
- Keep rendering, keyboard state, and navigation out of the CLI layer; keep stdout/stderr formatting and pipe behavior out of the TUI state model.
- Test parity for the same operation through the shared application layer, then test each adapter's terminal contract separately.

Do not duplicate a domain-specific CLI tree here. Use the CLI skill to derive commands from the product's actual resources and workflows.

## Core Architectural Pattern: The "Orchestrated State"

Regardless of the language, modern TUIs follow a state-driven approach where the UI is a pure function of the application state.

1. **Models:** Raw data structures and domain logic.
2. **Client:** Low-level wrapper for I/O (HTTP, SSH, File System) with connection pooling.
3. **Conductor/Orchestrator:** Handles the lifecycle of data, parallelisation, and caching.
4. **App State:** Manages user interaction (selections, filtering, modes).
5. **UI/View:** Transforms the `App State` into terminal frames.

### Language-Specific Selection

- **For Rust (Ratatui)**: Use the [rust_ratatui.md](references/rust_ratatui.md) for layout engine and widget patterns.
- **For Ruby (TTY/cli-ui)**: See [ruby_specific.md](references/ruby_specific.md) for modular gems and framing patterns.

### Domain-Specific Patterns

- **Monitoring (System/Network)**: See [monitoring.md](references/monitoring.md)
- **Data & DB Management**: See [data_management.md](references/data_management.md)
- **File Management**: See [file_management.md](references/file_management.md)
- **Media & Entertainment**: See [media_entertainment.md](references/media_entertainment.md)

## Expert TUI Workflow (General)

1. **Research:** Understand the data source. TUIs are "windows into data".
2. **Strategy:** Plan the layout segmentation (Header / Content / Status).
3. **Act:** Build in layers: Data Client -> State Manager -> UI Components.
4. **Validate:** Test resizing, narrow and non-UTF-8 terminals, keyboard-only use, text-entry focus, empty/loading/error states, and clean shutdown.

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

## Global TUI Aesthetics

- [ ] **Colour:** Use a small semantic palette with sufficient contrast; remain understandable with `NO_COLOR`, limited colour, and monochrome terminals.
- [ ] **Hotkey Discoverability:** Always show shortcut keys in brackets or a distinct colour (e.g., `[q] quit`).
- [ ] **Icons & Symbols:** Use UTF-8 symbols only with a tested ASCII fallback and never as the sole status signal.
- [ ] **Adaptive UI:** Collapse panels or switch views based on terminal width/height.
- [ ] **Muted Meta:** Dim secondary data (timestamps, hashes) to reduce cognitive load.

## Colour as a UI Primitive

Use colour strategically without making it the only carrier of meaning:

- **Status Perception:** Red/Yellow/Green for health.
- **Hierarchy:** Highlighting the "active" item in a list with a distinct background.
- **Focus:** Greying out inactive sections.
