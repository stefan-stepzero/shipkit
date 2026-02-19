---
name: shipkit-scout
description: Fetches latest Claude Code documentation, changelog, and GitHub issues to detect new features, breaking changes, and community patterns. Writes a structured scout report for downstream analysis. Use when checking what's new in Claude Code.
argument-hint: "[--full] [--quick] [--sources github,docs,issues]"
---

# shipkit-scout - Claude Code Intelligence Scout

**Purpose**: Detect what's new, changed, or emerging in Claude Code so Shipkit can stay current

**What it does**:
- Fetches Claude Code docs from `code.claude.com/docs/llms.txt` index
- Fetches CHANGELOG.md from GitHub repo
- Scans recent GitHub issues for patterns and feature requests
- Produces a structured `docs/development/scout-report.json` with categorized findings

---

## When to Invoke

**User says:**
- "What's new in Claude Code?"
- "Scout for changes"
- "Check Claude Code updates"
- "Run the scout"
- "Any new CC features?"

**Automated trigger:**
- As the first step of a Shipkit self-improvement team
- When `docs/development/scout-report.json` is older than 7 days
- Before running `/shipkit-analyst`

---

## Prerequisites

**Required**:
- Internet access (fetches from code.claude.com and GitHub)
- `gh` CLI authenticated (for GitHub API calls)

**Helpful context**:
- Previous scout report at `docs/development/scout-report.json`
- Claude Code changelog at `docs/development/claude-code-changelog.md`
- Changelog metadata at `docs/development/claude-code-changelog.meta.json`

---

## Process

### Step 0: Check Previous Report

Read `docs/development/scout-report.json` if it exists. Note the `scoutedAt` timestamp and `latestVersion` to identify what's new since the last run.

### Step 1: Fetch Documentation Index

Fetch `https://code.claude.com/docs/llms.txt` to get the full list of documentation pages.

**Priority pages to fetch** (most relevant to Shipkit):

| Page | Why |
|------|-----|
| `skills.md` | Skill authoring spec — frontmatter fields, behavior |
| `sub-agents.md` | Task tool, agent types, subagent patterns |
| `hooks.md` | Hook events, exit codes, input schema |
| `hooks-guide.md` | Hook best practices, patterns |
| `agent-teams.md` | Team primitives, coordination |
| `settings.md` | Settings schema, permissions |
| `permissions.md` | Permission model, allow/deny |
| `plugins.md` | Plugin system |
| `plugins-reference.md` | Plugin API reference |
| `memory.md` | Auto-memory, memory files |
| `features-overview.md` | Feature catalog |
| `best-practices.md` | Official best practices |
| `changelog.md` | Latest changes |

**For `--quick` mode**: Only fetch `changelog.md`, `skills.md`, `hooks.md`, `agent-teams.md`.

**For `--full` mode**: Fetch all pages listed in llms.txt.

For each page, use WebFetch with a structured extraction prompt:

```
Extract from this Claude Code documentation page:
1. Feature names and descriptions
2. Any configuration fields/schema
3. Any breaking changes or deprecations
4. Any new capabilities since {previous_version}
5. Code examples showing usage patterns

Return as structured JSON with: features[], breakingChanges[], deprecations[], examples[]
```

### Step 2: Fetch Changelog

Run the existing fetch script or directly fetch:

```bash
gh api repos/anthropics/claude-code/contents/CHANGELOG.md \
  --jq '.content' | base64 -d
```

Parse changelog entries. For each version since `latestVersion` from previous report:
- Extract new features
- Extract breaking changes
- Extract bug fixes
- Extract new tool/hook/event names

### Step 3: Scan GitHub Issues (Optional, `--sources issues`)

Use `gh` CLI to fetch recent issues:

```bash
gh issue list --repo anthropics/claude-code --limit 50 --state all --json title,body,labels,createdAt,closedAt
```

Categorize issues by:
- **Feature requests** — what users want
- **Bug reports** — what's broken
- **Discussions** — emerging patterns and use cases
- **Labels** — official categorization

### Step 4: Diff Against Previous Report

