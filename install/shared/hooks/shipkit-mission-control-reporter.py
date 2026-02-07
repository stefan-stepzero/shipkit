#!/usr/bin/env python3
"""
Shipkit Mission Control - Reporter Hook

Reports Claude Code events to the Mission Control server.
Passive mode: only reports if server is already running.
User must explicitly start server via /mission-control start.

Hook events: SessionStart, PostToolUse, Stop
"""

import sys
import os
import json
import time
from pathlib import Path

SERVER_URL = os.environ.get("SHIPKIT_MISSION_CONTROL_URL", "http://localhost:7777")

# Track last artifact sync time to avoid redundant sends
_ARTIFACT_CACHE_FILE = ".shipkit/.artifact-sync-cache.json"


def collect_artifacts(cwd: str) -> dict | None:
    """Scan .shipkit/ for JSON artifacts that follow the shipkit-artifact convention.

    Only includes artifacts modified since last sync to minimize payload.
    Returns dict of {filename: artifact_data} or None if nothing changed.
    """
    shipkit_dir = Path(cwd) / ".shipkit"
    if not shipkit_dir.exists():
        return None

    cache_path = Path(cwd) / _ARTIFACT_CACHE_FILE
    last_sync = 0
    try:
        if cache_path.exists():
            last_sync = json.loads(cache_path.read_text()).get("lastSync", 0)
    except Exception:
        pass

    artifacts = {}
    for json_file in shipkit_dir.glob("*.json"):
        # Skip internal files
        if json_file.name.startswith(".") or json_file.name == "skill-usage.json":
            continue
        try:
            mtime = json_file.stat().st_mtime
            if mtime <= last_sync:
                continue
            data = json.loads(json_file.read_text())
            # Only ship files that follow the shipkit-artifact convention
            if data.get("$schema") == "shipkit-artifact":
                artifacts[json_file.name] = data
        except Exception:
            continue

    if not artifacts:
        return None

    # Update sync cache
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"lastSync": time.time()}))
    except Exception:
        pass

    return artifacts


def server_running() -> bool:
    """Check if Mission Control server is running."""
    try:
        import urllib.request
        req = urllib.request.Request(f"{SERVER_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=0.5) as response:
            return response.status == 200
    except Exception:
        return False


def send_event(event_data: dict):
    """Send event to Mission Control server."""
    try:
        import urllib.request
        data = json.dumps(event_data).encode('utf-8')
        req = urllib.request.Request(
            f"{SERVER_URL}/api/events",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        hook_input = {}

    session_id = hook_input.get("session_id", "unknown")
    hook_event = hook_input.get("hook_event_name", "unknown")
    tool_name = hook_input.get("tool_name", "")
    cwd = hook_input.get("cwd", os.getcwd())

    # Extract project name from cwd
    project_name = Path(cwd).name

    # Build event payload
    event_data = {
        "sessionId": session_id,
        "project": project_name,
        "projectPath": cwd,
        "event": hook_event,
        "tool": tool_name,
        "timestamp": time.time()
    }

    # Add tool-specific data
    if tool_name == "Skill":
        tool_input = hook_input.get("tool_input", {})
        if isinstance(tool_input, dict):
            event_data["skill"] = tool_input.get("skill", "")

    # Only report if server is already running (passive mode)
    # User must explicitly start server via /mission-control start
    if not server_running():
        print(json.dumps({}))  # Silent exit - no server, no reporting
        return

    # Collect .shipkit/ JSON artifacts if any have changed
    artifacts = collect_artifacts(cwd)
    if artifacts:
        event_data["artifacts"] = artifacts

    # Server exists, report to it
    send_event(event_data)

    # No output needed - this hook is informational only
    print(json.dumps({}))


if __name__ == "__main__":
    main()
