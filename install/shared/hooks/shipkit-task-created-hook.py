#!/usr/bin/env python3
"""
Shipkit TaskCreated Hook

Minimal v1 validation gate that fires when a task is created.
Rejects tasks with an empty/missing title so the backlog stays legible.

IMPORTANT: the TaskCreated event payload carries `task_title` (plus task_id /
task_status / completion_notes) but NOT a description field (per
hooks-reference.md, CC 2.1.156). Requiring a description here would block EVERY
task creation — there is no description in the payload to satisfy. So this hook
always requires a non-empty title, and validates a description ONLY when the
payload actually includes one (future-proof if CC ever adds the field).

Hook events:
  - Exit 0: Allow task creation
  - Exit 2: Block creation, stderr message sent as feedback

Input: JSON on stdin with TaskCreated event data (task_title, task_id, ...)
Output: stderr for feedback message when blocking (exit 2)
"""

import json
import sys

HOOK_NAME = "task-created"


def first_nonempty(hook_input: dict, *keys: str) -> str:
    """Return the first present, stringified value for the given keys."""
    for key in keys:
        value = hook_input.get(key)
        if value is not None:
            return str(value).strip()
    return ""


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Accept either the documented (task_*) or bare key names defensively.
    title = first_nonempty(hook_input, "task_title", "title", "subject")

    # Always require a non-empty title (the event provides task_title).
    if not title:
        print(
            "Task rejected: missing title. "
            "A task needs a non-empty title before it can be created.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Validate a description ONLY if the payload actually carries one. The
    # standard TaskCreated event does not include a description, so we must not
    # require it unconditionally (that would block all task creation).
    desc_keys = ("task_description", "description")
    if any(key in hook_input for key in desc_keys):
        description = first_nonempty(hook_input, *desc_keys)
        if not description:
            print(
                "Task rejected: description field present but empty. "
                "Provide a non-empty description.",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
