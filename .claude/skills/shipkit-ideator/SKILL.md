---
name: shipkit-ideator
description: Brainstorms improvement opportunities across 4 parallel dimensions — new skills, skill improvements, workflow compositions, and architecture patterns. Produces ranked opportunity cards with effort/impact scores. Use after running shipkit-analyst.
argument-hint: "[--focus new-skills|improvements|compositions|all] [--top N]"
---

# shipkit-ideator - Shipkit Opportunity Ideator

**Purpose**: Turn gap analysis into actionable improvement ideas across 4 parallel brainstorm dimensions

**What it does**: Dispatches 4 parallel Sonnet agents:
- **New skills agent** — Brainstorms skills enabled by new CC features
- **Improvements agent** — Identifies upgrades for existing low-coverage skills
- **Compositions agent** — Discovers workflow automation and team patterns
- **Architecture agent** — Spots framework-wide structural improvements

Then scores all opportunities on impact vs effort and produces a prioritized roadmap.

---

## When to Invoke

**User says:**
- "What should we build next?"
- "Brainstorm improvements"
- "Run the ideator"
- "Suggest new skills"

**Automated trigger:**
- After `/shipkit-analyst` produces a new report
- As the third step of a Shipkit self-improvement team

---

## Prerequisites

**Required**:
- `docs/development/dev-progress/DOC-003-analyst-report.json` exists (run `/shipkit-analyst` first)

**Helpful context**:
- `docs/development/dev-progress/DOC-002-scout-report.json` — Raw CC findings
- `docs/development/dev-progress/DOC-004-opportunities.json` — Previous opportunities (dedup)

---

## Process

### Step 0: Load Context (Inline)

Read these files:
1. `docs/development/dev-progress/DOC-003-analyst-report.json` — Gap analysis (required)
2. `docs/development/dev-progress/DOC-002-scout-report.json` — Raw CC findings
3. `docs/development/dev-progress/DOC-004-opportunities.json` — Previous opportunities (dedup)
4. `CLAUDE.md` — Skill Value Test (the fundamental filter)

Extract from analyst report:
- All `info` findings (feature opportunities)
- All `warning` findings (deprecation migrations)
- `skillCoverage` array
- `summary.skillsCoverage.lowest`

Prepare a shared context block containing: the Skill Value Test rule, the findings summary, and the list of existing skills/agents (from manifest).

### Step 1: Dispatch 4 Parallel Agents

Launch ALL 4 agents simultaneously using the Agent tool. Each is `subagent_type: "general-purpose"` with `model: "sonnet"`.

**IMPORTANT**: Launch all 4 in a single message with 4 parallel Agent tool calls. Pass the shared context block to each.

---

#### Agent 1: New Skills Brainstorm

**Prompt:**
```
Brainstorm new Shipkit skills based on these Claude Code feature opportunities and gaps.

SKILL VALUE TEST (every idea MUST pass):
A skill is valuable if it: (1) Forces human decisions to be explicit, OR (2) Creates persistence Claude lacks.
A skill is redundant if Claude does it well without instruction (debugging, implementing, testing).

Current Shipkit skills (don't duplicate):
{list from manifest}

Feature opportunities from analyst:
{paste info findings}

Coverage gaps (lowest-scoring skills):
{paste lowest 5 from skillCoverage}

For each new skill idea, consider:
1. Does this CC feature enable a skill that passes the Value Test?
2. Are there workflow gaps — missing handoffs, lost context, manual steps?
3. Are there team composition patterns that need skills?

For each idea, produce:
{
  "type": "new-skill",
  "name": "shipkit-{proposed-name}",
  "category": "Vision|Planning|Knowledge|Execution|Quality|System",
  "description": "What it does",
  "valueTestResult": "Forces explicit: X / Creates persistence: Y",
  "triggeredBy": "GAP-xxx from analyst",
  "ccFeatures": ["features it would use"],
  "impact": 1-5,
  "effort": 1-5,
  "sketch": "2-3 sentence implementation approach"
}

Return 3-8 ideas. Quality over quantity — every idea must clearly pass the Value Test.
```

