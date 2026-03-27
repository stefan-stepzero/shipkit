---
name: shipkit-scout
description: Fetches latest Claude Code documentation, changelog, and source code patterns via 3 parallel agents. Detects new features, breaking changes, and emerging patterns. Writes a structured scout report for downstream analysis. Use when checking what's new in Claude Code.
argument-hint: "[--full] [--quick]"
---

# shipkit-scout - Claude Code Intelligence Scout

**Purpose**: Detect what's new, changed, or emerging in Claude Code so Shipkit can stay current

**What it does**: Dispatches 3 parallel Sonnet agents across different intelligence vectors:
- **Docs agent** — Fetches official documentation pages
- **Changelog agent** — Parses CHANGELOG.md from GitHub
- **Source agent** — Reads Claude Code source for actual tool definitions and patterns

Then aggregates findings, diffs against previous report, and writes structured output.

---

## When to Invoke

**User says:**
- "What's new in Claude Code?"
- "Scout for changes"
- "Check Claude Code updates"
- "Run the scout"

**Automated trigger:**
- As the first step of a Shipkit self-improvement team
- When `docs/development/dev-progress/DOC-002-scout-report.json` is older than 7 days
- Before running `/shipkit-analyst`

---

## Prerequisites

**Required**:
- Internet access (fetches from code.claude.com and GitHub)
- `gh` CLI authenticated (for GitHub API calls)

**Helpful context**:
- Previous scout report at `docs/development/dev-progress/DOC-002-scout-report.json`
- Claude Code changelog at `docs/development/cc-reference/claude-code-changelog.md`

---

## Process

### Step 0: Load Previous Report (Inline)

Read `docs/development/dev-progress/DOC-002-scout-report.json` if it exists. Extract `scoutedAt` and `latestVersion` to know what's new since last run. Store as `previous_version`.

### Step 1: Dispatch 3 Parallel Agents

Launch ALL 3 agents simultaneously using the Agent tool. Each is `subagent_type: "general-purpose"` with `model: "sonnet"`.

**IMPORTANT**: Launch all 3 in a single message with 3 parallel Agent tool calls.

---

#### Agent 1: Documentation Fetcher

**Prompt:**
```
Fetch Claude Code documentation from code.claude.com/docs to extract current feature specs.

1. Fetch https://code.claude.com/docs/llms.txt to get the page index
2. Fetch these priority pages (use WebFetch for each):
   - skills.md — skill frontmatter fields, behavior
   - sub-agents.md — Task tool, agent types, subagent patterns
   - hooks.md — hook events, exit codes, input schema
   - hooks-guide.md — hook best practices
   - agent-teams.md — team primitives, coordination
   - settings.md — settings schema, permissions
   - permissions.md — permission model
   - plugins.md — plugin system
   - plugins-reference.md — plugin API
   - memory.md — auto-memory, memory files
   - features-overview.md — feature catalog
   - best-practices.md — official best practices
   - tools-reference.md — built-in tools, parameters, permissions
   - channels.md — event channels system
   - channels-reference.md — channels API reference
   - cli-reference.md — CLI commands and flags
   - headless.md — programmatic/headless usage
   - scheduled-tasks.md — scheduled task system
   - web-scheduled-tasks.md — web-based scheduled tasks
   - env-vars.md — environment variables reference
   - permission-modes.md — permission mode details
   - model-config.md — model configuration

For --full mode, fetch ALL pages in llms.txt.
For --quick mode, only fetch: skills.md, hooks.md, agent-teams.md, tools-reference.md, changelog.md

For each page, extract with this WebFetch prompt:
"Extract from this Claude Code documentation:
1. Feature names and their configuration fields/schema
2. Breaking changes or deprecations
3. New capabilities
4. Code examples showing usage patterns
5. Plugin system changes
6. Channel/event system changes
7. Tool additions or parameter changes
Return as structured text: FEATURES, BREAKING_CHANGES, DEPRECATIONS, EXAMPLES sections"

Return a combined report:
DOCS_REPORT:
  pages_fetched: N
  features: [name, description, docsPage, configFields]
  breakingChanges: [description, docsPage]
  deprecations: [what, replacement, docsPage]
  examples: [pattern, docsPage, code]
```

---

#### Agent 2: Changelog Parser

**Prompt:**
```
Fetch and parse the Claude Code CHANGELOG.md from GitHub.

1. Run: gh api repos/anthropics/claude-code/contents/CHANGELOG.md --jq '.content' | base64 -d
   If that fails, try: bash docs/development/cc-reference/fetch-changelog.sh

2. Parse each version entry. For versions since {previous_version}:
   - Extract new features (with version number)
   - Extract breaking changes
   - Extract bug fixes relevant to skills/hooks/agents
   - Extract new tool names, hook events, or settings fields
   - Extract new plugin capabilities, channels features, or scheduled task changes

3. Identify the latest version number

Return:
CHANGELOG_REPORT:
  latestVersion: "X.Y.Z"
  previousVersion: "{previous_version}"
  versionsScanned: N
  newFeatures: [version, name, description, category (skills|hooks|agents|settings|tools|other)]
  breakingChanges: [version, description, migrationPath]
  deprecations: [version, what, replacement]
  newPrimitives: [version, type (tool|hook-event|setting|frontmatter-field), name, description]
```

---

#### Agent 3: Source Code Patterns

