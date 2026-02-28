---
name: shipkit-engineering-definition
description: "Define the technical approach — mechanisms, design decisions, stack direction, and component structure for building the product. Triggers: 'engineering approach', 'how to build this', 'technical design', 'mechanisms'."
argument-hint: "[focus area or --refresh]"
context: fork
agent: shipkit-architect-agent
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# shipkit-engineering-definition — Technical Approach

Defines HOW we build the product defined in product-definition.json. For each feature, designs the technical mechanisms, captures design decisions, recommends stack direction (greenfield), and defines component structure.

This is the engineering blueprint — it takes the product's features and UX patterns and defines the technical approach to implement them. Downstream skills (goals, architecture-memory, spec) read both product-definition.json and engineering-definition.json.

---

## When to Invoke

**User triggers**:
- "How should we build this?", "Technical approach", "Engineering design"
- "Define mechanisms", "Component structure", "Technical decisions"
- "Stack direction", "What technologies?"

**Workflow position**:
- After `/shipkit-product-definition` (needs features and UX patterns)
- Before `/shipkit-goals` (goals derive criteria from mechanisms)

---

## Prerequisites

**Required** (fail gracefully if missing):
- `.shipkit/product-definition.json` — features, UX patterns, differentiators

**Recommended** (enrich the proposal):
- `.shipkit/why.json` — project purpose and stage
- `.shipkit/stack.json` — existing technology constraints
- `.shipkit/product-discovery.json` — pain points for traceability

**Optional** (for existing projects):
- `.shipkit/codebase-index.json` — existing code structure

If product-definition.json is missing, tell the user: "Run `/shipkit-product-definition` first — I need to know what features to design mechanisms for." and stop.

---

## Process

### Step 0: Check for Existing File

1. Check if `.shipkit/engineering-definition.json` exists
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

If `.shipkit/product-definition.json` exists, attempt to propose a technical approach without asking:

1. Read `.shipkit/product-definition.json` (features, UX patterns, differentiators)
2. Read `.shipkit/why.json` if exists (vision, stage, constraints)
3. Read `.shipkit/stack.json` if exists (technology capabilities)
4. Read `.shipkit/product-discovery.json` if exists (pain points)
5. For each feature, propose the technical mechanism to implement it
6. Present the proposal as a Feature → Mechanism → Components flow:

```
Based on the product definition, here's a proposed technical approach:

Feature: [feature from product-definition]
  → Mechanism: [how we build it technically]
    → Components: [modules/services involved]

Feature: [another feature]
  → Mechanism: [technical approach]
    → Components: [modules/services]

Key Design Decisions: [cross-cutting technical choices]

Confirm, adjust, or switch to interactive mode?
```

7. If confirmed → proceed to Step 5 (stack direction) with the proposed data
8. If adjusted → incorporate changes, proceed to Step 5
9. If interactive requested → fall through to Step 1

---

### Step 1: Gather Context

**Read these files:**

```
.shipkit/product-definition.json  → features, UX patterns, differentiators (REQUIRED)
.shipkit/why.json                 → vision, stage, constraints (RECOMMENDED)
.shipkit/stack.json               → tech capabilities (RECOMMENDED)
.shipkit/product-discovery.json   → pain points for traceability (RECOMMENDED)
.shipkit/codebase-index.json      → existing code (OPTIONAL)
```

**Extract from product-definition.json:**
- All features (F-001, F-002, etc.) — the WHAT that needs mechanisms
- UX patterns (P-001, P-002, etc.) — interaction patterns that constrain implementation
- Feature dependencies — influences mechanism ordering
- Differentiators — technical requirements implied by competitive claims

---

### Step 2: Design Core Mechanisms

For each feature (or group of related features), define a mechanism:

**Use AskUserQuestion tool:**

```
header: "Mechanisms"
question: "For [feature name], what's the technical approach? How should we build this?"
options:
  - label: "[Proposed mechanism from context]"
    description: "Based on the feature requirements and stack"
  - label: "Different approach"
    description: "I have another idea"
```

