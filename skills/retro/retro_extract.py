#!/usr/bin/env python3
"""Extract and summarize Claude Code session data from .jsonl transcripts.

Usage:
    python retro_extract.py <project_path> --last N
    python retro_extract.py <project_path> --session-id <UUID>
    python retro_extract.py <project_path> --list
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"


def encode_project_path(project_path: str) -> str:
    """Convert a project path to Claude's directory name encoding.

    Claude encodes paths by replacing '/' with '-' and prepending '-'.
    e.g. /Users/damacus/repos/foo -> -Users-damacus-repos-foo
    """
    return project_path.replace("/", "-")


def find_project_dir(project_path: str) -> Path | None:
    """Find the Claude project directory for a given workspace path."""
    encoded = encode_project_path(os.path.abspath(project_path))
    candidate = CLAUDE_PROJECTS_DIR / encoded
    if candidate.is_dir():
        return candidate

    # Try partial match (worktrees, etc.)
    for d in CLAUDE_PROJECTS_DIR.iterdir():
        if d.is_dir() and encoded in d.name:
            return d

    return None


def find_all_project_dirs(
    project_path: str,
) -> list[Path]:
    """Find all Claude project dirs matching a path."""
    encoded = encode_project_path(
        os.path.abspath(project_path)
    )
    dirs = []
    if not CLAUDE_PROJECTS_DIR.is_dir():
        return dirs
    for d in CLAUDE_PROJECTS_DIR.iterdir():
        if d.is_dir() and encoded in d.name:
            dirs.append(d)
    return dirs


def list_sessions(project_path: str) -> list[dict]:
    """List all sessions for a project, sorted by modification time (newest first)."""
    sessions = []
    project_dirs = find_all_project_dirs(project_path)

    if not project_dirs:
        # Fall back to listing ALL projects
        if CLAUDE_PROJECTS_DIR.is_dir():
            project_dirs = [
                d for d in CLAUDE_PROJECTS_DIR.iterdir() if d.is_dir()
            ]

    for project_dir in project_dirs:
        for jsonl_file in project_dir.glob("*.jsonl"):
            # Skip subagent files
            if "subagents" in str(jsonl_file):
                continue

            session_id = jsonl_file.stem
            mtime = jsonl_file.stat().st_mtime
            size = jsonl_file.stat().st_size

            # Quick peek at first few lines for metadata
            metadata = _peek_session_metadata(jsonl_file)

            sessions.append(
                {
                    "session_id": session_id,
                    "path": str(jsonl_file),
                    "project_dir": project_dir.name,
                    "mtime": mtime,
                    "mtime_human": datetime.fromtimestamp(
                        mtime, tz=timezone.utc
                    ).strftime("%Y-%m-%d %H:%M UTC"),
                    "size_kb": round(size / 1024, 1),
                    **metadata,
                }
            )

    sessions.sort(key=lambda s: s["mtime"], reverse=True)
    return sessions


def _peek_session_metadata(jsonl_file: Path) -> dict:
    """Read first few lines to extract branch, version, cwd."""
    metadata = {"branch": "", "version": "", "cwd": "", "slug": ""}
    try:
        with open(jsonl_file) as f:
            for i, line in enumerate(f):
                if i > 20:
                    break
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("gitBranch") and not metadata["branch"]:
                    metadata["branch"] = record["gitBranch"]
                if record.get("version") and not metadata["version"]:
                    metadata["version"] = record["version"]
                if record.get("cwd") and not metadata["cwd"]:
                    metadata["cwd"] = record["cwd"]
                if record.get("slug") and not metadata["slug"]:
                    metadata["slug"] = record["slug"]
    except (OSError, UnicodeDecodeError):
        pass
    return metadata


def parse_session(jsonl_path: str) -> dict:
    """Parse a full session JSONL file and return structured summary."""
    records = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # Classify records
    type_counts: Counter = Counter()
    tool_counts: Counter = Counter()
    user_messages: list[dict] = []
    git_commits: list[str] = []
    skills_invoked: list[str] = []
    errors: list[str] = []
    timestamps: list[str] = []
    metadata = {"branch": "", "version": "", "cwd": "", "slug": ""}

    for record in records:
        record_type = record.get("type", "unknown")
        type_counts[record_type] += 1

        # Extract metadata from any record
        if record.get("gitBranch") and not metadata["branch"]:
            metadata["branch"] = record["gitBranch"]
        if record.get("version") and not metadata["version"]:
            metadata["version"] = record["version"]
        if record.get("cwd") and not metadata["cwd"]:
            metadata["cwd"] = record["cwd"]
        if record.get("slug") and not metadata["slug"]:
            metadata["slug"] = record["slug"]

        ts = record.get("timestamp")
        if ts:
            timestamps.append(ts)

        msg = record.get("message", {})
        if not isinstance(msg, dict):
            msg = {}
        content = msg.get("content", [])

        if record_type == "user" and not record.get("isMeta"):
            text = _extract_text(content)
            if text and not text.startswith("<local-command"):
                user_messages.append(
                    {
                        "text": text[:500],
                        "timestamp": ts or "",
                    }
                )

        elif record_type == "assistant":
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_use":
                        tool_name = block.get("name", "unknown")
                        tool_counts[tool_name] += 1

                        # Detect git commits
                        if tool_name == "Bash":
                            cmd = block.get("input", {}).get("command", "")
                            if "git commit" in cmd:
                                git_commits.append(cmd[:200])

                        # Detect skill/command invocations
                        if tool_name == "Agent":
                            agent_input = block.get("input", {})
                            task = agent_input.get("task", "")[:100]
                            skills_invoked.append(f"Agent: {task}")

        elif record_type == "progress":
            data = record.get("data", {})
            if isinstance(data, dict):
                progress_type = data.get("type", "")
                if progress_type == "hook_progress":
                    hook = data.get("hookName", "")
                    if hook:
                        skills_invoked.append(f"Hook: {hook}")

    # Calculate duration
    duration = ""
    if len(timestamps) >= 2:
        try:
            ts_sorted = sorted(timestamps)
            start = datetime.fromisoformat(ts_sorted[0].replace("Z", "+00:00"))
            end = datetime.fromisoformat(ts_sorted[-1].replace("Z", "+00:00"))
            delta = end - start
            minutes = int(delta.total_seconds() / 60)
            if minutes < 60:
                duration = f"{minutes}m"
            else:
                duration = f"{minutes // 60}h {minutes % 60}m"
        except (ValueError, IndexError):
            pass

    # Count turns (user message → assistant response pairs)
    turns = type_counts.get("user", 0)

    return {
        "session_id": Path(jsonl_path).stem,
        "metadata": metadata,
        "duration": duration,
        "turns": turns,
        "type_counts": dict(type_counts),
        "tool_counts": dict(
            sorted(tool_counts.items(), key=lambda x: -x[1])
        ),
        "user_messages": user_messages,
        "git_commits": git_commits,
        "skills_invoked": list(set(skills_invoked)),
        "errors": errors,
    }


def _extract_text(content) -> str:
    """Extract text from message content (handles both string and list formats)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return " ".join(parts).strip()
    return ""


