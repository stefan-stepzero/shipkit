---
name: shipkit-test-relentlessly
description: Run tests relentlessly until all pass. Use for TDD, fixing test failures, ensuring green builds.
argument-hint: "[task] [--max N]"
triggers:
  - test relentlessly
  - keep testing until green
  - fix all failing tests
  - make tests pass
  - TDD this
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-test-relentlessly

Execute tests repeatedly, fixing failures until all pass. The Stop hook prevents exit until tests are green or max iterations reached.

---

## CRITICAL: Fully Autonomous

**This skill runs WITHOUT user interaction.** Designed for overnight/unattended execution.

- **NEVER** use AskUserQuestion
- **NEVER** ask for confirmation
- **NEVER** stop to ask "what should I do?"
- **ALWAYS** auto-detect test commands
- **ALWAYS** make autonomous decisions
- **IF stuck**, try alternative approaches before giving up

The user invokes this skill and walks away. Come back to either success or a clear failure report.

---

## When to Invoke

**User triggers:**
- "Test relentlessly"
- "Make the tests pass"
- "Fix all failing tests"
- "Keep going until green"
- "TDD this feature"

**Use cases:**
- TDD implementation (tests exist, code doesn't)
- Fixing multiple test failures after refactor
- Ensuring all tests pass before commit
- Implementing feature to match test spec

---

## Arguments

```
/shipkit-test-relentlessly [task] [--max N]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `task` | No | "Fix all failing tests" | Description of what to implement/fix |
| `--max N` | No | 10 | Maximum iterations before giving up |

**Examples:**
```
/shipkit-test-relentlessly
/shipkit-test-relentlessly implement UserService
/shipkit-test-relentlessly --max 15 TDD the auth module
```

---

## How It Works

1. **You create a state file** with a `completion_promise`
2. **You work on making tests pass**
3. **You run the test command** to check progress
4. **If promise met:** Delete state file and stop
5. **If not met:** End response → Hook blocks → You continue

**You decide when the promise is met** - the hook just manages iteration.

---

## CRITICAL: Loop Mechanism

**The loop works differently than you might expect:**

1. **CREATE STATE FILE FIRST** - Before ANY other work, create `.shipkit/relentless-test.{sid8}.local.md`. Without this file, the Stop hook won't activate.

2. **YOU check if the promise is met** - Run the test command, check if all tests pass. The hook does NOT run commands.

3. **When promise is met:** Delete the state file, then finish your response. The hook will allow you to stop.

4. **When NOT met:** Just finish your response. The hook will:
   - Increment the iteration counter
   - Block your stop
   - Feed your task and completion_promise back to you

5. **When blocked, you'll see:**
   ```
   Relentless Mode: Test - Iteration 3/10

   Completion Promise: All tests pass with no failures

   Your Task: [your task from the state file body]
   ```

**The pattern is:** Create state file → Fix tests → Run tests → Promise met? Delete file & stop : End response → Hook blocks → Repeat

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
- Input: `--max 15 TDD auth module` → max=15, task="TDD auth module"
- Input: `implement UserService` → max=10, task="implement UserService"
- Input: (empty) → max=10, task="Fix all failing tests"

### Step 1: Detect Test Framework (Autonomous)

**Auto-detect test command - DO NOT ask user:**

| Indicator | Test Command |
|-----------|--------------|
| `package.json` with `test` script | `npm test` |
| `pytest.ini` or `conftest.py` | `pytest` |
| `pyproject.toml` with pytest | `pytest` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |
| `*.test.js` or `*.spec.ts` files | `npm test` |
| `jest.config.*` | `npx jest` |
| `vitest.config.*` | `npx vitest run` |
| `phpunit.xml` | `./vendor/bin/phpunit` |

**Detection order:**
1. Check `package.json` scripts for "test"
2. Check for test config files (jest.config, vitest.config, pytest.ini)
3. Check for test files pattern
4. **Fallback:** `npm test` for JS/TS, `pytest` for Python

**NEVER ask the user** - make your best guess and proceed.

### Step 2: Create State File

**Write to:** `.shipkit/relentless-test.{sid8}.local.md`

```markdown
---
skill: test-relentlessly
iteration: 1
max_iterations: [from --max or 10]
completion_promise: "All tests pass with no failures"
enabled: true
---

[User's task description or "Fix all failing tests"]
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
1. Run the test command to see current failures
2. Implement or fix code to make tests pass
3. Run tests again to check progress
4. **If all tests pass:** Delete `.shipkit/relentless-test.{sid8}.local.md` and finish
5. **If tests fail:** End your response normally → hook blocks → you continue

**YOU are responsible for:**
- Running the test command to check status
- Deciding if the completion_promise is met
- Deleting the state file when successful

**The hook only:**
- Increments the iteration counter
- Blocks your stop and reminds you of the task
- Enforces max_iterations limit

### Step 4: Completion

When tests pass:
- State file is automatically deleted
- You'll see: "Relentless mode: Success criteria met after N iteration(s)"

When max iterations reached:
- State file is automatically deleted
- Report to user what tests still fail
- Suggest next steps

---

## Constraints

- **Max iterations**: Default 10 (prevents infinite loops)
- **Focus**: Making tests pass, not changing test expectations
- **Timeout**: Test command has 120s timeout per check
- **Fully autonomous**: NO user prompts, NO confirmations, NO questions
- **When stuck**: Try different implementation approaches, check test assumptions, look for patterns in passing tests
- **Philosophy**: If a test seems wrong, note it but still try to make it pass
- **Decision making**: Make reasonable choices autonomously. Wrong guess + iterate > ask and wait

---

## Example Session

```
User: test relentlessly - implement the UserService class

Claude:
1. Detects npm test, uses `npm test`
2. Creates .shipkit/relentless-test.{sid8}.local.md
3. Runs tests, sees 5 failures in user.test.ts
4. Implements UserService.create() (2 tests pass)
5. [Attempts to stop]
6. Stop hook runs tests → 3 failures remain → continues
7. Implements UserService.findById() (2 more pass)
8. [Attempts to stop]
9. Stop hook runs tests → 1 failure remains → continues
10. Fixes edge case in UserService.delete()
11. [Attempts to stop]
12. Stop hook runs tests → all pass → allows stop
13. "Success criteria met after 4 iterations"
```

---

## Test Strategy Integration

If a spec exists at `.shipkit/specs/active/*.json`, check its **Test Strategy** section for:
- Which test types to focus on (unit, integration, e2e)
- Key test cases expected
- Mocking strategy

This guides which tests to prioritize and how to approach failures.

---

## State File Location

`.shipkit/relentless-test.{sid8}.local.md`

This file:
- Activates the relentless Stop hook
- Tracks iteration count
- Stores the test command and patterns
- Is auto-deleted on success or max iterations

**To cancel manually:** Delete this file.

---

## Integration with Other Skills

**Before:**
- `/shipkit-spec` - may have defined test strategy
- `/shipkit-build-relentlessly` - ensure it compiles first

**After:**
- `/shipkit-lint-relentlessly` - clean up code style
- `/shipkit-verify` - quality review before commit

**Natural progression:**
```
build-relentlessly → test-relentlessly → lint-relentlessly
```

---

## Context Files

**Reads:**
- Test configuration (package.json, pytest.ini, etc.)
- Test files to understand what's being tested
- Source files to implement/fix
- `.shipkit/specs/active/*.json` for test strategy (if exists)

**Writes:**
- `.shipkit/relentless-test.{sid8}.local.md` (temporary, auto-deleted)

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Test framework detected or provided
- [ ] State file created with correct command
- [ ] Tests analyzed and failures addressed
- [ ] All tests passing (exit code 0 + success pattern)
- [ ] State file cleaned up
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Tests pass. Consider:
- `/shipkit-lint-relentlessly` for code cleanup
- `/shipkit-verify` for quality review
- Commit the working code
<!-- /SECTION:after-completion -->
