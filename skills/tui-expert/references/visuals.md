# TUI Visuals & Pretty Colours

## Gemini Signature Gradients

Use this logic to create the signature Gemini CLI gradient effect.

### Colour Constants (RGB)
- **Blue (Start):** `(125, 207, 255)`
- **Purple (End):** `(187, 154, 247)`
- **Muted:** `Color::DarkGray`
- **Accent:** `Color::Cyan`

### Implementation Pattern (Rust/Ratatui)

```rust
pub fn gradient_text(text: &str, start_rgb: (u8, u8, u8), end_rgb: (u8, u8, u8)) -> Line<'static> {
    let chars: Vec<char> = text.chars().collect();
    let n = chars.len();
    if n == 0 { return Line::from(vec![]); }
    if n == 1 {
        return Line::from(vec![Span::styled(
            text.to_string(),
            Style::default().fg(Color::Rgb(start_rgb.0, start_rgb.1, start_rgb.2)),
        )]);
    }

    let mut spans = Vec::with_capacity(n);
    for (i, &c) in chars.iter().enumerate() {
        let ratio = i as f32 / (n - 1) as f32;
        let r = (start_rgb.0 as f32 + (end_rgb.0 as f32 - start_rgb.0 as f32) * ratio) as u8;
        let g = (start_rgb.1 as f32 + (end_rgb.1 as f32 - start_rgb.1 as f32) * ratio) as u8;
        let b = (start_rgb.2 as f32 + (end_rgb.2 as f32 - start_rgb.2 as f32) * ratio) as u8;
        spans.push(Span::styled(
            c.to_string(),
            Style::default().fg(Color::Rgb(r, g, b)).add_modifier(Modifier::BOLD),
        ));
    }
    Line::from(spans)
}
```

## Icons & Emojis

Modern TUIs use symbols to increase information density without clutter.

### Status Symbols
- **Healthy:** `✓`, `●`, `✔`
- **Warning:** `⚠`, `‼`, `?`
- **Error:** `✗`, `✖`, `✘`
- **Loading:** `⠋`, `⠙`, `⠹`, `⠸` (Braille dots for spinners)

### Hierarchy & Navigation
- **Active Item:** `▶`, `→`, `»`
- **Folder:** `📁`, `` (Nerd Fonts)
- **File:** `📄`, `` (Nerd Fonts)

## Box-Drawing & Borders

Avoid generic `+---+` ASCII boxes. Use UTF-8 box-drawing characters.

- **Double Borders:** `╔═══╗`
- **Rounded Corners:** `╭───╮` (Popular in Yazi and Spotify Player)
- **Dashed Lines:** `┆`, `┊` (Good for separating metadata)

## Side-Quest: The Popularity of Colour
My research confirms that **Colour is the #1 feature** users cite when describing a "beautiful" TUI.
- **Brand Identity:** TUIs like Spotify Player or Rainfrog use brand colours to feel "official".
- **Contrast is King:** All top TUIs use `Color::DarkGray` for secondary info to ensure the primary data pops.
- **Consistency:** Use a central `styles.rs` (Rust) or `theme.rb` (Ruby) to ensure the same "Green" is used everywhere.
