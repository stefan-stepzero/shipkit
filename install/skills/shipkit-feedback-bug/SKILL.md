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
- Existing specs: `.shipkit/specs/active/*.json` (avoid duplicates)

**Schema Reference**:
- `references/output-schema.md` - Complete JSON schema definition
- `references/example.json` - Realistic bug spec example

---

## Arguments

If `$ARGUMENTS` is provided (e.g. `/shipkit-feedback-bug The login button doesn't work on mobile`), treat it as the feedback input. Skip the "paste your feedback" prompt in Step 1 and proceed directly to parsing and categorization.

If `$ARGUMENTS` is empty, proceed normally — ask the user to provide feedback first.

---

## Process Overview

```
Step 1: Receive & Parse Feedback
    ↓
Step 2: Categorize Each Item (bug / feature / won't fix)
    ↓
Step 3: For Each Bug → Investigate (reproduce, isolate, root cause, stress-test fix)
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

### 3b: Isolate the Problem + Assess Blast Radius (PARALLEL)

**Index-Accelerated Investigation** — Read `.shipkit/codebase-index.json` if available:

1. `Read: .shipkit/codebase-index.json`
2. If index exists:
   - Use `concepts` to immediately locate files for the affected feature area
   - Use `coreFiles` to assess blast radius of high-dependency files
   - Pass file lists to agents below for targeted investigation
3. If index doesn't exist → agents discover related code via broad scanning

**FOR MULTIPLE BUGS, USE PARALLEL SUBAGENTS:**

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. CODE ISOLATION AGENT (subagent_type: "Explore")
   Prompt: "Find code related to [feature/component from bug].
   [If index exists, include: 'The codebase index maps these files for this area: [concept files]. Start from these.']
   Look for: event handlers, state management, API calls.
   Check for: error handling, edge cases, race conditions.
   Return: file paths, relevant code sections, potential problem areas."

2. BLAST RADIUS AGENT (subagent_type: "Explore")
   Prompt: "Find all places using similar patterns to [feature/component].
   [If index exists, include: 'Core files (high fan-in): [coreFiles]. Concepts: [concepts]. Use these to quickly identify blast radius scope.']
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

### 3d: Solution Robustness Check

**Goal**: Before proposing a fix, verify it handles the *general case* — not just the exact reported scenario.

Bugs return as variations. A fix that only addresses the specific report will break when reality throws edge cases at it. This step forces you to stress-test the fix strategy before it gets baked into the spec.

**Map root cause type to relevant edge case categories:**

| Root Cause Type | Always Check | Often Check |
|-----------------|-------------|-------------|
| `race-condition` | Loading, Data Consistency | Boundary |
| `state-management` | Data Consistency, Loading | Empty/Missing |
| `missing-validation` | Boundary, Empty/Missing, Error | — |
| `logic-error` | Boundary, Empty/Missing | — |
| `integration` | Error, Loading | External Service |
| `environment` | Error, Boundary | — |

**For each relevant category, stress-test the proposed fix:**

1. **Loading States** — Does the fix handle pending operations? What if the same action fires twice rapidly? What if the operation times out? Does the fix itself introduce new async that could race?

2. **Error States** — Does the fix degrade gracefully on network failure? What if the server returns an error mid-fix? Does the fix handle partial failure (some operations succeed, some don't)?

3. **Empty/Missing States** — Does the fix work when the data is empty, null, or undefined? What about a deleted resource? First-time user with no prior state?

4. **Boundary Conditions** — Does the fix handle min/max values? Zero items, one item, thousands of items? Off-by-one scenarios? Rate limits or quotas?

5. **Data Consistency** — Does the fix prevent stale data? What about concurrent users modifying the same resource? Cache invalidation? Partial updates that leave inconsistent state?

6. **External Service Constraints** (integration bugs only) — Does the fix respect timeout budgets? Rate limits from the provider? What happens when the external service is slow or down?

**Not every category applies to every bug.** Use the mapping table — skip categories that aren't relevant. But ALWAYS check the "Always Check" categories for your root cause type.

**How to apply:**

1. Draft the fix approach based on root cause
2. Look up relevant edge case categories from the mapping table
3. For each relevant category, ask: "Does this fix still work when [category scenario]?"
4. If the answer is "no" or "maybe" — expand the fix to handle it
5. Record findings in `robustness.findings` (these feed into acceptance criteria)

**Example — race condition bug (rapid save clicks):**

| Category | Question | Finding |
|----------|----------|---------|
| Loading | Does debouncing handle in-flight requests? | No — need AbortController to cancel pending request, not just debounce new ones |
| Consistency | Can two saves produce inconsistent state? | Yes — add optimistic update rollback on failure |
| Boundary | What about 0ms delay (instant double-click)? | Debounce alone won't catch it — need request deduplication too |

The original fix "debounce the save button" was a point-fix. After robustness check, the fix becomes "debounce + AbortController + request deduplication + rollback on failure."

**Why this matters**: The 10 seconds spent checking edge cases here prevents the next bug report that says "it still happens when [variation]."

### 3e: Capture Learnings

**Document patterns to avoid and patterns to use:**

- What caused this bug? (pattern to avoid)
- What's the better approach? (pattern to use)
- Significant enough for `/shipkit-architecture-memory`?

---

## Step 4: Finalize Bug Specs

**For each investigated bug, create spec file:**

**Location**: `.shipkit/specs/active/bug-[brief-name].json`

**Schema**: See `references/output-schema.md` for complete field reference.

**Template Structure**:

```json
{
  "$schema": "shipkit-artifact",
  "type": "bug-spec",
  "version": "1.0",
  "lastUpdated": "[ISO 8601 timestamp]",
  "source": "shipkit-feedback-bug",

  "summary": {
    "name": "[Brief Description]",
    "status": "active",
    "severity": "[critical/high/medium/low]",
    "feedbackSource": "[user-testing/beta/bug-report/general]",
    "rootCauseType": "[logic-error/race-condition/missing-validation/state-management/integration/environment]",
    "affectedComponentCount": 0,
    "hasBlastRadius": false
  },

  "metadata": {
    "id": "bug-[brief-name]",
    "created": "[YYYY-MM-DD]",
    "updated": "[YYYY-MM-DD]",
    "author": "shipkit-feedback-bug",
    "feedbackDate": "[YYYY-MM-DD]"
  },

  "originalFeedback": {
    "quote": "[Original user quote]",
    "source": "[Same as summary.feedbackSource]",
    "reporter": "[Who reported it]"
  },

  "problem": {
    "statement": "[Clear description of what's broken]",
    "expectedBehavior": "[What should happen]",
    "actualBehavior": "[What happens instead]"
  },

  "reproduction": {
    "confirmed": "[YYYY-MM-DD]",
    "steps": [
      "[Step 1]",
      "[Step 2]",
      "[Step 3]"
    ],
    "environment": {
      "browser": "[Browser if relevant]",
      "os": "[OS if relevant]",
      "prerequisites": ["[Required preconditions]"]
    },
    "minimumRepro": "[Simplest case that triggers bug]"
  },

  "investigation": {
    "codePath": {
      "entry": "[Where it starts]",
      "failurePoint": "[Where it goes wrong]",
      "relevantFiles": ["[file:line references]"]
    },
    "rootCause": {
      "fiveWhys": [
        { "level": 1, "symptom": "[Symptom]", "because": "[Why]" },
        { "level": 2, "symptom": "[That]", "because": "[Why]" },
        { "level": 3, "symptom": "[That]", "because": "[Root cause]" }
      ],
      "conclusion": "[Final root cause statement]",
      "type": "[Same as summary.rootCauseType]"
    },
    "blastRadius": {
      "description": "[Summary of impact or 'Isolated to this component']",
      "affectedComponents": [
        { "file": "[path]", "risk": "[high/medium/low]", "samePattern": true }
      ]
    }
  },

  "fix": {
    "approach": "[How to fix it — general strategy, not just the point-fix]",
    "robustness": {
      "edgeCasesConsidered": ["[categories checked from mapping table]"],
      "findings": [
        "[Category]: [What the robustness check revealed and how fix addresses it]"
      ]
    },
    "acceptanceCriteria": [
      "[Specific criterion from bug report]",
      "[Criterion from robustness findings]",
      "No regression in related functionality",
      "Blast radius addressed (if applicable)"
    ]
  },

  "learnings": {
    "patternToAvoid": "[What caused this]",
    "patternToUse": "[Better approach]",
    "architectureMemoryWorthy": false
  },

  "resolution": {
    "status": "open",
    "fixedIn": null,
    "verifiedBy": null,
    "verifiedDate": null
  },

  "references": {
    "stack": ".shipkit/stack.json",
    "codebaseIndex": ".shipkit/codebase-index.json",
    "relatedSpecs": [],
    "relatedBugs": []
  },

  "nextSteps": [
    "[Suggested next actions]",
    "/shipkit-verify after implementation"
  ]
}
```

**See `references/example.json` for a complete realistic example.**

---

## Step 5: Output Summary

```
Triage & Investigation Complete

