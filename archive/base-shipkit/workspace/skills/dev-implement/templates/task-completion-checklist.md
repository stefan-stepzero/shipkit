# Task Completion Checklist

Use this checklist before marking any task as complete.

## Task: [Task Number and Description]

### TDD Cycle Completion

- [ ] **🔴 RED** - Wrote failing test FIRST
  - Test demonstrates desired behavior
  - Test FAILED when first run (proving it works)
  - Never wrote production code before the test

- [ ] **🟢 GREEN** - Wrote minimal implementation
  - Wrote simplest code that makes test pass
  - No extra features or premature optimization
  - Test PASSES
  - ALL tests PASS (no regressions)

- [ ] **🔵 REFACTOR** - Cleaned up code
  - Improved code structure where needed
  - Removed duplication
  - Tests STILL PASS after refactoring

### Constitution Compliance

- [ ] Read constitution.md BEFORE writing code
- [ ] Followed architectural patterns from constitution
- [ ] Applied coding standards from constitution
- [ ] Met testing requirements from constitution
- [ ] Validated against performance/security standards

### Two-Stage Code Review

#### Stage 1: Spec Compliance

- [ ] Implementation matches user story acceptance criteria
- [ ] Nothing extra added (YAGNI principle)
- [ ] Nothing missing from requirements
- [ ] Follows patterns specified in constitution

#### Stage 2: Code Quality

- [ ] No magic numbers or strings
- [ ] Proper error handling
- [ ] Good naming (variables, functions, classes)
- [ ] No unnecessary complexity
- [ ] Constitution standards followed

### Verification (Evidence Required)

- [ ] Ran full test suite
- [ ] Captured FRESH test output (not cached)
- [ ] ALL tests PASS (with evidence shown)
- [ ] No warnings or errors in output

### Git Status

- [ ] All changes committed
- [ ] Commit message describes what was done
- [ ] No uncommitted changes in working directory

### Documentation (if applicable)

- [ ] Updated code comments where needed
- [ ] Updated README if public API changed
- [ ] Documented any non-obvious decisions

## Evidence

**Test Output:**
```
[Paste fresh test output here showing all tests passing]
```

**Git Commit:**
```
[Commit hash and message]
```

## Sign-off

- [ ] All checklist items completed
- [ ] Evidence provided above
- [ ] Ready to mark task [X] in tasks.md

---

**Notes:**
- This checklist ensures quality before claiming completion
- Skip items only if truly not applicable (document reason)
- When in doubt, verify again
- Evidence before claims, always
