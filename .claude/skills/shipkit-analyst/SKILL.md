---
name: shipkit-analyst
description: Maps Claude Code changes to Shipkit gaps. Dispatches 5 parallel agents to cross-reference scout findings against skills, agents, hooks, settings, and coverage. Identifies deprecated patterns, missing features, and update opportunities. Use after running shipkit-scout.
argument-hint: "[--scope skills|agents|hooks|all] [--severity critical|all]"
---

# shipkit-analyst - Shipkit Gap Analyst

**Purpose**: Map Claude Code evolution against Shipkit's current state to find gaps, risks, and opportunities

**What it does**: Dispatches 5 parallel Sonnet agents for cross-referencing:
- **Breaking changes agent** — Scans all components for patterns that are now broken
- **Deprecations agent** — Finds deprecated patterns still in use
- **Features agent** — Identifies new CC features Shipkit could adopt
- **Patterns agent** — Checks emerging patterns against Shipkit conventions
- **Coverage agent** — Produces per-skill coverage scores

Then aggregates, ranks by severity, and writes structured gap analysis.

---

## When to Invoke

**User says:**
- "Analyze gaps"
- "Run the analyst"
- "What needs updating in Shipkit?"
- "Map CC changes to our skills"

**Automated trigger:**
- After `/shipkit-scout` produces a new report
- As the second step of a Shipkit self-improvement team

---

## Prerequisites

**Required**:
- `docs/development/dev-progress/DOC-002-scout-report.json` exists (run `/shipkit-scout` first)

---

## Process

### Step 0: Load Scout Report (Inline)

Read `docs/development/dev-progress/DOC-002-scout-report.json`. Extract:
- `findings.newFeatures` — new CC capabilities
- `findings.breakingChanges` — things that may break Shipkit
- `findings.deprecations` — patterns to migrate away from
- `findings.undocumentedFeatures` — experimental capabilities
- `docsIndex.keyChanges` — per-page changes

Also read previous analyst report if it exists for diffing.

### Step 1: Dispatch 5 Parallel Agents

Launch ALL 5 agents simultaneously using the Agent tool. Each is `subagent_type: "general-purpose"` with `model: "sonnet"`.

**IMPORTANT**: Launch all 5 in a single message with 5 parallel Agent tool calls. Pass the relevant scout findings to each agent in its prompt.

---

#### Agent 1: Breaking Changes Scanner

**Prompt:**
```
Search the Shipkit framework at P:\Projects2\sg-shipkit for patterns affected by these Claude Code breaking changes:

{paste breakingChanges array from scout report}

For each breaking change:
1. Search ALL files in install/skills/shipkit-*/SKILL.md for the affected pattern
2. Search ALL files in install/agents/shipkit-*.md
3. Search install/shared/hooks/*.py
4. Search install/settings/shipkit.settings.json

For each match found, report:
- severity: "critical"
- file path and line number
- what the file uses that's now broken
- suggested migration action
- effort estimate (low=1 file, medium=2-5, high=6+)

Return:
BREAKING_CHANGES:
  totalMatches: N
  findings: [{severity, file, line, usage, ccChange, migrationAction, effort}]
  noMatchFound: [list of breaking changes with no Shipkit impact]
```

---

#### Agent 2: Deprecation Scanner

**Prompt:**
```
Search the Shipkit framework at P:\Projects2\sg-shipkit for deprecated Claude Code patterns:

{paste deprecations array from scout report}

For each deprecation:
1. Search install/skills/shipkit-*/SKILL.md for the deprecated pattern
2. Search install/agents/shipkit-*.md
3. Search install/shared/hooks/*.py
4. Search install/settings/shipkit.settings.json

Also scan for these known deprecated patterns regardless of scout report:
- ".claude.json" references (removed v2.0.8)
- "includeCoAuthoredBy" (deprecated v2.0.62)
- Legacy permission formats

For each match, report:
- severity: "warning"
- file, line, current usage
- replacement pattern
- deadline (if known)
- effort estimate

Return:
DEPRECATIONS:
  totalMatches: N
  findings: [{severity, file, line, currentUsage, replacement, deadline, effort}]
```

---

#### Agent 3: New Features Mapper

**Prompt:**
```
Check which new Claude Code features the Shipkit framework could adopt.

New features from scout report:
{paste newFeatures array}

For each feature:
1. Check if ANY Shipkit component already uses it (grep install/ for the feature name/pattern)
2. If not used, assess which components could benefit:
   - Which skills could use this feature?
   - Which agents could use this feature?
   - Is it a new hook event Shipkit should register for?
   - Is it a new settings field Shipkit should configure?

Read install/profiles/shipkit.manifest.json to understand all components.
Sample 5-10 representative SKILL.md files to understand current feature usage.

For each opportunity, report:
- severity: "info"
- feature name and CC version
- relevant Shipkit components (file paths)
- potential benefit description
- adoption effort estimate

Return:
FEATURE_OPPORTUNITIES:
  totalOpportunities: N
  alreadyAdopted: [features Shipkit already uses]
  opportunities: [{severity, ccFeature, version, relevantComponents[], benefit, effort}]
```

---

#### Agent 4: Pattern Scanner

