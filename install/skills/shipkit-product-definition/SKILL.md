---
name: shipkit-product-definition
description: "Design the solution blueprint — core mechanisms, UX patterns, differentiators, and MVP scope that define HOW we solve discovered user needs"
argument-hint: "[product name or focus area]"
context: fork
agent: shipkit-product-owner-agent
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# shipkit-product-definition — Solution Blueprint

Designs HOW we solve discovered user needs. Reads product-discovery.json (pain points, personas, opportunities) and produces a solution blueprint: core mechanisms, UX patterns, differentiators, design decisions, stack direction, MVP boundary, and features grounded in those mechanisms.

This is the product blueprint — everything downstream (goals, specs, architecture, plans, implementation) derives from it.

---

## When to Invoke

**User triggers**:
- "How should we solve this?", "Design the solution", "Solution blueprint"
- "Define features", "Product definition", "What to build"
- "Core approach", "How will it work?"

**Workflow position**:
- After `/shipkit-product-discovery` (needs discovered user needs)
- Before `/shipkit-goals` (goals derive success criteria from the blueprint)

---

## Prerequisites

**Required** (fail gracefully if missing):
- `.shipkit/product-discovery.json` — who the users are and what they need

**Recommended** (enrich the proposal):
- `.shipkit/why.json` — project purpose and stage
- `.shipkit/stack.json` — technology constraints and capabilities

**Optional** (for existing projects):
- `.shipkit/codebase-index.json` — what already exists

If product-discovery.json is missing, tell the user: "Run `/shipkit-product-discovery` first — I need to understand user needs before designing a solution." and stop.

---

## Process

### Step 0: Check for Existing File

1. Check if `.shipkit/product-definition.json` exists
2. If exists AND modified < 5 minutes ago: Show user, ask "Use this or regenerate?"
3. If exists AND modified > 5 minutes ago: Proceed to File Exists Workflow (Step 0b)
4. If doesn't exist: Skip to Step 1 (generate new)

**File Exists Workflow (Step 0b)**:
- Options: View / Update / Replace / Cancel
- View: Display current file, then ask what to do
- Update: Read existing, ask what to change, regenerate with updates
- Replace: Archive old version, generate completely new
- Cancel: Exit without changes

---

### Step 0c: Propose Mode (Context-Driven)

If `.shipkit/product-discovery.json` exists, attempt to propose a solution approach without asking:

1. Read `.shipkit/product-discovery.json` (pain points, personas, opportunities)
2. Read `.shipkit/why.json` if exists (vision, stage, constraints)
3. Read `.shipkit/stack.json` if exists (technology capabilities)
4. For each major pain point, propose a mechanism that addresses it
5. For each mechanism, identify UX patterns that support it
6. Present the proposal as a Problem → Mechanism → Feature flow:

```
Based on discovered user needs, here's a proposed solution:

Pain: [pain point from discovery]
  → Mechanism: [how we solve it]
    → Features: [what users interact with]

Pain: [another pain point]
  → Mechanism: [solution approach]
    → Features: [user-facing capabilities]

Differentiators: [what makes this unique]

Confirm, adjust, or switch to interactive mode?
```

7. If confirmed → proceed to Step 5 (MVP boundary) with the proposed data
8. If adjusted → incorporate changes, proceed to Step 5
9. If interactive requested → fall through to Step 1

If `.shipkit/product-discovery.json` does NOT exist → fail with message to run discovery first.

---

### Step 1: Gather Context

**Read these files:**

```
.shipkit/product-discovery.json  → pain points, personas, opportunities (REQUIRED)
.shipkit/why.json                → vision, stage, constraints (RECOMMENDED)
.shipkit/stack.json              → tech capabilities (RECOMMENDED)
.shipkit/codebase-index.json     → existing code (OPTIONAL)
```

**Multi-user detection**: If discovery has 2+ personas with distinct `primaryIntent` values, this is a multi-user product. Flag this upfront and ensure each mechanism, pattern, and feature explicitly maps to the persona(s) it serves via `addressesNeeds` tracing back through pain points.

---

### Step 2: Design Core Mechanisms

For each major user need/pain point from discovery, define a mechanism:

**Use AskUserQuestion tool:**

```
header: "Mechanisms"
question: "For [pain point], what's the core mechanism? How will the system solve this?"
options:
  - label: "[Proposed mechanism from context]"
    description: "Based on the pain point and opportunities"
  - label: "Different approach"
    description: "I have another idea"
```

For each mechanism, capture:
- **Name** — concise mechanism name
- **Description** — how it works at a conceptual level
- **Addresses needs** — which pain point IDs from discovery
- **Key design choices** — decisions made with rationale and alternatives

Aim for 2-4 mechanisms. Each should address at least one pain point. Every major pain point should be addressed by at least one mechanism.

---

### Step 3: Define UX Patterns

Based on the mechanisms, identify the key interaction patterns:

```
header: "UX Patterns"
question: "How should users interact with [mechanism]?"
options:
  - label: "[Proposed pattern]"
    description: "[Why this pattern fits]"
  - label: "Different pattern"
    description: "I have another UX approach in mind"
```

