---
name: shipkit-build-relentlessly
description: Build/compile relentlessly until success. Use for migrations, setup, major refactors.
argument-hint: "[task] [--max N]"
triggers:
  - build relentlessly
  - keep building until it compiles
  - fix all build errors
  - fix all type errors
  - make it compile
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-build-relentlessly

Execute build/compile operations repeatedly until successful. The Stop hook prevents exit until the build passes or max iterations reached.

---

## CRITICAL: Fully Autonomous

**This skill runs WITHOUT user interaction.** Designed for overnight/unattended execution.

- **NEVER** use AskUserQuestion
- **NEVER** ask for confirmation
- **NEVER** stop to ask "what should I do?"
- **ALWAYS** auto-detect build commands
- **ALWAYS** make autonomous decisions
- **IF stuck**, try alternative approaches before giving up

The user invokes this skill and walks away. Come back to either success or a clear failure report.

---

## When to Invoke

**User triggers:**
- "Build relentlessly"
- "Fix all the type errors"
- "Make it compile"
- "Keep going until it builds"

**Use cases:**
- TypeScript migration (many type errors)
- Major dependency upgrades (breaking changes)
- Initial project setup (getting first build working)
- Large refactors with compilation fallout

---

## Arguments

```
/shipkit-build-relentlessly [task] [--max N]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `task` | No | "Fix all build errors" | Description of what to fix |
| `--max N` | No | 10 | Maximum iterations before giving up |

**Examples:**
```
/shipkit-build-relentlessly
/shipkit-build-relentlessly migrate to TypeScript
/shipkit-build-relentlessly --max 20 fix all type errors
```

---

## How It Works

1. **You create a state file** with a `completion_promise`
2. **You work on fixing build errors**
3. **You run the build command** to check progress
4. **If promise met:** Delete state file and stop
5. **If not met:** End response → Hook blocks → You continue

**You decide when the promise is met** - the hook just manages iteration.

---

## CRITICAL: Loop Mechanism

**The loop works differently than you might expect:**

1. **CREATE STATE FILE FIRST** - Before ANY other work, create `.shipkit/relentless-build.local.md`. Without this file, the Stop hook won't activate.

2. **YOU check if the promise is met** - Run the build command, check if it passes. The hook does NOT run commands.

3. **When promise is met:** Delete the state file, then finish your response. The hook will allow you to stop.

4. **When NOT met:** Just finish your response. The hook will:
   - Increment the iteration counter
   - Block your stop
   - Feed your task and completion_promise back to you

5. **When blocked, you'll see:**
   ```
   Relentless Mode: Build - Iteration 3/10

   Completion Promise: Build compiles successfully with no errors

   Your Task: [your task from the state file body]
   ```

**The pattern is:** Create state file → Fix errors → Run build → Promise met? Delete file & stop : End response → Hook blocks → Repeat

---

## Process

### Step 0: Parse Arguments

**Extract from user input:**
1. `--max N` → Use N as `max_iterations` (default: 10)
2. Everything else → Use as task description

**Example parsing:**
- Input: `--max 20 fix type errors` → max=20, task="fix type errors"
- Input: `migrate to TS` → max=10, task="migrate to TS"
- Input: (empty) → max=10, task="Fix all build/compilation errors"

### Step 1: Detect Build System (Autonomous)

**Auto-detect build command - DO NOT ask user:**

| Indicator | Build Command |
|-----------|---------------|
| `package.json` with `build` script | `npm run build` |
| `package.json` with `tsc` in scripts | `npm run build` or the tsc script |
| `tsconfig.json` (no build script) | `npx tsc --noEmit` |
| `Cargo.toml` | `cargo build` |
| `go.mod` | `go build ./...` |
| `Makefile` | `make` |
| `pyproject.toml` | `pip install -e .` |
| `setup.py` | `python setup.py build` |

**Detection order:**
1. Check `package.json` scripts for "build", "compile", "tsc"
2. Check for `tsconfig.json` → use tsc
3. Check for language-specific build files
4. **Fallback:** If truly undetectable, use `npm run build` for JS/TS projects

**NEVER ask the user** - make your best guess and proceed.

### Step 2: Create State File

**Write to:** `.shipkit/relentless-build.local.md`

```markdown
---
skill: build-relentlessly
iteration: 1
max_iterations: [from --max or 10]
completion_promise: "Build compiles successfully with no errors"
enabled: true
---

[parsed task description or "Fix all build/compilation errors"]
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
1. Run the build command to see current errors
2. Fix errors systematically
3. Run build again to check progress
4. **If build passes:** Delete `.shipkit/relentless-build.local.md` and finish
5. **If build fails:** End your response normally → hook blocks → you continue

**When the hook blocks, you'll see your task and completion_promise again.**

**YOU are responsible for:**
- Running the build command to check status
- Deciding if the completion_promise is met
- Deleting the state file when successful

**The hook only:**
- Increments the iteration counter
- Blocks your stop and reminds you of the task
- Enforces max_iterations limit

### Step 4: Completion

When build succeeds:
- State file is automatically deleted
- You'll see: "Relentless mode: Success criteria met after N iteration(s)"

When max iterations reached:
- State file is automatically deleted
- Report to user what remains unfixed
- Suggest next steps

---

## Constraints

- **Max iterations**: Default 10 (prevents infinite loops)
- **Focus**: Build errors only, not runtime behavior
- **Timeout**: Build command has 120s timeout per check
- **Fully autonomous**: NO user prompts, NO confirmations, NO questions
- **When stuck**: Try different approaches (comment out problematic code, add type assertions, etc.) - only give up at max iterations
- **Decision making**: Make reasonable choices autonomously. Wrong guess + iterate > ask and wait

---

## Example Session

```
User: build relentlessly - migrate this JS project to TypeScript

Claude:
1. Detects tsconfig.json, uses `npx tsc --noEmit`
2. Creates .shipkit/relentless-build.local.md
3. Runs tsc, sees 47 type errors
4. Fixes errors in src/utils/*.ts (12 errors)
5. [Attempts to stop]
6. Stop hook runs tsc → 35 errors remain → continues
7. Fixes errors in src/components/*.tsx (20 errors)
8. [Attempts to stop]
9. Stop hook runs tsc → 15 errors remain → continues
10. Fixes remaining errors
11. [Attempts to stop]
12. Stop hook runs tsc → 0 errors → allows stop
13. "Success criteria met after 4 iterations"
```

---

## State File Location

`.shipkit/relentless-build.local.md`

This file:
- Activates the relentless Stop hook
- Tracks iteration count
- Stores the success command
- Is auto-deleted on success or max iterations

**To cancel manually:** Delete this file.

---

## Integration with Other Skills

**Before:**
- Feature spec may exist (`.shipkit/specs/active/*.json`)
- Not required - build-relentlessly works standalone

**After:**
- `/shipkit-test-relentlessly` - now that it builds, make tests pass
- `/shipkit-lint-relentlessly` - clean up code style

**Natural progression:**
```
build-relentlessly → test-relentlessly → lint-relentlessly
```

---

## Context Files

**Reads:**
- Build configuration files (package.json, tsconfig.json, etc.)
- Source files with errors

**Writes:**
- `.shipkit/relentless-build.local.md` (temporary, auto-deleted)

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Build system detected or provided
- [ ] State file created with correct command
- [ ] Build errors fixed iteratively
- [ ] Build command exits with code 0
- [ ] State file cleaned up
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Build passes. Consider:
- `/shipkit-test-relentlessly` if tests exist
- `/shipkit-lint-relentlessly` for code cleanup
- Continue with normal implementation
<!-- /SECTION:after-completion -->
