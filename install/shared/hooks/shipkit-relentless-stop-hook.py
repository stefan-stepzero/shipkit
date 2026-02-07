#!/usr/bin/env python3
"""
Shipkit Relentless Stop Hook

Prevents Claude from stopping until the completion promise is met.
Used by: shipkit-build-relentlessly, shipkit-test-relentlessly, shipkit-lint-relentlessly, shipkit-verify

Also supports standby mode via a separate state file, and loop mode for dev skills.
Priority: relentless-state > standby-state > loop-state.

Based on the ralph-wiggum pattern:
1. Globs for .shipkit/relentless-*.local.md (per-skill state files)
2. If none found, checks if .shipkit/standby-state.local.md exists (standby daemon)
3. If none found, globs for .shipkit/*-loop.local.md (dev skill loop files)
4. If none found, allows stop (quick exit)
5. If yes, blocks stop and feeds task back to Claude

Each relentless skill has its own state file so they can run in parallel:
- relentless-build.local.md  (build-relentlessly)
- relentless-test.local.md   (test-relentlessly)
- relentless-lint.local.md   (lint-relentlessly)
- relentless-verify.local.md (verify)

Loop mode state files (dev skills):
- framework-integrity-loop.local.md  (framework-integrity --loop N)
- validate-skill-loop.local.md       (validate-lite-skill --loop N)

The hook does NOT run commands - it just manages iteration and blocks/allows stop.
"""

import json
import os
import re
import sys
from pathlib import Path


# Note: No subprocess import - this hook does NOT run commands.
# Claude is responsible for running commands and checking if the promise is met.

# Per-skill relentless state files (glob pattern)
RELENTLESS_GLOB = "relentless-*.local.md"

# Standby state file (checked only if no relentless file found)
STANDBY_STATE_FILE = "standby-state.local.md"

# Loop mode state files (checked only if no relentless or standby found)
LOOP_GLOB = "*-loop.local.md"


def main():
    # Read hook input from stdin (required but not used for decisions)
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        pass  # Continue anyway

    # Find project directory
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    shipkit_dir = Path(project_dir) / ".shipkit"

    # Find active state file: relentless (per-skill) takes priority over standby
    state_file = None

    # 1. Check for any relentless-*.local.md files (per-skill state files)
    relentless_matches = sorted(shipkit_dir.glob(RELENTLESS_GLOB))
    if relentless_matches:
        # Pick the first match (alphabetical: build < lint < test < verify)
        state_file = relentless_matches[0]

    # 2. Fall back to standby state file
    if state_file is None:
        candidate = shipkit_dir / STANDBY_STATE_FILE
        if candidate.exists():
            state_file = candidate

    # 3. Fall back to loop state files (dev skill --loop N)
    if state_file is None:
        loop_matches = sorted(shipkit_dir.glob(LOOP_GLOB))
        if loop_matches:
            state_file = loop_matches[0]

    # Quick exit if no state file
    if state_file is None:
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
        skill = state.get("skill", "relentless")
        is_loop = state_file.name.endswith("-loop.local.md")
        if is_loop:
            label = "Loop"
        elif skill == "standby":
            label = "Standby"
        else:
            label = "Relentless"
        output = {
            "systemMessage": f"{label} mode: Reached max iterations ({max_iterations}). Stopping."
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

    is_loop = state_file.name.endswith("-loop.local.md")

    if is_loop:
        reason = build_loop_reason(
            skill=skill,
            iteration=new_iteration,
            max_iterations=max_iterations,
            task=task,
            completion_promise=completion_promise,
            state_filename=state_file.name
        )
    elif skill == "standby":
        reason = build_standby_reason(
            iteration=new_iteration,
            max_iterations=max_iterations,
            task=task,
            completion_promise=completion_promise
        )
    else:
        reason = build_relentless_reason(
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


def build_relentless_reason(skill: str, iteration: int, max_iterations: int,
                            task: str, completion_promise: str) -> str:
    """Build the reason message for relentless skills (build, test, lint, verify)."""

    skill_names = {
        "build-relentlessly": ("Build", "relentless-build.local.md"),
        "test-relentlessly": ("Test", "relentless-test.local.md"),
        "lint-relentlessly": ("Lint", "relentless-lint.local.md"),
        "verify": ("Verify", "relentless-verify.local.md"),
    }
    skill_display, state_filename = skill_names.get(
        skill, (skill.replace("-", " ").title(), f"relentless-{skill}.local.md")
    )

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
4. Check again - if the promise is now met, delete `.shipkit/{state_filename}` and stop
5. If not met, continue fixing (the hook will increment iteration when you try to stop)

Do not give up. Keep working until the completion promise is satisfied or you've exhausted reasonable approaches."""


def build_standby_reason(iteration: int, max_iterations: int,
                         task: str, completion_promise: str) -> str:
    """Build the reason message for standby daemon mode."""

    return f"""**Standby Mode - Iteration {iteration}/{max_iterations}**

You are in standby mode, polling for Mission Control commands.

**Your Task:**
{task}

**Instructions:**
1. If a command was injected via additionalContext on the previous tool call, execute it fully
2. After completing a command, rename the `.inflight` file to `.processed`
3. After completing a command, edit `.shipkit/standby-state.local.md` to set `idle_count: 0`
4. If no command was received, edit `.shipkit/standby-state.local.md` to increment `idle_count` by 1
5. Read `idle_count` from the state file and calculate sleep: min(10 * 2^idle_count, 300) seconds
6. Run `sleep N` via Bash — no other output during idle polls
7. If a command contains "shutdown" or "exit standby", delete `.shipkit/standby-state.local.md` and stop

Note: You manage `idle_count` yourself. The hook only manages `iteration`.
Minimize output during idle polls. Produce full output only when executing commands."""


def build_loop_reason(skill: str, iteration: int, max_iterations: int,
                      task: str, completion_promise: str,
                      state_filename: str) -> str:
    """Build the reason message for loop mode (dev skills with --loop N)."""

    return f"""**Loop Mode: {skill} - Iteration {iteration}/{max_iterations}**

You are in loop mode. The completion promise has NOT been met yet.

**Completion Promise:**
{completion_promise}

**Previous Progress & Task:**
{task}

**Instructions:**
1. Read the Progress section above — it contains what was done in previous iterations
2. Re-run the check to see current status
3. Fix any remaining issues
4. Update the Progress section in `.shipkit/{state_filename}` with what you did this iteration
5. If the promise is now met (zero errors, zero warnings), delete `.shipkit/{state_filename}` and stop
6. If not met, end your response (the hook will re-prompt for the next iteration)

Focus on issues NOT yet addressed in previous iterations."""


if __name__ == "__main__":
    main()
