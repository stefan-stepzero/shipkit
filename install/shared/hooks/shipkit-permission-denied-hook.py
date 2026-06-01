#!/usr/bin/env python3
"""
Shipkit PermissionDenied Hook

Fires AFTER the auto-mode classifier denies a tool call (NOT when a human
denies an interactive dialog — that path never reaches this event). Surfaces
the denied permission with a remediation message pointing the user at the fix
(add the permission to settings, or re-run /shipkit-update to refresh the
canonical permission set).

Event: PermissionDenied (confirmed event per hooks-reference.md, CC 2.1.156).
Input fields: tool_name, tool_input, denial_reason. Wire this in settings.json
under "PermissionDenied". This event is NOT blockable — exit code 2 only shows
stderr; execution continues regardless. The only structured lever is the
documented output:

    {"hookSpecificOutput": {"hookEventName": "PermissionDenied", "retry": true}}

`retry: true` tells the model it may retry the denied call. We emit it ONLY for
known-safe / transient-looking denials (conservative default: do NOT retry).
When in doubt we surface the denial + remediation and leave retry off.

JSON output is parsed only at exit 0 (per hooks-reference.md exit-code rule),
so this hook always exits 0 and prints its JSON to stdout.

Input: JSON on stdin with PermissionDenied event data.
Output: JSON on stdout (systemMessage + PermissionDenied hookSpecificOutput).
"""

import json
import sys

HOOK_NAME = "permission-denied"

# Tools whose auto-mode denial is typically a benign/recoverable classifier
# miss rather than a genuine policy block — safe to signal a retry. Kept
# deliberately narrow: read-only / inspection tools only. Anything that writes,
# executes shell, or mutates state is NOT auto-retried.
RETRY_SAFE_TOOLS = {"Read", "Glob", "Grep", "LS", "NotebookRead", "TaskList", "TaskGet"}


def describe_permission(hook_input: dict) -> str:
    """Build a human-readable name for the denied permission."""
    tool_name = hook_input.get("tool_name", "unknown tool")

    # For Bash, surface the command; otherwise the tool name is enough.
    tool_input = hook_input.get("tool_input", {})
    detail = ""
    if isinstance(tool_input, dict):
        cmd = tool_input.get("command") or tool_input.get("file_path")
        if cmd:
            detail = f" (`{str(cmd)[:80]}`)"

    return f"{tool_name}{detail}"


def is_retry_safe(hook_input: dict) -> bool:
    """Conservatively decide whether to signal retry:true.

    Only read-only/inspection tools qualify. If we can't confidently classify
    the denial as safe, we return False (no auto-retry).
    """
    tool_name = hook_input.get("tool_name", "")
    if tool_name not in RETRY_SAFE_TOOLS:
        return False
    # A Bash/exec tool can sneak in via odd tool_name casing — guard the input.
    tool_input = hook_input.get("tool_input", {})
    if isinstance(tool_input, dict) and tool_input.get("command"):
        return False
    return True


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    permission = describe_permission(hook_input)
    denial_reason = ""
    if isinstance(hook_input, dict):
        denial_reason = hook_input.get("denial_reason", "") or ""

    message = (
        f"Auto-mode denied: {permission}. "
        f"Shipkit's settings don't currently grant this. To allow it going "
        f"forward, add the permission to .claude/settings.json (permissions.allow), "
        f"or run /shipkit-update to refresh Shipkit's canonical permission set."
    )
    if denial_reason:
        message += f" (reason: {denial_reason})"

    hook_specific = {
        "hookEventName": "PermissionDenied",
    }
    # Conservative: only suggest a retry for known-safe read-only denials.
    if is_retry_safe(hook_input):
        hook_specific["retry"] = True
        message += " This looks like a recoverable read-only denial; retrying."

    output = {
        "systemMessage": message,
        "hookSpecificOutput": hook_specific,
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
