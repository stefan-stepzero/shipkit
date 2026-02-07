---
name: shipkit-spec
description: "Use when user describes a feature to build. Triggers: 'spec this', 'create specification', 'define requirements', 'I want to build'."
argument-hint: "<feature name or description>"
model: opus
agent: shipkit-product-owner-agent
---

# shipkit-spec - Lightweight Feature Specification

**Purpose**: Transform feature descriptions into structured JSON specifications with Given/When/Then scenarios and comprehensive edge case coverage, creating clear acceptance criteria for implementation.

**Output format**: JSON -- structured data readable by Claude, renderable by mission control dashboard, and queryable by other skills.

---

## When to Invoke

**User triggers**:
- "Spec this feature"
- "Create a specification"
- "What are the requirements?"
- "Define the feature properly"
- User describes a new feature idea

**Before**:
- `/shipkit-plan` (this creates the spec that planning needs)
- `implement (no skill needed)` (need spec before implementing)

**Workflow position**:
- After feature concept is clear
- Before implementation planning
- Can be used standalone for requirement clarification

---

## Prerequisites

**Recommended**:
- Stack defined: `.shipkit/stack.json` (to understand tech constraints)
- Schema defined: `.shipkit/schema.json` (to understand data model)

**Optional but helpful**:
- Architecture decisions: `.shipkit/architecture.json`
- Existing specs: `.shipkit/specs/active/*.json` (check for similar patterns)

**If missing**: Ask user basic questions about tech stack and data instead

---

## Process

### Step 1: Understand the Feature

**Before generating anything**, use AskUserQuestion tool to gather requirements:

**Question 1 - Feature Type:**
```
header: "Type"
question: "What type of feature are you specifying?"
options:
  - label: "User-facing UI"
    description: "Forms, dashboards, navigation, visual components"
  - label: "API/Backend"
    description: "Endpoints, services, data processing"
  - label: "Integration"
    description: "Third-party services, webhooks, external APIs"
  - label: "Infrastructure"
    description: "Auth, caching, database changes"
```

**Question 2 - Complexity:**
```
header: "Scope"
question: "How complex is this feature?"
options:
  - label: "Simple (Recommended)"
    description: "Single component/endpoint, minimal state"
  - label: "Medium"
    description: "Multiple components, some state management"
  - label: "Complex"
    description: "Cross-cutting concerns, significant architecture"
```

**If user selects "Other"**: Follow up with clarifying questions about their specific needs.

**Why ask first**: Avoid generating wrong spec based on assumptions.

---

### Step 2: Read Existing Context

**USE PARALLEL READS FOR CONTEXT LOADING** - All context files are independent:

```
Read these files IN PARALLEL (single message, multiple tool calls):

1. Read: .shipkit/stack.json         # Tech constraints
2. Read: .shipkit/schema.json      # Data model
3. Read: .shipkit/architecture.json  # Past decisions
4. Glob + Read: .shipkit/specs/active/*.json  # Similar specs
```

**Why parallel**: All 4 reads are independent - no file depends on another. Parallel reads reduce context loading time by ~40%.

**Token budget**: Keep context reading under 1500 tokens total.

**If files don't exist**: Proceed without them, ask user about tech/data as needed.

---

### Step 3: Explore Affected Code

**Before writing a spec, understand the actual codebase that will change.**

Specs written without reading source code miss existing patterns, hidden constraints, and ripple effects. This step ensures the spec is grounded in reality.

**3a. Identify code areas** — From the feature description + context files, determine:
- Which files/modules will be directly modified or created?
- What naming patterns, conventions, or abstractions exist in those areas?

**3b. Launch explore agents** — Use the Task tool with `subagent_type: Explore` to investigate:

```
Agent 1 - Direct code: "Find and summarize the code directly related to
[feature area]. Look for existing patterns, data structures, API signatures,
and component interfaces. Report: what exists today, what patterns are used,
what constraints the existing code imposes."

Agent 2 - Ripple effects: "Find code that depends on or interacts with
[feature area]. Look for callers, consumers, imports, tests, shared state,
and integration points. Report: what other code would be affected by changes,
what contracts exist that must be preserved."
```

**Launch both agents in parallel** — they are independent searches.

