# Data & DB Management TUIs

These TUIs are optimized for tabular navigation, CRUD operations, and complex filtering.

## Key Examples
- **Rainfrog:** Database manager (Postgres/MySQL/SQLite).
- **CSVlens:** Tabular data viewer.

## Specialized Patterns

### 1. Tabular Navigation
- **Header Locking:** Keep table headers visible while scrolling rows.
- **Column Highlighting:** Highlight the "Sort Key" column with a distinct background or underline.
- **Dynamic Widths:** Use constraints (e.g., `Constraint::Min(10)`) to ensure columns don't collapse on small terminals.

### 2. Selection & Modal Editing
- **Interactive Selection:** Use a highlight bar for the active row.
- **Modals:** Use `centered_rect` for editing values or entering SQL queries.

### 3. Progressive Filtering
- Use a persistent search bar at the bottom or top.
- Apply filters locally if the dataset is small; otherwise, trigger a "re-fetch" conductor task.

## Design Rules
- **Contrast:** High contrast between text and background for readability of small characters.
- **Pagination:** If the dataset is huge, show "Page X of Y" in the status bar.
