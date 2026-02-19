---
name: shipkit-analyst
description: Maps Claude Code changes to Shipkit gaps. Reads scout report and audits all skills, agents, hooks, and settings against current CC capabilities. Identifies deprecated patterns, missing features, and update opportunities. Use after running shipkit-scout.
argument-hint: "[--scope skills|agents|hooks|all] [--severity critical|all]"
---

# shipkit-analyst - Shipkit Gap Analyst

**Purpose**: Map Claude Code evolution against Shipkit's current state to find gaps, risks, and opportunities

**What it does**:
- Reads the scout report (`docs/development/scout-report.json`)
- Audits every skill, agent, hook, and settings file against scout findings
- Produces a structured gap analysis at `docs/development/analyst-report.json`
- Categorizes findings by severity: critical (breaking), warning (deprecated), info (opportunity)

---

## When to Invoke

**User says:**
- "Analyze gaps"
- "Run the analyst"
- "What needs updating in Shipkit?"
- "Map CC changes to our skills"
- "Check for deprecated patterns"

**Automated trigger:**
- After `/shipkit-scout` produces a new report
- As the second step of a Shipkit self-improvement team

---

## Prerequisites

**Required**:
- `docs/development/scout-report.json` exists (run `/shipkit-scout` first)

**Helpful context**:
- Previous analyst report at `docs/development/analyst-report.json`
- Framework integrity state at `.claude/skills/shipkit-framework-integrity/.integrity-state.json`

---

## Process

### Step 1: Load Scout Report

Read `docs/development/scout-report.json`. Extract:
- `findings.newFeatures` — new CC capabilities
- `findings.breakingChanges` — things that may break Shipkit
- `findings.deprecations` — patterns Shipkit should migrate away from
- `findings.newPatterns` — emerging patterns Shipkit could adopt
- `docsIndex.keyChanges` — per-page changes in CC docs

### Step 2: Inventory Shipkit Components

Scan the framework to build a component inventory:

**Skills** — Read all `install/skills/shipkit-*/SKILL.md`:
- Extract frontmatter fields used
- Extract tools/features referenced in the skill body
- Note which CC features each skill relies on

**Agents** — Read all `install/agents/shipkit-*.md`:
- Extract frontmatter fields used (model, permissionMode, memory, tools, etc.)
- Note which CC agent features each uses

**Hooks** — Read all `install/shared/hooks/*.py`:
- Extract hook events referenced
- Note stdin schema expectations
- Check exit code patterns

**Settings** — Read `install/settings/shipkit.settings.json`:
- Extract all permission patterns
- Extract hook event registrations
- Extract env vars

**Manifest** — Read `install/profiles/shipkit.manifest.json`:
- Extract skill/agent/MCP registrations

### Step 3: Cross-Reference — Breaking Changes

For each breaking change in scout report:

1. Search all Shipkit components for the affected pattern
2. If found, mark as **CRITICAL**:
   ```
   {
     "severity": "critical",
     "type": "breaking-change",
     "ccChange": "Removed X in v2.2.0",
     "affectedComponents": [
       {"file": "install/skills/shipkit-spec/SKILL.md", "line": 45, "usage": "Uses X in frontmatter"},
       {"file": "install/agents/shipkit-implementer-agent.md", "line": 12, "usage": "References X"}
     ],
     "migrationAction": "Replace X with Y",
     "effort": "low|medium|high"
   }
   ```

### Step 4: Cross-Reference — Deprecations

For each deprecation in scout report:

1. Search all Shipkit components for the deprecated pattern
2. If found, mark as **WARNING**:
   ```
   {
     "severity": "warning",
     "type": "deprecation",
     "ccChange": "X deprecated in favor of Y",
     "affectedComponents": [...],
     "migrationAction": "Replace X with Y",
     "deadline": "v3.0 (estimated)",
     "effort": "low|medium|high"
   }
   ```

### Step 5: Cross-Reference — New Features

For each new feature in scout report:

1. Check if any Shipkit component already uses it
2. If not, assess relevance:
   - **Which skills could benefit?** — Match feature category to skill purpose
   - **Which agents could benefit?** — Match to agent role
   - **Is it a new hook event?** — Could Shipkit register for it?
   - **Is it a new settings field?** — Should Shipkit configure it?

3. Mark as **INFO** with opportunity details:
   ```
   {
     "severity": "info",
     "type": "feature-opportunity",
     "ccFeature": "New memory field on agents",
     "relevantComponents": [
       {"file": "install/agents/shipkit-implementer-agent.md", "reason": "Could persist implementation patterns"},
       {"file": "install/agents/shipkit-researcher-agent.md", "reason": "Could persist research findings"}
     ],
     "potentialBenefit": "Agents remember patterns across sessions",
     "adoptionEffort": "low"
   }
   ```