Bugs (X) - Investigated & Spec'd:
┌─────────────────────────────────┬──────────┬─────────────────────────────┐
│ Spec                            │ Severity │ Root Cause                  │
├─────────────────────────────────┼──────────┼─────────────────────────────┤
│ bug-save-button.json            │ High     │ Race condition in async     │
│ bug-login-timeout.json          │ Medium   │ Missing error handler       │
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

For obvious bugs that don't need deep investigation, use the same JSON schema but with minimal fields:

```json
{
  "$schema": "shipkit-artifact",
  "type": "bug-spec",
  "version": "1.0",
  "lastUpdated": "[ISO 8601 timestamp]",
  "source": "shipkit-feedback-bug",

  "summary": {
    "name": "[Brief Description]",
    "status": "active",
    "severity": "[level]",
    "feedbackSource": "[source]",
    "rootCauseType": "[type]",
    "affectedComponentCount": 0,
    "hasBlastRadius": false
  },

  "metadata": {
    "id": "bug-[name]",
    "created": "[YYYY-MM-DD]",
    "updated": "[YYYY-MM-DD]",
    "author": "shipkit-feedback-bug",
    "feedbackDate": "[YYYY-MM-DD]"
  },

  "originalFeedback": {
    "quote": "[Original report]",
    "source": "[source]"
  },

  "problem": {
    "statement": "[What's broken]",
    "expectedBehavior": "[Expected]",
    "actualBehavior": "[Actual]"
  },

  "reproduction": {
    "confirmed": "[YYYY-MM-DD]",
    "steps": ["[Steps]"],
    "minimumRepro": "[Minimum repro]"
  },

  "investigation": {
    "codePath": {
      "entry": "[Entry point]",
      "failurePoint": "[Failure point]",
      "relevantFiles": []
    },
    "rootCause": {
      "fiveWhys": [
        { "level": 1, "symptom": "[Symptom]", "because": "[Root cause]" }
      ],
      "conclusion": "[Why it happens - even simple bugs should have this]",
      "type": "[type]"
    },
    "blastRadius": {
      "description": "Isolated to this component",
      "affectedComponents": []
    }
  },

  "fix": {
    "approach": "[How to fix — general strategy]",
    "robustness": {
      "edgeCasesConsidered": ["[relevant categories]"],
      "findings": ["[Category]: [Finding]"]
    },
    "acceptanceCriteria": ["[Acceptance criterion]"]
  },

  "learnings": {
    "patternToAvoid": "[Pattern]",
    "patternToUse": "[Better pattern]",
    "architectureMemoryWorthy": false
  },

  "resolution": {
    "status": "open",
    "fixedIn": null,
    "verifiedBy": null,
    "verifiedDate": null
  },

  "references": {
    "stack": ".shipkit/stack.json",
    "codebaseIndex": ".shipkit/codebase-index.json",
    "relatedSpecs": [],
    "relatedBugs": []
  },

  "nextSteps": ["/shipkit-verify after fix"]
}
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
- `.shipkit/specs/active/*.json` - Check for duplicates

---

## Context Files This Skill Writes

**Write Strategy: CREATE**

**Creates**:
- `.shipkit/specs/active/bug-[name].json` - Investigated bug spec per confirmed bug (see `references/output-schema.md`)

**Lifecycle**:
- Active bugs live in `specs/active/`
- When fixed, update `resolution.status` to `"resolved"` and move to `specs/implemented/`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Bug specs saved with investigation findings
2. **Root causes** - Each bug has identified root cause (not just symptoms)
3. **Robustness** - Fix stress-tested against relevant edge case categories
4. **Blast radius** - Other affected code identified where applicable
5. **Learnings** - Patterns to avoid/use documented

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
- [ ] Fix stress-tested against relevant edge case categories (robustness check)
- [ ] Bug specs created with findings
- [ ] Blast radius assessed
- [ ] Feature requests noted for `/shipkit-spec`
- [ ] Summary provided with next steps
<!-- /SECTION:success-criteria -->

---

**Remember**: Don't just document symptoms - investigate to find root causes. The goal is specs that are ready to fix, with learnings that prevent similar bugs.
