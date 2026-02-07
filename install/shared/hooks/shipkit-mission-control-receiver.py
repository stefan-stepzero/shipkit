#!/usr/bin/env python3
"""
Shipkit Mission Control - Receiver Hook

Checks for pending commands from Mission Control and injects them into Claude's context.
Supports both legacy single-file inbox and new queue directory format.

Queue lifecycle: .json (pending) → .inflight (claimed) → .processed (done by Claude)

Hook events: PreToolUse
"""

import sys
import os
import json
from pathlib import Path

# Hub location - shared across all instances
INBOX_DIR = Path.home() / ".shipkit-mission-control" / ".shipkit" / "mission-control" / "inbox"


def find_pending_command_queue(session_dir: Path):
    """Find oldest pending .json command in the session queue directory.
    Returns (command_data, inflight_path) or (None, None).
    Skips pickup if a command is already inflight (prevents mid-execution injection).
    """
    try:
        # Guard: if any .inflight file exists, a command is being processed — skip
        if list(session_dir.glob("*.inflight")):
            return None, None

        pending = sorted(session_dir.glob("*.json"))
    except Exception:
        return None, None

    if not pending:
        return None, None

    # Take the oldest (FIFO)
    command_file = pending[0]

    try:
        with open(command_file, 'r', encoding='utf-8') as f:
            command = json.load(f)

        # Atomic claim: rename .json → .inflight
        inflight_path = command_file.with_suffix('.inflight')
        command_file.rename(inflight_path)

        return command, inflight_path
    except Exception:
        return None, None


def find_pending_command_legacy(session_id: str):
    """Legacy: check for single-file inbox/{sessionId}.json.
    Returns (command_data, None) or (None, None).
    Legacy format deletes on pickup (no .inflight tracking).
    """
    command_file = INBOX_DIR / f"{session_id}.json"

    if not command_file.exists():
        return None, None

    try:
        with open(command_file, 'r', encoding='utf-8') as f:
            command = json.load(f)

        # Legacy: delete on consume
        command_file.unlink()
        return command, None
    except Exception:
        return None, None


def build_context(command: dict, inflight_path=None) -> str:
    """Build the additionalContext string for injection."""
    prompt = command.get("prompt", "")
    source = command.get("source", "Mission Control")

    if not prompt:
        return ""

    lines = [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "MISSION CONTROL - Operator Instruction Received",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        prompt,
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"Source: {source}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "**IMPORTANT**: The operator has sent you an instruction via Mission Control.",
        "Please acknowledge receipt and act on this instruction.",
    ]

    if inflight_path:
        # Use POSIX paths (forward slashes) so the mv command works in Git Bash on Windows
        inflight_posix = inflight_path.as_posix()
        processed_posix = inflight_posix.replace('.inflight', '.processed')
        lines.extend([
            "",
            f"**After completing this command**, rename the inflight file to mark it done:",
            f"```",
            f'mv "{inflight_posix}" "{processed_posix}"',
            f"```",
        ])

    return "\n".join(lines)


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        hook_input = {}

    session_id = hook_input.get("session_id", "unknown")
    sid8 = session_id[:8] if session_id != "unknown" else "unknown"

    # Standby bypass: when standby is active, it polls the inbox directly.
    # The hook must NOT claim commands or they'll get stuck as .inflight.
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    standby_state = Path(project_dir) / ".shipkit" / f"standby-state.{sid8}.local.md"
    if standby_state.exists():
        print(json.dumps({}))
        return

    # Try queue directory first (new format)
    session_dir = INBOX_DIR / session_id
    command = None
    inflight_path = None

    if session_dir.is_dir():
        command, inflight_path = find_pending_command_queue(session_dir)

    # Fall back to legacy single-file format
    if command is None:
        command, inflight_path = find_pending_command_legacy(session_id)

    if command:
        context = build_context(command, inflight_path)
        if context:
            print(json.dumps({"additionalContext": context}))
            return

    # No command pending - empty response
    print(json.dumps({}))


if __name__ == "__main__":
    main()
