---
name: shipkit-ideator
description: Brainstorms new skill opportunities, workflow improvements, and composition patterns based on analyst findings. Produces ranked opportunity cards with effort/impact scores and implementation sketches. Use after running shipkit-analyst.
argument-hint: "[--focus new-skills|improvements|compositions|all] [--top N]"
---

# shipkit-ideator - Shipkit Opportunity Ideator

**Purpose**: Turn gap analysis into actionable improvement ideas — new skills, workflow enhancements, and composition patterns

**What it does**:
- Reads the analyst report (`docs/development/analyst-report.json`)
- Brainstorms opportunities across four dimensions: new skills, skill improvements, workflow compositions, and architecture patterns
- Scores each opportunity on impact vs effort
- Produces ranked opportunity cards at `docs/development/opportunities.json`

---

## When to Invoke

**User says:**
- "What should we build next?"
- "Brainstorm improvements"
- "Run the ideator"
- "What opportunities exist?"
- "How can we improve Shipkit?"
- "Suggest new skills"

**Automated trigger:**
- After `/shipkit-analyst` produces a new report
- As the third step of a Shipkit self-improvement team

---

## Prerequisites

**Required**:
- `docs/development/analyst-report.json` exists (run `/shipkit-analyst` first)

**Helpful context**:
- `docs/development/scout-report.json` — Raw CC findings for additional context
- Previous opportunities at `docs/development/opportunities.json`
- Design philosophy at `docs/development/SHIPKIT-DESIGN-PHILOSOPHY.md`
- Skill quality standards at `docs/development/SKILL-QUALITY-AND-PATTERNS.md`

---

## Process

### Step 1: Load Context

Read these files:
1. `docs/development/analyst-report.json` — Gap analysis (required)
2. `docs/development/scout-report.json` — Raw CC findings (for additional context)
3. `docs/development/opportunities.json` — Previous opportunities (to avoid duplicates)
4. `CLAUDE.md` — Framework development instructions (for the Skill Value Test)

Extract from analyst report:
- All `info` findings (feature opportunities)
- All `warning` findings (deprecation migrations)
- `skillCoverage` array (coverage gaps)
- `summary.skillsCoverage.lowest` (weakest skills)

### Step 2: Apply the Skill Value Test

Before brainstorming, recall the fundamental rule from CLAUDE.md:

> A skill is **valuable** if it:
> 1. Forces human decisions to be explicit
> 2. Creates persistence Claude lacks

> A skill is **redundant** if Claude does it well without instruction.

**Every opportunity must pass this test.** If Claude can do it well without a skill, it's not a valid opportunity.

### Step 3: Brainstorm — New Skills

For each feature opportunity from the analyst report, consider:

1. **Does this CC feature enable a new skill that passes the Value Test?**
   - Example: New `memory` field → skill for managing what agents remember across sessions (persistence Claude lacks)
   - Counter-example: New syntax highlighting → Claude already does this, no skill needed

2. **Are there workflow gaps the analyst found?**
   - Missing handoffs between existing skills
   - Manual steps that could be automated
   - Context that gets lost between sessions

3. **Are there team composition patterns that need skills?**
   - Team orchestration variations beyond `/shipkit-team`
   - Specialized review patterns
   - Debug investigation workflows

For each new skill idea, produce:
```json
{
  "type": "new-skill",
  "name": "shipkit-{proposed-name}",
  "category": "Vision|Planning|Knowledge|Execution|Quality|System",
  "description": "What it does",
  "valueTestResult": "Forces explicit: X / Creates persistence: Y",
  "triggeredBy": "GAP-xxx from analyst report",
  "ccFeatures": ["Features it would use"],
  "impact": 1-5,
  "effort": 1-5,
  "sketch": "2-3 sentence implementation approach"
}
```

### Step 4: Brainstorm — Skill Improvements

For each existing skill with low coverage score:

1. **What CC features is it not using that it could benefit from?**
   - `context: fork` for isolated execution
   - `memory` for cross-session persistence
   - `hooks` in frontmatter for lifecycle events
   - New tool capabilities

