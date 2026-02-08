---
name: shipkit-plan
description: "Use when a spec exists and user wants implementation steps. Triggers: 'how to implement', 'create plan', 'plan this', 'what are the steps'."
argument-hint: "[spec name]"
model: opus
agent: shipkit-architect-agent
---

# shipkit-plan - Implementation Planning with Failure Mode Prevention

**Purpose**: Transform feature specifications into validated implementation plans that prevent common planning failures: orphaned foundations, magical steps, codebase blindness, and incomplete coverage.

---

## When to Invoke

**User triggers**:
- "Plan how to build this"
- "Create implementation plan"
- "How should we implement this feature?"
- "Design the technical approach"

**After**:
- `/shipkit-spec` has created specification for the feature
- Feature is ready for implementation planning

---

## Prerequisites

**Check before starting**:
- Spec exists: `.shipkit/specs/active/[feature-name].json`
- Stack defined: `.shipkit/stack.json` (from shipkit-project-context)

**UI-Heavy Feature Check** (CRITICAL):
- If spec describes significant UI/UX → Prototype MUST exist before planning
- Check: `.shipkit-mockups/[feature-name]/` OR spec contains `## UI/UX Patterns` section
- See "Step 1.5: UI-Heavy Gate" below

**Optional but helpful**:
- Architecture decisions: `.shipkit/architecture.json`
- Type definitions: `.shipkit/contracts.json`

---

## Process

**Subagent Principle**: Use Explore subagents for codebase scanning and verification tasks. They're faster, use less context, and return focused results. See Steps 2.7 and 3 for specific subagent prompts.

---

### Step 1: Confirm Scope

**First, scan available specs:**
```bash
ls .shipkit/specs/active/*.json 2>/dev/null || echo "No specs found"
```

**Then use AskUserQuestion tool:**

**Question 1 - Spec Selection:** (if multiple specs exist)
```
header: "Spec"
question: "Which spec are you planning?"
options:
  - (dynamically list spec files found)
```

**Question 2 - Plan Detail:**
```
header: "Detail"
question: "What level of planning do you need?"
options:
  - label: "Quick POC (Recommended)"
    description: "Minimal steps, get something working fast"
  - label: "Standard"
    description: "Balanced detail, covers major concerns"
  - label: "Detailed"
    description: "Comprehensive plan with alternatives"
```

**If user selects "Other"**: Ask clarifying questions about their specific needs.

---

### Step 1.5: UI-Heavy Gate (CRITICAL)

**Before proceeding to planning, check if spec is UI-heavy.**

**UI-heavy indicators** (if 3+ found): form, modal, table, grid, dashboard, navigation, animation, drag/drop, chart, upload

**Decision logic:**
- UI-heavy + No prototype → BLOCK - Require prototype first
- UI-heavy + Prototype exists → Proceed to Step 2
- Not UI-heavy → Proceed to Step 2

**If BLOCKED**: Suggest `/shipkit-prototyping` or let user skip with acknowledgment of risk.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:
- `.shipkit/specs/active/[feature-name].json` (Required)
- `.shipkit/stack.json` (Stack info)
- `.shipkit/architecture.json` (Past decisions)

**Optional context** (load if relevant): contracts.json, schema.json

**Extract from spec:**
- All requirements (for coverage mapping later)
- Acceptance criteria
- Integration points mentioned

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 2.5: Architecture Anti-Pattern Check

**Before generating plan, check for architecture anti-patterns.**

**Reference**: See `shipkit-spec/references/best-practices.md` for frontend/backend patterns.

**Quick checks:**
1. **Auth**: Does spec mention auth? Is centralized auth in place? If not, add to Phase 1.
2. **Error Handling**: Global error boundary exists? If not, add to Phase 1.
3. **Data Fetching**: Shared data needed? Provider pattern exists? If not, add to Phase 1.

**Pattern Checklist** (ensure these exist or will be created in Phase 1):
- Auth: Centralized middleware/layout
- Errors: Global error boundary
- Data: Provider pattern (if needed)
- Config: Env validation
- API Response: Consistent format

---

### Step 2.7: Codebase Pattern Scan (CRITICAL - Prevents Codebase Blindness)

**Before proposing ANY pattern, verify what the codebase actually uses.**