**Prompt:**
```
Check emerging Claude Code patterns against Shipkit conventions.

Patterns from scout report:
{paste newPatterns/undocumentedFeatures arrays}

For each pattern:
1. Check if Shipkit follows this pattern already
2. If not, assess whether Shipkit should adopt it
3. Check if any Shipkit skill or agent contradicts this pattern

Also check these cross-cutting concerns:
- Do any skills reference tools that no longer exist?
- Do any agents use frontmatter fields that aren't in the CC spec?
- Are hook event names in settings.json all valid?
- Are permission string formats all valid?

Return:
PATTERNS:
  adopted: [patterns Shipkit already follows]
  shouldAdopt: [{pattern, reason, affectedComponents[], effort}]
  conflicts: [{pattern, conflictingFile, issue}]
  crossCuttingIssues: [{type, file, issue, suggestion}]
```

---

#### Agent 5: Coverage Scorer

**Prompt:**
```
Produce a coverage score for each Shipkit skill against available Claude Code features.

1. Read install/profiles/shipkit.manifest.json to get the full skill list
2. For each skill, read its SKILL.md and check which CC features it uses:
   - context: fork (agent isolation)
   - agent: (agent persona)
   - memory: (cross-session persistence)
   - allowed-tools: / disallowedTools: (tool restrictions)
   - model: (model selection)
   - disable-model-invocation: (infrastructure skill)
   - argument-hint: (CLI hint)
   - user-invocable: (visibility control)
   - paths: (file path scoping, supports YAML list of globs)
   - description: (skill description for model matching)
   - initialPrompt: (auto-submit first turn for agents)
   - skills: (preload specific skills in agents)
   - background: (run agent in background)
   - maxTurns: (agent turn budget)

3. Calculate coverage = features_used / features_available
   Where features_available = features relevant to this skill type

4. Identify the 5 lowest-scoring skills

Return:
COVERAGE:
  totalSkills: N
  averageCoverage: 0.XX
  skills: [{skill, featuresUsed[], featuresAvailable[], coverage, missingOpportunities[]}]
  lowest5: [{skill, coverage, topMissing}]
  highest5: [{skill, coverage}]
```

---

### Step 2: Aggregate & Rank (Inline)

After all 5 agents return:

1. **Merge all findings** into a single list
2. **Assign IDs**: GAP-001, GAP-002, etc.
3. **Sort by severity**: critical → warning → info
4. **Within severity, sort by effort** (low effort first = quick wins)
5. **Deduplicate** findings that appear in multiple agent results

### Step 3: Write Analyst Report (Inline)

Write `docs/development/dev-progress/DOC-003-analyst-report.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "analyst-report",
  "version": "2.0",
  "analyzedAt": "2026-...",
  "source": "shipkit-analyst",
  "basedOn": {
    "scoutReport": "docs/development/dev-progress/DOC-002-scout-report.json",
    "scoutedAt": "...",
    "ccVersion": "X.Y.Z"
  },
  "summary": {
    "critical": N,
    "warnings": N,
    "opportunities": N,
    "skillsCoverage": {
      "average": 0.XX,
      "lowest": {"skill": "...", "score": 0.X},
      "highest": {"skill": "...", "score": 0.X}
    }
  },
  "findings": [
    {
      "id": "GAP-001",
      "severity": "critical|warning|info",
      "type": "breaking-change|deprecation|feature-opportunity|pattern-adoption",
      "title": "Short description",
      "ccChange": "What changed in CC",
      "affectedComponents": [{file, line, usage}],
      "migrationAction": "What to do",
      "effort": "low|medium|high",
      "priority": 1
    }
  ],
  "skillCoverage": [...]
}
```

### Step 4: Present Summary (Inline)

```
## Gap Analysis — CC v{version}

**Agents**: 5 parallel (breaking, deprecations, features, patterns, coverage)

### Critical ({N})
- GAP-001: {title} — {affectedComponents count} files, effort: {effort}

### Warnings ({N})
- GAP-00X: {title}

### Opportunities ({N})
- GAP-00X: {title} — {benefit}

### Coverage
- Average: {X}% | Lowest: {skill} ({X}%) | Highest: {skill} ({X}%)

Ready for ideation? Run `/shipkit-ideator`
```

---

## Output Quality Checklist

- [ ] Scout report was fully parsed
- [ ] ALL skills audited (not just a sample) — coverage agent reads all
- [ ] ALL agents audited — breaking/deprecation agents grep all
- [ ] Each finding has concrete `migrationAction`
- [ ] Effort estimates are realistic
- [ ] No duplicate findings across agents
- [ ] Findings sorted by priority

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-scout` — Produces the scout report this skill reads

### After This Skill
- `/shipkit-ideator` — Reads analyst report, brainstorms opportunities

---

## Context Files This Skill Reads

**Agent 1-2 read**: scout report + all skill/agent/hook/settings files
**Agent 3 reads**: scout report + manifest + sample SKILL.md files
**Agent 4 reads**: scout report + all component files
**Agent 5 reads**: manifest + all SKILL.md files

## Context Files This Skill Writes

- `docs/development/dev-progress/DOC-003-analyst-report.json` — Structured gap analysis

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--scope skills` | Only audit skills |
| `--scope agents` | Only audit agents |
| `--scope hooks` | Only audit hooks |
| `--scope all` | Full audit (default) |
| `--severity critical` | Only report critical/breaking issues |
