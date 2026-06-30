---
name: shipkit-engineering-definition
description: "Define the technical approach — mechanisms, design decisions, stack direction, and component structure. Triggers: 'engineering approach', 'how to build this', 'technical design', 'mechanisms'."
argument-hint: "[focus area or --refresh]"
agent: shipkit-architect-agent
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
effort: medium
---

# shipkit-engineering-definition — Technical Approach

Defines HOW we build the product defined in product-definition.json. For each feature, designs the technical mechanisms, captures design decisions, recommends stack direction (greenfield), and defines component structure.

This is the engineering blueprint — it takes the product's features and UX patterns and defines the technical approach to implement them. Downstream skills (goals, spec) read both product-definition.json and engineering-definition.json. Architecture decisions are captured directly in this file.

---

## When to Invoke

**User triggers**:
- "How should we build this?", "Technical approach", "Engineering design"
- "Define mechanisms", "Component structure", "Technical decisions"
- "Stack direction", "What technologies?"

**Workflow position**:
- After `/shipkit-product-definition` (needs features and UX patterns)
- Before `/shipkit-product-goals` and `/shipkit-engineering-goals` (goals derive criteria from mechanisms)

---

## Prerequisites

**Required** (fail gracefully if missing):
- `.shipkit/product-definition.json` — features, UX patterns, differentiators

**Recommended** (enrich the proposal):
- `.shipkit/why.json` — project purpose and vision
- `.shipkit/goals/strategic.json` — project stage and constraints
- `.shipkit/stack.json` — existing technology constraints
- `.shipkit/product-discovery.json` — pain points for traceability

**Optional** (for existing projects):
- `.shipkit/codebase-index.json` — existing code structure

If product-definition.json is missing, tell the user: "Run `/shipkit-product-definition` first — I need to know what features to design mechanisms for." and stop.

---

## Process

### Completion Tracking

After reading prerequisites, create tasks:
- `TaskCreate`: "Design 2-5 mechanisms mapped to features"
- `TaskCreate`: "Define 2-6 components mapped to mechanisms"
- `TaskCreate`: "Capture cross-cutting design decisions"
- `TaskCreate`: "Write engineering-definition.json"
- `TaskCreate`: "Derive and dual-write architecture.json (lean) + architecture-archive.json (full)"

engineering-definition.json alone is NOT done — the architecture decisions log must also be derived and written. The log is **dual-written**: a lean `architecture.json` (capped, `@`-imported) plus a full `architecture-archive.json` (complete bodies, read on demand). See `references/architecture-log-schema.md` for the canonical convention. This applies to propose mode (Step 0c) as well.

### Step 0: Check for Existing File

> **Fork context — no user prompts.** You are dispatched in a fork and have no user channel. Skip the file-exists menu entirely.

1. Check if `.shipkit/engineering-definition.json` exists
2. If exists: read `.shipkit/reviews/direction-assessment.json` if present. If the latest review lists a gap against this artifact, archive the existing file to `.shipkit/.archive/engineering-definition.YYYY-MM-DD.json` and regenerate addressing the gap. Otherwise, read the existing file and exit early with a "no changes needed" report — the reviewer already accepted it.
3. If no file exists: proceed to Step 0c (propose mode).

---

### Step 0c: Propose Mode (Context-Driven)

If `.shipkit/product-definition.json` exists, attempt to propose a technical approach without asking:

1. Read `.shipkit/product-definition.json` (features, UX patterns, differentiators)
2. Read `.shipkit/why.json` if exists (vision, constraints)
2b. Read `.shipkit/goals/strategic.json` if exists (stage)
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

