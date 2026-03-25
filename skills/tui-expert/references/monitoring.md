# Monitoring TUIs (System, Network, Services)

Monitoring TUIs prioritize real-time data flow, health status, and dense information display.

## Key Examples
- **Kmon:** Linux kernel monitor.
- **Oryx:** eBPF network sniffer.
- **Oxker:** Docker container controller.
- **GitLab Runner TUI:** Service/Job monitor.

## Specialized Patterns

### 1. The Polling Lifecycle
- Use a background thread/async task to refresh data.
- **Visual Feedback:** Always show a "last updated" timestamp or a "Refreshing..." spinner.
- **Backoff:** Increase poll interval if the terminal is hidden or the API returns errors.

### 2. Status Density
- Use small symbols: `●` (Live), `○` (Paused), `✖` (Error).
- **Sparklines:** If supported (e.g., `ratatui` Sparkline), show historical trends (CPU/RAM usage) in a single line.

### 3. Log Streaming
- Dedicate a section (usually the bottom 30%) to a scrolling list of logs.
- Use `ratatui`'s `List` or `Paragraph` with a manual scroll offset.

## Design Rules
- **Color by Status:** Red is critical, Yellow is warning, Green is healthy.
- **Muted Inactive:** Grey out "offline" or "dead" items to focus on what's running.
