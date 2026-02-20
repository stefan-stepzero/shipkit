---
name: shipkit-product-definition
description: "Synthesizes vision artifacts (why, goals, personas, stack) into a product definition — feature portfolio mapped to goals with dependency ordering and coverage analysis"
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

# shipkit-product-definition

Bridges the gap between vision artifacts and feature specifications. Reads why.json, goals.json, product-discovery.json, and stack.json, then proposes a complete feature portfolio with goal-to-feature traceability, dependency ordering, and coverage analysis.

This is the product blueprint — everything downstream (specs, architecture, plans, implementation) derives from it.

---

## Process

### Step 1: Load Context

Read all available vision artifacts:

**Required** (fail gracefully if missing):
- `.shipkit/goals.json` — what outcomes we need
- `.shipkit/product-discovery.json` — who the users are (personas)

**Recommended** (enrich the proposal):
- `.shipkit/why.json` — project purpose and stage
- `.shipkit/stack.json` — technology constraints and capabilities

**Optional** (for existing projects):
- `.shipkit/codebase-index.json` — what already exists
- `.shipkit/specs/todo/*.json` or `.shipkit/specs/active/*.json` — specs already written

If goals.json is missing, tell the user: "Run `/shipkit-goals` first — I need goals to map features against." and stop.

If product-discovery.json is missing but goals.json exists, warn but proceed: "No personas found. Feature mapping will be goal-only. Run `/shipkit-product-discovery` for persona coverage."

### Step 2: Check for Existing Product Definition

If `.shipkit/product-definition.json` exists:

1. Read it
2. Show summary:
   ```
   Existing product definition found.
   Features: {N} ({N} todo, {N} specced, {N} planned, {N} implemented)
   Goal coverage: {N}/{N} goals covered
   Last updated: {timestamp}
   ```
3. Ask: "Update this definition, or start fresh?"
4. If updating, load existing features as the base for modifications

If `$ARGUMENTS` contains `--refresh`, skip the question and start fresh.

### Step 3: Analyze Goals and Personas

Extract from loaded artifacts:

1. **Goals** — list each goal with its ID, text, and priority from goals.json
2. **Personas** — list each persona with their key needs and pain points
3. **Stage** — from why.json, determine project stage (MVP, growth, scale)
4. **Tech capabilities** — from stack.json, note what the tech stack supports (real-time, offline, mobile, etc.)

For existing projects, also scan:
- What features are already partially built (from codebase-index)
- What specs already exist (from specs/)

### Step 4: Propose Feature Portfolio

Based on the analysis, propose a feature set. For each feature:

1. **Name** — concise feature name
2. **Description** — 1-2 sentences on what it does
3. **Goals served** — which goal IDs this feature helps achieve
4. **Personas served** — which personas benefit
5. **Priority tier**:
   - Tier 1 (foundation): Auth, data model, core infrastructure — must exist before other features
   - Tier 2 (core): The features that make this product useful — the reason users come
   - Tier 3 (enhancement): Polish, notifications, analytics, integrations — nice to have
6. **Dependencies** — which other features must exist first
7. **Existing work** — for existing projects, note what's already built

**Feature count guidance**:
- MVP stage: 3-5 features (foundation + core only)
- Growth stage: 5-8 features (foundation + core + some enhancements)
- Scale stage: 7-12 features (full portfolio)

**Stack awareness**: Only propose features the tech stack can support. If goals require real-time but stack has no WebSocket/SSE support, flag it as a constraint.

### Step 5: Build Goal Coverage Matrix

Map every goal to features and every feature to goals:

```
## Goal Coverage

| Goal | Features | Coverage |
|------|----------|----------|
| G-001: Users can track progress | F-001 (Auth), F-004 (Dashboard) | Full |
| G-002: Spaced repetition scheduling | F-003 (SR Engine) | Full |
| G-003: Multiple quiz formats | F-002 (Quiz Engine) | Full |
| G-004: Instructor content management | — | UNCOVERED |

## Feature Justification

| Feature | Goals Served | Justified? |
|---------|-------------|------------|
| F-001: Auth + Profile | G-001, G-004 | Yes |
| F-002: Quiz Engine | G-003 | Yes |
```

**Flag issues**:
- Goals with no features → "UNCOVERED — needs a feature or is out of scope for this stage"
- Features with no goals → "UNJUSTIFIED — consider removing or linking to a goal"

### Step 6: Present Proposal

Present the full proposal in two views:

**View 1: Feature Portfolio**
```
## Proposed Features (ordered by dependency)

### Tier 1: Foundation
1. F-001: Auth + User Profile
   Goals: G-001, G-004 | Personas: learner, instructor | Deps: none

### Tier 2: Core
2. F-002: Quiz Engine
   Goals: G-003 | Personas: learner | Deps: F-001
3. F-003: Spaced Repetition Engine
   Goals: G-002 | Personas: learner | Deps: F-002

### Tier 3: Enhancement
4. F-005: Notification System
   Goals: G-005 | Personas: learner | Deps: F-003, F-004
```

