# TUI Layout & Responsiveness

## Adaptive Layout Mode

TUIs should adapt to the terminal size to remain usable on both laptops and large monitors.

### Pattern: Detail Layout Mode
```rust
pub enum DetailLayoutMode {
    SidePanel,   // Large width
    BottomPanel, // Large height, small width
    Compact,     // Small terminal
}

pub fn detail_layout_mode(width: u16, height: u16) -> DetailLayoutMode {
    if width > 140 {
        DetailLayoutMode::SidePanel
    } else if height > 40 {
        DetailLayoutMode::BottomPanel
    } else {
        DetailLayoutMode::Compact
    }
}
```

## Modals & Centered Popups

Use a "centered rect" function to render popups consistently.

### Pattern: Centered Rect
```rust
pub fn centered_rect(width_percent: u16, height_percent: u16, area: Rect) -> Rect {
    let vert = Layout::vertical([
        Constraint::Percentage((100 - height_percent) / 2),
        Constraint::Percentage(height_percent),
        Constraint::Percentage((100 - height_percent) / 2),
    ])
    .split(area);

    Layout::horizontal([
        Constraint::Percentage((100 - width_percent) / 2),
        Constraint::Percentage(width_percent),
        Constraint::Percentage((100 - width_percent) / 2),
    ])
    .split(vert[1])[1]
}
```

### Ruby Manual Layout (tty-screen)
In Ruby, without a built-in layout engine, use `tty-screen` to detect dimensions and manually slice the view.
```ruby
require 'tty-screen'
width, height = TTY::Screen.size
header_height = 3
body_height = height - header_height - 3
# Render based on calculated segments
```

## Dashboard Segmentation (Header / Tabs / Status)

A robust TUI should maintain a consistent frame structure:

1. **Header (Length 3-4):** Title, Polling state, dynamic info.
2. **Tabs (Length 1):** Top-level navigation hints.
3. **Filter Bar (Length 1):** Current filters, sort order, or search input.
4. **Content (Min 1):** The main functional area (Table, List, Help).
5. **Status Bar (Length 3):** Hotkey hints, loading states, counts.
