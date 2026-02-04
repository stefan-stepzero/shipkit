---
name: shipkit-build-relentlessly
description: Build/compile relentlessly until success. Use for migrations, setup, major refactors.
argument-hint: "[task] [--max N] [--cmd \"command\"]"
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
/shipkit-build-relentlessly [task] [--max N] [--cmd "command"]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `task` | No | "Fix all build errors" | Description of what to fix |
| `--max N` | No | 10 | Maximum iterations before giving up |
| `--cmd "..."` | No | Auto-detected | Explicit build command to use |

**Examples:**
```
/shipkit-build-relentlessly
/shipkit-build-relentlessly migrate to TypeScript
/shipkit-build-relentlessly --max 20 fix all type errors
/shipkit-build-relentlessly --cmd "npm run build" --max 5
```

---

## How It Works

1. **You create a state file** that activates the Stop hook
2. **You work on fixing build errors**
3. **When you try to stop**, the Stop hook:
   - Runs the build command
   - If build fails → blocks stop, shows errors, increments iteration
   - If build passes → allows stop, cleans up state file
4. **Loop continues** until build succeeds or max iterations reached

**You don't manage the loop** - the Stop hook handles iteration.

---

## CRITICAL: Loop Mechanism

**READ THIS CAREFULLY - the loop works differently than you might expect:**

1. **CREATE STATE FILE FIRST** - Before ANY other work, create `.shipkit/relentless-state.local.md`. Without this file, the Stop hook won't activate and you'll just stop after one attempt.

2. **DO NOT implement your own loop** - No `while` loops, no "let me try again", no manual iteration. The Stop hook handles ALL iteration automatically.

3. **"Trying to stop" IS the loop** - After fixing some errors, simply finish your response normally. The Stop hook will:
   - Run the build command
   - If it fails → You'll receive the errors and continue (this is iteration)
   - If it passes → Session ends successfully

4. **When blocked, you'll see** a message like:
   ```
   Relentless mode: Build check FAILED (iteration 3/10)
   [error output here]
   Continuing...
   ```
   This means: read the errors, fix them, then try to finish again.

5. **Work in batches** - Fix a reasonable number of errors per iteration (5-15), then let the hook check. Don't try to fix everything at once.

**The pattern is:** Create state file → Fix some errors → Finish response → Hook checks → (repeat if needed)

---

## Process

### Step 0: Parse Arguments

**Extract from user input:**
1. `--max N` → Use N as `max_iterations` (default: 10)
2. `--cmd "..."` → Use as `success_command` (skip auto-detection)
3. Everything else → Use as task description

**Example parsing:**
- Input: `--max 20 fix type errors` → max=20, task="fix type errors"
- Input: `--cmd "npm run build"` → cmd="npm run build", max=10, task=default
- Input: `migrate to TS` → max=10, task="migrate to TS"

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

**Write to:** `.shipkit/relentless-state.local.md`

```markdown
---
skill: build-relentlessly
iteration: 1
max_iterations: [from --max or 10]
success_command: "[from --cmd or auto-detected]"
success_pattern: ""
---

[parsed task description or "Fix all build/compilation errors"]
```

**Use parsed values from Step 0:**
- `max_iterations`: From `--max N` argument, or default 10
- `success_command`: From `--cmd` argument, or auto-detected in Step 1
- `success_pattern`: Empty (just check exit code 0)

**⚠️ VERIFY:** Confirm the state file was created before proceeding. If it doesn't exist, the loop won't work.

### Step 3: Begin Working

Start fixing build errors:

1. Run the build command to see current errors
2. Analyze error output
3. Fix errors systematically (file by file or error type by type)
4. **End your response normally** (this triggers the Stop hook to check)

**DO NOT:**
- Say "let me try building again" and loop manually
- Ask the user if you should continue
- Implement any kind of retry logic yourself

**The Stop hook automatically:**
- Runs the build command when you finish responding
- If errors remain → blocks exit, shows errors, you continue in next turn
- If build passes → allows exit, session completes

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
2. Creates .shipkit/relentless-state.local.md
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

`.shipkit/relentless-state.local.md`

This file:
- Activates the relentless Stop hook
- Tracks iteration count
- Stores the success command
- Is auto-deleted on success or max iterations

**To cancel manually:** Delete this file.

---

## Integration with Other Skills

**Before:**
- Feature spec may exist (`.shipkit/specs/active/*.md`)
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
- `.shipkit/relentless-state.local.md` (temporary, auto-deleted)

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
