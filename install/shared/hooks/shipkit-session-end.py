#!/usr/bin/env python3
"""
Shipkit SessionEnd Hook

Final checkpoint + cleanup when session terminates.
Writes exit checkpoint to progress.json and cleans up .local. temp files.

Exit 0 always — SessionEnd cannot block and has a 1.5s default timeout.
Keep this script fast.
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

    reason = hook_input.get("reason", "unknown")

    # ── Write exit checkpoint to progress.json ──
    progress_file = shipkit_dir / "progress.json"
    progress = {}
    if progress_file.exists():
        try:
            progress = json.loads(progress_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            progress = {}

    sessions = progress.get("sessions", [])
    sessions.append({
        "timestamp": datetime.now().isoformat(),
        "summary": f"Session ended ({reason})",
        "source": "session-end-hook"
    })

    if len(sessions) > 20:
        sessions = sessions[-20:]

    progress["sessions"] = sessions
    progress["lastSessionEnd"] = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason
    }

    try:
        progress_file.write_text(
            json.dumps(progress, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError:
        pass

    # ── Clean up .local. temp state files ──
    # These are session-scoped and should not persist across sessions
    for local_file in shipkit_dir.glob("*.local.*"):
        # Keep .update-check.local (rate-limit cache)
        if "update-check" in local_file.name:
            continue
        try:
            local_file.unlink()
        except OSError:
            pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
