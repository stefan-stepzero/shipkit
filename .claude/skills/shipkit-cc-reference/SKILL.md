---
name: shipkit-cc-reference
description: Fetches latest Claude Code documentation on skills, agents, hooks, and settings, then synthesizes it into maintained coding reference files. Merges official docs with DOC-023 empirical test results. Use when CC reference docs are stale or before authoring new skills/agents.
argument-hint: "[--domain skills|agents|hooks|settings|all] [--quick] [--diff]"
---

# shipkit-cc-reference - CC Primitives Reference Builder

**Purpose**: Maintain up-to-date, practical coding references for Claude Code primitives by fetching official docs, merging with empirically confirmed behaviors, and writing synthesized reference files.

**Why this exists**: Claude's training data lags behind CC releases. Official docs are spread across multiple pages. Empirical test results (DOC-023) live in a separate file. This skill merges all sources into domain-specific coding guides that other skills can reference.

---

## When to Invoke

**User says:**
- "Update the CC reference docs"
- "Refresh the skills/agents reference"
- "What's the latest CC frontmatter spec?"
- "Sync CC docs"

**Before:**
- Authoring a new skill or agent
- Running `/shipkit-dev-spec` for a framework change
- After a CC version upgrade

---

## Inputs

**Required**: None (fetches from web)

**Reads**:
- `docs/development/cc-reference/synthesized/*.md` — previous synthesized files (for diffing)
- `docs/development/cc-reference/synthesized/cc-reference.meta.json` — last run metadata
- `docs/development/cc-reference/DOC-023-pipeline-test-report.md` — empirical test results

**Arguments**:
- `--domain <name>` — Only refresh one domain: `skills`, `agents`, `hooks`, or `settings`. Default: `all`
- `--quick` — Fetch only primary doc page per domain (faster, 4 pages total)
- `--diff` — Show what changed since last synthesis without rewriting files

---

## Outputs

**Writes**:
- `docs/development/cc-reference/synthesized/skills-reference.md`
- `docs/development/cc-reference/synthesized/agents-reference.md`
- `docs/development/cc-reference/synthesized/hooks-reference.md`
- `docs/development/cc-reference/synthesized/settings-reference.md`
- `docs/development/cc-reference/synthesized/cc-reference.meta.json`

These files are gitignored (inside `docs/development/`) and available as references for other dev skills.

---

## Process

### Step 0: Parse Arguments & Load State (Inline)

1. Parse `--domain`, `--quick`, `--diff` from user input. Defaults: domain=all, quick=false, diff=false
2. Read `docs/development/cc-reference/synthesized/cc-reference.meta.json` if it exists — extract `synthesizedAt` and `ccVersion`
3. Read `docs/development/cc-reference/DOC-023-pipeline-test-report.md` — this is REQUIRED for merge. If missing, note all behaviors as "unverified"
4. Determine which domains to process

### Step 1: Fetch CC Documentation (Parallel Agents)

Launch one Agent per domain being refreshed. Each agent is `subagent_type: "general-purpose"` with `model: "sonnet"`.

For `--quick` mode, launch a single agent that fetches all primary pages.

**IMPORTANT**: Launch all agents simultaneously in a single message.

Each agent fetches pages via WebFetch and extracts structured content.

---

#### Skills Domain Agent

**Pages to fetch**:
- Primary: `https://code.claude.com/docs/en/skills.md`
- Secondary (skip in --quick): `https://code.claude.com/docs/en/best-practices.md`

**Prompt**:
```
Fetch Claude Code skills documentation. For each page use WebFetch.

Pages:
1. https://code.claude.com/docs/en/skills.md
2. https://code.claude.com/docs/en/best-practices.md (skip if told --quick)

For each page, extract with this WebFetch prompt:
"Extract ALL technical details about Claude Code Skills:
1. Complete frontmatter field reference (field name, type, required?, default, description)
2. SKILL.md file structure and conventions
3. File organization (references/, scripts/, examples/ subdirectories)
4. How and when skills are loaded into context
5. Context window budget and size constraints
6. Invocation patterns (user-invocable, model-invocable, disable-model-invocation)
7. Code examples showing skill frontmatter and structure
8. Any warnings, gotchas, or anti-patterns mentioned
Return as structured text with clear section headers."

Return a combined SKILLS_DOCS report with these sections:
- FRONTMATTER_FIELDS: [field, type, required, default, description, example]
- FILE_STRUCTURE: how SKILL.md and subdirectories work
- CONTEXT_LOADING: when/how skills are loaded, budget rules
- INVOCATION: user-invocable vs model, triggering
- EXAMPLES: code blocks from docs
- WARNINGS: gotchas, anti-patterns
```

---

#### Agents Domain Agent

**Pages to fetch**:
- Primary: `https://code.claude.com/docs/en/sub-agents.md`
- Primary: `https://code.claude.com/docs/en/agent-teams.md`
- Secondary (skip in --quick): `https://code.claude.com/docs/en/cli-reference.md` (for --agents flag)

