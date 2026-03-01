#!/usr/bin/env python3
"""
Shipkit TeammateIdle Hook

Fires when a teammate is about to go idle (stop working).
Checks if the teammate still has uncompleted tasks and keeps them working if so.

Hook events:
  - Exit 0: Allow idle
  - Exit 2: Send feedback, keep teammate working

Requires: .shipkit/team-state.local.json to be present (written by /shipkit-team).
If no team state file exists, this hook exits 0 (no-op outside team mode).

Input: JSON on stdin with hook event data (session_id, teammate info, etc.)
Output: stderr for feedback messages when keeping teammate working (exit 2)
"""

import json
import os
import sys
from pathlib import Path


def find_project_root(start: Path) -> Path | None:
    """Walk up from start to find the project root (directory containing .shipkit/ or .claude/)."""
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
    # Read hook input from stdin
    hook_input = {}
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        pass

    # Find project directory — walk up from CWD to handle subdirectories
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    start_dir = Path(env_dir) if env_dir else Path(hook_input.get("cwd", os.getcwd()))
    project_dir = find_project_root(start_dir) or start_dir
    shipkit_dir = project_dir / ".shipkit"

    # Quick exit if not in team mode
    team_state_file = shipkit_dir / "team-state.local.json"
    if not team_state_file.exists():
        sys.exit(0)

    # Read team state
    try:
        team_state = json.loads(team_state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Can't read state, allow idle
        sys.exit(0)

    # Check plan for incomplete tasks
    plan_path = team_state.get("planPath", "")
    if not plan_path:
        sys.exit(0)

    plan_file = project_dir / plan_path
    if not plan_file.exists():
        sys.exit(0)

    try:
        plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    # Count pending tasks across all phases
    pending_tasks = []
    phases = plan_data.get("plan", {}).get("phases", [])
    for phase in phases:
        for task in phase.get("tasks", []):
            if task.get("status", "pending") != "completed":
                pending_tasks.append(f"  - {task['id']}: {task['description']}")

    if pending_tasks:
        task_list = "\n".join(pending_tasks[:10])  # Cap at 10 to avoid huge messages
        remaining = len(pending_tasks)
        print(
            f"There are {remaining} incomplete tasks in the plan. "
            f"Please continue working on your assigned tasks:\n\n"
            f"{task_list}",
            file=sys.stderr,
        )
        sys.exit(2)

    # All tasks done, allow idle
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Silent failure — never block on hook errors
        sys.exit(0)
