---
name: shipkit-lint-relentlessly
description: Fix lint/format errors relentlessly until clean. Use for code cleanup, PR prep, style fixes.
argument-hint: "[task] [--max N]"
triggers:
  - lint relentlessly
  - fix all lint errors
  - clean up code style
  - fix formatting
  - make lint pass
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-lint-relentlessly

Fix linting and formatting errors repeatedly until code is clean. The Stop hook prevents exit until lint passes or max iterations reached.

---

## CRITICAL: Fully Autonomous

**This skill runs WITHOUT user interaction.** Designed for overnight/unattended execution.

- **NEVER** use AskUserQuestion
- **NEVER** ask for confirmation
- **NEVER** stop to ask "what should I do?"
- **ALWAYS** auto-detect lint commands
- **ALWAYS** make autonomous decisions
- **ALWAYS** try auto-fix first
- **IF stuck**, try alternative approaches before giving up

The user invokes this skill and walks away. Come back to either success or a clear failure report.

---

## When to Invoke

**User triggers:**
- "Lint relentlessly"
- "Fix all lint errors"
- "Clean up the code style"
- "Make lint pass"
- "Fix formatting issues"

**Use cases:**
- Code cleanup after large changes
- Preparing code for PR review
- Fixing all ESLint/Prettier/etc. violations
- Enforcing code style consistency

---

## Arguments