**Prompt:**
```
Examine Claude Code source code on GitHub to find actual tool definitions, hook schemas, and implementation patterns that may not be in docs yet.

1. Fetch key source files using gh api:
   gh api repos/anthropics/claude-code/contents/src --jq '.[].name' (explore structure)

   Look for files related to:
   - Tool definitions (what tools exist, their parameters)
   - Hook event definitions (what events are supported, their schemas)
   - Skill loading (how skills are parsed, what frontmatter fields are supported)
   - Agent/subagent spawning (how context:fork works, what fields are passed)
   - Settings schema (what keys are valid in settings.json)

2. For each interesting file, fetch its content:
   gh api repos/anthropics/claude-code/contents/{path} --jq '.content' | base64 -d

3. Extract patterns:
   - Undocumented frontmatter fields
   - Tool parameter schemas not in docs
   - Hook event payloads/schemas
   - Internal feature flags or experimental features
   - Permission string parsing patterns

Return:
SOURCE_REPORT:
  filesExamined: N
  undocumentedFeatures: [name, file, description]
  toolDefinitions: [toolName, parameters, file]
  hookSchemas: [eventName, inputFields, file]
  frontmatterFields: [field, type, default, file]
  experimentalFeatures: [name, featureFlag, file]
  patterns: [name, description, file, codeSnippet]
```

---

### Step 2: Aggregate & Diff (Inline)

After all 3 agents return:

1. **Merge findings** across all three vectors:
   - Features found in docs + changelog + source = high confidence
   - Features in source only = potentially undocumented/experimental
   - Features in docs but not source = possibly deprecated or moved

2. **Deduplicate** — same feature may appear in multiple vectors

3. **Diff against previous report**:
   - New features (not in previous report)
   - Changed features (spec or behavior changed)
   - Removed features (deprecated or removed)

4. **Assess relevance to Shipkit** for each finding:
   - high = directly affects skills, agents, hooks, or settings
   - medium = could enable new Shipkit capabilities
   - low = informational, no immediate action

### Step 3: Write Scout Report (Inline)

Write `docs/development/dev-progress/DOC-002-scout-report.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "scout-report",
  "version": "2.0",
  "scoutedAt": "2026-...",
  "source": "shipkit-scout",
  "latestVersion": "X.Y.Z",
  "previousVersion": "...",
  "vectors": ["docs", "changelog", "source"],
  "summary": {
    "newFeatures": N,
    "breakingChanges": N,
    "deprecations": N,
    "undocumentedFeatures": N,
    "pagesScanned": N,
    "sourceFilesExamined": N
  },
  "findings": {
    "newFeatures": [
      {
        "name": "Feature name",
        "version": "X.Y.Z",
        "category": "skills|hooks|agents|settings|tools|other",
        "description": "What it does",
        "vectors": ["docs", "changelog"],
        "confidence": "high|medium",
        "relevanceToShipkit": "high|medium|low",
        "relevanceReason": "Why this matters"
      }
    ],
    "breakingChanges": [...],
    "deprecations": [...],
    "undocumentedFeatures": [
      {
        "name": "Feature name",
        "sourceFile": "src/...",
        "description": "What it appears to do",
        "confidence": "low",
        "note": "Found in source only — may be internal/experimental"
      }
    ]
  },
  "docsIndex": {
    "fetchedPages": [...],
    "totalAvailable": N
  }
}
```

### Step 4: Update Changelog Cache (Inline)

If changelog was fetched, update:
- `docs/development/cc-reference/claude-code-changelog.md`
- `docs/development/cc-reference/claude-code-changelog.meta.json`

### Step 5: Present Summary (Inline)

```
## Scout Report — CC v{version}

**Vectors**: Docs ({N} pages) + Changelog ({N} versions) + Source ({N} files)

### Key Findings
- {N} new features ({N} high relevance)
- {N} breaking changes
- {N} deprecations
- {N} undocumented/experimental features

### High Relevance
1. {feature} — {description} (from {vectors})
2. ...

### Breaking Changes
1. {change} — {migration}

Ready for analysis? Run `/shipkit-analyst`
```

---

## Output Quality Checklist

- [ ] All 3 vectors returned results (or errors noted)
- [ ] Findings are deduplicated across vectors
- [ ] Each finding has `relevanceToShipkit` assessment
- [ ] Breaking changes include migration paths
- [ ] `summary` counts match actual findings arrays
- [ ] Previous version correctly identified for diffing
- [ ] Undocumented features clearly marked as low-confidence

---

## When This Skill Integrates with Others

### Before This Skill
- None — Scout is the entry point for the intelligence pipeline

### After This Skill
- `/shipkit-analyst` — Reads scout report, maps findings to Shipkit gaps

### Team Composition
In a self-improvement team: Scout → Analyst → Ideator → Plan → Implement

---

## Context Files This Skill Reads

- `docs/development/dev-progress/DOC-002-scout-report.json` — Previous report (for diffing)
- `docs/development/cc-reference/claude-code-changelog.md` — Cached changelog
- `docs/development/cc-reference/claude-code-changelog.meta.json` — Cache freshness

## Context Files This Skill Writes

- `docs/development/dev-progress/DOC-002-scout-report.json` — Structured findings report
- `docs/development/cc-reference/claude-code-changelog.md` — Updated changelog cache
- `docs/development/cc-reference/claude-code-changelog.meta.json` — Updated cache metadata

---

## Mode Variations

| Mode | What it does |
|------|-------------|
| `--quick` | Changelog + 4 key docs pages only, skip source |
| `--full` | All docs pages + full source exploration |
| (default) | Changelog + priority docs pages + key source files |
