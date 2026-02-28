---
name: shipkit-product-definition
description: "Define what to build — features, UX patterns, and differentiators that solve discovered user needs. Triggers: 'product definition', 'what to build', 'features', 'solution design'."
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

# shipkit-product-definition — Product Blueprint

Defines WHAT we build to solve discovered user needs. Reads product-discovery.json (pain points, personas, opportunities) and produces a product blueprint: features, UX patterns, and differentiators.

This is the product blueprint — it defines the user-facing solution. The technical approach (mechanisms, design decisions, stack) is handled by `/shipkit-engineering-definition`. Feature phasing (what to build now vs. later) is handled by `/shipkit-goals` through stage gates.

---

## When to Invoke

**User triggers**:
- "What should we build?", "Define features", "Product definition"
- "UX patterns", "Differentiators", "What to build"
- "Solution design", "Product blueprint"

**Workflow position**:
- After `/shipkit-product-discovery` (needs discovered user needs)
- Before `/shipkit-engineering-definition` (engineering designs mechanisms for these features)
- Before `/shipkit-goals` (goals derive criteria from features and mechanisms)

---

## Prerequisites

**Required** (fail gracefully if missing):
- `.shipkit/product-discovery.json` — who the users are and what they need

**Recommended** (enrich the proposal):
- `.shipkit/why.json` — project purpose and stage

**Optional** (for existing projects):
- `.shipkit/stack.json` — technology constraints (informs feasibility)
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

If `.shipkit/product-discovery.json` exists, attempt to propose a solution without asking:

1. Read `.shipkit/product-discovery.json` (pain points, personas, opportunities)
2. Read `.shipkit/why.json` if exists (vision, stage, constraints)
3. For each major pain point, propose features that address it
4. For each feature, identify UX patterns that support it
5. Present the proposal as a Problem → Feature → UX flow:

```
Based on discovered user needs, here's a proposed product:

Pain: [pain point from discovery]
  → Feature: [what users interact with]
    → UX: [how they experience it]

Pain: [another pain point]
  → Feature: [user-facing capability]
    → UX: [interaction pattern]

Differentiators: [what makes this unique]

Confirm, adjust, or switch to interactive mode?
```

6. If confirmed → proceed to Step 4 (differentiators) with the proposed data
7. If adjusted → incorporate changes, proceed to Step 4
8. If interactive requested → fall through to Step 1

If `.shipkit/product-discovery.json` does NOT exist → fail with message to run discovery first.

---

### Step 1: Gather Context

**Read these files:**

```
.shipkit/product-discovery.json  → pain points, personas, opportunities (REQUIRED)
.shipkit/why.json                → vision, stage, constraints (RECOMMENDED)
.shipkit/stack.json              → tech capabilities (OPTIONAL — feasibility check)
```

**Multi-user detection**: If discovery has 2+ personas with distinct `primaryIntent` values, this is a multi-user product. Flag this upfront and ensure each feature explicitly maps to the persona(s) it serves via `addressesNeeds` tracing back through pain points.

---

### Step 2: Define Features

For each major user need/pain point from discovery, define features:

**Use AskUserQuestion tool:**

```
header: "Features"
question: "For [pain point], what should users be able to do?"
options:
  - label: "[Proposed feature from context]"
    description: "Based on the pain point and opportunities"
  - label: "Different feature"
    description: "I have another idea"
```

For each feature:
1. **Name** — concise feature name
2. **Description** — 1-2 sentences on what it does from the user's perspective
3. **Addresses needs** — which pain point IDs from discovery
4. **Dependencies** — which other feature IDs must exist first

**Feature count guidance**:
- POC: 2-3 features
- MVP: 3-6 features
- Growth: 5-10 features

**Note**: Feature phasing (now/next/later) is handled by `/shipkit-goals` through stage gates. This skill defines WHAT exists, not WHEN it ships.

---

### Step 3: Define UX Patterns

Based on the features, identify the key interaction patterns:

```
header: "UX Patterns"
question: "How should users interact with [feature]?"
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

Based on features and UX patterns, articulate what makes this product unique:

- What do competitors do differently?
- What combination of features/patterns creates unique value?
- What would be hard to replicate?

Capture 1-3 differentiator statements, each tied to the features or patterns that enable it.

---

### Step 5: Present Blueprint and Confirm

Present the full product blueprint:

**View 1: Product Design**
```
## Product Blueprint: [Product Name]

### Problem Space
[Summary from discovery — key pain points and personas]

### Features (ordered by dependency)
1. F-001: [Name] — [description]
   Addresses: [pain points]
2. F-002: [Name] — [description]

### UX Patterns
1. P-001: [Name] — [description]
2. P-002: [Name] — [description]