For each mechanism, capture:
- **Name** — concise mechanism name
- **Description** — how it works at a technical level
- **Implements features** — which feature IDs from product-definition
- **Key design choices** — decisions made with rationale and alternatives

Aim for 2-5 mechanisms. Each feature should be served by at least one mechanism. Mechanisms can serve multiple features.

---

### Step 3: Define Component Structure

Based on mechanisms, define how the solution is modularized:

```
header: "Components"
question: "How should the system be componentized?"
options:
  - label: "[Proposed structure based on mechanisms]"
    description: "[Why this structure]"
  - label: "Different structure"
    description: "I have a different modularity in mind"
```

For each component, capture:
- **Name** — component/module/service name
- **Responsibility** — what it owns (single responsibility)
- **Mechanisms** — which mechanism IDs it implements
- **Interfaces** — how it communicates with other components

Aim for 2-6 components. Each mechanism should map to at least one component.

---

### Step 4: Capture Design Decisions

Identify cross-cutting technical decisions that affect multiple mechanisms or components:

- Technology choices (framework, database, hosting)
- Architectural patterns (monolith vs microservices, REST vs GraphQL)
- Data flow decisions (SSR vs CSR, caching strategy)
- Security patterns (auth approach, data encryption)

For each decision, capture:
- **Decision** — what was decided
- **Rationale** — why this direction
- **Alternatives** — what was considered but rejected

---

### Step 5: Stack Direction (Greenfield Only)

**Skip if `.shipkit/stack.json` already exists.**

For greenfield projects, ask about technology direction:

```
header: "Stack"
question: "What tech direction for this solution?"
options:
  - label: "[Recommended stack based on mechanisms]"
    description: "[Why it fits the technical design]"
  - label: "Different stack"
    description: "I have preferences"
```

Capture:
- Recommended technologies (frontend, backend, database, hosting)
- Rationale tied to the mechanism design
- Constraints that drove the choice

---

### Step 6: Present Blueprint and Confirm

Present the full engineering blueprint:

**View 1: Technical Design**
```
## Engineering Blueprint: [Product Name]

### Core Mechanisms
1. M-001: [Name] — [description]
   Implements: F-001, F-002
   Design choices: [key decisions]
2. M-002: [Name] — [description]

### Component Structure
1. C-001: [Name] — [responsibility]
   Implements mechanisms: M-001
   Interfaces: [how it connects]

### Design Decisions
1. [Decision] — [rationale]
```

**View 2: Feature → Mechanism Map**
```
### Feature Coverage

  F-001: [Feature Name] → M-001: [Mechanism] via C-001: [Component]
  F-002: [Feature Name] → M-001, M-002 via C-001, C-002
  F-003: [Feature Name] → M-003 via C-003
```

Then ask: **"Confirm this engineering blueprint, or adjust?"**

Incorporate adjustments and re-present if changed significantly.

---

### Step 7: Write Engineering Definition

After confirmation, write `.shipkit/engineering-definition.json`.