**3c. Synthesize findings** — Before generating the spec, note:
- Existing patterns the spec should follow or explicitly deviate from
- Integration points and contracts the spec must preserve
- Hidden complexity the user's description didn't mention
- Test coverage that already exists and would need updating

**If exploration reveals surprises**: Surface them to the user before proceeding. Example: *"The codebase already has a partial implementation of X using pattern Y — should the spec build on that or replace it?"*

**Token budget**: Each explore agent should return a focused summary (~500 tokens). Don't dump raw code into context — summarize patterns and constraints.

**When to skip**: If the feature is entirely greenfield (no existing related code), or the user explicitly says "I know the codebase, just spec it", this step can be abbreviated to a quick Glob search to confirm there's nothing unexpected.

---

### Step 4: Generate Specification

**Create spec file using Write tool**:

**Location**: `.shipkit/specs/active/{feature-name}.json`

**Use kebab-case for filename**: `recipe-sharing.json`, `user-authentication.json`

**JSON Schema**: See `references/output-schema.md` for complete schema definition

**Example**: See `references/example.json` for realistic feature spec

---

### Step 5: Validate Completeness

**Before saving spec, verify**:

- [ ] User story has `as`, `iWant`, `soThat` fields
- [ ] At least 2-3 scenarios with Given/When/Then structure
- [ ] ALL 6 core edge case categories have entries (+ External Service Constraints if feature uses external APIs)
- [ ] Must Have / Should Have / Won't Have prioritization
- [ ] Technical notes include database/API changes
- [ ] Test strategy identifies call flows and coverage
- [ ] Key test cases mapped from scenarios
- [ ] Summary counts match actual array lengths

---

### Step 6: Save and Suggest Next Step

**Use Write tool to create**: `.shipkit/specs/active/{feature-name}.json`

**Output to user**:
```
Specification created

Location: .shipkit/specs/active/{feature-name}.json

Summary:
  - [X] core scenarios
  - [Y] edge cases identified across 6+ categories
  - [Z] acceptance criteria (must/should/won't)
  - [N] key test cases mapped

Completeness:
  - User story: done
  - Scenarios (Given/When/Then): done
  - Edge cases: done (all core categories + external-service if applicable)
  - Acceptance criteria: done
  - Test strategy: done

```

---

## Completion Checklist

Copy and track:
- [ ] Asked 2-3 clarifying questions
- [ ] Explored affected code (direct + ripple effects)
- [ ] Surfaced surprises to user before speccing
- [ ] Created spec with Given/When/Then scenarios
- [ ] Applied all 6 core edge case categories (+ external-service if applicable)
- [ ] Defined test strategy (call flows, coverage, mocking)
- [ ] Mapped key test cases from scenarios
- [ ] Saved to `.shipkit/specs/active/{name}.json`

---

## JSON Output Structure

