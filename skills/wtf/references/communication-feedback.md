# Central communication feedback

The authored skills repository owns feedback. Use the configured skills-source
checkout; on Dan's machine this is /Users/damacus/repos/damacus/skills.
Verify the checkout is damacus/skills before writing. Do not use the caller's
project or the installed skill folder as a fallback.

Keep one file per session in feedback/communication/, named with a sanitised
stable session ID. Use a timestamp plus available thread reference if no ID is
exposed. Reuse the same file after compaction or another clarification.

Record only:

- Session ID, date and non-sensitive project label.
- Unique triggering turn IDs and occurrence count.
- A short sanitised excerpt or paraphrase of the confusing wording.
- The clearer explanation and suspected cause, with uncertainty.
- The focused retro finding, proposed improvement and owner's response.
- Whether the improvement was applied and whether confusion recurred.

Redact credentials, personal/health data and private implementation details.
Paraphrase when an excerpt cannot safely be retained. Do not copy whole
transcripts. Never invent a historical incident.

Preserve unrelated changes. Append new occurrences to the same session record;
use an atomic file update and re-read if another writer changed it. Do not
commit or push incident records without the user's explicit approval.

If the central checkout is unavailable or writing is denied, retain the compact
record in the session handoff and explain that central recording is pending.
Do not claim it was saved or create a competing feedback store.
