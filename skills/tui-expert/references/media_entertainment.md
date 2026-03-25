# Media & Entertainment TUIs

Media TUIs focus on visualization, synced lyrics/metadata, and audio/video playback control.

## Key Examples
- **Spotify Player:** Feature-rich Spotify client.
- **Audio Visualizers:** Various FFT-based terminal tools.

## Specialized Patterns

### 1. The Visualization Loop
- Use high-frequency updates (e.g., 30-60 FPS) for smooth visualization.
- **FFT Bars:** Map audio frequency data to character heights (e.g., `▂▃▅▆█`).

### 2. Synced Content
- Sync lyrics or subtitles by tracking the precise playback offset.
- Use a dedicated "Scrolling Lyrics" widget that centers the current line.

### 3. Playback State Management
- Clearly show "Shuffle", "Repeat", and "Volume" icons.
- Use a persistent "Now Playing" bar at the bottom.

## Design Rules
- **Vibrant Colours:** Use brand-specific colours (e.g., Spotify Green) but maintain accessibility.
- **Gradients:** Apply gradients to visualization bars for a "premium" feel.