For each pattern, capture:
- **Name** — pattern name (e.g., "wizard flow", "live preview", "progressive disclosure")
- **Description** — how users experience it
- **Used in** — which features will use this pattern
- **Rationale** — why this pattern over alternatives

Aim for 2-4 patterns. Patterns can be shared across features.

---

### Step 4: Identify Differentiators

Based on mechanisms and patterns, articulate what makes this solution unique:

- What do competitors do differently?
- What combination of mechanisms/patterns creates unique value?
- What would be hard to replicate?

Capture 1-3 differentiator statements, each tied to the mechanisms or patterns that enable it.

---

### Step 5: Define MVP Boundary

**Use AskUserQuestion tool:**

```
header: "MVP Scope"
question: "Which of these should ship in v1?"
multiSelect: true
options:
  - label: "[Feature A]"
    description: "Uses [mechanism], addresses [pain point]"
  - label: "[Feature B]"
    description: "Uses [mechanism], addresses [pain point]"
  ...
```

Separate features into:
- **In scope (v1)** — minimum needed to validate the solution
- **Deferred (Phase 2+)** — valuable but not required for first validation

Capture rationale for the boundary.

---

### Step 6: Stack Direction (Greenfield Only)

**Skip if `.shipkit/stack.json` already exists.**

For greenfield projects, ask about technology direction:

```
header: "Stack"
question: "What tech direction for this solution?"
options:
  - label: "[Recommended stack based on mechanisms]"
    description: "[Why it fits the solution design]"
  - label: "Different stack"
    description: "I have preferences"
```

Capture:
- Recommended technologies (frontend, backend, database, hosting)
- Rationale tied to the solution design
- Constraints that drove the choice

---

### Step 7: Map Features

Based on mechanisms, patterns, and MVP boundary, define features:

For each feature:
1. **Name** — concise feature name
2. **Description** — 1-2 sentences on what it does
3. **Mechanisms** — which mechanism IDs this feature uses
4. **Patterns** — which UX pattern IDs this feature follows
5. **MVP** — boolean: ships in v1 or deferred
6. **Dependencies** — which other feature IDs must exist first

**Feature count guidance**:
- POC: 2-3 features
- MVP: 3-6 features
- Growth: 5-10 features

---

### Step 8: Present Blueprint and Confirm

Present the full solution blueprint:

**View 1: Solution Design**
```
## Solution Blueprint: [Product Name]

### Problem Space
[Summary from discovery — key pain points and personas]

### Solution Approach
[2-3 sentences on how we solve it]

### Core Mechanisms
1. M-001: [Name] — [description]
   Addresses: [pain points]
2. M-002: [Name] — [description]

### UX Patterns
1. P-001: [Name] — [description]
2. P-002: [Name] — [description]

### Differentiators
- D-001: [statement] (enabled by M-001 + P-002)

### MVP Boundary
In scope: [features]
Deferred: [features]
```

**View 2: Feature Map**
```
### Features (ordered by dependency)

MVP:
  F-001: [Name] — mechanisms: M-001 | patterns: P-001 | deps: none
  F-002: [Name] — mechanisms: M-001, M-002 | patterns: P-002 | deps: F-001

Deferred:
  F-004: [Name] — mechanisms: M-003 | patterns: P-001 | deps: F-002
```

Then ask: **"Confirm this solution blueprint, or adjust?"**

User can:
- Confirm as-is
- Add/remove/modify mechanisms, patterns, or features
- Adjust MVP boundary
- Change differentiators

Incorporate adjustments and re-present if changed significantly.

---

### Step 9: Write Product Definition

After confirmation, write `.shipkit/product-definition.json`.