### Differentiators
- D-001: [statement] (enabled by F-001 + P-002)
```

**View 2: Feature Map**
```
### Feature → UX Pattern Map

  F-001: [Name] — patterns: P-001 | deps: none | addresses: pain-1
  F-002: [Name] — patterns: P-001, P-002 | deps: F-001 | addresses: pain-2
  F-003: [Name] — patterns: P-003 | deps: F-002 | addresses: pain-1, pain-3
```

Then ask: **"Confirm this product blueprint, or adjust?"**

User can:
- Confirm as-is
- Add/remove/modify features or patterns
- Change differentiators

Incorporate adjustments and re-present if changed significantly.

---

### Step 6: Write Product Definition

After confirmation, write `.shipkit/product-definition.json`.

See [Product Definition JSON Schema](#product-definition-json-schema) below.

---

### Step 7: Suggest Next Steps

```
Product blueprint written to .shipkit/product-definition.json
Features: {N} | Patterns: {N} | Differentiators: {N}

Next:
  1. /shipkit-engineering-definition — Design the technical approach for these features
  2. /shipkit-goals — Define success criteria (after engineering definition)
  3. /shipkit-spec — Create specs for features (after goals)

Ready to design the engineering approach?
```

---

## Product Definition JSON Schema (Quick Reference)

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-definition",
  "version": "3.0",
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
  "solutionApproach": "High-level product approach to addressing discovered needs",
  "features": [
    {
      "id": "F-001",
      "name": "Feature name",
      "description": "What it does from user's perspective",
      "addressesNeeds": ["pain-1"],
      "patterns": ["P-001"],
      "dependencies": []
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
      "enabledBy": ["F-001", "P-001"]
    }
  ],
  "summary": {
    "totalFeatures": 0,
    "totalPatterns": 0,
    "totalDifferentiators": 0
  }
}
```

**Full schema reference**: See `references/output-schema.md`
**Realistic example**: See `references/example.json`

### Graph Relationships

The ID-based cross-references enable these graph traversals:

- **Feature -> Pain Points**: `features[].addressesNeeds` references `painPoints[].id` from product-discovery.json
- **Feature -> Patterns**: `features[].patterns` references `uxPatterns[].id`
- **UX Pattern -> Features**: `uxPatterns[].usedIn` references `features[].id`
- **Differentiator -> Features/Patterns**: `differentiators[].enabledBy` references feature and pattern IDs

---

## When $ARGUMENTS is Provided

If `$ARGUMENTS` contains text:
- **Product name/description**: Use as seed for product name and to focus the proposal
- **`--refresh`**: Start fresh even if product-definition.json exists

---

## When This Skill Integrates with Others

### Before This Skill
| Skill | Why |
|-------|-----|
| `shipkit-why-project` | Produces why.json — project purpose and stage |
| `shipkit-product-discovery` | Produces product-discovery.json — required input (user needs) |

### After This Skill
| Skill | How |
|-------|-----|
| `shipkit-engineering-definition` | Reads product-definition.json features — designs mechanisms for each feature |
| `shipkit-goals` | Reads product-definition.json to derive criteria from features and patterns |
| `shipkit-spec` | Reads product-definition.json features — one spec per feature |
| `shipkit-plan` | Indirectly — plans derive from specs which come from product-definition |

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-discovery.json` | User needs, pain points, personas | Route to `/shipkit-product-discovery` |
| `.shipkit/why.json` | Project purpose and stage | Proceed with user input |
| `.shipkit/stack.json` | Tech capabilities (feasibility check) | Proceed without |
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
2. **Prerequisites** - Does the next action need engineering definition or goals first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to define technical approach (`/shipkit-engineering-definition`), define success criteria (`/shipkit-goals`), or create detailed specs (`/shipkit-spec`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Product blueprint is complete when:
- [ ] Product-discovery.json read and problem space summarized
- [ ] Features defined, each addressing at least one pain point
- [ ] Every major pain point addressed by at least one feature
- [ ] 2-4 UX patterns defined with rationale
- [ ] 1-3 differentiators tied to features/patterns
- [ ] Features reference patterns by ID
- [ ] All cross-references use stable IDs (F-001, P-001, D-001)
- [ ] Summary counts match actual array lengths
- [ ] User confirmed the blueprint before writing
- [ ] File saved to `.shipkit/product-definition.json`
<!-- /SECTION:success-criteria -->

---

**Remember**: This skill captures the product design — WHAT you build to solve discovered needs. The technical approach (mechanisms, components, stack) is handled by `/shipkit-engineering-definition`. Feature phasing (now/next/later) is handled by `/shipkit-goals`. Update the blueprint as the product evolves.