def format_session_summary(session: dict) -> str:
    """Format a parsed session as readable markdown."""
    meta = session["metadata"]
    lines = []

    lines.append(f"# Session: {session['session_id']}")
    if meta.get("slug"):
        lines.append(f"**Slug**: {meta['slug']}")
    lines.append("")

    lines.append("## Metadata")
    lines.append("")
    if meta.get("branch"):
        lines.append(f"- **Branch**: `{meta['branch']}`")
    if meta.get("cwd"):
        lines.append(f"- **Working Dir**: `{meta['cwd']}`")
    if meta.get("version"):
        lines.append(f"- **CLI Version**: {meta['version']}")
    if session.get("duration"):
        lines.append(f"- **Duration**: {session['duration']}")
    lines.append(f"- **Turns**: {session['turns']}")
    lines.append("")

    # Type distribution
    lines.append("## Record Types")
    lines.append("")
    for rtype, count in sorted(
        session["type_counts"].items(), key=lambda x: -x[1]
    ):
        lines.append(f"- {rtype}: {count}")
    lines.append("")

    # Tool usage
    if session["tool_counts"]:
        lines.append("## Tool Usage")
        lines.append("")
        for tool, count in session["tool_counts"].items():
            lines.append(f"- **{tool}**: {count}")
        lines.append("")

    # Skills/hooks invoked
    if session["skills_invoked"]:
        lines.append("## Skills / Hooks Invoked")
        lines.append("")
        for skill in session["skills_invoked"]:
            lines.append(f"- {skill}")
        lines.append("")

    # Git commits
    if session["git_commits"]:
        lines.append("## Git Commits")
        lines.append("")
        for commit in session["git_commits"]:
            lines.append(f"- `{commit}`")
        lines.append("")

    # User messages (conversation flow)
    if session["user_messages"]:
        lines.append("## Conversation Flow (User Messages)")
        lines.append("")
        for i, msg in enumerate(session["user_messages"], 1):
            text = msg["text"].replace("\n", " ")[:200]
            ts = msg.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts_short = dt.strftime("%H:%M")
                except ValueError:
                    ts_short = ""
            else:
                ts_short = ""
            prefix = f"[{ts_short}] " if ts_short else ""
            lines.append(f"{i}. {prefix}{text}")
        lines.append("")

    return "\n".join(lines)


