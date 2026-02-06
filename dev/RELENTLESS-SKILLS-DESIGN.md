# Relentless Skills Design

Implementation plan for Shipkit's relentless execution skills.

---

## Overview

Three skills that prevent Claude from stopping until success criteria are met:

| Skill | Criteria | Use Case |
|-------|----------|----------|
| `/shipkit-build-relentlessly` | Build/compile succeeds | Migrations, setup, refactors |
| `/shipkit-test-relentlessly` | All tests pass | Feature dev, bug fixes |
| `/shipkit-lint-relentlessly` | No lint errors | Code quality cleanup |

**Key insight:** These guarantee *execution quality*, not *design quality*. They converge on correctness relative to the tests/spec you have.

---

## Architecture

### Components

```
install/
├── skills/
│   ├── shipkit-build-relentlessly/
│   │   └── SKILL.md
│   ├── shipkit-test-relentlessly/
│   │   └── SKILL.md
│   └── shipkit-lint-relentlessly/
│       └── SKILL.md
├── shared/
│   └── hooks/
│       └── shipkit-relentless-stop-hook.py   # Shared Stop hook
```

### Flow

```
1. User invokes /shipkit-test-relentlessly
2. Skill creates .shipkit/relentless-state.local.md
3. Claude works on the task
4. Claude tries to stop → Stop hook fires
5. Hook reads state file, checks criteria
6. If not done: return {"decision": "block", "reason": "..."}
7. Claude continues with reason as next instruction
8. Repeat until success or max iterations
9. Hook allows stop, deletes state file
```

---

## State File

**Location:** `.shipkit/relentless-state.local.md`

**Format:**
```markdown
---
skill: test-relentlessly
iteration: 1
max_iterations: 10
success_command: "npm test"
success_pattern: "passed|0 failures|All tests passed"
failure_pattern: "failed|FAIL|error"
---

# Task

Implement the user authentication feature.
Ensure all tests pass after each change.
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `skill` | Yes | Which relentless skill is active |
| `iteration` | Yes | Current iteration (1-indexed) |
| `max_iterations` | Yes | Maximum attempts before giving up |
| `success_command` | Yes | Command to run to check success |
| `success_pattern` | Yes | Regex pattern indicating success |
| `failure_pattern` | No | Regex pattern indicating failure |

---

## Shared Stop Hook

**File:** `install/shared/hooks/shipkit-relentless-stop-hook.py`

```python
#!/usr/bin/env python3
"""
Shipkit Relentless Stop Hook

Prevents Claude from stopping until success criteria are met.
Used by: shipkit-build-relentlessly, shipkit-test-relentlessly, shipkit-lint-relentlessly
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
        sys.exit(0)  # Allow stop if can't parse input

    # Check if already in a relentless loop (prevent infinite loops)
    if hook_input.get("stop_hook_active", False):
        # Already continuing from a stop hook - be cautious
        pass

    # Find state file
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    state_file = Path(project_dir) / ".shipkit" / "relentless-state.local.md"

    # Quick exit if no state file (not in relentless mode)
    if not state_file.exists():
        sys.exit(0)

    # Parse state file
    state = parse_state_file(state_file)
    if not state:
        sys.exit(0)  # Allow stop if can't parse state

    # Check iteration limit
    iteration = state.get("iteration", 1)
    max_iterations = state.get("max_iterations", 10)

    if iteration >= max_iterations:
        # Max iterations reached - allow stop, clean up
        cleanup_state_file(state_file)
        print(json.dumps({
            "systemMessage": f"Relentless mode: Reached max iterations ({max_iterations}). Stopping."
        }))
        sys.exit(0)

    # Run success check command
    success_command = state.get("success_command", "")
    if not success_command:
        cleanup_state_file(state_file)
        sys.exit(0)

    success, output = run_check_command(success_command, project_dir)

    # Check against patterns
    success_pattern = state.get("success_pattern", "")
    failure_pattern = state.get("failure_pattern", "")

    is_success = False
    if success and success_pattern:
        is_success = bool(re.search(success_pattern, output, re.IGNORECASE | re.MULTILINE))
    elif success and not success_pattern:
        # No pattern specified, just check exit code
        is_success = True

    if is_success:
        # Success! Allow stop, clean up
        cleanup_state_file(state_file)
        print(json.dumps({
            "systemMessage": f"Relentless mode: Success criteria met after {iteration} iteration(s)."
        }))
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
    print(json.dumps({
        "decision": "block",
        "reason": reason
    }))
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


def run_check_command(command: str, cwd: str) -> tuple[bool, str]:
    """Run the success check command and return (success, output)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + "\n" + result.stderr
        return (result.returncode == 0, output)
    except subprocess.TimeoutExpired:
        return (False, "Command timed out")
    except Exception as e:
        return (False, str(e))


