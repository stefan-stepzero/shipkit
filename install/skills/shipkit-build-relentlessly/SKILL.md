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

## Process

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
max_iterations: 10
success_command: "[detected or provided build command]"
success_pattern: ""
---

[User's task description or "Fix all build/compilation errors"]
```

**Parameters:**
- `max_iterations`: Default 10, user can override
- `success_command`: The build command to run
- `success_pattern`: Empty (just check exit code 0)

### Step 3: Begin Working

Start fixing build errors:

1. Run the build command to see current errors
2. Analyze error output
3. Fix errors systematically (file by file or error type by type)
4. When you think you're done, attempt to conclude

**The Stop hook will:**
- Run the build command
- If errors remain → show them and continue
- If build passes → allow completion

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
