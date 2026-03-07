---
name: shipkit-spec-roadmap
description: "Prioritize which specs to write first from product + engineering definitions. Triggers: 'spec roadmap', 'what to spec first', 'prioritize features', 'spec backlog'."
argument-hint: "[--update | --regenerate]"
context: fork
agent: shipkit-product-owner-agent
---

# shipkit-spec-roadmap — Spec Prioritization Roadmap

**Purpose**: Bridge the gap between definitions and specs by building an explicit prioritization roadmap. Scores features by goal-gate phasing, dependency depth, foundation value, and mechanism complexity to determine spec order.

**Output format**: JSON — structured roadmap at `.shipkit/spec-roadmap.json`

---

## When to Invoke

**User triggers**:
- "What should I spec first?"
- "Prioritize the features"
- "Create a spec roadmap"
- "Spec backlog"
- "What order should I write specs?"

**Before**:
- `/shipkit-spec` (this determines WHICH spec to write next)

**After**:
- `/shipkit-product-definition` (need features to prioritize)
- `/shipkit-engineering-definition` (need mechanisms for effort estimation)
- `/shipkit-product-goals` (recommended — gates drive phasing)

**Workflow position**:
- After definitions are complete, before writing individual specs
- Can be re-run after new features are added or priorities change

---

## Prerequisites

**Required**:
- `.shipkit/product-definition.json` — features to prioritize
- `.shipkit/engineering-definition.json` — mechanisms for effort estimation

**Recommended**:
- `.shipkit/goals/*.json` — gate definitions for phase mapping (especially `goals/strategic.json` or `goals/product.json`)

**Optional**:
- `.shipkit/specs/` — detect already-specced features to mark as completed

**If goals missing**: Fall back to single-phase roadmap sorted by dependency + foundation value only.

---

## Arguments

If `$ARGUMENTS` contains `--update`: Load existing `spec-roadmap.json`, refresh spec statuses, re-score, and present changes.

If `$ARGUMENTS` contains `--regenerate`: Discard existing roadmap and rebuild from scratch.

If `$ARGUMENTS` is empty: Check for existing file and offer choices.

---

## Process

### Step 0: Check Existing Roadmap

1. Read `.shipkit/spec-roadmap.json` (if exists)
2. If found, present current state:
   ```
   Existing spec roadmap found (last updated: {date})
   {N} features across {M} phases, {K} already specced

   View current | Update (re-score + refresh) | Regenerate from scratch?
   ```
3. If user selects "View" → display roadmap summary and exit
4. If user selects "Update" → proceed to Step 1 with existing data as baseline
5. If user selects "Regenerate" or no file exists → proceed to Step 1 fresh

---

### Step 1: Load Context

**Read all context files in parallel** (single message, multiple tool calls):

```
1. Read: .shipkit/product-definition.json    # Features, patterns, differentiators
2. Read: .shipkit/engineering-definition.json # Mechanisms, components, design choices
3. Read: .shipkit/goals/*.json               # Gates and criteria (glob for all goal files)
4. Read: .shipkit/why.json                   # Vision and purpose context
5. Read: .shipkit/codebase-index.json        # Existing code patterns and structure
6. Glob + Read: .shipkit/specs/**/*.json     # Existing specs (todo, active, shipped)
```

**Extract from context**:
- **Features**: ID, name, description, dependencies, mechanisms, mvp flag
- **Mechanisms**: ID, name, complexity indicators (design choices count, component count)
- **Gates**: ID, name, criteria list, which features map to which gate
- **Existing specs**: Which features already have specs (and their status)

---

### Step 2: Build Feature-Mechanism-Gate Graph

For each feature in `product-definition.json`:

1. **Map to gate**: Which gate does this feature's criteria belong to? (from goals)
   - If no goals exist, assign all features to a single "Default" phase
2. **Map to mechanisms**: Which mechanisms does this feature use? (from engineering-definition)
3. **Map dependencies**: What features must be specced/built before this one?
4. **Map pain coverage**: Which user pain points does this feature address? (from product-discovery if available)
5. **Detect already-specced**: Does a spec already exist in `.shipkit/specs/`?

---

### Step 3: Score and Rank

For each unspecced feature, compute three scores:

**Foundation Value** (0-10): How many other features depend on this one?
- Count direct dependents + transitive dependents
- Higher score = more features unlocked by speccing this first

**Pain Coverage** (0-10): How many user pain points does this feature address?
- Count pain points from product-discovery.json that this feature addresses
- Weight by pain severity if available

**Dependency Depth** (0-N): How deep in the dependency chain is this feature?
- 0 = no dependencies (can be specced immediately)
- Higher = more prerequisites needed first

**Effort Estimate** (T-shirt size):
- Count mechanisms used by this feature
- Count design choices within those mechanisms
- Apply sizing:

| Size | Mechanisms | Design Choices | Typical Duration |
|------|-----------|----------------|-----------------|
| XS | 0 | 0 | < 1 day |
| S | 1 | 0-1 | 1-2 days |
| M | 1-2 | 2-3 | 3-5 days |
| L | 2-3 | 4-6 | 1-2 weeks |
| XL | 3+ | 7+ | 2+ weeks |