def update_iteration(state_file: Path, new_iteration: int):
    """Update the iteration count in the state file."""
    try:
        content = state_file.read_text(encoding="utf-8")
        # Simple regex replacement for iteration field
        updated = re.sub(
            r'^iteration:\s*\d+',
            f'iteration: {new_iteration}',
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
        pass


def build_continue_reason(skill: str, iteration: int, max_iterations: int,
                          output: str, task: str) -> str:
    """Build the reason message that becomes Claude's next instruction."""

    # Truncate output if too long
    max_output_len = 500
    if len(output) > max_output_len:
        output = output[:max_output_len] + "\n... (truncated)"

    skill_names = {
        "build-relentlessly": "Build",
        "test-relentlessly": "Test",
        "lint-relentlessly": "Lint"
    }
    skill_display = skill_names.get(skill, skill)

    return f"""**Relentless Mode: {skill_display} - Iteration {iteration}/{max_iterations}**

The success criteria have NOT been met yet. Continue working.

**Last check output:**
```
{output.strip()}
```

**Your task:**
{task}

Analyze the errors above, make fixes, and try again. Do not stop until the criteria are met or you've exhausted all reasonable approaches for this iteration.
"""


if __name__ == "__main__":
    main()
```

---

## Skill Definitions

### shipkit-build-relentlessly

**File:** `install/skills/shipkit-build-relentlessly/SKILL.md`

```markdown
---
name: shipkit-build-relentlessly
version: 1.0.0
description: Build/compile relentlessly until success
triggers:
  - build relentlessly
  - keep building until it compiles
  - fix all build errors
arguments:
  - name: task
    description: What to build or fix
    required: false
  - name: max_iterations
    description: Maximum attempts (default: 10)
    required: false
  - name: build_command
    description: Build command (auto-detected if not specified)
    required: false
---

# Build Relentlessly

Execute build/compile operations repeatedly until successful.

## Purpose

Use when you need to:
- Fix many compilation errors (TypeScript migration, dependency upgrades)
- Get a new project to compile for the first time
- Resolve build issues after major refactors

## Workflow

1. **Detect build system** (or use provided command):
   - `package.json` with build script → `npm run build`
   - `tsconfig.json` → `npx tsc --noEmit`
   - `Cargo.toml` → `cargo build`
   - `go.mod` → `go build ./...`
   - `Makefile` → `make`

2. **Create state file** at `.shipkit/relentless-state.local.md`:
   ```yaml
   ---
   skill: build-relentlessly
   iteration: 1
   max_iterations: {max_iterations or 10}
   success_command: "{detected or provided build command}"
   success_pattern: ""
   ---

   {task or "Fix all build/compilation errors"}
   ```

3. **Begin working** on the build errors

4. **Stop hook handles iteration** - you don't need to manage the loop

## Success Criteria

- Build command exits with code 0
- No compilation errors in output

## Example Usage

User: "build relentlessly - migrate this JS project to TypeScript"

You:
1. Create state file with `npx tsc --noEmit` as success command
2. Start fixing type errors
3. Continue until `tsc` exits cleanly

## Constraints

- Maximum iterations: {max_iterations} (default: 10)
- Focus on build errors only, not runtime behavior
- If stuck after several iterations, report blocker to user
```

---

### shipkit-test-relentlessly

**File:** `install/skills/shipkit-test-relentlessly/SKILL.md`

```markdown
---
name: shipkit-test-relentlessly
version: 1.0.0
description: Run tests relentlessly until all pass
triggers:
  - test relentlessly
  - keep testing until green
  - fix all failing tests
  - make tests pass
arguments:
  - name: task
    description: What to implement or fix
    required: false
  - name: max_iterations
    description: Maximum attempts (default: 10)
    required: false
  - name: test_command
    description: Test command (auto-detected if not specified)
    required: false
---

# Test Relentlessly

Execute tests repeatedly, fixing failures until all pass.

## Purpose

Use when you need to:
- Implement a feature with TDD (tests exist, implementation doesn't)
- Fix multiple failing tests after a refactor
- Ensure all tests pass before committing

## Workflow

1. **Detect test framework** (or use provided command):
   - `package.json` with test script → `npm test`
   - `pytest.ini` or `pyproject.toml` → `pytest`
   - `Cargo.toml` → `cargo test`
   - `go.mod` → `go test ./...`
   - `*.test.js` files → `npm test`

2. **Create state file** at `.shipkit/relentless-state.local.md`:
   ```yaml
   ---
   skill: test-relentlessly
   iteration: 1
   max_iterations: {max_iterations or 10}
   success_command: "{detected or provided test command}"
   success_pattern: "passed|0 failures|0 failed|OK"
   failure_pattern: "FAIL|failed|error|Error"
   ---

   {task or "Fix all failing tests"}
   ```

3. **Begin working** on failing tests

4. **Stop hook handles iteration** - you don't need to manage the loop

## Success Criteria

- Test command exits with code 0
- Output matches success pattern (e.g., "All tests passed")

## Example Usage

User: "test relentlessly - implement the authentication module"

You:
1. Create state file with `npm test` as success command
2. Run tests to see failures
3. Implement code to fix failures
4. Continue until all tests pass

## Constraints

- Maximum iterations: {max_iterations} (default: 10)
- Focus on making tests pass, not changing test expectations
- If a test seems wrong, note it but still try to make it pass
- If truly stuck, report blocker to user
```

---

### shipkit-lint-relentlessly

**File:** `install/skills/shipkit-lint-relentlessly/SKILL.md`

```markdown
---
name: shipkit-lint-relentlessly
version: 1.0.0
description: Fix lint/format errors relentlessly until clean
triggers:
  - lint relentlessly
  - fix all lint errors
  - clean up code style
arguments:
  - name: task
    description: Scope of linting (specific files/dirs or all)
    required: false
  - name: max_iterations
    description: Maximum attempts (default: 10)
    required: false
  - name: lint_command
    description: Lint command (auto-detected if not specified)
    required: false
---

# Lint Relentlessly

Fix linting and formatting errors repeatedly until code is clean.

## Purpose

Use when you need to:
- Clean up code style after a large change
- Fix all ESLint/Prettier/etc. violations
- Prepare code for PR review

## Workflow

1. **Detect linter** (or use provided command):
   - `package.json` with lint script → `npm run lint`
   - `.eslintrc*` → `npx eslint . --max-warnings=0`
   - `pyproject.toml` with ruff/black → `ruff check .`
   - `.prettierrc*` → `npx prettier --check .`
   - `rustfmt.toml` → `cargo fmt --check`

2. **Create state file** at `.shipkit/relentless-state.local.md`:
   ```yaml
   ---
   skill: lint-relentlessly
   iteration: 1
   max_iterations: {max_iterations or 10}
   success_command: "{detected or provided lint command}"
   success_pattern: "0 errors|no issues|0 problems"
   failure_pattern: "error|warning|problem"
   ---

   {task or "Fix all linting and formatting errors"}
   ```

3. **Begin fixing** lint errors

4. **Stop hook handles iteration** - you don't need to manage the loop

## Success Criteria

- Lint command exits with code 0
- No errors or warnings in output

## Example Usage

User: "lint relentlessly - clean up the src/ directory"

You:
1. Create state file with `npm run lint` as success command
2. Run linter to see violations
3. Fix violations (prefer auto-fix where safe)
4. Continue until lint is clean

## Auto-fix Strategy

1. Try auto-fix first if available (`--fix` flag)
2. For remaining issues, fix manually
3. Preserve code behavior - lint fixes should be cosmetic only

## Constraints

- Maximum iterations: {max_iterations} (default: 10)
- Don't change code behavior to satisfy lint
- If a lint rule seems wrong, note it but still fix it
- If rule is truly problematic, can disable with inline comment (last resort)
```

---

## Hook Configuration

Add to `install/settings/shipkit.settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.shipkit/hooks/shipkit-relentless-stop-hook.py\"",
            "timeout": 180
          }
        ]
      }
    ]
  }
}
```

**Note:** The hook needs to be installed into user projects. Options:
1. Install hook script to `.shipkit/hooks/` during shipkit installation
2. Reference from a central location
3. Bundle with the skills themselves

---

## Integration Checklist

### 7-File Integration

1. **Manifest** (`install/profiles/shipkit.manifest.json`):
   - Add all three skills

2. **Settings** (`install/settings/shipkit.settings.json`):
   - Add Stop hook configuration

3. **CLAUDE.md** (`install/claude-md/shipkit.md`):
   - Add to skill reference table

4. **README.md**:
   - Update skill count (24 → 27)
   - Add to skill list

5. **HTML Overview** (`docs/generated/shipkit-overview.html`):
   - Update skill count
   - Add to implementation section

6. **Session Hook** - No changes needed

7. **Router Hook** - Add triggers for natural language routing

### Installation

The relentless stop hook needs to be:
1. Copied to user project during `/shipkit-update`
2. Hook configuration added to project's `.claude/settings.json`

---

## Usage Examples

### Example 1: TypeScript Migration

```
User: build relentlessly - I just converted all .js files to .ts

