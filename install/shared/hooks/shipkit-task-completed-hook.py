#!/usr/bin/env python3
"""
Shipkit TaskCompleted Hook

Quality gate that fires when a teammate marks a task as complete.
Validates that build and tests pass before allowing task completion.

Hook events:
  - Exit 0: Allow task completion
  - Exit 2: Block completion, stderr message sent as feedback

Requires: .shipkit/team-state.local.json to be present (written by /shipkit-team).
If no team state file exists, this hook exits 0 (no-op outside team mode).

Input: JSON on stdin with hook event data (session_id, task info, etc.)
Output: stderr for feedback messages when blocking (exit 2)
"""

import json
import os
import subprocess
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


def detect_build_command(project_dir: Path) -> list[str] | None:
    """Auto-detect the project's build command."""
    if (project_dir / "package.json").exists():
        try:
            pkg = json.loads((project_dir / "package.json").read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            if "build" in scripts:
                # Detect package manager
                if (project_dir / "pnpm-lock.yaml").exists():
                    return ["pnpm", "run", "build"]
                if (project_dir / "yarn.lock").exists():
                    return ["yarn", "build"]
                return ["npm", "run", "build"]
        except (json.JSONDecodeError, OSError):
            pass
    if (project_dir / "Cargo.toml").exists():
        return ["cargo", "build"]
    if (project_dir / "pyproject.toml").exists():
        return ["python", "-m", "build"]
    return None


def detect_test_command(project_dir: Path) -> list[str] | None:
    """Auto-detect the project's test command."""
    if (project_dir / "package.json").exists():
        try:
            pkg = json.loads((project_dir / "package.json").read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            if "test" in scripts:
                if (project_dir / "pnpm-lock.yaml").exists():
                    return ["pnpm", "run", "test"]
                if (project_dir / "yarn.lock").exists():
                    return ["yarn", "test"]
                return ["npm", "run", "test"]
        except (json.JSONDecodeError, OSError):
            pass
    if (project_dir / "Cargo.toml").exists():
        return ["cargo", "test"]
    if (project_dir / "pyproject.toml").exists():
        return ["pytest"]
    return None


def run_command(cmd: list[str], cwd: Path, timeout: int = 90) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        # Truncate to avoid huge feedback messages
        if len(output) > 1000:
            output = output[:500] + "\n...(truncated)...\n" + output[-500:]
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"


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
        # Can't read state, allow completion (don't block on corrupt state)
        sys.exit(0)

    # Gate tasks (phase verification) are handled by the lead, not this hook
    task_description = hook_input.get("task_description", "")
    if task_description.startswith("GATE"):
        sys.exit(0)

    # Run build check
    build_cmd = detect_build_command(project_dir)
    if build_cmd:
        success, output = run_command(build_cmd, project_dir)
        if not success:
            print(
                f"Build failed. Fix before completing this task.\n\n"
                f"Command: {' '.join(build_cmd)}\n"
                f"Output:\n{output}",
                file=sys.stderr,
            )
            sys.exit(2)

    # Run test check
    test_cmd = detect_test_command(project_dir)
    if test_cmd:
        success, output = run_command(test_cmd, project_dir)
        if not success:
            print(
                f"Tests failed. Fix before completing this task.\n\n"
                f"Command: {' '.join(test_cmd)}\n"
                f"Output:\n{output}",
                file=sys.stderr,
            )
            sys.exit(2)

    # All checks passed
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Silent failure — never block on hook errors
        sys.exit(0)
