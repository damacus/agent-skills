# Ruby TUI Patterns (TTY & cli-ui)

Ruby TUIs often lean on modularity and high-level abstractions rather than a unified layout engine like Ratatui.

## Core Ecosystem
- **TTY Toolkit:** A collection of independent gems (`tty-prompt`, `tty-table`, `tty-progressbar`).
- **cli-ui:** Shopify's library for structured, "framed" CLI output.

## Specialized Patterns

### 1. Sequential Prompting (Interactive Wizards)
Instead of a full dashboard, Ruby TUIs often use interactive prompts.
```ruby
prompt = TTY::Prompt.new
choice = prompt.select("Choose your runner mode?", %w(Active Idle Offline))
```

### 2. Framing & Sections (cli-ui)
Use frames to logically group output.
```ruby
CLI::UI::Frame.open('Database Status') do
  puts "Connecting to DB..."
end
```

### 3. Async Interaction
While Ruby is traditionally synchronous, use the `async` gem or `Concurrent::Ruby` to update spinners while waiting for I/O.

## Design Rules
- **Gemini Aesthetics in Ruby:**
  - Use `pastel` gem for RGB/Gradient support.
  - Use `tty-screen` to manually calculate adaptive layouts if building a full-screen app.
