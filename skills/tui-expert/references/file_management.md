# File Management TUIs

File managers focus on tree navigation, previews, and high-performance I/O.

## Key Examples
- **Yazi:** Blazing-fast file manager.
- **Termscp:** Dual-pane file transfer utility.

## Specialized Patterns

### 1. Dual/Triple Pane Layouts
- **Left:** Parent directory.
- **Middle:** Current directory (Active).
- **Right:** File preview (Metadata, Image, or Text).

### 2. Previews
- Use terminal image protocols (Kitty, Sixel, Iturm2) for image previews if supported.
- Use syntax highlighting (e.g., `syntect` in Rust) for code previews.

### 3. Async Task Queue
- File operations (Copy, Move, Hash) should run in a background queue.
- Show a persistent "Tasks" indicator with progress bars for long-running I/O.

## Design Rules
- **Quick Jump:** Implement fuzzy finding for files.
- **Mode Indicators:** Clearly show "Select Mode", "Normal Mode", or "Visual Mode".