Claude:
1. Creates state file with `npx tsc --noEmit`
2. Runs tsc, sees 47 type errors
3. Fixes errors file by file
4. [Stop hook blocks, shows remaining errors]
5. Continues fixing...
6. [After iteration 4, tsc exits clean]
7. Stop hook allows stop, reports success
```

### Example 2: TDD Implementation

```
User: test relentlessly - implement the UserService class, tests are in user.test.ts

Claude:
1. Creates state file with `npm test`
2. Runs tests, sees 5 failing
3. Implements UserService methods
4. [Stop hook blocks, shows 2 still failing]
5. Fixes remaining issues
6. [All tests pass]
7. Stop hook allows stop, reports success
```

### Example 3: Code Cleanup

```
User: lint relentlessly

Claude:
1. Creates state file with `npm run lint`
2. Runs lint, sees 23 violations
3. Runs `npm run lint -- --fix` for auto-fixable
4. Manually fixes remaining
5. [Stop hook blocks, shows 3 remaining]
6. Fixes last issues
7. [Lint clean]
8. Stop hook allows stop, reports success
```

---

## Edge Cases

### What if build system isn't detected?

Ask user for the command:
```
I couldn't auto-detect your build system. What command should I use to check if the build succeeds?
```

### What if max iterations reached without success?

Report to user with summary:
```
Reached maximum iterations (10) without achieving success criteria.

**Last output:**
[truncated error output]

**What I tried:**
- Fixed X type errors
- Resolved Y import issues
- ...

**Remaining blockers:**
- Z appears to require external dependency
- ...

Would you like me to continue with a higher iteration limit, or should we address the blockers first?
```

### What if user wants to stop early?

User can:
1. Delete `.shipkit/relentless-state.local.md` manually
2. Say "stop" or "cancel relentless mode"
3. Use Ctrl+C to interrupt

---

## Future Enhancements

1. **Parallel checks** - Run build AND lint simultaneously
2. **Smart retries** - Skip unchanged files on retry
3. **Progress tracking** - Show errors fixed vs remaining
4. **Composite mode** - `shipkit-ship-relentlessly` = build + test + lint