**Priority within phase**: Sort by:
1. Dependency depth ascending (unblocked first)
2. Foundation value descending (unlocks most work)
3. Pain coverage descending (addresses most user pain)

---

### Step 4: Present Roadmap

Group features by phase (gate), sorted by priority within each phase.

```
## Spec Roadmap for {product name}

### Phase 1: {gate name} ({N} features, ~{X} total effort-days)
 #1  F-001 Worksheet Creator          [L]  foundation:8  pain:3  deps:none
 #2  F-002 Standards Browser          [M]  foundation:2  pain:2  deps:none
 #3  F-003 Export & Print             [M]  foundation:1  pain:1  deps:F-001

### Phase 2: {gate name} ({N} features, ~{X} total effort-days)
 #4  F-004 Differentiated Sets        [L]  foundation:1  pain:2  deps:F-001
 #5  F-005 Classroom Integration      [XL] foundation:0  pain:1  deps:F-003

### Already Specced
 - F-006 User Auth (specs/active/user-auth.json)

### Dependency Warnings
 - F-003 depends on F-001 (must spec F-001 first)
 - F-005 depends on F-003 → F-001 (chain of 2)

Confirm this roadmap? (Adjust priorities / Confirm / Regenerate)
```

**If user adjusts**: Incorporate changes and re-present.

---

### Step 5: Write Roadmap

**Use Write tool to create**: `.shipkit/spec-roadmap.json`

**JSON Schema**: See `references/output-schema.md` for complete schema definition.

**Example**: See `references/example.json` for realistic roadmap.

---

## Effort Estimation Guide

Effort is derived from mechanism complexity, NOT from implementation guesswork:

| Signal | What It Means |
|--------|--------------|
| Feature uses 0 mechanisms | Pure UI/content, XS effort |
| Feature uses 1 mechanism with no design choices | Straightforward implementation, S |
| Feature uses mechanisms with design choices | Each design choice = a decision point during implementation |
| Feature has 3+ mechanisms | Cross-cutting concerns, likely L or XL |
| Feature depends on unbuilt features | Effective effort includes prerequisite work |

**Don't guess duration in days** — use T-shirt sizes. The `effortDays` field is a rough midpoint for summary math only.

---

## Completion Checklist

- [ ] Loaded product-definition.json and engineering-definition.json
- [ ] Loaded goals (if available) for gate-based phasing
- [ ] Detected already-specced features
- [ ] Built dependency graph with no cycles
- [ ] Scored all unspecced features (foundation, pain, depth)
- [ ] Assigned effort sizes from mechanism complexity
- [ ] Presented roadmap grouped by phase for user validation
- [ ] Wrote `.shipkit/spec-roadmap.json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has the roadmap been saved to `.shipkit/spec-roadmap.json`?
2. **Next step** - Suggest: "Run `/shipkit-spec` to start speccing the top-priority feature."
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Roadmap is complete when:
- [ ] JSON file conforms to Shipkit artifact convention ($schema, type, version, lastUpdated, source, summary)
- [ ] Every feature from product-definition.json is accounted for (either in phases or completed)
- [ ] Phases map to goal gates (or single "Default" phase if no goals)
- [ ] Priority order is defensible (dependency-first, then foundation value, then pain coverage)
- [ ] Effort sizes derived from mechanism complexity (not guessed)
- [ ] Dependency graph has no cycles and warnings are surfaced
- [ ] Already-specced features listed in `completed` array
- [ ] Summary counts match actual data
- [ ] File saved to `.shipkit/spec-roadmap.json`
<!-- /SECTION:success-criteria -->

---

## Context Files This Skill Reads

**Required** (read if exist — error if missing):
- `.shipkit/product-definition.json` — Features to prioritize
- `.shipkit/engineering-definition.json` — Mechanisms for effort estimation

**Recommended** (read if exist):
- `.shipkit/goals/*.json` — Gate definitions for phase mapping
- `.shipkit/why.json` — Vision and purpose context
- `.shipkit/codebase-index.json` — Existing code patterns and structure

**Optional** (read if relevant):
- `.shipkit/specs/**/*.json` — Detect already-specced features
- `.shipkit/product-discovery.json` — Pain points for coverage scoring

---

## Context Files This Skill Writes

**Write Strategy: CREATE or UPDATE**

**Creates/Updates**:
- `.shipkit/spec-roadmap.json` — Prioritized spec roadmap

**Update Behavior**:
- Full file replacement on each write
- Previous version is overwritten
- Use `--update` flag to refresh an existing roadmap

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-product-definition` — Defines features to prioritize (required)
- `/shipkit-engineering-definition` — Defines mechanisms for effort estimation (required)
- `/shipkit-product-goals` — Defines gates for phase mapping (recommended)

### After This Skill

- `/shipkit-spec` — Uses roadmap to determine which feature to spec next
- `/shipkit-plan` — After specs are written, plans implementation

---

**Remember**: This skill bridges definitions and specs. It doesn't write specs — it tells you which specs to write first and why. The roadmap is a living document; re-run with `--update` as features get specced or priorities change.
