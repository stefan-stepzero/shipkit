#!/usr/bin/env python3
"""
Shipkit Relentless Stop Hook

Prevents Claude from stopping until the completion promise is met.
Used by: shipkit-build-relentlessly, shipkit-test-relentlessly, shipkit-lint-relentlessly

Based on the ralph-wiggum pattern:
1. Checks if .shipkit/relentless-state.local.md exists
2. If not, allows stop (quick exit)
3. If yes, blocks stop and feeds task back to Claude
4. Claude is responsible for:
   - Checking if the completion_promise is met
   - Deleting the state file when successful
   - Then stopping again

The hook does NOT run commands - it just manages iteration and blocks/allows stop.
"""

import json
import os
import re
import sys
from pathlib import Path


# Note: No subprocess import - this hook does NOT run commands.
# Claude is responsible for running commands and checking if the promise is met.


def main():
    # Read hook input from stdin (required but not used for decisions)
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        pass  # Continue anyway

    # Find project directory
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    state_file = Path(project_dir) / ".shipkit" / "relentless-state.local.md"

    # Quick exit if no state file (not in relentless mode)
    if not state_file.exists():
        sys.exit(0)

    # Parse state file
    state = parse_state_file(state_file)
    if not state:
        # Can't parse state, allow stop
        sys.exit(0)

    # Check if explicitly disabled
    enabled = state.get("enabled", True)
    if enabled is False or str(enabled).lower() == "false":
        # Disabled - allow stop without cleanup (user can re-enable)
        sys.exit(0)

    # Check iteration limit
    iteration = state.get("iteration", 1)
    max_iterations = state.get("max_iterations", 10)

    if iteration >= max_iterations:
        # Max iterations reached - allow stop, clean up
        cleanup_state_file(state_file)
        output = {
            "systemMessage": f"Relentless mode: Reached max iterations ({max_iterations}). Stopping."
        }
        print(json.dumps(output))
        sys.exit(0)

    # Not done yet - increment iteration and block stop
    new_iteration = iteration + 1
    update_iteration(state_file, new_iteration)

    # Build the continue reason from task + completion_promise
    skill = state.get("skill", "relentless")
    task = state.get("task", "Complete the task")
    completion_promise = state.get("completion_promise", "Task completed successfully")

    reason = build_continue_reason(
        skill=skill,
        iteration=new_iteration,
        max_iterations=max_iterations,
        task=task,
        completion_promise=completion_promise
    )

    # Block the stop
    result = {
        "decision": "block",
        "reason": reason
    }
    print(json.dumps(result))
    sys.exit(0)


def parse_state_file(state_file: Path) -> dict:
    """Parse the YAML frontmatter and body from state file."""
    try:
        content = state_file.read_text(encoding="utf-8")
    except Exception:
        return {}

    # Split frontmatter and body
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    frontmatter = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML frontmatter (simple key: value parsing)
    state = {}
    for line in frontmatter.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Try to parse as int
            try:
                value = int(value)
            except ValueError:
                pass
            state[key] = value

    state["task"] = body
    return state


def update_iteration(state_file: Path, new_iteration: int):
    """Update the iteration count in the state file."""
    try:
        content = state_file.read_text(encoding="utf-8")
        # Simple regex replacement for iteration field
        updated = re.sub(
            r"^iteration:\s*\d+",
            f"iteration: {new_iteration}",
            content,
            flags=re.MULTILINE
        )
        state_file.write_text(updated, encoding="utf-8")
    except Exception:
        pass  # Best effort


def cleanup_state_file(state_file: Path):
    """Remove the state file to exit relentless mode."""
    try:
        state_file.unlink()
    except Exception:
        pass  # Best effort


def build_continue_reason(skill: str, iteration: int, max_iterations: int,
                          task: str, completion_promise: str) -> str:
    """Build the reason message that becomes Claude's next instruction."""

    skill_names = {
        "build-relentlessly": "Build",
        "test-relentlessly": "Test",
        "lint-relentlessly": "Lint"
    }
    skill_display = skill_names.get(skill, skill.replace("-", " ").title())

    return f"""**Relentless Mode: {skill_display} - Iteration {iteration}/{max_iterations}**

You are in relentless mode. The completion promise has NOT been met yet.

**Completion Promise:**
{completion_promise}

**Your Task:**
{task}

**Instructions:**
1. Run the appropriate command to check current status
2. Analyze any errors or failures
3. Make fixes to address the issues
4. Check again - if the promise is now met, delete `.shipkit/relentless-state.local.md` and stop
5. If not met, continue fixing (the hook will increment iteration when you try to stop)

Do not give up. Keep working until the completion promise is satisfied or you've exhausted reasonable approaches."""


if __name__ == "__main__":
    main()