**Prompt**:
```
Fetch Claude Code subagents and agent teams documentation. For each page use WebFetch.

Pages:
1. https://code.claude.com/docs/en/sub-agents.md
2. https://code.claude.com/docs/en/agent-teams.md
3. https://code.claude.com/docs/en/cli-reference.md (skip if told --quick; only extract --agents flag section)

For each page, extract with this WebFetch prompt:
"Extract ALL technical details about Claude Code agents/subagents:
1. Agent file format — complete frontmatter fields (field, type, required?, default, description)
2. Built-in agent types (Explore, Plan, general-purpose) with their tools and models
3. Custom agent configuration options
4. context: fork — what it isolates, what it shares
5. Tool restrictions — tools field, disallowedTools field, how enforcement works
6. Agent Teams — TeamCreate, TaskCreate, teammate patterns
7. Model selection — aliases, inherit, defaults
8. Resumable agents — how resume works
9. CLI --agents flag JSON format
10. Code examples showing agent files and invocation
Return as structured text with clear section headers."

Return a combined AGENTS_DOCS report with these sections:
- FRONTMATTER_FIELDS: [field, type, required, default, description]
- BUILTIN_AGENTS: [name, model, tools, purpose]
- FORK_BEHAVIOR: what context:fork does and doesn't isolate
- TOOL_RESTRICTIONS: how tools/disallowedTools work
- AGENT_TEAMS: team primitives and patterns
- MODEL_SELECTION: aliases, inherit, defaults
- RESUME: how resumable agents work
- CLI_FORMAT: --agents flag JSON schema
- EXAMPLES: code blocks from docs
- WARNINGS: gotchas
```

---

#### Hooks Domain Agent

**Pages to fetch**:
- Primary: `https://code.claude.com/docs/en/hooks.md`
- Secondary (skip in --quick): `https://code.claude.com/docs/en/hooks-guide.md`

**Prompt**:
```
Fetch Claude Code hooks documentation. For each page use WebFetch.

Pages:
1. https://code.claude.com/docs/en/hooks.md
2. https://code.claude.com/docs/en/hooks-guide.md (skip if told --quick)

For each page, extract with this WebFetch prompt:
"Extract ALL technical details about Claude Code hooks:
1. All hook event types (PreToolUse, PostToolUse, Notification, Stop, SubagentStart, ConfigChange, TeammateIdle, TaskCompleted, etc.)
2. Hook configuration format in settings.json
3. Input schema for each event type (what fields are available)
4. Exit codes and their effects (0=allow, 1=warn, 2=block, etc.)
5. Hook matching patterns (tool_name matchers)
6. Environment variables available to hooks
7. Code examples (bash scripts, Python hooks)
8. Any warnings or limitations
Return as structured text with clear section headers."

Return a combined HOOKS_DOCS report with these sections:
- EVENT_TYPES: [event, description, when_fired]
- CONFIG_FORMAT: settings.json hook configuration schema
- INPUT_SCHEMAS: [event, fields available in stdin JSON]
- EXIT_CODES: [code, meaning, effect]
- MATCHING: how tool_name patterns work
- ENV_VARS: environment variables in hook context
- EXAMPLES: code blocks from docs
- WARNINGS: gotchas, limitations
```

---

#### Settings Domain Agent

**Pages to fetch**:
- Primary: `https://code.claude.com/docs/en/settings.md`
- Primary: `https://code.claude.com/docs/en/permissions.md`
- Secondary (skip in --quick): `https://code.claude.com/docs/en/memory.md`

**Prompt**:
```
Fetch Claude Code settings and permissions documentation. For each page use WebFetch.

Pages:
1. https://code.claude.com/docs/en/settings.md
2. https://code.claude.com/docs/en/permissions.md
3. https://code.claude.com/docs/en/memory.md (skip if told --quick)

For each page, extract with this WebFetch prompt:
"Extract ALL technical details about Claude Code settings and permissions:
1. settings.json file locations and precedence order
2. Complete settings.json schema (all fields with types and defaults)
3. Permission modes (default, acceptEdits, bypassPermissions, plan, dontAsk, ignore)
4. Allowed tools patterns — wildcards, Bash() patterns, MCP tool patterns
5. CLAUDE.md structure and loading behavior
6. @path imports in CLAUDE.md
7. .claude/rules/*.md with YAML paths frontmatter for path-scoping
8. Environment variables (experimental flags, configuration)
9. Auto-memory system
10. Code examples
Return as structured text with clear section headers."

Return a combined SETTINGS_DOCS report with these sections:
- FILE_LOCATIONS: settings file paths and precedence
- SCHEMA: [field, type, default, description]
- PERMISSION_MODES: [mode, description, behavior]
- ALLOWED_TOOLS: pattern syntax and examples
- CLAUDE_MD: structure, @path imports, loading
- RULES: .claude/rules/ format and path-scoping
- ENV_VARS: experimental flags, configuration vars
- MEMORY: auto-memory system
- EXAMPLES: code blocks from docs
- WARNINGS: gotchas
```

---

