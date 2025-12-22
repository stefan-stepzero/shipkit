# Verification Before Completion Reference

Complete guide to evidence-based completion verification.

## The Core Principle

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

This means:
- No "should be working now"
- No "looks good"
- No "probably fixed"
- No "let me know if it works"

**Evidence first. Claims second. Always.**

## What is Verification?

**Verification** = Running a command and showing the output that proves your claim.

**Not verification:**
- Remembering what happened last time
- Assuming it still works
- Visual inspection without running
- Partial output
- Summarized results

**Verification:**
- Running the actual command
- Capturing the FULL output
- Showing it proves the claim
- Fresh (not cached)

## The Verification Pattern

### Step 1: Identify the Verification Command

**For each claim, ask: "What command proves this?"**

| Claim | Verification Command |
|-------|---------------------|
| "Tests pass" | `npm test` (or language equivalent) |
| "Code compiles" | `npm run build` or `tsc` |
| "Linter happy" | `npm run lint` |
| "App runs" | `npm start` (show startup logs) |
| "API works" | `curl http://localhost:3000/api/health` |
| "Database migrated" | `npm run db:status` |

### Step 2: Run the Command

**In the project directory, run the command:**

```bash
cd /path/to/project
npm test
```

### Step 3: Read the Output

**Capture the FULL output, not a summary:**

❌ **Wrong:**
```
Tests passed.
```

✅ **Right:**
```
PASS  src/utils/calculateTotal.test.js
  calculateTotal
    ✓ sums item prices (3 ms)
    ✓ handles empty array (1 ms)
    ✓ handles null items (2 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.234 s
Ran all test suites.
```

### Step 4: Verify Success

**Check the output shows success:**

For tests:
- "X passed" (all tests listed)
- "0 failed"
- No error messages
- Exit code 0

For builds:
- "Build succeeded"
- Output files created
- No errors
- Exit code 0

For linters:
- "0 errors, 0 warnings"
- Or specific count with details
- Exit code 0

### Step 5: Claim Completion

**Only NOW can you claim success:**

✅ **Right:**
```
Task complete. All tests passing:

PASS  src/utils/calculateTotal.test.js
  calculateTotal
    ✓ sums item prices (3 ms)
    ✓ handles empty array (1 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
```

## Evidence Requirements

### Requirement 1: Fresh Output

**The output must be from a command you JUST ran.**

❌ **Not fresh:**
- "Tests passed earlier"
- "I ran this yesterday"
- "Should still work"

✅ **Fresh:**
- Run command now
- Capture output now
- Show output now

### Requirement 2: Complete Output

**Show enough output to prove the claim.**

❌ **Incomplete:**
```
Tests: 15 passed
```
(What about failures? How many total?)

✅ **Complete:**
```
Test Suites: 3 passed, 3 total
Tests:       15 passed, 15 total
Snapshots:   0 total
Time:        2.456 s
Ran all test suites.
```

### Requirement 3: Relevant Output

**The output must prove the specific claim.**

**Claim:** "All tests pass"

❌ **Not relevant:**
```
$ npm run build
Build succeeded in 1.2s
```
(This proves build works, not that tests pass)

✅ **Relevant:**
```
$ npm test
PASS src/calculate.test.js
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

## Common Scenarios

### Scenario 1: Tests Pass

**Claim:** All tests passing

**Verification:**
```bash
npm test

# or
pytest

# or
go test ./...

# or
cargo test
```

**Evidence:**
```
✓ Show test count (X passed, Y total)
✓ Show 0 failed
✓ Show which test files ran
✓ Show exit code 0 (implicit or explicit)
```

### Scenario 2: Feature Works

**Claim:** Feature implemented and working

**Verification:**
```bash
# Run tests for that feature
npm test -- calculateTotal.test.js

# AND run the app
npm start

# AND test the feature manually (show output)
curl http://localhost:3000/api/calculate -d '{"items":[{"price":10}]}'
```

**Evidence:**
```
✓ Tests for feature pass
✓ App starts without errors
✓ Manual test shows expected output
```

### Scenario 3: Bug Fixed

**Claim:** Bug fixed

**Verification:**
```bash
# Run the test that was failing
npm test -- bugfix.test.js

# Run ALL tests (ensure no regressions)
npm test
```

**Evidence:**
```
✓ Specific test that was failing now passes
✓ All other tests still pass
✓ No new failures introduced
```

### Scenario 4: Code Refactored

**Claim:** Code refactored successfully

**Verification:**
```bash
# Run ALL tests
npm test

# Run linter
npm run lint
```

**Evidence:**
```
✓ All tests still pass (behavior unchanged)
✓ No linter errors
✓ Code compiles (if typed language)
```

### Scenario 5: Build Succeeds

**Claim:** Build successful

**Verification:**
```bash
# Clean previous build
npm run clean

# Run fresh build
npm run build
```

**Evidence:**
```
✓ Build command exits successfully
✓ Output files created
✓ No errors in build log
```

## Red Flags

### Red Flag 1: "Should be working now"

**Problem:** No evidence provided

**Fix:**
```bash
# Don't say "should work"
# Run the command and SHOW it works