Compare current findings against previous `scout-report.json`:
- **New features** — not in previous report
- **Changed features** — spec or behavior changed
- **Removed features** — deprecated or removed
- **New patterns** — from issues/discussions

### Step 5: Write Scout Report

Write `docs/development/scout-report.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "scout-report",
  "version": "1.0",
  "scoutedAt": "2026-02-20T...",
  "source": "shipkit-scout",
  "latestVersion": "2.1.34",
  "previousVersion": "2.1.33",
  "summary": {
    "newFeatures": 5,
    "breakingChanges": 1,
    "deprecations": 2,
    "newPatterns": 3,
    "issueInsights": 8
  },
  "findings": {
    "newFeatures": [
      {
        "name": "Feature name",
        "version": "2.1.34",
        "category": "skills|hooks|agents|settings|tools|other",
        "description": "What it does",
        "docsPage": "skills.md",
        "relevanceToShipkit": "high|medium|low",
        "relevanceReason": "Why this matters for Shipkit"
      }
    ],
    "breakingChanges": [
      {
        "name": "Change name",
        "version": "2.1.34",
        "description": "What broke",
        "migrationPath": "How to fix",
        "affectsShipkit": true,
        "affectedFiles": ["install/skills/..."]
      }
    ],
    "deprecations": [
      {
        "name": "Deprecated thing",
        "version": "2.1.34",
        "replacement": "What to use instead",
        "deadline": "When it's removed (if known)"
      }
    ],
    "newPatterns": [
      {
        "name": "Pattern name",
        "source": "docs|issues|changelog",
        "description": "What the pattern is",
        "exampleCode": "..."
      }
    ],
    "issueInsights": [
      {
        "title": "Issue title",
        "url": "https://github.com/...",
        "category": "feature-request|bug|discussion",
        "relevance": "Why this matters for Shipkit"
      }
    ]
  },
  "docsIndex": {
    "fetchedPages": ["skills.md", "hooks.md", "..."],
    "totalAvailable": 57,
    "keyChanges": {
      "skills.md": ["New frontmatter field: X"],
      "hooks.md": ["New hook event: Y"]
    }
  }
}
```

### Step 6: Update Changelog Cache

If changelog was fetched, update:
- `docs/development/claude-code-changelog.md` — full changelog
- `docs/development/claude-code-changelog.meta.json` — timestamp and version

---

## Output Quality Checklist

Before writing the report, verify:
- [ ] All priority docs pages fetched (or errors noted)
- [ ] Changelog parsed with version-by-version breakdown
- [ ] Each finding has `relevanceToShipkit` assessment
- [ ] Breaking changes include `affectedFiles` list
- [ ] No duplicate findings across categories
- [ ] `summary` counts match actual findings arrays
- [ ] Previous version correctly identified for diffing

---

## When This Skill Integrates with Others

### Before This Skill
- None — Scout is the entry point for the intelligence pipeline

### After This Skill
- `/shipkit-analyst` — Reads scout report, maps findings to Shipkit gaps
  - **Trigger**: Scout report written with new findings
  - **Why**: Findings need to be mapped against actual Shipkit codebase

### Team Composition
In a self-improvement team:
- **Scout** runs first (this skill)
- **Analyst** reads scout output
- **Ideator** reads analyst output
- Can be orchestrated by `/shipkit-team` or run manually in sequence

---

## Context Files This Skill Reads

- `docs/development/scout-report.json` — Previous scout report (for diffing)
- `docs/development/claude-code-changelog.md` — Cached changelog
- `docs/development/claude-code-changelog.meta.json` — Cache freshness

## Context Files This Skill Writes

- `docs/development/scout-report.json` — Structured findings report
- `docs/development/claude-code-changelog.md` — Updated changelog cache
- `docs/development/claude-code-changelog.meta.json` — Updated cache metadata

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--quick` | Changelog + 4 key docs pages only |
| `--full` | All 57 docs pages + issues + changelog |
| `--sources github` | GitHub only (changelog + issues) |
| `--sources docs` | Documentation pages only |
| `--sources issues` | GitHub issues only |
| (default) | Changelog + priority docs pages |