### Step 6: Cross-Reference — Patterns

For each new pattern from scout report:

1. Check if Shipkit already follows this pattern
2. If not, assess whether Shipkit should adopt it
3. Mark as **INFO** with pattern details

### Step 7: Skill Coverage Analysis

For each skill, produce a coverage assessment:

```json
{
  "skill": "shipkit-spec",
  "ccFeaturesUsed": ["skills", "frontmatter.name", "frontmatter.description"],
  "ccFeaturesAvailable": ["context:fork", "memory", "hooks in frontmatter"],
  "coverageScore": 0.6,
  "missingOpportunities": [
    "Could use context:fork for isolated spec generation",
    "Could use hooks to auto-validate spec format"
  ]
}
```

### Step 8: Write Analyst Report

Write `docs/development/analyst-report.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "analyst-report",
  "version": "1.0",
  "analyzedAt": "2026-02-20T...",
  "source": "shipkit-analyst",
  "basedOn": {
    "scoutReport": "docs/development/scout-report.json",
    "scoutedAt": "2026-02-20T...",
    "ccVersion": "2.1.34"
  },
  "summary": {
    "critical": 1,
    "warnings": 3,
    "opportunities": 12,
    "skillsCoverage": {
      "average": 0.72,
      "lowest": {"skill": "shipkit-implement-independently", "score": 0.4},
      "highest": {"skill": "shipkit-team", "score": 0.95}
    },
    "totalComponents": {
      "skills": 39,
      "agents": 9,
      "hooks": 5,
      "settings": 1
    }
  },
  "findings": [
    {
      "id": "GAP-001",
      "severity": "critical|warning|info",
      "type": "breaking-change|deprecation|feature-opportunity|pattern-adoption",
      "title": "Short description",
      "ccChange": "What changed in CC",
      "affectedComponents": [...],
      "migrationAction": "What to do",
      "effort": "low|medium|high",
      "priority": 1
    }
  ],
  "skillCoverage": [
    {
      "skill": "shipkit-spec",
      "ccFeaturesUsed": [...],
      "ccFeaturesAvailable": [...],
      "coverageScore": 0.6,
      "missingOpportunities": [...]
    }
  ]
}
```

---

## Output Quality Checklist

Before writing the report, verify:
- [ ] Scout report was read and parsed completely
- [ ] ALL skills in `install/skills/` were audited (not just a sample)
- [ ] ALL agents in `install/agents/` were audited
- [ ] ALL hooks in `install/shared/hooks/` were audited
- [ ] Each finding has a concrete `migrationAction` (not vague)
- [ ] `effort` estimates are realistic (low = 1 file, medium = 2-5 files, high = 6+ files)
- [ ] No duplicate findings
- [ ] Findings are sorted by priority (critical first)
- [ ] Coverage scores are based on actual feature counts, not guesses

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-scout` — Produces the scout report this skill reads
  - **Trigger**: Scout report must exist
  - **Why**: Analyst maps CC changes against Shipkit — needs to know what changed

### After This Skill
- `/shipkit-ideator` — Reads analyst report, brainstorms opportunities
  - **Trigger**: Analyst report written with gaps/opportunities
  - **Why**: Gaps need to be turned into actionable improvement ideas
- `/shipkit-framework-integrity` — Can validate fixes after analyst identifies issues
  - **Trigger**: After implementing fixes from analyst findings
  - **Why**: Ensures fixes don't break other things

### Team Composition
In a self-improvement team:
- **Scout** runs first
- **Analyst** reads scout output (this skill)
- **Ideator** reads analyst output
- Findings can feed into `/shipkit-plan` for implementation

---

## Context Files This Skill Reads

- `docs/development/scout-report.json` — Scout findings (required)
- `docs/development/analyst-report.json` — Previous analyst report (for diffing)
- `install/skills/shipkit-*/SKILL.md` — All skill definitions
- `install/agents/shipkit-*.md` — All agent definitions
- `install/shared/hooks/*.py` — All hook scripts
- `install/settings/shipkit.settings.json` — Framework settings
- `install/profiles/shipkit.manifest.json` — Framework manifest

## Context Files This Skill Writes

- `docs/development/analyst-report.json` — Structured gap analysis report

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--scope skills` | Only audit skills |
| `--scope agents` | Only audit agents |
| `--scope hooks` | Only audit hooks |
| `--scope all` | Full audit (default) |
| `--severity critical` | Only report critical/breaking issues |
| `--severity all` | Report all severities (default) |
