---
name: shipkit-feedback-bug
description: "Process user feedback into investigated bug specs with root cause analysis. Triggers: 'triage feedback', 'process bug reports', 'user testing feedback'."
argument-hint: "<paste feedback or describe source>"
context: fork
agent: shipkit-researcher-agent
---

# shipkit-feedback-bug - Feedback to Investigated Bug Specs

**Purpose**: Transform raw user feedback into fully investigated bug specifications with root cause analysis, blast radius assessment, and captured learnings.

---

## When to Invoke

**User triggers**:
- "Triage this feedback"
- "Process these bug reports"
- "I got user testing feedback"
- "Here's what testers found"
- User pastes a dump of feedback from testing

**Workflow position**:
- After user testing or beta feedback received
- Before debugging/fixing begins
- Creates investigated specs ready for implementation

---

## Prerequisites

**Required**:
- Feedback to process (user provides)

**Recommended**:
- Stack defined: `.shipkit/stack.json` (tech context)
- Codebase indexed: `.shipkit/codebase-index.json` (faster investigation)
- Existing specs: `.shipkit/specs/active/*.md` (avoid duplicates)

---

## Process Overview

```
Step 1: Receive & Parse Feedback
    ↓
Step 2: Categorize Each Item (bug / feature / won't fix)
    ↓
Step 3: For Each Bug → Investigate (reproduce, isolate, root cause)
    ↓
Step 4: Finalize Bug Specs with Findings
    ↓
Step 5: Output Summary
```

---

## Step 1: Receive & Parse Feedback

**If user hasn't provided feedback**, ask:

```
header: "Feedback"
question: "Paste your feedback dump, or describe where it's coming from"
```

**Ask for context**:

```
header: "Source"
question: "Where did this feedback come from?"
options:
  - label: "User Testing Session"
    description: "Structured testing with specific tasks"
  - label: "Beta Testers"
    description: "Real users trying the product"
  - label: "Bug Reports"
    description: "Formal bug submissions"
  - label: "General Feedback"
    description: "Mixed feedback from various sources"
```

**Parse the feedback** into discrete items:
- Extract individual complaints/observations
- Note any reproduction steps mentioned
- Identify severity hints (frustration level, blockers)
- Group related items (multiple reports of same issue → one item)

---

## Step 2: Categorize Each Item

**Present items for user categorization:**

```
[1/N] "[Brief description of the issue]"

Category:
- Bug: Something broken that should work
- Feature Request: New capability → route to /shipkit-spec
- UX Issue: Works but confusing → route to /shipkit-spec
- Won't Fix: User error, out of scope, or not reproducible

Severity (for bugs):
- Critical: Blocks core functionality, data loss
- High: Major feature broken, workaround difficult
- Medium: Feature impaired, workaround exists
- Low: Minor issue, cosmetic, edge case
```

**For Feature Requests / UX Issues**: Note them for summary, suggest `/shipkit-spec`.

**For Won't Fix**: Capture the reason for future reference.

---

## Step 3: Investigate Each Bug

**For each confirmed bug, investigate before finalizing the spec.**

### 3a: Reproduce & Confirm

**Goal**: Verify the bug is real, find minimum reproduction.

- Follow reported steps
- Note exact error messages, console output
- Find the simplest case that triggers the bug

### 3b: Isolate the Problem + 3d: Assess Blast Radius (PARALLEL)

**FOR MULTIPLE BUGS, USE PARALLEL SUBAGENTS:**

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. CODE ISOLATION AGENT (subagent_type: "Explore")
   Prompt: "Find code related to [feature/component from bug].
   Look for: event handlers, state management, API calls.
   Check for: error handling, edge cases, race conditions.
   Return: file paths, relevant code sections, potential problem areas."

2. BLAST RADIUS AGENT (subagent_type: "Explore")
   Prompt: "Find all places using similar patterns to [feature/component].
   Check if same bug pattern could occur elsewhere.
   Return: list of files with similar code, risk assessment per file."
```

**Why parallel**: Isolation and blast radius are independent investigations - running them simultaneously speeds up the analysis.

**Isolation techniques** (after agent returns):
- Binary search: Disable half the code path, does bug persist?
- Input variation: What inputs trigger vs don't trigger?
- State inspection: What's the state when it fails?

### 3c: Root Cause Analysis (5 Whys)

**Keep asking "why" until you reach the actual cause:**

```
Why doesn't save work?
→ Success handler doesn't run

Why doesn't success handler run?
→ Loading check fails

Why does loading check fail?
→ State reset before response arrives

Why is state reset early?
→ useEffect cleanup on re-render

ROOT CAUSE: Race condition between parent re-render and async response
```

**Classify the root cause**:
- Logic error (wrong condition, off-by-one)
- Race condition (timing, async, state)
- Missing validation (null check, type check)
- State management (stale state, wrong scope)
- Integration issue (API contract, external service)
- Environment issue (browser, config)

**Document blast radius**: Use results from parallel agent to identify other code/features with same issue.

### 3e: Capture Learnings

**Document patterns to avoid and patterns to use:**

- What caused this bug? (pattern to avoid)
- What's the better approach? (pattern to use)
- Significant enough for `/shipkit-architecture-memory`?

---

## Step 4: Finalize Bug Specs

**For each investigated bug, create spec file:**

**Location**: `.shipkit/specs/active/bug-[brief-name].md`

**Template**:

```markdown
# Bug: [Brief Description]