```

7. Write `engineering-definition.json` directly and present a summary
8. The orchestrator's review cycle will catch issues — no confirmation needed

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

**Fork context — no user prompts.** Infer mechanisms from upstream context (.shipkit/ files). If insufficient, return `gaps_found` and exit; the reviewer will trigger re-dispatch.

For each mechanism, capture:
- **Name** — concise mechanism name
- **Description** — how it works at a technical level
- **Implements features** — which feature IDs from product-definition
- **Key design choices** — decisions made with rationale and alternatives

Aim for 2-5 mechanisms. Each feature should be served by at least one mechanism. Mechanisms can serve multiple features.

---

### Step 2b: Ecosystem Audit

Before structuring components, ground each mechanism in what the stack already provides — don't reinvent libraries and patterns that exist.

**Fork context — no user prompts.** Read the stack and consult the reference files; infer the rest.

1. **Read the stack.** Use `.shipkit/stack.json` if present; otherwise use the Step 5 stack direction. For hybrid stacks (e.g. a Next.js frontend + a Python API backend), consult **every** matching reference.
2. **Consult the standards.** Read [`references/mechanism-standards.md`](references/mechanism-standards.md) (stack-agnostic mechanism → standard mapping, with anti-patterns) plus the matching [`references/ecosystem-defaults/<stack>.md`](references/ecosystem-defaults/) file(s) for the concrete library per concern.
3. **Default to the standard.** For each mechanism, adopt the standard library/pattern for its concern (e.g. Pydantic for Python data models, Zod for TS validation, an auth library over custom auth). Design something custom only when the standard genuinely doesn't fit.
4. **Record it on the mechanism.** Capture `uses: [library, ...]` for the libraries/patterns it adopts, and `whyNotStandard: "<reason>"` when you deliberately deviate.

Tone is **"default to this," not "you must"** — deviating is fine, but it should be a conscious, recorded choice rather than an oversight.

---

### Step 3: Define Component Structure

Based on mechanisms, define how the solution is modularized:

**Fork context — no user prompts.** Infer component structure from mechanisms and upstream context. If insufficient, return `gaps_found` and exit; the reviewer will trigger re-dispatch.

For each component, capture:
- **Name** — component/module/service name
- **Responsibility** — what it owns (single responsibility)
- **Mechanisms** — which mechanism IDs it implements
- **Interfaces** — how it communicates with other components
- **Data contracts** — key data shapes flowing in/out (types, schemas, API payloads)

Aim for 2-6 components. Each mechanism should map to at least one component.

**Data contracts note**: Define the key data shapes at component boundaries — request/response types, shared models, event payloads. Use Zod schemas, TypeScript types, or JSON Schema depending on the stack.

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

**Fork context — no user prompts.** Infer stack direction from existing `.shipkit/` context files and mechanism requirements. If insufficient, return `gaps_found` and exit; the reviewer will trigger re-dispatch.

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

> **Fork context — do not prompt for confirmation.** Write the blueprint directly. The direction reviewer will flag any misalignment on the next review cycle.

---

### Step 7: Write Engineering Definition + Architecture Decisions

After confirmation, write **three** files — the engineering blueprint, plus the **dual-written**
architecture decisions log (lean index + full archive):

1. **`.shipkit/engineering-definition.json`** — Full engineering blueprint (mechanisms, components, design decisions, stack direction)

2. **`.shipkit/architecture-archive.json`** — FULL append-only decisions log. Every ADR with complete `rationale`, `alternatives`, and supersession history. **NOT `@`-imported** — read on demand. This is the file that never loses information.

3. **`.shipkit/architecture.json`** — LEAN active-decisions index, derived from the archive. Stays `@`-imported. Holds active/governing ADRs (capped), superseded ADRs as one-line stubs, and the `patterns` / `constraints` (and `designSystem`, written by `shipkit-design-system`) summaries. This is what downstream skills (plan, spec, preflight, review-shipping) read for pattern context; they read the archive only when they need an ADR's full rationale or rejected alternatives.

> **Canonical convention — read it before writing:** the lean/full split, the capped active
> schema, the superseded-stub schema, and the dual-write + supersession/amendment rules are
> defined once in [`references/architecture-log-schema.md`](references/architecture-log-schema.md).
> Follow it exactly. The shapes below are a quick reference.

**Lean `architecture.json`** (capped active entries + superseded stubs):
```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-decisions",
  "version": "1.0",
  "lastUpdated": "ISO timestamp",
  "source": "shipkit-engineering-definition",
  "note": "Lean active-decisions index. Full ADR bodies live in .shipkit/architecture-archive.json — read on demand.",
  "decisions": [
    { "id": "ADR-001", "decision": "What was decided (one line)", "rationale": "One-line rationale", "scope": "cross-cutting | mechanism:M-001", "date": "ISO date" },
    { "id": "ADR-038", "status": "superseded", "supersededBy": "ADR-055", "decision": "One-line decision (replaced)" }
  ],
  "patterns": ["Key architectural patterns in use"],
  "constraints": ["Technical constraints driving decisions"]
}
```

**Full `architecture-archive.json`** (complete bodies, append-only):
```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-decisions-archive",
  "version": "1.0",
  "lastUpdated": "ISO timestamp",
  "source": "shipkit-engineering-definition",
  "note": "Full append-only ADR log. Not @-imported — read on demand.",
  "decisions": [
    { "id": "ADR-001", "status": "active", "decision": "...", "rationale": "Full rationale", "alternatives": ["What was considered"], "scope": "cross-cutting | mechanism:M-001", "date": "ISO date" }
  ],
  "patterns": ["..."],
  "constraints": ["..."]
}
```

**Derivation**: Merge top-level `designDecisions` (scope: `"cross-cutting"`) with per-mechanism `designChoices` (scope: `"mechanism:M-001"`) into a flat ADR list. Add patterns and constraints inferred from the stack and mechanisms.

**Dual-write (every ADR write):**
1. Write/append the **full** entry to `architecture-archive.json` (complete rationale + alternatives + status + any supersession links). Append-only — never delete; preserve original `date`.
2. Write the **capped** projection to the lean `architecture.json`:
   - active or amended ADR → `{ id, decision, scope, date, rationale(one line) }` (drop `alternatives` and long rationale — they live in the archive)
   - superseded ADR → stub `{ id, status:"superseded", supersededBy, decision(one line) }`

**On update**: regenerate from the archive. New ADRs append to the archive (full) and to the lean file (capped). Existing ADRs keep their original dates.

**On supersession** (a new ADR replaces a prior one — mark this explicitly): in the archive, add the new ADR with `supersedes` and set the prior ADR `status:"superseded"` + `supersededBy` (keeping its full body); in the lean file, add the new ADR (capped) and **collapse the prior ADR to a one-line stub**. Amended ADRs (partial change, still governing) stay active and capped — do NOT stub them.

See [Engineering Definition JSON Schema](#engineering-definition-json-schema) below, and `references/architecture-log-schema.md` for the full convention.

---

### Step 8: Suggest Next Steps

```
Engineering blueprint written to .shipkit/engineering-definition.json
Mechanisms: {N} | Components: {N} | Design Decisions: {N}

