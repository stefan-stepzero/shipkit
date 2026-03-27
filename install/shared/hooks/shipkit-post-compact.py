#!/usr/bin/env python3
"""
Shipkit PostCompact Hook

Auto-saves a progress checkpoint after context compaction.
Ensures session state survives compaction without user intervention.

Fires after compaction completes (trigger: manual or auto).
Exit 0 always — this is observability only, never blocks.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_project_root(start: Path) -> Path | None:
    """Walk up from start to find the project root."""
    current = start.resolve()
    for _ in range(20):
        if (current / '.shipkit').is_dir() or (current / '.claude').is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    env_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    start_dir = Path(env_dir) if env_dir else Path(hook_input.get("cwd", os.getcwd()))
    project_dir = find_project_root(start_dir) or start_dir
    shipkit_dir = project_dir / ".shipkit"

    if not shipkit_dir.exists():
        sys.exit(0)

    progress_file = shipkit_dir / "progress.json"
    trigger = hook_input.get("trigger", "unknown")

    # Read existing progress or create skeleton
    progress = {}
    if progress_file.exists():
        try:
            progress = json.loads(progress_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            progress = {}

    # Append compaction checkpoint to sessions
    sessions = progress.get("sessions", [])
    sessions.append({
        "timestamp": datetime.now().isoformat(),
        "summary": f"Auto-checkpoint after {trigger} compaction",
        "source": "post-compact-hook"
    })

    # Keep last 20 sessions to prevent unbounded growth
    if len(sessions) > 20:
        sessions = sessions[-20:]

    progress["sessions"] = sessions
    progress["lastCompaction"] = {
        "timestamp": datetime.now().isoformat(),
        "trigger": trigger
    }

    try:
        progress_file.write_text(
            json.dumps(progress, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError:
        pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