2. **What analyst findings apply to this skill?**
   - Deprecated patterns to migrate
   - New patterns to adopt
   - Missing integrations

For each improvement idea:
```json
{
  "type": "skill-improvement",
  "skill": "shipkit-{name}",
  "currentCoverage": 0.6,
  "proposedCoverage": 0.85,
  "improvements": [
    {
      "change": "Add context:fork to frontmatter",
      "benefit": "Isolated execution prevents context pollution",
      "effort": 1
    }
  ],
  "triggeredBy": "GAP-xxx",
  "totalImpact": 3,
  "totalEffort": 2
}
```

### Step 5: Brainstorm — Workflow Compositions

Look at the full Shipkit pipeline and consider:

1. **Which skill sequences could be automated with teams?**
   - spec → plan → implement is already covered by `/shipkit-team`
   - What about: scout → analyst → ideator → plan → implement?
   - What about: feedback-bug → spec → plan → implement → verify?

2. **Which skills work better in parallel than serial?**
   - Multiple reviewers with different lenses
   - Multiple researchers evaluating options
   - Multiple implementers on different file clusters

3. **What team templates are missing?**
   - Compare against `install/skills/shipkit-team/references/TEAM-TEMPLATES.md`
   - Are there common workflows not covered?

For each composition idea:
```json
{
  "type": "workflow-composition",
  "name": "Descriptive name",
  "pipeline": ["skill-a", "skill-b", "skill-c"],
  "parallelSteps": [["skill-b", "skill-c"]],
  "teamTemplate": "Template description if applicable",
  "triggeredBy": "Workflow gap observation",
  "impact": 4,
  "effort": 3,
  "sketch": "How the composition works"
}
```

### Step 6: Brainstorm — Architecture Patterns

Consider broader framework improvements:

1. **Are there new CC primitives that change how Shipkit should be structured?**
   - New agent capabilities → rethink agent roles?
   - New hook events → new quality gates?
   - New settings options → new configuration patterns?

2. **Are there cross-cutting concerns?**
   - All skills could benefit from pattern X
   - The hook system could be extended with Y
   - The `.shipkit/` context model could evolve

For each architecture idea:
```json
{
  "type": "architecture-pattern",
  "name": "Pattern name",
  "scope": "framework-wide|skills|agents|hooks|settings",
  "description": "What the pattern is",
  "affectedComponents": ["List of affected files/systems"],
  "triggeredBy": "CC evolution or gap observation",
  "impact": 5,
  "effort": 4,
  "sketch": "Implementation approach",
  "risks": "What could go wrong"
}
```

### Step 7: Score and Rank

For all opportunities:

1. **Impact** (1-5): How much does this improve Shipkit?
   - 5 = Enables entirely new capability
   - 4 = Significantly improves existing workflow
   - 3 = Noticeable improvement for users
   - 2 = Minor quality-of-life improvement
   - 1 = Cosmetic or marginal

2. **Effort** (1-5): How hard is this to implement?
   - 1 = Single file change, < 1 hour
   - 2 = 2-3 files, < half day
   - 3 = 4-6 files, ~1 day
   - 4 = Major feature, multi-day
   - 5 = Architecture change, multi-week

3. **Priority Score** = Impact / Effort (higher = do first)

4. **Rank all opportunities by priority score**

### Step 8: Write Opportunities Report