---

#### Agent 2: Skill Improvements Brainstorm

**Prompt:**
```
Identify improvements for existing Shipkit skills based on coverage gaps and analyst findings.

Coverage data:
{paste skillCoverage array — focus on lowest scoring}

Analyst findings (deprecations + opportunities):
{paste warning + info findings}

Available CC features that skills could use:
- context: fork (agent isolation)
- agent: (agent persona binding)
- memory: (cross-session persistence)
- hooks: (lifecycle hooks in frontmatter)
- allowed-tools / disallowedTools (tool restrictions)
- model: (model selection)

For each skill with low coverage or relevant analyst finding:
1. What CC features is it not using that it could benefit from?
2. What deprecated patterns does it use that should be migrated?
3. What new capabilities could enhance its output?

For each improvement:
{
  "type": "skill-improvement",
  "skill": "shipkit-{name}",
  "currentCoverage": 0.X,
  "proposedCoverage": 0.X,
  "improvements": [{"change": "...", "benefit": "...", "effort": 1-5}],
  "triggeredBy": "GAP-xxx",
  "totalImpact": 1-5,
  "totalEffort": 1-5
}

Return improvements for all skills with coverage < 0.7 or with relevant analyst findings.
```

---

#### Agent 3: Workflow Compositions Brainstorm

**Prompt:**
```
Discover workflow automation and team composition opportunities for Shipkit.

Current skill pipeline: Scout → Analyst → Ideator → Spec → Plan → Implement → Verify
Current team templates (read install/skills/shipkit-team/references/TEAM-TEMPLATES.md)

Consider:
1. What skill sequences could be automated with teams?
   - spec → plan → implement is already covered
   - What about: scout → analyst → ideator → plan → implement?
   - What about: feedback-bug → spec → plan → implement → verify?

2. Which skills work better in parallel than serial?
   - Multiple reviewers with different lenses
   - Multiple researchers evaluating options
   - Multiple implementers on different file clusters

3. What team templates are missing?
   - Compare against existing templates
   - Are there common workflows not covered?

For each composition idea:
{
  "type": "workflow-composition",
  "name": "Descriptive name",
  "pipeline": ["skill-a", "skill-b", "skill-c"],
  "parallelSteps": [["skill-b", "skill-c"]],
  "teamTemplate": "Template description",
  "triggeredBy": "Workflow gap observation",
  "impact": 1-5,
  "effort": 1-5,
  "sketch": "How it works"
}

Return 2-5 ideas.
```

---

#### Agent 4: Architecture Patterns Brainstorm

**Prompt:**
```
Identify framework-wide structural improvements for Shipkit.

Current architecture:
- 37 skills in install/skills/ (orchestrator + producer + review gateway types)
- 12 agents in install/agents/ (4 orchestrators + 5 producers + 3 reviewers)
- 4 hooks in install/shared/hooks/
- Settings, manifest, rules files
- .shipkit/ context directory for user projects

Analyst findings:
{paste all findings}

Consider:
1. Are there new CC primitives that change how Shipkit should be structured?
   - New agent capabilities → rethink agent roles?
   - New hook events → new quality gates?
   - New settings options → new configuration patterns?
   - Plugin system → should Shipkit be a plugin?

2. Are there cross-cutting improvements?
   - All skills could benefit from pattern X
   - The hook system could be extended
   - The .shipkit/ context model could evolve
   - Better crash recovery patterns

For each idea:
{
  "type": "architecture-pattern",
  "name": "Pattern name",
  "scope": "framework-wide|skills|agents|hooks|settings",
  "description": "What the pattern is",
  "affectedComponents": ["file/system list"],
  "triggeredBy": "CC evolution or gap observation",
  "impact": 1-5,
  "effort": 1-5,
  "sketch": "Implementation approach",
  "risks": "What could go wrong"
}

Return 2-4 ideas. Only high-impact structural improvements, not cosmetic changes.
```