**Every spec MUST follow the Shipkit artifact convention:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "spec",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-spec",

  "summary": {
    "name": "Feature Name",
    "status": "active",
    "featureType": "user-facing-ui",
    "complexity": "medium",
    "scenarioCount": 3,
    "acceptanceCriteriaCount": 10,
    "edgeCasesApplied": ["loading", "error", "empty", "permission", "boundary", "consistency", "external-service"]
  },

  "metadata": {
    "id": "spec-feature-name",
    "created": "2025-01-15",
    "updated": "2025-01-15",
    "author": "shipkit-spec"
  },

  "problem": {
    "statement": "Clear problem statement",
    "userStory": {
      "as": "user type",
      "iWant": "to do something",
      "soThat": "I get some benefit"
    }
  },

  "scenarios": [
    {
      "id": "scenario-1",
      "name": "Primary happy path",
      "type": "happy-path",
      "given": ["Initial state 1", "Initial state 2"],
      "when": "User action",
      "then": ["Expected outcome 1", "Expected outcome 2"]
    }
  ],

  "edgeCases": {
    "loading": ["Loading consideration 1"],
    "error": ["Error handling 1"],
    "empty": ["Empty state 1"],
    "permission": ["Permission check 1"],
    "boundary": ["Boundary condition 1"],
    "consistency": ["Data consistency 1"]
  },

  "acceptanceCriteria": {
    "mustHave": ["Critical requirement 1"],
    "shouldHave": ["Nice to have 1"],
    "wontHave": ["Explicitly excluded 1"]
  },

  "outOfScope": ["What is NOT included"],

  "dependencies": ["What must be in place first"],

  "technical": {
    "databaseChanges": ["Table/field additions"],
    "apiEndpoints": [
      { "method": "POST", "path": "/api/resource", "purpose": "Create resource" }
    ],
    "existingCode": {
      "directlyAffected": ["src/path/to/file.ts — description of what exists and how it changes"],
      "rippleEffects": ["src/path/to/consumer.ts — depends on X, must update Y"],
      "patternsToFollow": ["Existing codebase uses pattern Z for similar features"],
      "contractsToPreserve": ["API signature of functionA() is consumed by 3 callers"]
    },
    "notes": ["Implementation hints"]
  },

  "testStrategy": {
    "callFlows": ["User -> Component -> API -> DB -> Response"],
    "coverage": [
      { "layer": "Business logic", "testType": "Unit", "whatToTest": "..." }
    ],
    "mocking": {
      "mock": ["External services"],
      "testDoubles": ["Database"],
      "real": ["Fast internal services"]
    },
    "keyTestCases": [
      { "scenario": "Happy path", "testType": "Integration", "testName": "should..." }
    ]
  },

  "references": {
    "stack": ".shipkit/stack.json",
    "schema": ".shipkit/schema.json",
    "architecture": ".shipkit/architecture.json",
    "relatedSpecs": []
  },

  "nextSteps": ["/shipkit-plan to create implementation plan"]
}
```

**Full schema**: See `references/output-schema.md`
**Example**: See `references/example.json`

---

## Edge Case Categories

**Apply ALL 6 core categories to EVERY feature (+ External Service Constraints when feature involves external APIs):**

### Loading States
- Show spinner/skeleton during initial load
- Disable UI controls during async operations
- Handle timeout scenarios (>5 seconds)
- Prevent duplicate submissions (double-click)

### Error States
- Network failure during operation
- Server error (500)
- Validation errors
- Permission errors (401/403)

### Empty/Missing States
- No data available
- Search with no results
- Deleted/missing resource
- First-time user experience

### Permission States
- Unauthenticated user access
- Authenticated but unauthorized
- Role-based restrictions
- Ownership checks

### Boundary Conditions
- Minimum values (0, empty string, null)
- Maximum values (string length, array size)
- Rate limits
- Quota/usage limits

### Data Consistency
- Stale data refresh
- Partial updates
- Cache invalidation
- Concurrent access conflicts

### External Service Constraints (when feature uses external APIs)
- Timeout budget per call and cumulative across chains
- Resource limits (max tokens, payload size, file size caps)
- Platform execution limits (serverless duration vs total call time)
- Cost bounds (per-call cost, per-user quotas, spending alerts)
- Rate limits from the provider (429 handling, backoff strategy)
- Service degradation (what happens when the external service is slow or down?)

**See `references/best-practices.md` for frontend and backend quality standards.**

---

## What Makes This "Lite"

**Included**:
- Structured JSON output for dashboard rendering
- Given/When/Then scenarios (clear, actionable)
- Comprehensive edge case checklist (6 core + 1 conditional category)
- Acceptance criteria with prioritization
- Technical notes for context
- Test strategy (call flows, coverage, key test cases)
- Moves to implemented/ folder when done

**Not included** (vs full /dev-specify):
- Formal Cucumber/Gherkin syntax
- Automated test generation
- BDD framework integration
- Extensive examples library
- Multi-stakeholder review workflow

**Philosophy**: Clear enough to implement correctly, concise enough to read quickly. JSON format enables dashboard visualization and programmatic access.

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-project-context` - Generates stack.json and schema.json
  - **When**: Project initialization or when stack/schema missing
  - **Why**: Spec needs tech constraints and data model context
  - **Trigger**: Missing stack.json or schema.json detected during spec creation

- **User describes feature idea** - Provides initial feature concept
  - **When**: User has new feature to build
  - **Why**: Can't spec what hasn't been described
  - **Trigger**: User says "I want to add..." or "spec this feature"

### After This Skill