See [Product Definition JSON Schema](#product-definition-json-schema) below.

---

### Step 10: Suggest Next Steps

```
Solution blueprint written to .shipkit/product-definition.json
Mechanisms: {N} | Patterns: {N} | Features: {N} ({N} MVP, {N} deferred)

Next:
  1. /shipkit-goals — Define success criteria for this solution
  2. /shipkit-spec — Create specs for MVP features
  3. /shipkit-architecture-memory — Log key architecture decisions

Ready to define success criteria?
```

---

## Product Definition JSON Schema (Quick Reference)

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-definition",
  "version": "2.0",
  "lastUpdated": "ISO timestamp",
  "source": "shipkit-product-definition",
  "product": {
    "name": "Product name",
    "vision": "One-line from why.json",
    "stage": "poc|mvp|production|scale"
  },
  "problemSpace": {
    "summary": "Brief summary of discovered user needs",
    "keyPainPoints": ["pain-1"],
    "primaryPersona": "persona-1",
    "personaIntents": {
      "persona-1": "Their primaryIntent from discovery",
      "persona-2": "Their primaryIntent (multi-user apps only)"
    }
  },
  "solutionApproach": "How the solution addresses discovered needs",
  "mechanisms": [
    {
      "id": "M-001",
      "name": "Mechanism name",
      "description": "What this does and how",
      "addressesNeeds": ["pain-1"],
      "designChoices": [
        { "decision": "Choice", "rationale": "Why", "alternatives": ["Rejected option"] }
      ]
    }
  ],
  "uxPatterns": [
    {
      "id": "P-001",
      "name": "Pattern name",
      "description": "How users interact with this",
      "usedIn": ["F-001"],
      "rationale": "Why this pattern"
    }
  ],
  "differentiators": [
    {
      "id": "D-001",
      "statement": "What makes this unique",
      "enabledBy": ["M-001", "P-001"]
    }
  ],
  "designDecisions": [
    {
      "decision": "Key choice",
      "rationale": "Why",
      "alternatives": ["What was considered"]
    }
  ],
  "stackDirection": {
    "recommended": { "frontend": "...", "backend": "...", "database": "...", "hosting": "..." },
    "rationale": "Why these choices",
    "constraints": ["Driving factors"],
    "note": "Only for greenfield. Skipped if stack.json exists."
  },
  "mvpBoundary": {
    "inScope": ["What ships in v1"],
    "deferred": ["Phase 2+"],
    "rationale": "Why this boundary"
  },
  "features": [
    {
      "id": "F-001",
      "name": "Feature name",
      "description": "What it does",
      "mechanisms": ["M-001"],
      "patterns": ["P-001"],
      "mvp": true,
      "dependencies": []
    }
  ],
  "summary": {
    "totalMechanisms": 0,
    "totalPatterns": 0,
    "totalDifferentiators": 0,
    "totalFeatures": 0,
    "mvpFeatures": 0,
    "deferredFeatures": 0
  }
}
```

**Full schema reference**: See `references/output-schema.md`
**Realistic example**: See `references/example.json`

### Graph Relationships

The ID-based cross-references enable these graph traversals:

- **Mechanism -> Pain Points**: `mechanisms[].addressesNeeds` references `painPoints[].id` from product-discovery.json
- **UX Pattern -> Features**: `uxPatterns[].usedIn` references `features[].id`
- **Feature -> Mechanisms**: `features[].mechanisms` references `mechanisms[].id`
- **Feature -> Patterns**: `features[].patterns` references `uxPatterns[].id`
- **Differentiator -> Mechanisms/Patterns**: `differentiators[].enabledBy` references mechanism and pattern IDs

---

## When $ARGUMENTS is Provided

If `$ARGUMENTS` contains text:
- **Product name/description**: Use as seed for product name and to focus the solution proposal
- **`--refresh`**: Start fresh even if product-definition.json exists
- **`--mvp`**: Focus only on MVP boundary review (Steps 5-6 only against existing definition)

---

## When This Skill Integrates with Others

### Before This Skill
| Skill | Why |
|-------|-----|
| `shipkit-why-project` | Produces why.json — project purpose and stage |
| `shipkit-product-discovery` | Produces product-discovery.json — required input (user needs) |
| `shipkit-project-context` | Produces stack.json — tech capabilities |

### After This Skill
| Skill | How |
|-------|-----|
| `shipkit-goals` | Reads product-definition.json to derive success criteria from the solution design |
| `shipkit-spec` | Reads product-definition.json features — one spec per feature |
| `shipkit-architecture-memory` | Reads product-definition.json for solution context in architecture decisions |
| `shipkit-plan` | Indirectly — plans derive from specs which come from product-definition |

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-discovery.json` | User needs, pain points, personas | Route to `/shipkit-product-discovery` |
| `.shipkit/why.json` | Project purpose and stage | Proceed with user input |
| `.shipkit/stack.json` | Tech capabilities and constraints | Ask about stack (greenfield) or proceed |
| `.shipkit/codebase-index.json` | Existing code for existing projects | Skip |
| `.shipkit/product-definition.json` | Previous definition (for update mode) | Generate new |

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

| File | When |
|------|------|
| `.shipkit/product-definition.json` | Created on first run, updated on subsequent runs |

**Archive location** (if replacing):
- `.shipkit/archive/product-definition/product-definition.[timestamp].json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need goals or a spec first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to define success criteria (`/shipkit-goals`), create detailed specs (`/shipkit-spec`), or log architecture decisions (`/shipkit-architecture-memory`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Solution blueprint is complete when:
- [ ] Product-discovery.json read and problem space summarized
- [ ] 2-4 mechanisms defined, each addressing at least one pain point
- [ ] Every major pain point addressed by at least one mechanism
- [ ] 2-4 UX patterns defined with rationale
- [ ] 1-3 differentiators tied to mechanisms/patterns
- [ ] Key design decisions captured with rationale
- [ ] MVP boundary explicitly defined with rationale
- [ ] Stack direction captured (greenfield only)
- [ ] Features reference mechanisms and patterns by ID
- [ ] All cross-references use stable IDs (M-001, P-001, F-001, D-001)
- [ ] Summary counts match actual array lengths
- [ ] User confirmed the blueprint before writing
- [ ] File saved to `.shipkit/product-definition.json`
<!-- /SECTION:success-criteria -->

---

**Remember**: This skill captures the solution design — HOW you solve discovered needs. It's the bridge between understanding users (discovery) and measuring success (goals). Update it as the solution evolves. The mechanism/pattern structure makes it easy to trace from user pain points through to features.
