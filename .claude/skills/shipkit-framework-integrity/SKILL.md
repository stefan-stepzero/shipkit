---
name: shipkit-framework-integrity
description: Validates Shipkit framework integrity before release. Dispatches 5 parallel agents for manifest sync, references, installer/hooks, documentation, and agent cross-refs. Use when preparing releases or after refactoring.
argument-hint: "[--full] [--quick] [--fix] [--loop N]"
---

# shipkit-framework-integrity - Framework Integrity Checker

**Purpose**: Validate the Shipkit framework repo is internally consistent and ready for release

**What it does**: Dispatches 5 parallel Sonnet agents for fast, token-efficient validation:
- Manifest ↔ disk sync (skills, agents)
- Broken file references in all SKILL.md files
- Hook and installer integrity
- Documentation counts and accuracy
- Agent cross-references from skill frontmatter

---

## When to Invoke

**User says:**
- "Check framework integrity"
- "Validate repo before release"
- "Are there broken references?"
- "Audit shipkit repo"
- "Pre-release check"

**Use when:**
- Before publishing to GitHub
- After aggressive refactoring or culling
- After adding/removing skills
- During release preparation

---

## Prerequisites

**Required**:
- Running from Shipkit framework repo root
- `install/skills/` directory exists
- `install/profiles/shipkit.manifest.json` exists

---

## Process

### Step 0: Pre-checks (Inline — Before Dispatching Agents)

Run these quick checks inline before dispatching agents:

**VERSION file:**
```
1. Read VERSION — if missing → ERROR
2. Read package.json version — if mismatch → ERROR
3. Check git tag: git describe --tags --abbrev=0 2>/dev/null
   If tag exists and doesn't match VERSION → WARNING
```

