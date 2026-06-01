#!/usr/bin/env python3
"""
Shipkit PreCompact Hook

Snapshots orchestration state before context compaction so the pipeline can
recover if compaction loses in-context state.

Fires before compaction begins (trigger: manual or auto).
Reads .shipkit/orchestration.json if present and writes a timestamped copy to
.shipkit/orchestration-checkpoint.json (with a checkpointedAt field).
Exit 0 always — this is observability only, never blocks. If orchestration.json
is absent, exits 0 silently.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

HOOK_NAME = "pre-compact"

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
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    env_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    start_dir = Path(env_dir) if env_dir else Path(hook_input.get("cwd", os.getcwd()))
    project_dir = find_project_root(start_dir) or start_dir
    shipkit_dir = project_dir / ".shipkit"

    orchestration_file = shipkit_dir / "orchestration.json"
    if not orchestration_file.exists():
        # Nothing to checkpoint — exit silently.
        sys.exit(0)

    try:
        orchestration = json.loads(orchestration_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Can't read state — don't block compaction.
        sys.exit(0)

    trigger = hook_input.get("trigger", "unknown")
    checkpoint = {
        "checkpointedAt": datetime.now().isoformat(),
        "trigger": trigger,
        "source": "pre-compact-hook",
        "orchestration": orchestration,
    }

    checkpoint_file = shipkit_dir / "orchestration-checkpoint.json"
    try:
        checkpoint_file.write_text(
            json.dumps(checkpoint, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError:
        pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
