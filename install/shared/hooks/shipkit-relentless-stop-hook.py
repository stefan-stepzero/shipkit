#!/usr/bin/env python3
"""
Shipkit Relentless Stop Hook

Prevents Claude from stopping until success criteria are met.
Used by: shipkit-build-relentlessly, shipkit-test-relentlessly, shipkit-lint-relentlessly

This hook:
1. Checks if .shipkit/relentless-state.local.md exists
2. If not, allows stop (quick exit)
3. If yes, runs the success_command
4. If command succeeds, allows stop and cleans up
5. If command fails, blocks stop with error output as reason
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Can't parse input, allow stop
        sys.exit(0)

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

    # Check iteration limit
    iteration = state.get("iteration", 1)
    max_iterations = state.get("max_iterations", 10)

    if iteration >= max_iterations:
        # Max iterations reached - allow stop, clean up
        cleanup_state_file(state_file)
        output = {
            "systemMessage": f"Relentless mode: Reached max iterations ({max_iterations}). Stopping. Review remaining issues and decide next steps."
        }
        print(json.dumps(output))
        sys.exit(0)

    # Get success command
    success_command = state.get("success_command", "")
    if not success_command:
        # No command to check, allow stop
        cleanup_state_file(state_file)
        sys.exit(0)

    # Run success check command
    success, output, exit_code = run_check_command(success_command, project_dir)

    # Check against patterns
    success_pattern = state.get("success_pattern", "")

    is_success = False
    if exit_code == 0:
        if success_pattern:
            # Check if output matches success pattern
            is_success = bool(re.search(success_pattern, output, re.IGNORECASE | re.MULTILINE))
        else:
            # No pattern, just check exit code
            is_success = True

    if is_success:
        # Success! Allow stop, clean up
        cleanup_state_file(state_file)
        result = {
            "systemMessage": f"Relentless mode: Success criteria met after {iteration} iteration(s)."
        }
        print(json.dumps(result))
        sys.exit(0)

    # Not successful yet - increment iteration and block stop
    new_iteration = iteration + 1
    update_iteration(state_file, new_iteration)

    # Build the continue reason
    skill = state.get("skill", "relentless")
    task = state.get("task", "Complete the task")

    reason = build_continue_reason(
        skill=skill,
        iteration=new_iteration,
        max_iterations=max_iterations,
        output=output,
        task=task
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


def run_check_command(command: str, cwd: str) -> tuple:
    """Run the success check command and return (success, output, exit_code)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        return (result.returncode == 0, output, result.returncode)
    except subprocess.TimeoutExpired:
        return (False, "Command timed out after 120 seconds", -1)
    except Exception as e:
        return (False, f"Error running command: {str(e)}", -1)


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
                          output: str, task: str) -> str:
    """Build the reason message that becomes Claude's next instruction."""

    # Truncate output if too long
    max_output_len = 1500
    if len(output) > max_output_len:
        # Keep first and last parts
        half = max_output_len // 2
        output = output[:half] + "\n\n... (truncated) ...\n\n" + output[-half:]

    skill_names = {
        "build-relentlessly": "Build",
        "test-relentlessly": "Test",
        "lint-relentlessly": "Lint"
    }
    skill_display = skill_names.get(skill, skill.replace("-", " ").title())

    return f"""**Relentless Mode: {skill_display} - Iteration {iteration}/{max_iterations}**

The success criteria have NOT been met yet. Continue working.

**Last check output:**
```
{output.strip()}
```

**Your task:**
{task}

Analyze the errors/failures above, make fixes, and try again. Do not give up until the criteria are met or you've exhausted reasonable approaches for this iteration."""


if __name__ == "__main__":
    main()