**View 2: Goal Coverage Matrix** (from Step 5)

Then ask: **"Confirm this product definition, or adjust?"**

User can:
- Confirm as-is
- Add features ("add a feature for instructor analytics")
- Remove features ("drop notifications for MVP")
- Reorder/reprioritize ("move dashboard to Tier 1")
- Split or merge features
- Adjust goal mappings

Incorporate adjustments and re-present if changed significantly.

### Step 7: Write Product Definition

After confirmation, write `.shipkit/product-definition.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-definition",
  "version": "1.0",
  "lastUpdated": "ISO timestamp",
  "source": "shipkit-product-definition",
  "product": {
    "name": "Product name",
    "vision": "One-line from why.json",
    "stage": "mvp|growth|scale"
  },
  "features": [
    {
      "id": "F-001",
      "name": "Auth + User Profile",
      "description": "User registration, login, profile management",
      "goalsServed": ["G-001", "G-004"],
      "personasServed": ["learner", "instructor"],
      "priority": 1,
      "tier": "foundation",
      "dependsOn": [],
      "status": "todo",
      "specPath": null
    }
  ],
  "goalCoverage": {
    "G-001": {
      "goal": "Users can track learning progress",
      "features": ["F-001", "F-004"],
      "coverage": "full"
    }
  },
  "dependencyOrder": ["F-001", "F-002", "F-003", "F-004", "F-005"],
  "summary": {
    "totalFeatures": 5,
    "byTier": {"foundation": 1, "core": 3, "enhancement": 1},
    "goalsFullyCovered": 4,
    "goalsPartiallyCovered": 0,
    "goalsUncovered": 1
  }
}
```

**Dependency order**: Topological sort — features with no dependencies first, then features whose dependencies are all earlier in the list.

**Feature IDs**: Use F-001, F-002, etc. Sequential, stable. If updating an existing definition, preserve existing IDs.

### Step 8: Suggest Next Steps

After writing:

```
Product definition written to .shipkit/product-definition.json
Features: {N} ({tier counts})
Goal coverage: {covered}/{total} goals covered

Next: Run `/shipkit-spec` to generate specs for each feature (batch mode from product-definition)
```

---

## When $ARGUMENTS is Provided

If `$ARGUMENTS` contains text (e.g., `/shipkit-product-definition "learning app"` or `/shipkit-product-definition --refresh`):

- **Product name/description**: Use as seed for the product name and to focus the feature proposals
- **`--refresh`**: Start fresh even if product-definition.json exists
- **`--coverage`**: Only run the coverage analysis (Steps 5-6) against existing definition — useful for checking if new goals are covered

---

<!-- SECTION:after-completion -->
## After Completion

The product definition is the central planning artifact. Keep it current as the product evolves:

- After adding new goals → re-run with `--coverage` to check if features cover them
- After completing features → update status fields (the spec skill does this automatically)
- Before each development cycle → review the definition for priority changes

The goal coverage matrix is your product health indicator. Uncovered goals mean missing features. Unjustified features mean scope creep.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] All vision artifacts read (goals.json required, others recommended)
- [ ] Feature portfolio proposed with 3-12 features appropriate to project stage
- [ ] Every feature has goals served, personas served, priority tier, and dependencies
- [ ] Goal coverage matrix shows coverage for every goal
- [ ] Uncovered goals flagged explicitly
- [ ] Unjustified features (no goals) flagged explicitly
- [ ] Dependency order is a valid topological sort (no circular deps)
- [ ] User confirmed the portfolio before writing
- [ ] product-definition.json written with complete schema
- [ ] Feature IDs are stable (preserved across updates)
<!-- /SECTION:success-criteria -->

---

## Integration

### Before This Skill
| Skill | Why |
|-------|-----|
| `shipkit-why-project` | Produces why.json — project purpose and stage |
| `shipkit-goals` | Produces goals.json — required input |
| `shipkit-product-discovery` | Produces product-discovery.json — personas |
| `shipkit-project-context` | Produces stack.json — tech capabilities |

### After This Skill
| Skill | How |
|-------|-----|
| `shipkit-spec` | Reads product-definition.json in batch mode — one spec per feature |
| `shipkit-architecture-memory` | Reads product-definition.json for feature scope in solution architect mode |
| `shipkit-plan` | Indirectly — plans are generated from specs which come from product-definition |

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `.shipkit/goals.json` | Goal list — required input |
| `.shipkit/product-discovery.json` | Personas — recommended input |
| `.shipkit/why.json` | Project purpose and stage |
| `.shipkit/stack.json` | Tech capabilities and constraints |
| `.shipkit/codebase-index.json` | Existing code for existing projects |
| `.shipkit/specs/*.json` | Existing specs (for update mode) |
| `.shipkit/product-definition.json` | Previous definition (for update mode) |

## Context Files This Skill Writes

| File | When |
|------|------|
| `.shipkit/product-definition.json` | Created on first run, updated on subsequent runs |