```
/shipkit-lint-relentlessly [task] [--max N]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `task` | No | "Fix all lint errors" | Description/scope of what to fix |
| `--max N` | No | 10 | Maximum iterations before giving up |

**Examples:**
```
/shipkit-lint-relentlessly
/shipkit-lint-relentlessly fix src/components only
/shipkit-lint-relentlessly --max 5 quick cleanup
```

---

## How It Works

1. **You create a state file** with a `completion_promise`
2. **You work on fixing lint errors**
3. **You run the lint command** to check progress
4. **If promise met:** Delete state file and stop
5. **If not met:** End response → Hook blocks → You continue

**You decide when the promise is met** - the hook just manages iteration.

---

## CRITICAL: Loop Mechanism

**The loop works differently than you might expect:**

1. **CREATE STATE FILE FIRST** - Before ANY other work, create `.shipkit/relentless-lint.{sid8}.local.md`. Without this file, the Stop hook won't activate.

2. **YOU check if the promise is met** - Run the lint command, check if it passes. The hook does NOT run commands.

3. **When promise is met:** Delete the state file, then finish your response. The hook will allow you to stop.

4. **When NOT met:** Just finish your response. The hook will:
   - Increment the iteration counter
   - Block your stop
   - Feed your task and completion_promise back to you

5. **When blocked, you'll see:**
   ```
   Relentless Mode: Lint - Iteration 3/10

   Completion Promise: Lint passes with no errors or warnings

   Your Task: [your task from the state file body]
   ```

**The pattern is:** Create state file → Fix violations → Run lint → Promise met? Delete file & stop : End response → Hook blocks → Repeat

---

## Session ID

Your session-start context includes `Session ID: {sid8}`.
Use this 8-character ID in all state file names below. If not found in session context, use `unknown`.

---

## Process

### Step 0: Parse Arguments

**Extract from user input:**
1. `--max N` → Use N as `max_iterations` (default: 10)
2. Everything else → Use as task description

**Example parsing:**
- Input: `--max 5 quick cleanup` → max=5, task="quick cleanup"
- Input: `fix src/components` → max=10, task="fix src/components"
- Input: (empty) → max=10, task="Fix all linting and formatting errors"

### Step 1: Detect Linter (Autonomous)

**Auto-detect lint command - DO NOT ask user:**

| Indicator | Lint Command |
|-----------|--------------|
| `package.json` with `lint` script | `npm run lint` |
| `.eslintrc*` (no lint script) | `npx eslint . --max-warnings=0` |
| `pyproject.toml` with ruff | `ruff check .` |
| `pyproject.toml` with flake8 | `flake8 .` |
| `.prettierrc*` | `npx prettier --check .` |
| `rustfmt.toml` or Cargo.toml | `cargo fmt --check` |
| `golangci.yml` | `golangci-lint run` |
| `.pylintrc` | `pylint **/*.py` |

**Detection order:**
1. Check `package.json` scripts for "lint"
2. Check for lint config files (.eslintrc, .prettierrc, ruff in pyproject)
3. Check for language-specific linters
4. **Fallback:** `npm run lint` for JS/TS, `ruff check .` for Python

**NEVER ask the user** - make your best guess and proceed.

### Step 2: Create State File

**Write to:** `.shipkit/relentless-lint.{sid8}.local.md`

```markdown
---
skill: lint-relentlessly
iteration: 1
max_iterations: [from --max or 10]
completion_promise: "Lint passes with no errors or warnings"
enabled: true
---

[User's task description or "Fix all linting and formatting errors"]
```

**State file fields:**
| Field | Purpose |
|-------|---------|
| `skill` | Identifies which relentless skill is running |
| `iteration` | Current iteration (auto-incremented by hook) |
| `max_iterations` | From `--max N` or default 10 |
| `completion_promise` | Semantic description of what success looks like |
| `enabled` | Set to `false` to pause without deleting file |

**Body:** Your task - this is fed back to you when the hook blocks.

**⚠️ VERIFY:** Confirm the state file was created before proceeding.

### Step 3: Begin Working

**The loop works like this:**
1. Run lint command to see current violations
2. **Try auto-fix first** if available:
   - `npm run lint -- --fix`
   - `npx eslint . --fix`
   - `ruff check . --fix`
   - `npx prettier --write .`
3. Manually fix remaining issues that auto-fix can't handle
4. Run lint again to check progress
5. **If lint passes:** Delete `.shipkit/relentless-lint.{sid8}.local.md` and finish
6. **If lint fails:** End your response normally → hook blocks → you continue

**YOU are responsible for:**
- Running the lint command to check status
- Deciding if the completion_promise is met
- Deleting the state file when successful

**The hook only:**
- Increments the iteration counter
- Blocks your stop and reminds you of the task
- Enforces max_iterations limit

### Step 4: Completion

When lint passes:
- State file is automatically deleted
- You'll see: "Relentless mode: Success criteria met after N iteration(s)"

When max iterations reached:
- State file is automatically deleted
- Report to user what violations remain
- Suggest next steps (maybe disable problematic rules?)

---

## Auto-Fix Strategy

**Prioritize automatic fixes:**

1. Run auto-fix command first (safe, fast)
2. Review what was auto-fixed (ensure no behavior changes)
3. Manually fix remaining violations
4. For truly problematic rules, can disable with inline comment (last resort)

**Common auto-fix commands:**

| Tool | Auto-fix Command |
|------|------------------|
| ESLint | `npx eslint . --fix` |
| Prettier | `npx prettier --write .` |
| Ruff | `ruff check . --fix` |
| Black | `black .` |
| Rust | `cargo fmt` |
| Go | `gofmt -w .` |

---

## Constraints

- **Max iterations**: Default 10 (prevents infinite loops)
- **Focus**: Code style only, not behavior changes
- **Timeout**: Lint command has 120s timeout per check
- **Fully autonomous**: NO user prompts, NO confirmations, NO questions
- **When stuck**: Use inline disable comments as last resort, try alternative fixes
- **Philosophy**: Fix violations, don't change code behavior
- **Decision making**: Make reasonable choices autonomously. Auto-fix first, manual fix second, disable comment last

---

## Example Session

```
User: lint relentlessly

Claude:
1. Detects npm run lint, uses that
2. Creates .shipkit/relentless-lint.{sid8}.local.md
3. Runs lint, sees 23 violations
4. Runs `npm run lint -- --fix` (auto-fixes 18)
5. [Attempts to stop]
6. Stop hook runs lint → 5 violations remain → continues
7. Manually fixes unused imports (2 violations)
8. [Attempts to stop]
9. Stop hook runs lint → 3 violations remain → continues
10. Fixes remaining any types and missing returns
11. [Attempts to stop]
12. Stop hook runs lint → 0 violations → allows stop
13. "Success criteria met after 4 iterations"
```

---

## State File Location

`.shipkit/relentless-lint.{sid8}.local.md`

This file:
- Activates the relentless Stop hook
- Tracks iteration count
- Stores the lint command and patterns
- Is auto-deleted on success or max iterations

**To cancel manually:** Delete this file.

---

## Integration with Other Skills

**Before:**
- `/shipkit-build-relentlessly` - ensure it compiles first
- `/shipkit-test-relentlessly` - ensure tests pass first

**After:**
- `/shipkit-verify` - final quality review
- Ready to commit

**Natural progression:**
```
build-relentlessly → test-relentlessly → lint-relentlessly → commit
```

---

## Common Lint Rules That Need Manual Fixes

Some violations can't be auto-fixed:

| Rule | Why Manual | Fix Strategy |
|------|------------|--------------|
| `no-explicit-any` | Needs proper types | Add real types |
| `no-unused-vars` | Code decision | Remove or use |
| `complexity` | Needs refactor | Simplify function |
| `max-lines` | Needs split | Extract to modules |
| `no-console` | Intentional? | Remove or disable inline |

---

## Context Files

**Reads:**
- Lint configuration (.eslintrc, prettier.config, etc.)
- Source files with violations

**Writes:**
- `.shipkit/relentless-lint.{sid8}.local.md` (temporary, auto-deleted)

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Linter detected or provided
- [ ] State file created with correct command
- [ ] Auto-fix applied where possible
- [ ] Remaining violations fixed manually
- [ ] Lint command exits clean (0 errors/warnings)
- [ ] State file cleaned up
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Lint passes. Code is clean. Consider:
- `/shipkit-verify` for final quality review
- Commit the clean code
- Open PR for review
<!-- /SECTION:after-completion -->