### Step 2: Read DOC-023 (Inline)

Read the full `docs/development/cc-reference/DOC-023-pipeline-test-report.md`.

Organize confirmed behaviors by domain:
- **Skills domain**: skill loading, context behavior, Skill tool dispatch
- **Agents domain**: fork isolation, tool restrictions, nesting, Agent tool blocked, teams
- **Hooks domain**: settings.json hook propagation, frontmatter hooks silently ignored
- **Settings domain**: permissionMode in forks, env vars

### Step 3: Synthesize Per Domain (Inline)

For each domain, write a synthesized markdown reference file following this template:

```markdown
# {Domain} Reference — Claude Code vX.Y.Z

> Synthesized from official CC docs + DOC-023 empirical tests. Generated by shipkit-cc-reference.
> Last updated: {ISO date} | CC version: {version}

## Field Reference

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| ... | ... | ... | ... | ... |

## {Section per domain-specific topic}

### Official Behavior
{What CC docs say}

### Confirmed Behavior (DOC-023)
{What empirical tests confirmed — with test ID references}

### Gotchas
{Surprises, inconsistencies, things that don't work as documented}

## Code Examples

{Practical examples — frontmatter, file structure, configuration}

## Quick Reference

{Cheat-sheet style summary for fast lookup}
```

**Synthesis rules**:
1. Official docs are authoritative for **field definitions** (names, types, defaults)
2. DOC-023 is authoritative for **behavioral confirmations** (what actually works)
3. When docs and DOC-023 conflict, include BOTH and flag the conflict: `> CONFLICT: Docs say X, but DOC-023 test {ID} found Y`
4. Features from docs not tested in DOC-023: mark as `[untested]`
5. Behaviors in DOC-023 not mentioned in docs: mark as `[undocumented]`
6. Keep it practical — field tables, code examples, gotchas. Not a tutorial

### Step 4: Write Outputs (Inline)

Write each domain's synthesized reference to its output file.

Write metadata sidecar `docs/development/cc-reference/synthesized/cc-reference.meta.json`:

```json
{
  "synthesizedAt": "2026-...",
  "ccVersion": "X.Y.Z",
  "generator": "shipkit-cc-reference",
  "domains": {
    "skills": {
      "pagesUsed": ["best-practices", "overview"],
      "doc023Sections": ["T1: Agent Frontmatter", "T2: Pipeline Delegation"],
      "fieldCount": N,
      "lastChanged": "2026-..."
    },
    "agents": { ... },
    "hooks": { ... },
    "settings": { ... }
  },
  "previousRun": null
}
```

### Step 5: Diff Report (Inline)

If `--diff` mode: read existing synthesized files and compare with newly fetched content. Report changes without writing.

For normal mode: compare against previous run's metadata to show what changed.

Present summary:

```
## CC Reference Updated — vX.Y.Z

### Domains Refreshed
- Skills: {N} fields, {N} examples ({changed/unchanged} since last run)
- Agents: {N} fields, {N} examples
- Hooks: {N} events, {N} examples
- Settings: {N} fields, {N} examples

### Conflicts Found
- {any doc vs DOC-023 conflicts}

### Untested Features
- {features from docs not in DOC-023}

Reference files written to docs/development/cc-reference/synthesized/
```

---

## --diff Mode

When `--diff` is passed:
1. Fetch docs as normal
2. Compare against existing synthesized files
3. Report what would change (new fields, removed fields, changed descriptions)
4. Do NOT write any files

---

## Error Handling

- **WebFetch fails**: Use existing synthesized files if available, note staleness in output. If no existing files, report which domains could not be fetched
- **DOC-023 missing**: Synthesize from docs only, mark all behavioral notes as `[unverified — DOC-023 not found]`
- **URL changed**: If a specific page 404s, fetch `https://code.claude.com/docs/llms.txt` to find updated URLs. All docs are at `https://code.claude.com/docs/en/{page}.md`

---

## Integration

### Upstream
- `shipkit-scout` — optional, can run first to update changelog cache
- DOC-023 — always read for behavioral confirmations

### Downstream
- All dev skills that author skills/agents reference these synthesized files
- `shipkit-dev-spec` — can read synthesized refs when speccing new skills
- `shipkit-framework-integrity` — can validate against current CC spec

### As References for Other Skills
The synthesized files in `docs/development/cc-reference/synthesized/` can be read by any dev skill that needs CC primitive reference material. Point skills to read these files rather than maintaining their own CC knowledge.

---

## Output Quality Checklist

- [ ] All requested domains have synthesized reference files
- [ ] Field tables are complete (every frontmatter/config field from docs)
- [ ] DOC-023 confirmed behaviors are merged with correct test IDs
- [ ] Conflicts between docs and DOC-023 are flagged explicitly
- [ ] Untested features are marked `[untested]`
- [ ] Undocumented behaviors are marked `[undocumented]`
- [ ] Code examples are practical and copy-pasteable
- [ ] Metadata sidecar reflects actual content
- [ ] Quick reference section exists per domain