Next:
  1. /shipkit-product-goals — Define product success criteria; then /shipkit-engineering-goals for engineering criteria
  2. /shipkit-spec — Create specs for features (with mechanism context)

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
      "uses": ["library-or-pattern"],
      "whyNotStandard": null,
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
      "interfaces": ["REST API to C-002", "Event bus to C-003"],
      "dataContracts": ["Key data shapes at this component's boundaries"]
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
| `shipkit-product-goals` | Reads engineering-definition.json to derive product criteria from mechanisms |
| `shipkit-engineering-goals` | Reads engineering-definition.json to derive engineering criteria from mechanisms |
| `shipkit-spec` | Reads engineering-definition.json for mechanism context when specifying features |
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

**Artifact strategy: replace** — Overwrites `engineering-definition.json` and the lean `architecture.json` (the lean file is re-derived from the archive each write). **Exception:** `architecture-archive.json` is **append-only / merge** — existing ADR bodies are never dropped; superseding sets status + links but keeps the prior body.

**Write Strategy: OVERWRITE** (lean files) / **APPEND-MERGE** (`architecture-archive.json`)

| File | When |
|------|------|
| `.shipkit/engineering-definition.json` | Created on first run, updated on subsequent runs |
| `.shipkit/architecture-archive.json` | FULL append-only decisions log — every ADR with complete rationale/alternatives. NOT `@`-imported. |
| `.shipkit/architecture.json` | LEAN active-decisions index (capped active ADRs + superseded stubs). `@`-imported. Derived from the archive on every write. See `references/architecture-log-schema.md`. |

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

**Suggest skill when:** User needs to define success criteria (`/shipkit-product-goals`, `/shipkit-engineering-goals`), create detailed specs (`/shipkit-spec`), or update architecture decisions (`/shipkit-engineering-definition`).
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
- [ ] File saved to `.shipkit/engineering-definition.json`
- [ ] Architecture decisions dual-written: full bodies to `.shipkit/architecture-archive.json`, capped/stubbed lean index to `.shipkit/architecture.json` (per `references/architecture-log-schema.md`)
<!-- /SECTION:success-criteria -->

---

**Remember**: This skill captures the technical approach — HOW you build the features defined in product-definition.json. It's the bridge between product design (what users see) and implementation (architecture, specs, code). Each mechanism maps to product features, giving full traceability from user needs through to technical approach.