- `/shipkit-plan` - Creates implementation plan from spec
  - **When**: Spec is complete and approved
  - **Why**: Spec defines WHAT to build, plan defines HOW
  - **Trigger**: Spec saved to specs/active/, user confirms "ready to plan"

- `/shipkit-prototyping` - Creates rapid UI mockup
  - **When**: Spec includes significant UI/UX components (optional step)
  - **Why**: Validate UI direction before committing to full implementation
  - **Trigger**: User wants to see UI mockup before building real code

- `/shipkit-architecture-memory` - Logs architectural decisions made during spec
  - **When**: Spec reveals architectural choices (optional step)
  - **Why**: Document tech decisions for future reference
  - **Trigger**: Spec's technical notes reveal important architectural choice

---

## Context Files This Skill Reads

**Recommended** (read if exist):
- `.shipkit/stack.json` - Tech stack constraints
- `.shipkit/schema.json` - Data model
- `.shipkit/architecture.json` - Past decisions

**Optional** (read if relevant):
- `.shipkit/specs/active/*.json` - Check for similar specs

**If missing**: Ask user for needed context

---

## Context Files This Skill Writes

**Write Strategy: CREATE (with ARCHIVE on completion)**

**Creates**:
- `.shipkit/specs/active/{feature-name}.json` - New specification

**Update Behavior**:
- Active specs can be modified during planning/implementation (overwrites previous version)
- Each update REPLACES the file contents completely
- No version history maintained in active/ folder

**Archive Behavior** (when feature complete):
- Moves: `.shipkit/specs/active/{feature-name}.json` -> `.shipkit/specs/implemented/{feature-name}.json`
- Updates `status` field from `"active"` to `"implemented"`
- Adds completion metadata (implemented date)
- Archived specs become read-only historical records
- Moving specs: Either manual or via `/shipkit-verify` when feature ships

**Why CREATE with ARCHIVE:**
- Specs are living documents during development (can be refined)
- Each feature gets its own independent file (not appending to shared file)
- History preserved by moving completed specs to implemented/ folder
- JSON format enables dashboard visualization

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-spec` or describes feature
2. shipkit-master tells Claude to read this SKILL.md
3. Claude asks 2-3 clarifying questions
4. Claude reads stack.json + schema.json (~500 tokens)
5. Claude optionally reads architecture.json if relevant (~300 tokens)
6. Claude launches explore agents to examine affected code + ripple effects (~1000 tokens from summaries)
7. Claude surfaces surprises to user, then generates spec
8. Total context loaded: ~2000-2500 tokens (focused)

**Not loaded unless needed**:
- Other specs (unless checking for similar patterns)
- Plans
- Implementations
- User tasks

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Spec is complete when:
- [ ] JSON file conforms to Shipkit artifact convention ($schema, type, version, lastUpdated, source, summary)
- [ ] Codebase explored: directly affected files and ripple effects identified
- [ ] Existing patterns and contracts documented in `technical.existingCode`
- [ ] User story has `as`, `iWant`, `soThat` fields
- [ ] 2-3 scenarios with Given/When/Then structure
- [ ] All 6 core edge case categories have entries (+ external-service if applicable)
- [ ] Acceptance criteria prioritized (Must/Should/Won't)
- [ ] Technical notes include DB/API changes
- [ ] Test strategy identifies call flows and coverage approach
- [ ] Key test cases mapped from scenarios
- [ ] File saved to `.shipkit/specs/active/{name}.json`
<!-- /SECTION:success-criteria -->
---

## Reference Documentation

**For detailed patterns and examples:**

- **JSON schema** - `references/output-schema.md`
  - Complete field reference
  - Validation rules
  - Status lifecycle

- **Example spec** - `references/example.json`
  - Realistic feature specification
  - All fields populated with sample data

- **Best practices** - `references/best-practices.md`
  - Frontend best practices (state management, user feedback, accessibility, performance, security, forms, navigation)
  - Backend best practices (input validation, auth, error handling, data integrity, security, performance, API design)
  - Quick checklist for spec review

---

**Remember**: This is a lightweight spec for POC/MVP work. Get enough clarity to build correctly, but don't over-specify. JSON format enables dashboard rendering and programmatic access. Ship, learn, iterate.