**Created**: [YYYY-MM-DD]
**Status**: Active
**Severity**: [Critical/High/Medium/Low]
**Source**: [User testing / Beta / Bug report]

---

## Problem

[Clear description of what's broken]

**Reported as**: "[Original user quote]"

---

## Reproduction

**Confirmed**: [date]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Environment**: [Browser/OS/state if relevant]

**Minimum repro**: [Simplest case that triggers bug]

---

## Expected vs Actual

**Expected**: [What should happen]

**Actual**: [What happens instead]

---

## Investigation Findings

### Code Path
- Entry: [where it starts]
- Failure point: [where it goes wrong]
- Relevant files: [file:line references]

### Root Cause (5 Whys)
1. [Symptom] → because
2. [That] → because
3. [That] → because
4. **Root**: [Actual cause]

### Blast Radius
- [Other affected code/features]
- [Or "Isolated to this component"]

---

## Fix

### Approach
[How to fix it]

### Acceptance Criteria
- [ ] [Specific criterion]
- [ ] No regression in related functionality
- [ ] Blast radius addressed (if applicable)

---

## Learnings

**Pattern to avoid**: [What caused this]

**Pattern to use**: [Better approach]

---

## Resolution

**Status**: Open
**Fixed in**: [version/commit - when resolved]
**Verified**: [/shipkit-verify or manual - when done]
```

---

## Step 5: Output Summary

```
Triage & Investigation Complete

Bugs (X) - Investigated & Spec'd:
┌─────────────────────────────────┬──────────┬─────────────────────────────┐
│ Spec                            │ Severity │ Root Cause                  │
├─────────────────────────────────┼──────────┼─────────────────────────────┤
│ bug-save-button.md              │ High     │ Race condition in async     │
│ bug-login-timeout.md            │ Medium   │ Missing error handler       │
└─────────────────────────────────┴──────────┴─────────────────────────────┘

Feature Requests (Y) - Route to /shipkit-spec:
- Export to PDF
- Dark mode toggle

Won't Fix (Z):
- "App is slow" - too vague, need specific reproduction

Blast Radius Notes:
- bug-save-button: Same pattern in useDelete, useUpdate (3 files total)

Next Steps:
1. Fix bugs in severity order (start with High)
2. Run /shipkit-spec for feature requests worth pursuing
3. Run /shipkit-verify after fixes
4. Consider /shipkit-architecture-memory for significant learnings
```

---

## Bug Spec Template (Minimal)

For obvious bugs that don't need deep investigation:

```markdown
# Bug: [Brief Description]

**Status**: Active | **Severity**: [Level] | **Source**: [Source]

## Problem
[What's broken]

## Reproduction
1. [Steps]

## Root Cause
[Why it happens - even simple bugs should have this]

## Fix When
- [ ] [Acceptance criterion]
```

---

## When This Skill Integrates with Others

### Before This Skill
- **User testing session** - Generates the raw feedback
- **Beta release** - Users discover issues

### After This Skill
- **Implementation (no skill)** - Fix bugs using the investigated specs
- `/shipkit-spec` - Spec out feature requests found in feedback
- `/shipkit-verify` - Verify fixes meet acceptance criteria
- `/shipkit-architecture-memory` - Log significant learnings as decisions

---

## Context Files This Skill Reads

- `.shipkit/stack.json` - Tech context for investigation
- `.shipkit/codebase-index.json` - Navigate codebase efficiently
- `.shipkit/specs/active/*.md` - Check for duplicates

---

## Context Files This Skill Writes

**Write Strategy: CREATE**

**Creates**:
- `.shipkit/specs/active/bug-[name].md` - Investigated bug spec per confirmed bug

**Lifecycle**:
- Active bugs live in `specs/active/`
- When fixed, move to `specs/implemented/` with resolution notes

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Bug specs saved with investigation findings
2. **Root causes** - Each bug has identified root cause (not just symptoms)
3. **Blast radius** - Other affected code identified where applicable
4. **Learnings** - Patterns to avoid/use documented

**Natural capabilities** (no skill needed): Implementing fixes, writing tests.

**Suggest skill when:**
- Significant learnings → `/shipkit-architecture-memory`
- Fix needs verification → `/shipkit-verify`
- Feature requests worth pursuing → `/shipkit-spec`
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Triage is complete when:
- [ ] All feedback items categorized
- [ ] Each bug investigated (reproduced, root cause found)
- [ ] Bug specs created with findings
- [ ] Blast radius assessed
- [ ] Feature requests noted for `/shipkit-spec`
- [ ] Summary provided with next steps
<!-- /SECTION:success-criteria -->

---

**Remember**: Don't just document symptoms - investigate to find root causes. The goal is specs that are ready to fix, with learnings that prevent similar bugs.