Write `docs/development/opportunities.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "opportunities-report",
  "version": "1.0",
  "generatedAt": "2026-02-20T...",
  "source": "shipkit-ideator",
  "basedOn": {
    "analystReport": "docs/development/analyst-report.json",
    "analyzedAt": "2026-02-20T...",
    "ccVersion": "2.1.34"
  },
  "summary": {
    "totalOpportunities": 15,
    "byType": {
      "new-skill": 4,
      "skill-improvement": 6,
      "workflow-composition": 3,
      "architecture-pattern": 2
    },
    "topPriority": {
      "name": "Highest priority opportunity",
      "score": 2.5,
      "type": "skill-improvement"
    },
    "quickWins": 5,
    "majorInvestments": 2
  },
  "opportunities": [
    {
      "id": "OPP-001",
      "type": "new-skill|skill-improvement|workflow-composition|architecture-pattern",
      "name": "...",
      "impact": 4,
      "effort": 2,
      "priorityScore": 2.0,
      "category": "quick-win|standard|major-investment",
      "... type-specific fields ...": "..."
    }
  ],
  "quickWins": ["OPP-001", "OPP-003"],
  "roadmap": {
    "immediate": ["OPP-001", "OPP-002"],
    "shortTerm": ["OPP-005", "OPP-008"],
    "longTerm": ["OPP-012", "OPP-015"]
  }
}
```

### Step 9: Present Summary

After writing the report, present a human-readable summary:

```
## Shipkit Improvement Opportunities

Based on CC v{version} analysis:

### Quick Wins (high impact, low effort)
1. OPP-001: {name} — Impact: 4, Effort: 1 → Score: 4.0
2. OPP-003: {name} — Impact: 3, Effort: 1 → Score: 3.0

### Standard Improvements
3. OPP-005: {name} — Impact: 4, Effort: 3 → Score: 1.3

### Major Investments
4. OPP-012: {name} — Impact: 5, Effort: 4 → Score: 1.25

### Suggested Roadmap
- **Now**: Quick wins (OPP-001, OPP-003)
- **Next sprint**: Standard improvements (OPP-005, OPP-008)
- **Later**: Major investments (OPP-012)

Ready to plan implementation? Run `/shipkit-plan` with any opportunity.
```

---

## Output Quality Checklist

Before writing the report, verify:
- [ ] Every opportunity passes the Skill Value Test
- [ ] No duplicate ideas (check against previous `opportunities.json`)
- [ ] Impact/effort scores are justified, not arbitrary
- [ ] Each opportunity has a concrete `sketch` (not vague)
- [ ] `triggeredBy` traces back to specific analyst finding or gap
- [ ] Quick wins are genuinely quick (effort 1-2)
- [ ] Major investments have `risks` documented
- [ ] Roadmap is realistic (not everything in "immediate")

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-analyst` — Produces the gap analysis this skill reads
  - **Trigger**: Analyst report must exist
  - **Why**: Ideation needs to be grounded in actual gaps, not speculation

### After This Skill
- `/shipkit-plan` — Plan implementation of a chosen opportunity
  - **Trigger**: User selects an opportunity to implement
  - **Why**: Opportunities need concrete implementation plans
- `/shipkit-spec` — Spec out a new skill opportunity
  - **Trigger**: User selects a "new-skill" type opportunity
  - **Why**: New skills need proper specification before building

### Team Composition
In a self-improvement team:
- **Scout** runs first (intelligence gathering)
- **Analyst** runs second (gap mapping)
- **Ideator** runs third (this skill — opportunity generation)
- Output feeds into normal Shipkit workflow: spec → plan → implement

---

## Context Files This Skill Reads

- `docs/development/analyst-report.json` — Gap analysis (required)
- `docs/development/scout-report.json` — Raw CC findings (additional context)
- `docs/development/opportunities.json` — Previous opportunities (dedup)
- `docs/development/SHIPKIT-DESIGN-PHILOSOPHY.md` — Design principles
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards
- `CLAUDE.md` — Skill Value Test and framework rules
- `install/skills/shipkit-team/references/TEAM-TEMPLATES.md` — Existing team templates

## Context Files This Skill Writes

- `docs/development/opportunities.json` — Ranked opportunity cards

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--focus new-skills` | Only brainstorm new skill ideas |
| `--focus improvements` | Only improve existing skills |
| `--focus compositions` | Only workflow composition ideas |
| `--focus all` | All dimensions (default) |
| `--top 5` | Only output top 5 by priority score |
| `--top 10` | Output top 10 (default) |