**Why this matters**: Claude defaults to training data patterns. If codebase uses SWR but Claude proposes React Query, the plan creates inconsistency and technical debt.

**Index-Accelerated Scanning** — Read `.shipkit/codebase-index.json` first:

1. `Read: .shipkit/codebase-index.json`
2. If index exists:
   - Extract `framework`, `concepts`, `entryPoints`, `coreFiles`
   - Pass to Explore agents below so they skip broad discovery and focus on **pattern detail** (which specific library, how it's used, code snippets)
   - Skip detecting framework/stack (index already has it)
3. If index doesn't exist → proceed with full exploration below

**USE PARALLEL SUBAGENTS FOR PATTERN SCANNING** - Launch multiple Explore agents simultaneously for faster, more thorough scanning:

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. FRONTEND PATTERNS AGENT (subagent_type: "Explore")
   Prompt: "Scan codebase for frontend patterns.
   [If index exists, include: 'The codebase index shows: framework=[X], concepts=[Y], entry points=[Z]. Use these as starting points — focus on HOW patterns are used, not WHAT exists.']
   Find and report:
   - State management (useState/useReducer/Redux/Zustand/Jotai/signals)
   - Data fetching (fetch/axios/SWR/React Query/tRPC)
   - Component structure (feature folders/atomic/barrel exports)
   For each: pattern name, example file path, brief usage snippet."

2. BACKEND & INFRASTRUCTURE AGENT (subagent_type: "Explore")
   Prompt: "Scan codebase for backend/infrastructure patterns.
   [If index exists, include: 'The codebase index shows: framework=[X], concepts.auth=[files], concepts.database=[files]. Start from these files — focus on implementation detail, not discovery.']
   Find and report:
   - Auth pattern (session/JWT/middleware/protected routes)
   - Error handling (ErrorBoundary/try-catch/error middleware)
   - API patterns (route handlers, response format, validation)
   For each: pattern name, example file path, brief usage snippet."
```

**Why parallel subagents**:
- Each agent focuses on related patterns (frontend vs backend)
- Runs simultaneously → faster total execution
- More thorough coverage within each domain
- Reduces context usage in main conversation

**Fallback** (if subagent unavailable): Manual grep commands:
```bash
# State management
grep -r "useReducer\|create.*Store\|configureStore" --include="*.ts" --include="*.tsx" -l | head -3

# Data fetching
grep -r "useSWR\|useQuery\|createApi" --include="*.ts" --include="*.tsx" -l | head -3

# Error handling
grep -r "ErrorBoundary\|onError\|handleError" --include="*.ts" --include="*.tsx" -l | head -3
```

**After subagent returns**, read 1-2 representative files if more detail needed.

**Record findings** (will go into plan):
| Concern | Pattern Found | Example File |
|---------|---------------|--------------|
| State | [e.g., Zustand] | [file path] |
| Data fetching | [e.g., SWR] | [file path] |
| Error handling | [e.g., ErrorBoundary] | [file path] |
| Auth | [e.g., JWT middleware] | [file path] |
| Components | [e.g., feature folders] | [file path] |

**Iron rule:** Plan MUST use patterns found here. If codebase uses pattern X, plan uses pattern X. No exceptions without explicit justification.

---

### Step 3: Generate Implementation Plan

**Create plan file using Write tool**:

**Location**: `.shipkit/plans/active/[feature-name].json`

**Output format**: JSON (see `references/output-schema.md` for full schema, `references/example.json` for realistic example)

**During generation, apply these rules:**

1. **Existence Verification**: Before referencing ANY existing code ("use the UserService", "extend the auth middleware"):
   - Read or Grep to confirm it exists
   - If not found: add creation step to plan
   - Never assume code exists without verification

   **For multiple references** (3+ existing files/functions to verify), use Explore subagent:
   ```
   Task tool with subagent_type: "Explore"
   Prompt: "Verify these code artifacts exist and return their locations:
   1. [UserService or similar]
   2. [Auth middleware]
   3. [Error handler]
   For each: confirm exists (yes/no), file path, brief description of what it does."
   ```

2. **Granularity Check**: Each step must be:
   - Completable in < 2 hours
   - Have a clear done state
   - NOT be a project in disguise

   **Red flag phrases that need decomposition:**
   - "Implement authentication" → Break into: create token util, add middleware, add login endpoint, etc.
   - "Set up testing" → Break into: install deps, create first test file, add test script
   - "Add error handling" → Break into: create error boundary, add to layout, create error types
   - "Create API layer" → Break into: create fetch wrapper, add first endpoint, add types

3. **Consumption Requirement**: Every artifact created must have a consumer defined in the same plan.

4. **Permission Pre-declaration**: Track all actions that will need permission during implementation:
   - Count files to create vs modify
   - List bash commands that will run (tests, build, migrations)
   - Note any new dependencies to install
   - This populates the `permissions` object

**JSON Plan Structure:**

```json
{
  "$schema": "https://shipkit.io/schemas/plan.json",
  "type": "plan",
  "version": "1.0.0",
  "lastUpdated": "[ISO 8601 timestamp]",
  "source": "shipkit-plan",
  "plan": {
    "id": "plan-[feature-name]",
    "name": "[Feature Name]",
    "status": "ready",
    "specId": "spec-[feature-name]",
    "created": "[ISO 8601 timestamp]",
    "updated": "[ISO 8601 timestamp]",
    "overview": {
      "goal": "[1-2 sentence summary from spec]",
      "complexity": "[simple/medium/complex]"
    },
    "summary": {
      "phaseCount": 0,
      "taskCount": 0,
      "completionPercentage": 0,
      "filesCreated": 0,
      "filesModified": 0
    },
    "codebasePatterns": [
      {
        "concern": "[state/data-fetching/error-handling/auth]",
        "currentPattern": "[pattern name]",
        "sourceFile": "[example file path]",
        "planWillUse": "[same pattern]"
      }
    ],
    "phases": [
      {
        "id": "phase-1",
        "name": "[Phase Name]",
        "gate": {
          "condition": "[Specific testable condition]",
          "verification": "[Command or manual check]"
        },
        "tasks": [
          {
            "id": "1.1",
            "description": "[Specific actionable task]",
            "status": "pending",
            "dependencies": [],
            "creates": {
              "artifact": "[file path or function name]",
              "type": "[file/function/type/config/component/hook/api-endpoint/test/migration]"
            },
            "consumedBy": {
              "reference": "[file:function OR task ID OR 'entry-point']",
              "type": "[file/task/entry-point]"
            },
            "files": {
              "create": ["[paths]"],
              "modify": ["[paths]"]
            },
            "acceptanceCriteria": ["[criteria]"],
            "estimatedHours": 1.0
          }
        ]
      }
    ],
    "consumptionMap": [
      {
        "artifact": "[artifact name]",
        "type": "[artifact type]",
        "consumedBy": "[consumer]",
        "verified": true
      }
    ],
    "specCoverage": [
      {
        "requirement": "[requirement from spec]",
        "taskIds": ["1.1", "1.2"],
        "covered": true
      }
    ],
    "files": {
      "create": [
        { "path": "[path]", "purpose": "[purpose]" }
      ],
      "modify": [
        { "path": "[path]", "changes": "[what changes]" }
      ]
    },
    "permissions": {
      "createFiles": ["[paths]"],
      "modifyFiles": ["[paths]"],
      "commands": ["npm run dev", "npm run test"],
      "database": [],
      "dependencies": []
    },
    "decisions": [
      {
        "decision": "[what was decided]",
        "rationale": "[why this choice]",
        "alternatives": ["[alternative 1]", "[alternative 2]"]
      }
    ],
    "risks": [
      {
        "risk": "[risk description]",
        "likelihood": "[low/medium/high]",
        "impact": "[low/medium/high]",
        "mitigation": "[how to mitigate]"
      }
    ],
    "openQuestions": [
      {
        "question": "[open question]",
        "impact": "[how it affects plan]",
        "resolution": "[blocking/can-proceed/resolved]",
        "owner": "[who should resolve]"
      }
    ],
    "validation": {
      "consumption": { "creates": 0, "consumed": 0, "orphans": 0, "passed": true },
      "granularity": { "totalSteps": 0, "oversized": 0, "passed": true },
      "existence": { "references": 0, "verified": 0, "passed": true },
      "phaseGates": { "totalPhases": 0, "testableGates": 0, "passed": true },
      "specCoverage": { "totalRequirements": 0, "mapped": 0, "passed": true },
      "patternAlignment": { "aligned": true, "divergences": 0, "justified": true, "passed": true },
      "permissions": { "newFiles": 0, "modifiedFiles": 0, "commands": 0, "passed": true },
      "status": "valid"
    }
  }
}
```

**Gate quality rules** (never use vague gates):
- Bad: "Setup complete" → Good: "`npm run dev` starts without errors"
- Bad: "Core done" → Good: "User can see login form at /login"
- Bad: "It works" → Good: "Token appears in localStorage after successful login"

**Why this matters**: Approving the plan pre-grants permission categories in `permissions`, avoiding constant prompts during implementation. User sees full scope upfront.

---

### Step 3.5: Plan Validation Gate (CRITICAL - Do Not Skip)

**Before outputting plan, run all validation checks.**

#### Check 1: Consumption Tracing (Prevents Orphaned Foundations)

Review Consumption Map:
- [ ] Every "Creates" has specific artifact (not vague like "setup")
- [ ] Every "Consumed By" references specific location (file:function) or step (Phase X.Y)
- [ ] Zero rows have empty or vague "Consumed By"

**If orphan found**:
- Option A: Add a step that consumes the artifact
- Option B: Remove the creation step (it's not needed)
- Option C: The artifact is an entry point (API endpoint, CLI command, UI page) - mark as "Entry point"

**Never proceed with orphans.**

#### Check 2: Granularity Validation (Prevents Magical Steps)

Review every step:
- [ ] Each step completable in < 2 hours
- [ ] Each step has clear, unambiguous done state
- [ ] No step is a project disguised as a task

**Red flags to find and decompose:**
- "Implement [feature]" - What specific files/functions?
- "Set up [system]" - What specific configuration steps?
- "Add [broad capability]" - What specific components?
- "Create [layer]" - What specific modules?

**If oversized step found**: Decompose into 2-5 specific sub-steps.

#### Check 3: Existence Verification (Prevents Dependency Assumptions)

Review every reference to existing code:
- [ ] File paths verified via Read or Grep during Step 3
- [ ] If file not found, creation step added to plan
- [ ] No assumptions about existing code structure

**Common dangerous assumptions:**
- "Extend the existing UserService" - Does UserService exist?
- "Add to the utils folder" - Is there a utils folder? What's the pattern?
- "Use the auth middleware" - Does auth middleware exist? Where?

**If unverified reference found**: Verify now or add creation step.

#### Check 4: Phase Gate Quality (Prevents Missing Checkpoints)

Review Phase Gates Summary:
- [ ] Every phase has a gate
- [ ] Every gate is testable (can run command or check specific behavior)
- [ ] No vague gates ("done", "complete", "works")

**Gate test**: Could a different developer verify this gate passed? If no, make it more specific.

#### Check 5: Spec Coverage (Prevents Incomplete Plans)

Review Spec Coverage Map:
- [ ] Every requirement from spec has at least one plan step
- [ ] No spec requirements left unmapped
- [ ] Coverage is genuine (step actually addresses requirement, not just tangentially related)

**If gap found**:
- Add missing steps
- Or flag that spec requirement is out of scope (explicit decision)

#### Check 6: Pattern Alignment (Prevents Codebase Blindness)

Review Codebase Patterns table:
- [ ] Every "Plan Will Use" matches "Current Pattern"
- [ ] If diverging, explicit justification provided
- [ ] No training-data patterns introduced without verification

**Validation output** (populate in plan's `validation` object):
```json
"validation": {
  "consumption": { "creates": X, "consumed": X, "orphans": 0, "passed": true },
  "granularity": { "totalSteps": X, "oversized": 0, "passed": true },
  "existence": { "references": X, "verified": X, "passed": true },
  "phaseGates": { "totalPhases": X, "testableGates": X, "passed": true },
  "specCoverage": { "totalRequirements": X, "mapped": X, "passed": true },
  "patternAlignment": { "aligned": true, "divergences": 0, "justified": true, "passed": true },
  "permissions": { "newFiles": X, "modifiedFiles": X, "commands": X, "passed": true },
  "status": "valid"
}
```

**If ANY check fails**: Fix before proceeding. Set `status` to `"invalid"` if plan has known failures.

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it via `/shipkit-architecture-memory`

---

### Step 5: Suggest Next Step

**Output to user**:
- Plan location
- Summary: X phases, Y steps, Z files to create/modify
- Validation status (all checks passing)
- Next action: "Ready to implement - start with Phase 1"

---

## Completion Checklist

Copy and track:
- [ ] Read spec from `.shipkit/specs/active/`
- [ ] Completed codebase pattern scan
- [ ] Created plan with all required sections
- [ ] Consumption map has zero orphans
- [ ] All steps are granular (< 2 hours each)
- [ ] All existing code references verified
- [ ] All phases have testable gates
- [ ] All spec requirements mapped to steps
- [ ] Pattern alignment confirmed
- [ ] Saved to `.shipkit/plans/active/[name].json`

---

## What Makes This Plan Robust

**Failure modes prevented:**

| Failure Mode | Prevention Mechanism |
|--------------|---------------------|
| Orphaned foundations | Consumption Map + Check 1 |
| Magical steps | Granularity rules + Check 2 |
| Codebase blindness | Pattern Scan (Step 2.7) + Check 6 |
| Dependency assumptions | Existence Verification + Check 3 |
| Missing checkpoints | Phase Gates + Check 4 |
| Incomplete coverage | Spec Coverage Map + Check 5 |

**What's NOT included** (vs full design doc):
- Research phase (no unknowns investigation)
- API contracts (OpenAPI/GraphQL schemas)
- Detailed data model design
- Performance benchmarks
- Security threat modeling

**Philosophy**: Validated plan that catches common failures, not exhaustive design doc.

---

## The Iron Laws

**LAW 1: PLANS ANSWER "HOW", NOT "WHY" OR "WHAT"**
- Plan assumes spec defined "what" and "why"
- If questioning WHAT to build → Go back to `/shipkit-spec`

**LAW 2: NO ORPHANS**
- Every artifact created must be consumed
- If nothing uses it, don't create it

**LAW 3: NO MAGIC**
- Every step must be specific and actionable
- If you can't explain exactly what to do, decompose further

**LAW 4: VERIFY, DON'T ASSUME**
- Before referencing existing code, prove it exists
- Before proposing a pattern, check what codebase uses

**LAW 5: GATES MUST BE TESTABLE**
- If you can't verify a phase is complete, the gate is bad
- Another developer should be able to check the gate

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` - Creates feature specification (required)
- `/shipkit-project-context` - Generates stack.json, schema.json
- `/shipkit-architecture-memory` - Logs past decisions
- `/shipkit-prototyping` - Creates UI prototypes (if UI-heavy)

### After This Skill
- `implement (no skill needed)` - Executes the plan
- `/shipkit-architecture-memory` - Logs significant decisions (optional)
- `/shipkit-verify` - Validates implementation matches plan

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit/specs/active/[feature].json` - Feature requirements
- `.shipkit/stack.json` - Tech stack info

**Scans** (for pattern detection):
- Existing source files matching patterns (state, fetch, error, auth)

**Conditionally reads**:
- `.shipkit/architecture.json` - Past decisions
- `.shipkit/contracts.json` - Type definitions
- `.shipkit/schema.json` - Database schema

---

## Context Files This Skill Writes

**Creates**:
- `.shipkit/plans/active/[feature].json` - Validated implementation plan (JSON format)

**JSON Schema**: See `references/output-schema.md` for full schema definition.

**Example**: See `references/example.json` for a realistic implementation plan.

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**: Each plan is feature-specific and tied to a single spec. If user re-plans the same feature, they want a fresh plan based on current context.

**Never modifies**: Specs, stack, architecture (read-only)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Plan saved to `.shipkit/plans/active/`
2. **Validation** - All 6 checks passing
3. **Prerequisites** - Implementation can start with Phase 1

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Plan is complete when:
- [ ] Codebase pattern scan completed
- [ ] All implementation steps identified with Creates/Consumed By
- [ ] Consumption map has zero orphans
- [ ] All steps are granular (< 2 hours)
- [ ] All existing code references verified
- [ ] Every phase has testable gate
- [ ] Every spec requirement maps to step(s)
- [ ] Patterns align with codebase
- [ ] Implementation permissions declared (files, commands, deps)
- [ ] Validation summary shows all checks passing
<!-- /SECTION:success-criteria -->

---

**Remember**: A validated plan catches failures before they happen. The 15 minutes spent on validation saves hours of rework from orphaned foundations, missing pieces, and codebase conflicts.