See [Engineering Definition JSON Schema](#engineering-definition-json-schema) below.

---

### Step 8: Suggest Next Steps

```
Engineering blueprint written to .shipkit/engineering-definition.json
Mechanisms: {N} | Components: {N} | Design Decisions: {N}

Next:
  1. /shipkit-goals — Define success criteria (reads both product + engineering definitions)
  2. /shipkit-spec — Create specs for features (with mechanism context)
  3. /shipkit-architecture-memory — Log detailed architecture decisions

Ready to define success criteria?
```

---

## Engineering Definition JSON Schema (Quick Reference)

```json
{
  "$schema": "shipkit-artifact",
  "type": "engineering-definition",
  "version": "1.0",
  "lastUpdated": "ISO timestamp",
  "source": "shipkit-engineering-definition",
  "product": {
    "name": "Product name (from product-definition)",
    "stage": "poc|mvp|production|scale"
  },
  "mechanisms": [
    {
      "id": "M-001",
      "name": "Mechanism name",
      "description": "How this works technically",
      "implementsFeatures": ["F-001", "F-002"],
      "designChoices": [
        { "decision": "Choice", "rationale": "Why", "alternatives": ["Rejected option"] }
      ]
    }
  ],
  "components": [
    {
      "id": "C-001",
      "name": "Component name",
      "responsibility": "What it owns",
      "mechanisms": ["M-001"],
      "interfaces": ["REST API to C-002", "Event bus to C-003"]
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
  "summary": {
    "totalMechanisms": 0,
    "totalComponents": 0,
    "totalDesignDecisions": 0
  }
}
```

**Full schema reference**: See `references/output-schema.md`
**Realistic example**: See `references/example.json`

### Graph Relationships

The ID-based cross-references enable these graph traversals:

- **Mechanism -> Features**: `mechanisms[].implementsFeatures` references `features[].id` from product-definition.json
- **Component -> Mechanisms**: `components[].mechanisms` references `mechanisms[].id`
- **Feature -> Mechanism** (reverse lookup): For any feature in product-definition, find mechanisms where `implementsFeatures` contains that feature ID

---

## When $ARGUMENTS is Provided

If `$ARGUMENTS` contains text:
- **Focus area**: Use to narrow mechanism design to specific features
- **`--refresh`**: Start fresh even if engineering-definition.json exists

---

## When This Skill Integrates with Others

### Before This Skill
| Skill | Why |
|-------|-----|
| `shipkit-product-definition` | Produces product-definition.json — required input (features, UX patterns) |
| `shipkit-project-context` | Produces stack.json — technology constraints |
| `shipkit-why-project` | Produces why.json — project purpose and stage |

### After This Skill
| Skill | How |
|-------|-----|
| `shipkit-goals` | Reads engineering-definition.json to derive criteria from mechanisms |
| `shipkit-spec` | Reads engineering-definition.json for mechanism context when specifying features |
| `shipkit-architecture-memory` | Reads engineering-definition.json for solution context in architecture decisions |
| `shipkit-plan` | Indirectly — plans derive from specs which reference mechanisms |

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-definition.json` | Features, UX patterns, differentiators | Route to `/shipkit-product-definition` |
| `.shipkit/why.json` | Project purpose and stage | Proceed with user input |
| `.shipkit/stack.json` | Tech capabilities and constraints | Ask about stack (greenfield) or proceed |
| `.shipkit/product-discovery.json` | Pain points for traceability | Skip |
| `.shipkit/codebase-index.json` | Existing code for existing projects | Skip |
| `.shipkit/engineering-definition.json` | Previous definition (for update mode) | Generate new |

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

| File | When |
|------|------|
| `.shipkit/engineering-definition.json` | Created on first run, updated on subsequent runs |

**Archive location** (if replacing):
- `.shipkit/archive/engineering-definition/engineering-definition.[timestamp].json`

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

Engineering blueprint is complete when:
- [ ] Product-definition.json read and features extracted
- [ ] 2-5 mechanisms defined, each implementing at least one feature
- [ ] Every feature served by at least one mechanism
- [ ] 2-6 components defined with clear responsibilities
- [ ] Key design decisions captured with rationale
- [ ] Stack direction captured (greenfield only)
- [ ] All cross-references use stable IDs (M-001, C-001)
- [ ] Summary counts match actual array lengths
- [ ] User confirmed the blueprint before writing
- [ ] File saved to `.shipkit/engineering-definition.json`
<!-- /SECTION:success-criteria -->

---

**Remember**: This skill captures the technical approach — HOW you build the features defined in product-definition.json. It's the bridge between product design (what users see) and implementation (architecture, specs, code). Each mechanism maps to product features, giving full traceability from user needs through to technical approach.
