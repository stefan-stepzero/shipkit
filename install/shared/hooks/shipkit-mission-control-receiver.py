#!/usr/bin/env python3
"""
Shipkit Mission Control - Receiver Hook

Checks for pending commands from Mission Control and injects them into Claude's context.
Runs on PreToolUse to check before each tool execution.

Hook events: PreToolUse
"""

import sys
import os
import json
from pathlib import Path

# Hub location - shared across all instances
INBOX_DIR = Path.home() / ".shipkit-mission-control" / ".shipkit" / "mission-control" / "inbox"


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        hook_input = {}

    session_id = hook_input.get("session_id", "unknown")

    # Check for pending command for this session
    command_file = INBOX_DIR / f"{session_id}.json"

    if command_file.exists():
        try:
            with open(command_file, 'r', encoding='utf-8') as f:
                command = json.load(f)

            # Remove the command file (consume it)
            command_file.unlink()

            # Extract the prompt/instruction
            prompt = command.get("prompt", "")
            source = command.get("source", "Mission Control")
            timestamp = command.get("timestamp", "")

            if prompt:
                # Inject into Claude's context via additionalContext
                print(json.dumps({
                    "additionalContext": f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 MISSION CONTROL - Operator Instruction Received
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{prompt}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: {source}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**IMPORTANT**: The operator has sent you an instruction via Mission Control.
Please acknowledge receipt and act on this instruction.
"""
                }))
                return
        except Exception as e:
            # Failed to read command, log but don't block
            pass

    # No command pending - empty response
    print(json.dumps({}))


if __name__ == "__main__":
    main()
