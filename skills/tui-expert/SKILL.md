---
name: tui-expert
description: Expert guidance for building professional, responsive, and beautiful Terminal User Interfaces (TUIs) in Rust (Ratatui) and Ruby (TTY, cli-ui). Covers architectural patterns (Conductor/Model/App), async client reuse, parallelisation, secure authentication, and modern visual aesthetics. Use when building, refactoring, or styling TUI applications in any language.
---

# TUI Expert

This skill provides the architectural and aesthetic foundation for building world-class TUIs across Rust and Ruby ecosystems.

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