def format_session_list(sessions: list[dict]) -> str:
    """Format session list as a table."""
    if not sessions:
        return "No sessions found."

    lines = []
    lines.append("# Available Sessions")
    lines.append("")
    lines.append(
        "| # | Date | Branch | Slug"
        " | Size | Session ID |"
    )
    lines.append(
        "|---|------|--------|------"
        "|------|------------|"
    )
    for i, s in enumerate(sessions, 1):
        slug = s.get("slug", "")[:25]
        branch = s.get("branch", "")[:20]
        sid = s['session_id'][:8]
        lines.append(
            f"| {i} | {s['mtime_human']}"
            f" | `{branch}` | {slug}"
            f" | {s['size_kb']}KB"
            f" | `{sid}…` |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and summarize Claude Code session data"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the project (used to find matching sessions)",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=None,
        help="Analyze the N most recent sessions (default: 1, max: 5)",
    )
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Analyze a specific session by UUID",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available sessions",
    )
    parser.add_argument(
        "--all-projects",
        action="store_true",
        help="Search across all projects (not just the specified path)",
    )

    args = parser.parse_args()

    if args.list:
        sessions = list_sessions(args.project_path)
        print(format_session_list(sessions))
        return

    if args.session_id:
        # Find the specific session across all projects
        found = None
        if CLAUDE_PROJECTS_DIR.is_dir():
            for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
                if not project_dir.is_dir():
                    continue
                candidate = project_dir / f"{args.session_id}.jsonl"
                if candidate.exists():
                    found = str(candidate)
                    break

        if not found:
            print(f"Session {args.session_id} not found.", file=sys.stderr)
            sys.exit(1)

        session = parse_session(found)
        print(format_session_summary(session))
        return

    # Default: --last N
    n = min(args.last or 1, 5)
    sessions = list_sessions(args.project_path)

    if not sessions and not args.all_projects:
        # Try all projects
        sessions = list_sessions("/nonexistent-to-trigger-fallback")

    if not sessions:
        print("No sessions found.", file=sys.stderr)
        sys.exit(1)

    for s in sessions[:n]:
        session = parse_session(s["path"])
        print(format_session_summary(session))
        if n > 1:
            print("---")
            print("")


if __name__ == "__main__":
    main()