**Changelog freshness (optional — skip if docs/development/ doesn't exist):**
```
1. Read docs/development/cc-reference/claude-code-changelog.meta.json
2. If missing or fetchedAt > 7 days old → run: bash docs/development/cc-reference/fetch-changelog.sh
```

### Step 1: Dispatch 5 Parallel Agents

Launch ALL 5 agents simultaneously using the Agent tool. Each agent is `subagent_type: "general-purpose"` with `model: "sonnet"`. Each returns a structured text report.

**IMPORTANT**: Launch all 5 in a single message with 5 parallel Agent tool calls.

---

#### Agent 1: Manifest & Naming Sync

**Prompt:**
```
Check manifest ↔ disk sync for the Shipkit framework at P:\Projects2\sg-shipkit.

SKILLS:
1. List all directories: install/skills/shipkit-*/
2. Read install/profiles/shipkit.manifest.json
3. Extract all skill names (skills.mandatory[] + skills.optional[*][].name)
4. Report orphan skills (on disk, not in manifest) and ghost skills (in manifest, not on disk)

AGENTS:
1. List all files: install/agents/shipkit-*.md
2. Extract agent names from manifest agents section (object with orchestrators/producers/reviewers keys)
3. Report orphan/ghost agents

NAMING:
1. Check orchestrator skills use shipkit-orch-* prefix (dir name AND name: field)
2. Check review gateway skills use shipkit-review-* prefix
3. Check orchestrator agents use shipkit-orch-* prefix
4. Check reviewer agents use shipkit-reviewer-* prefix
5. Search for bare "shipkit-direction", "shipkit-planning", "shipkit-shipping" (without orch-) in install/ — report any found

Report format:
MANIFEST_SYNC:
  skills_disk: N
  skills_manifest: N
  orphan_skills: [list or "none"]
  ghost_skills: [list or "none"]
  agents_disk: N
  agents_manifest: N
  orphan_agents: [list or "none"]
  ghost_agents: [list or "none"]
NAMING:
  errors: [list or "none"]
```

---

#### Agent 2: Broken References

**Prompt:**
```
Scan ALL SKILL.md files in install/skills/shipkit-*/ for broken file references.

For EACH skill:
1. Read the SKILL.md file
2. Find LOCAL references: pattern references/something.md (without prefix)
   → Check exists at {skill_dir}/references/{file}
3. Find SHARED references: pattern shared/references/something.md
   → Check exists at install/shared/references/{file}
4. Find CROSS-SKILL references: pattern shipkit-{name}/references/something.md
   → Check exists at install/skills/shipkit-{name}/references/{file}

Skip: URLs (http/https), placeholder paths ({variable}), .shipkit/ paths (user project templates)

Report format:
BROKEN_REFERENCES:
  total_skills_scanned: N
  total_refs_found: N
  broken: [list with skill name, ref type, missing path — or "none"]
```

---

#### Agent 3: Hooks & Installer Integrity

**Prompt:**
```
Validate hooks and installer integrity for Shipkit at P:\Projects2\sg-shipkit.

HOOKS:
1. Check these required hooks exist in install/shared/hooks/:
   - shipkit-session-start.py
   - shipkit-track-skill-usage.py
   - shipkit-task-completed-hook.py
   - shipkit-teammate-idle-hook.py
2. Report any missing

INSTALLER PATHS:
1. Check these paths exist:
   install/shared, install/shared/hooks, install/skills, install/agents,
   install/settings, install/claude-md, install/profiles, docs/generated
2. Check CLI paths exist:
   cli/bin/shipkit.js, cli/src/index.js, cli/src/init.js, cli/src/update.js,
   cli/src/hooks.js, cli/src/settings.js, VERSION, package.json

HOOK COVERAGE:
1. List all .py files in install/shared/hooks/
2. Read cli/src/init.js — find HOOK_FILES mapping (maps source → destination names)
3. Check each hook on disk is in HOOK_FILES
4. Report any hooks that exist on disk but the CLI won't install

SETTINGS CONSISTENCY:
1. Read install/settings/shipkit.settings.json
2. Read cli/src/hooks.js — find buildHooksConfig
3. Check that hook events and commands are consistent between them
4. Check package.json version matches VERSION file

Report format:
HOOKS:
  required_present: N/4
  missing: [list or "none"]
INSTALLER:
  paths_ok: true/false
  missing_paths: [list or "none"]
HOOK_COVERAGE:
  hooks_on_disk: N
  hooks_in_cli: N
  uncovered: [list or "none"]
SETTINGS:
  version_match: true/false
  hook_consistency: [issues or "ok"]
```

---

#### Agent 4: Documentation Counts & Permissions

**Prompt:**
```
Check documentation counts and settings permissions for Shipkit at P:\Projects2\sg-shipkit.

COUNTS:
1. Read install/profiles/shipkit.manifest.json — count total skills and agents (source of truth)
2. Read README.md — find ALL skill/agent count claims (sync markers AND plain text like "33 skill definitions")
3. Read CLAUDE.md — find skill count claims
4. Read package.json — check description for count claims
5. Read docs/generated/shipkit-overview.html — check stat-number spans for skill/agent counts
6. Report any mismatches

PERMISSIONS:
1. Read install/settings/shipkit.settings.json
2. Extract all Skill() entries from permissions.allow
3. Compare to manifest skill list
4. Report skills missing Skill() permission or extra Skill() without manifest entry

7-FILE INTEGRATION (spot check):
1. Read install/rules/shipkit.md — check each manifest skill appears as /shipkit-{name}
2. Report skills missing from rules file

Report format:
COUNTS:
  manifest_skills: N
  manifest_agents: N
  mismatches: [list with file, claimed, actual — or "none"]
PERMISSIONS:
  total_permissions: N
  missing: [list or "none"]
  extra: [list or "none"]
RULES_COVERAGE:
  missing_from_rules: [list or "none"]
```

---

#### Agent 5: Agent Cross-References & Frontmatter

**Prompt:**
```
Validate agent cross-references and frontmatter in Shipkit at P:\Projects2\sg-shipkit.

AGENT FILE VALIDATION:
1. For each .md file in install/agents/shipkit-*:
   - Check file is non-empty
   - Check it starts with --- (YAML frontmatter)
   - Extract name: field
   - Report any issues

SKILL → AGENT CROSS-REFS:
1. For each SKILL.md in install/skills/shipkit-*/:
   - Check if frontmatter contains "agent:" field
   - If yes, extract the agent name
   - Check install/agents/{agent-name}.md exists
   - Report any broken references

AGENT → SKILL CROSS-REFS:
1. For each agent in install/agents/shipkit-*:
   - Grep for skill references (patterns like skill: "shipkit-*" or /shipkit-*)
   - Check referenced skills exist as directories in install/skills/
   - Report broken references

Report format:
AGENT_FILES:
  total: N
  valid: N
  issues: [list or "none"]
SKILL_TO_AGENT:
  skills_with_agent: N
  broken: [list with skill name and missing agent — or "none"]
AGENT_TO_SKILL:
  broken: [list with agent name and missing skill — or "none"]
```

---

### Step 2: Collect & Aggregate Results

After all 5 agents return, aggregate their reports into a single integrity report.

**Count totals:**
- Errors: broken refs + orphan/ghost + missing permissions + broken agent refs + missing hooks
- Warnings: count mismatches + missing from rules + naming issues

### Step 3: Format & Display Report

```
============================================
SHIPKIT FRAMEWORK INTEGRITY REPORT
============================================
Timestamp: {now}
Mode: Parallel (5 agents)

MANIFEST ↔ DISK SYNC
─────────────────────
Skills on disk:     {N}
Skills in manifest: {N}
Agents on disk:     {N}
Agents in manifest: {N}
{orphan/ghost details or ✓ All synced}

NAMING CONVENTIONS
──────────────────
{naming errors or ✓ All consistent}

BROKEN REFERENCES
─────────────────
Skills scanned: {N}
References found: {N}
{broken details or ✓ All references valid}

HOOKS & INSTALLER
─────────────────
{hook/installer details or ✓ All valid}

DOCUMENTATION COUNTS
────────────────────
{mismatch details or ✓ All counts match}

SETTINGS PERMISSIONS
────────────────────
{missing/extra or ✓ All permissions present}

AGENT CROSS-REFERENCES
──────────────────────
{broken refs or ✓ All agent references valid}

============================================
SUMMARY
============================================
Errors:   {N}
Warnings: {N}

{error/warning list if any}

============================================
RESULT: {PASS or FAIL}
============================================
```

### Step 4: Handle --fix (If Requested)

If `--fix` was passed, attempt to auto-fix simple issues:
- Missing Skill() permissions → add to settings.json
- Count mismatches → update sync markers in README.md
- Orphan skills → prompt to add to manifest or remove from disk

Re-run the check after fixes to verify.

---

## Loop Mode

When invoked with `--loop N`, the skill runs iteratively — checking, fixing, and re-checking — until either zero errors/warnings remain or N iterations are exhausted.

**State file**: `.shipkit/framework-integrity-loop.local.md`

**Default completion promise**: "Framework integrity check reports zero errors and zero warnings"

**How it works**:
1. Parse `--loop N` from arguments (default N=3 if omitted)
2. Create state file with frontmatter (skill, iteration, max_iterations, completion_promise)
3. Run the normal integrity check (dispatch 5 agents)
4. Update the Progress section in the state file with findings and fixes applied
5. If zero errors and zero warnings → delete state file, report success, stop
6. If issues remain → end response; the relentless stop hook blocks exit and re-prompts

**Shared reference**: See `.claude/skills/_shared/loop-mode-reference.md` for state file format and protocol details.

---

## Validation Rules Summary

| Check | Severity | Agent | Description |
|-------|----------|-------|-------------|
| VERSION missing | ERROR | inline | VERSION file doesn't exist |
| VERSION invalid | ERROR | inline | VERSION file empty or not valid semver |
| VERSION/tag mismatch | WARNING | inline | VERSION doesn't match latest git tag |
| Orphan skill | ERROR | 1 | Skill directory exists but not in manifest |
| Ghost skill | ERROR | 1 | Skill in manifest but no directory |
| Naming violation | ERROR | 1 | Orch/review prefix missing or old names found |
| Broken reference | ERROR | 2 | SKILL.md references file that doesn't exist |
| Missing hook | ERROR | 3 | Required hook file missing |
| Hook not in installer | ERROR | 3 | Hook exists on disk but installer won't copy it |
| Installer path missing | ERROR | 3 | Path referenced by installer doesn't exist |
| Version mismatch (pkg) | ERROR | 3 | package.json version doesn't match VERSION |
| Missing permission | ERROR | 4 | Skill not in settings.json allow list |
| Count mismatch | WARNING | 4 | Doc counts don't match manifest |
| Missing from rules | WARNING | 4 | Skill not in rules/shipkit.md |
| Broken agent ref | ERROR | 5 | Skill references agent that doesn't exist |
| Invalid agent file | ERROR | 5 | Agent file empty or missing frontmatter |
| Broken skill ref in agent | WARNING | 5 | Agent references skill that doesn't exist |

---

## When This Skill Integrates with Others

### Before This Skill
- After refactoring skills or removing files
- After adding/removing skills or agents
- Before `git push` to main branch

### After This Skill
- Fix identified issues manually or with `--fix`
- Re-run with `--full` to verify fixes
- Proceed with release/commit

### Related Skills
- `shipkit-dev-spec` → `shipkit-dev-plan` — Design and plan new skills/changes
- `shipkit-dev-review` — Reviews changes for quality after implementation

---

## Context Files This Skill Reads

**Agent 1 reads**: manifest, skill dirs, agent files
**Agent 2 reads**: all SKILL.md files, reference/template files
**Agent 3 reads**: hook files, CLI source, settings, VERSION, package.json
**Agent 4 reads**: manifest, README, CLAUDE.md, package.json, HTML overview, settings, rules
**Agent 5 reads**: all agent files, all SKILL.md frontmatter

## Context Files This Skill Writes

**Write Strategy: STATE FILE ONLY**

- `.claude/skills/shipkit-framework-integrity/.integrity-state.json` — Caching state
- `.shipkit/framework-integrity-loop.local.md` — Loop mode state (only when `--loop N` used)

This skill does NOT modify source files unless `--fix` is used.