---

### Step 2: Score & Rank (Inline)

After all 4 agents return:

1. **Collect all opportunities** from all 4 agents
2. **Apply Skill Value Test filter** — reject any that don't pass
3. **Deduplicate** against previous `DOC-004-opportunities.json`
4. **Calculate priority score** = Impact / Effort (higher = do first)
5. **Categorize**:
   - Quick wins: effort 1-2, impact 3+
   - Standard: effort 3, any impact
   - Major investments: effort 4-5
6. **Rank by priority score** within each category

### Step 3: Write Opportunities Report (Inline)

Write `docs/development/dev-progress/DOC-004-opportunities.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "opportunities-report",
  "version": "2.0",
  "generatedAt": "2026-...",
  "source": "shipkit-ideator",
  "basedOn": {
    "analystReport": "docs/development/dev-progress/DOC-003-analyst-report.json",
    "ccVersion": "X.Y.Z"
  },
  "summary": {
    "totalOpportunities": N,
    "byType": {
      "new-skill": N,
      "skill-improvement": N,
      "workflow-composition": N,
      "architecture-pattern": N
    },
    "quickWins": N,
    "majorInvestments": N
  },
  "opportunities": [
    {
      "id": "OPP-001",
      "type": "...",
      "name": "...",
      "impact": N,
      "effort": N,
      "priorityScore": N.N,
      "category": "quick-win|standard|major-investment",
      "...type-specific fields..."
    }
  ],
  "roadmap": {
    "immediate": ["OPP-001", ...],
    "shortTerm": ["OPP-005", ...],
    "longTerm": ["OPP-012", ...]
  }
}
```

### Step 4: Present Summary (Inline)

```
## Improvement Opportunities — CC v{version}

**Agents**: 4 parallel (new-skills, improvements, compositions, architecture)

### Quick Wins (high impact, low effort)
1. OPP-001: {name} — Impact: {N}, Effort: {N} → Score: {N.N}

### Standard Improvements
2. OPP-005: {name} — Impact: {N}, Effort: {N}

### Major Investments
3. OPP-012: {name} — Impact: {N}, Effort: {N}

### Roadmap
- **Now**: Quick wins
- **Next**: Standard improvements
- **Later**: Major investments

Ready to plan? Run `/shipkit-dev-spec` with any opportunity.
```

---

## Output Quality Checklist

- [ ] Every opportunity passes the Skill Value Test
- [ ] No duplicates against previous opportunities
- [ ] Impact/effort scores are justified
- [ ] Each has concrete `sketch` (not vague)
- [ ] `triggeredBy` traces to analyst finding
- [ ] Quick wins are genuinely quick (effort 1-2)
- [ ] Major investments have `risks` documented

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-analyst` — Produces the gap analysis this skill reads

### After This Skill
- `/shipkit-dev-spec` — Spec out a chosen opportunity
- `/shipkit-dev-plan` — Plan implementation

### Team Composition
Scout → Analyst → **Ideator** → Dev-Spec → Dev-Plan → Dev-Team

---

## Context Files This Skill Reads

**Inline**: analyst report, scout report, previous opportunities, CLAUDE.md
**Agent 3**: also reads team templates reference file

## Context Files This Skill Writes

- `docs/development/dev-progress/DOC-004-opportunities.json` — Ranked opportunity cards

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--focus new-skills` | Only dispatch Agent 1 |
| `--focus improvements` | Only dispatch Agent 2 |
| `--focus compositions` | Only dispatch Agent 3 |
| `--focus all` | All 4 dimensions (default) |
| `--top 5` | Only output top 5 by priority score |
| `--top 10` | Output top 10 (default) |