npm test
# [paste output here]
```

### Red Flag 2: "Looks good"

**Problem:** Visual inspection, no command run

**Fix:**
```bash
# Don't just look at code
# Run verification command

npm run lint
npm test
# [paste output here]
```

### Red Flag 3: "Probably fixed"

**Problem:** Uncertainty without verification

**Fix:**
```bash
# Don't guess
# Verify

npm test
# [paste output showing fix worked]
```

### Red Flag 4: "Let me know if it works"

**Problem:** Shifting verification responsibility to user

**Fix:**
```bash
# Don't ask user to verify
# Verify yourself FIRST

npm test
# [output showing it works]

# THEN: "Verified working. Please test on your end."
```

### Red Flag 5: Partial Output

**Problem:**
```
Some tests passed...
```

**Fix:**
```
PASS  src/feature.test.js
  Feature
    ✓ test 1 (3ms)
    ✓ test 2 (2ms)
    ✓ test 3 (1ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

### Red Flag 6: Summary Instead of Output

**Problem:**
```
All 15 tests passed.
```

**Fix:**
```
$ npm test

PASS  src/calculate.test.js
PASS  src/format.test.js
PASS  src/validate.test.js

Test Suites: 3 passed, 3 total
Tests:       15 passed, 15 total
Snapshots:   0 total
Time:        2.456 s
```

## When Verification Fails

### Failure Pattern

```
1. Run verification command
   ↓
2. Command fails
   ↓
3. DON'T claim completion
   ↓
4. Investigate failure
   ↓
5. Fix root cause
   ↓
6. Run verification again
   ↓
7. ONLY claim completion when verification PASSES
```

### Example: Test Failure

**Attempt:**
```bash
$ npm test

FAIL  src/calculate.test.js
  ● calculateTotal › handles empty array

    expect(received).toBe(expected)

    Expected: 0
    Received: undefined

      10 |   test('handles empty array', () => {
    > 11 |     expect(calculateTotal([])).toBe(0);
         |                                ^

Test Suites: 1 failed, 1 total
Tests:       1 failed, 2 passed, 3 total
```

**Response:**
❌ "Should be fixed now" (without re-running)
❌ "Let me know if it passes"

✅ Fix the issue → Run again → Show passing output

**Fixed:**
```bash
$ npm test

PASS  src/calculate.test.js
  calculateTotal
    ✓ sums item prices (3 ms)
    ✓ handles empty array (1 ms)  ← NOW PASSES
    ✓ handles null items (2 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

## Verification Checklist

Before claiming ANY task complete:

- [ ] Identified verification command
- [ ] Ran command in project directory
- [ ] Captured FULL output (not summary)
- [ ] Output shows SUCCESS (no failures)
- [ ] Output is FRESH (just ran it)
- [ ] Output is RELEVANT (proves the claim)
- [ ] No errors or warnings
- [ ] Exit code 0

**If ANY checkbox is unchecked → NOT verified → CANNOT claim completion**

## Quick Reference

```
┌──────────────────────────────────────────┐
│ VERIFICATION QUICK REFERENCE             │
├──────────────────────────────────────────┤
│ Before claiming completion:              │
│                                          │
│ 1. What proves this?                     │
│    → Identify command                    │
│                                          │
│ 2. Run the command                       │
│    → Execute in project directory        │
│                                          │
│ 3. Read the output                       │
│    → Capture FULL output                 │
│                                          │
│ 4. Verify success                        │
│    → Check for errors/failures           │
│                                          │
│ 5. Show evidence                         │
│    → Paste output with claim             │
│                                          │
│ ONLY THEN:                               │
│ "Task complete [evidence]"               │
└──────────────────────────────────────────┘

RED FLAGS:
• "Should work" → RUN IT
• "Looks good" → VERIFY IT
• "Probably fixed" → PROVE IT
• "Let me know" → VERIFY YOURSELF
• Partial output → SHOW COMPLETE
• Old output → RUN FRESH
```

## Examples by Language

### JavaScript/TypeScript

```bash
# Tests
npm test

# Build
npm run build

# Lint
npm run lint

# Type check
npm run type-check
# or
tsc --noEmit
```

### Python

```bash
# Tests
pytest

# Tests with coverage
pytest --cov

# Lint
flake8

# Type check
mypy src/
```

### Go

```bash
# Tests
go test ./...

# Tests with coverage
go test -cover ./...

# Build
go build

# Lint
golangci-lint run
```

### Rust

```bash
# Tests
cargo test

# Build
cargo build

# Lint
cargo clippy

# Format check
cargo fmt -- --check
```

## When You Can't Verify

**Scenario:** No automated tests exist yet

**Wrong approach:**
"Can't verify, no tests"

**Right approach:**
1. Write a test first (TDD)
2. Or create manual verification steps
3. Document the verification process
4. Run the steps
5. Show the output

**Manual verification example:**
```bash
# Start the app
npm start
# → Server running on http://localhost:3000

# Test the endpoint
curl http://localhost:3000/api/users
# → {"users": [...]} (200 OK)

# Verify UI
# → Open http://localhost:3000
# → Screenshot showing feature works
```

**Still evidence-based, even if manual.**

---

**Remember:** Verification is not bureaucracy. It's how you KNOW it works, not HOPE it works.
