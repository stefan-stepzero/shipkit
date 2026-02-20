---
name: shipkit-framework-integrity
description: Validates Shipkit framework integrity before release. Checks for broken references, manifest/disk sync, installer validity, hook references, cross-skill dependencies, documentation accuracy, and Claude Code changelog compatibility. Auto-fetches latest changelog and flags deprecated patterns, unknown hook events, and feature adoption gaps. Uses caching to skip unchanged files. Use when preparing releases or after refactoring.
argument-hint: "[--full] [--quick] [--fix] [--json] [--loop N]"
---

# shipkit-framework-integrity - Framework Integrity Checker

**Purpose**: Validate the Shipkit framework repo is internally consistent and ready for release

**What it does**: Comprehensive integrity validation with smart caching:
- Manifest ↔ disk sync (skills, agents)
- Broken file references in all SKILL.md files
- Cross-skill references validity
- Hook file references and syntax
- Installer integrity (paths, syntax)
- Documentation counts and accuracy
- Skips unchanged files since last check

---

## When to Invoke

**User says:**
- "Check framework integrity"
- "Validate repo before release"
- "Are there broken references?"
- "Audit shipkit repo"
- "Pre-release check"
- "Run integrity check"

**Use when:**
- Before publishing to GitHub
- After aggressive refactoring or culling
- After adding/removing skills
- When skills fail to load unexpectedly
- During release preparation

---

## Prerequisites

**Required**:
- Running from Shipkit framework repo root
- `install/skills/` directory exists
- `install/profiles/shipkit.manifest.json` exists

**Not required**:
- No external dependencies
- No API keys

---

## State File (Smart Caching)

**Location**: `.claude/skills/shipkit-framework-integrity/.integrity-state.json`

**Structure**:
```json
{
  "lastFullCheck": "2025-02-05T10:30:00Z",
  "lastVerifiedVersion": "2.1.34",
  "fileHashes": {
    "install/skills/shipkit-spec/SKILL.md": "sha256:abc123...",
    "install/skills/shipkit-plan/SKILL.md": "sha256:def456...",
    "installers/install.py": "sha256:789xyz..."
  },
  "lastResults": {
    "errors": 0,
    "warnings": 2,
    "skipped": 15
  }
}
```

**Caching Logic**:
1. On run, compute SHA-256 hash of each file
2. Compare to stored hash in state file
3. If unchanged → skip detailed validation, carry forward previous result
4. If changed → run full validation
5. Always re-check cross-cutting concerns (counts, manifest sync) since they depend on multiple files
6. Update state file after check

**Force full check**: Pass `--full` or delete state file

---

## Process

### Step 0a: Ensure Changelog Freshness (Always Run)

**Before running any checks, verify the Claude Code changelog is current.**

```
1. Check if docs/development/claude-code-changelog.meta.json exists
   If NOT exists → run: bash docs/development/fetch-changelog.sh

2. If exists, read fetchedAt timestamp
   If older than 7 days → run: bash docs/development/fetch-changelog.sh

3. Read latestVersion from meta.json
   Store as: claude_code_version (e.g., "2.1.34")
   Display: "Claude Code changelog: v{claude_code_version} (fetched {date})"
```

**Why**: Framework integrity includes alignment with Claude Code's evolving feature set. Stale changelog = blind spots.

---

### Step 0b: VERSION File Validation (Always Run)

**Check VERSION file exists and is valid**:
```
1. Verify VERSION exists
   If NOT exists:
     → ERROR: VERSION file missing (single source of truth for releases)

2. Read VERSION content, trim whitespace
   If empty or invalid semver:
     → ERROR: VERSION must contain valid semver (e.g., "1.3.0")

3. Check VERSION matches latest git tag (if tags exist):
   git describe --tags --abbrev=0 2>/dev/null
   If tag exists and doesn't match VERSION:
     → WARNING: VERSION ({version}) doesn't match latest git tag ({tag})
```

**Why this matters**: VERSION is the single source of truth. During installation:
- Written to `_shipkit` key in settings.json
- Inserted into CLAUDE.md markers

Stale VERSION = users get wrong version after update.

---

### Step 1: Load State & Compute Hashes

```python
import hashlib
import json
from pathlib import Path
from datetime import datetime

STATE_FILE = Path('.claude/skills/shipkit-framework-integrity/.integrity-state.json')

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"fileHashes": {}, "lastResults": {}}

def compute_hash(filepath):
    content = Path(filepath).read_bytes()
    return f"sha256:{hashlib.sha256(content).hexdigest()[:16]}"

def file_changed(filepath, state):
    current_hash = compute_hash(filepath)
    stored_hash = state.get("fileHashes", {}).get(str(filepath))
    return current_hash != stored_hash, current_hash
```

---

### Step 2: Inventory Collection

**Collect all skills on disk**:
```bash
ls -1d install/skills/shipkit-*/
```

**Collect all skills in manifest**:
Read `install/profiles/shipkit.manifest.json` and extract:
- `skills.mandatory[]`
- `skills.optional[*][].name`

**Collect all agents on disk**:
```bash
ls -1d install/agents/shipkit-*
```

**Collect all agents in manifest**:
Read `install/profiles/shipkit.manifest.json` → `agents[].name`

---

### Step 3: Manifest ↔ Disk Sync (Always Run)

**Check for orphan skills** (on disk but not in manifest):
```
For each skill directory in install/skills/shipkit-*/:
  If skill_name NOT in manifest.skills.mandatory AND NOT in manifest.skills.optional:
    → ERROR: Orphan skill "{skill_name}" exists on disk but not in manifest
```

**Check for ghost skills** (in manifest but not on disk):
```
For each skill in manifest:
  If no directory exists at install/skills/{skill_name}/:
    → ERROR: Ghost skill "{skill_name}" in manifest but no directory exists
```

**Check for orphan/ghost agents**: Same logic for `install/agents/`

---

### Step 4: Reference Validation in SKILL.md Files (Cached)

**For each skill, if SKILL.md changed since last check**:

**CRITICAL: There are THREE types of references. Handle each differently:**

| Type | Pattern Example | Resolves To | Common Use |
|------|-----------------|-------------|------------|
| **Local** | `references/foo.md` | `{skill}/references/foo.md` | Skill-specific docs |
| **Shared** | `shared/references/foo.md` | `install/shared/references/foo.md` | Cross-skill standards |
| **Cross-Skill** | `shipkit-spec/references/foo.md` | `install/skills/shipkit-spec/references/foo.md` | Reuse another skill's docs |

#### Type 1: Local References (most common)
Pattern: `references/foo.md` or `templates/foo.md` (NO prefix)

```
Example: "See references/best-practices.md for patterns"
Resolution: {skill_dir}/references/best-practices.md
Check: Does install/skills/shipkit-spec/references/best-practices.md exist?
```

**Detection regex**: `(?<![/\w])references/[\w-]+\.md` or `(?<![/\w])templates/[\w-]+\.md`
(Negative lookbehind ensures no prefix like `shared/` or `shipkit-spec/`)

#### Type 2: Shared References
Pattern: `shared/references/foo.md`

```
Example: "See also: shared/references/VERIFICATION-PROTOCOL.md"
Resolution: install/shared/references/VERIFICATION-PROTOCOL.md
Check: Does install/shared/references/VERIFICATION-PROTOCOL.md exist?
```

**Detection regex**: `shared/references/[\w-]+\.md`

#### Type 3: Cross-Skill References
Pattern: `shipkit-{name}/references/foo.md` or `other-skill/references/foo.md`

```
Example: "Reference: See shipkit-spec/references/best-practices.md"
Resolution: install/skills/shipkit-spec/references/best-practices.md
Check: Does install/skills/shipkit-spec/references/best-practices.md exist?
```

**Detection regex**: `shipkit-[\w-]+/references/[\w-]+\.md`

---

**Validation logic (bash)**:
```bash
for skill in install/skills/shipkit-*/; do
  name=$(basename "$skill")

  # Type 1: Local references (no prefix)
  local_refs=$(grep -oE '(?<![/\w])references/[\w-]+\.md' "$skill/SKILL.md" 2>/dev/null | sort -u)
  for ref in $local_refs; do
    if [ ! -f "$skill/$ref" ]; then
      echo "BROKEN LOCAL: $name → $ref"
    fi
  done

  # Type 2: Shared references
  shared_refs=$(grep -oE 'shared/references/[\w-]+\.md' "$skill/SKILL.md" 2>/dev/null | sort -u)
  for ref in $shared_refs; do
    if [ ! -f "install/$ref" ]; then
      echo "BROKEN SHARED: $name → $ref"
    fi
  done

  # Type 3: Cross-skill references
  cross_refs=$(grep -oE 'shipkit-[\w-]+/references/[\w-]+\.md' "$skill/SKILL.md" 2>/dev/null | sort -u)
  for ref in $cross_refs; do
    if [ ! -f "install/skills/$ref" ]; then
      echo "BROKEN CROSS-SKILL: $name → $ref"
    fi
  done
done
```

**Skip validation for**:
- URLs (http://, https://)
- Placeholder paths (contains {variable})
- User project paths (.shipkit/ context - these are templates for user projects)

---

### Step 4b: Broken Reference Triage

When a broken reference is found, **don't automatically create the file**. First determine if the reference is necessary.

**Decision Tree**:
```
Broken reference found: {skill}/SKILL.md → references/{file}.md
    │
    ├─► Is this reference USED in the skill logic?
    │   (Does the skill say "Read:", "Load:", "See:" this file?)
    │       │
    │       ├─► YES, actively used
    │       │   └─► Does similar content exist elsewhere?
    │       │       ├─► YES → Consolidate/move content, update reference
    │       │       └─► NO  → Create the reference file with needed content
    │       │
    │       └─► NO, just mentioned/aspirational
    │           └─► REMOVE the stale reference from SKILL.md
    │
    └─► Is this a "shared/references/" path?
        └─► Check if ANY skill actually needs it
            ├─► YES → Create shared file
            └─► NO  → Remove references from all skills
```

**Reference Necessity Indicators**:

| Pattern in SKILL.md | Likely Necessary | Action |
|---------------------|------------------|--------|
| `Read: references/X.md` | Yes - actively loaded | Create or fix |
| `Load references/X.md` | Yes - actively loaded | Create or fix |
| `**See:** references/X.md` | Maybe - informational | Check if content exists inline |
| `See references/X.md for...` | Maybe - informational | Check if content exists inline |
| Just mentioned in passing | No - stale | Remove reference |

**Report format for broken references**:
```
BROKEN REFERENCE TRIAGE
───────────────────────
shipkit-spec/SKILL.md → references/best-practices.md
  Usage: "See references/best-practices.md for quality standards"
  Necessity: INFORMATIONAL (not actively loaded)
  Recommendation: Check if content exists inline; if yes, REMOVE reference

shipkit-project-context/SKILL.md → references/bash-commands.md
  Usage: "**Commands**: See references/bash-commands.md for platform-specific..."
  Necessity: LIKELY NEEDED (documentation reference)
  Recommendation: CREATE file or INLINE the content
```

---

### Step 5: Cross-Skill Reference Validation (Cached)

**For each SKILL.md, extract skill references**:

Patterns:
- `/shipkit-{name}` — slash command references
- `shipkit-{name}` in "After This Skill" / "Before This Skill" sections
- `install/skills/shipkit-{name}` — explicit paths

**Validate each reference**:
```
For each referenced skill name:
  If install/skills/{skill_name}/ does NOT exist:
    → ERROR: {source_skill} references non-existent skill "{skill_name}"
```

---

### Step 6: Hook Validation

**6.1: Hook files exist**:
```
Required hooks in install/shared/hooks/:
- shipkit-session-start.py
- shipkit-after-skill-router.py
- shipkit-track-skill-usage.py
- shipkit-relentless-stop-hook.py

For each required hook:
  If NOT exists:
    → ERROR: Required hook missing: {hook_name}
```

**6.2: Hook syntax validation**:
```bash
python -m py_compile install/shared/hooks/*.py
```

**6.3: Skills referencing hooks**:
```
For each SKILL.md mentioning a hook file:
  Extract hook filename
  If hook file does NOT exist:
    → ERROR: {skill_name} references non-existent hook "{hook_file}"
```

---

### Step 7: Installer Integrity (Cached)

**7.1: Installer syntax validation**:
```bash
python -m py_compile installers/install.py
python -m py_compile installers/uninstall.py
```

**7.2: Installer path references**:

The installer (`installers/install.py`) references these paths:
```python
INSTALLER_REQUIRED_PATHS = [
    "install/shared",
    "install/shared/hooks",
    "install/skills",
    "install/agents",
    "install/settings",
    "install/claude-md",
    "install/profiles",
    "docs/generated"
]
```

**Validate**:
```
For each required path:
  If NOT exists:
    → ERROR: Installer references missing path: {path}
```

**7.3: Manifest validity**:
```
For each .manifest.json in install/profiles/:
  Try to parse as JSON
  If fails:
    → ERROR: Invalid JSON in {manifest_file}

  Check required keys exist:
  - skills.mandatory (array)
  - skills.optional (object)
  - agents (array)
```

**7.4: Installer Coverage Check** (CRITICAL):

The installer has **hardcoded hook copies**. If a new hook is added to `install/shared/hooks/`, it won't be installed unless the installer is updated.

```python
# Extract hardcoded hooks from installers/install.py
# Look for shutil.copy2() calls in install_shared_core() function
# Pattern: shutil.copy2(hooks_src / "filename.py", ...)

INSTALLER_HARDCODED_HOOKS = [
    "shipkit-session-start.py",
    "shipkit-after-skill-router.py",
    "shipkit-track-skill-usage.py",
    "shipkit-relentless-stop-hook.py"
]
```

**Validate coverage**:
```
1. List all .py files in install/shared/hooks/
2. Compare to INSTALLER_HARDCODED_HOOKS extracted from installer
3. For each hook on disk NOT in installer:
   → ERROR: Hook "{hook}" exists but installer won't install it
   → Action: Update installers/install.py to include this hook

4. For each hook in installer NOT on disk:
   → ERROR: Installer references hook "{hook}" that doesn't exist
   → Action: Create the hook or remove from installer
```

**Why this matters**:
- Skills: Driven by manifest → auto-discovered ✓
- Agents: Driven by manifest → auto-discovered ✓
- Hooks: **Hardcoded in installer** → must be manually synced ✗

---

### Step 8: 7-File Integration Consistency

**File 1: SKILL.md exists** — Covered in Step 3

**File 2: Overview HTML**:
```
Read: docs/generated/shipkit-overview.html
For each skill in manifest:
  If skill_name NOT found in HTML:
    → WARNING: {skill_name} not listed in overview HTML

Extract skill count from HTML (stat-number)
Compare to manifest count
If mismatch:
  → WARNING: HTML shows {html_count} skills, manifest has {manifest_count}
```

**File 3: shipkit.md skill reference**:
```
Read: install/claude-md/shipkit.md
For each skill in manifest (excluding shipkit-detect):
  If "/{skill_name}" NOT found:
    → WARNING: {skill_name} not in shipkit.md skill reference
```

**File 4: Manifest** — Covered in Step 7.3

**File 5: Hooks** — Covered in Step 6

**File 6: Master routing**:
```
Read: install/skills/shipkit-master/SKILL.md
For each skill in manifest (excluding shipkit-master, shipkit-detect):
  If skill_name NOT found in master routing:
    → WARNING: {skill_name} not in master routing table
```

**File 7: Settings permissions**:
```
Read: install/settings/shipkit.settings.json
Validate JSON syntax
For each skill in manifest:
  If "Skill({skill_name})" NOT in permissions.allow:
    → ERROR: {skill_name} missing from settings permissions
```

---

### Step 9: Documentation Count Validation (Always Run)

**README.md skill count**:
```
Read: README.md
Extract claimed skill count (pattern: "\d+ skills")
Compare to actual count from manifest
If mismatch:
  → WARNING: README claims {claimed} skills, manifest has {actual}
```

**CLAUDE.md skill count**:
```
Read: CLAUDE.md
Extract claimed skill count from "Total:" line
Compare to actual count
If mismatch:
  → WARNING: CLAUDE.md claims {claimed} skills, manifest has {actual}
```

---

### Step 9b: JSON Artifact Migration Tracking (Always Run)

**Check**: Which skills output structured data to `.shipkit/` and whether they use the JSON artifact convention.

**Logic**:
```
1. Scan all SKILL.md files for "Context Files This Skill Writes" sections
2. Extract output paths that write to .shipkit/
3. Classify each:
   - .json with $schema: "shipkit-artifact" → ✓ Migrated
   - .json without convention → ⚠ JSON but missing convention
   - .md with structured data (lists, status, counts) → ⚠ Should migrate
   - .md with narrative content (specs, plans, decisions) → ✓ Correct as markdown

4. Report migration progress
```

**Classification rules**:
| Output Pattern | Classification |
|---------------|---------------|
| `.shipkit/*.json` with `$schema: "shipkit-artifact"` in SKILL.md | ✓ JSON artifact |
| `.shipkit/*.md` with structured/countable data | ⚠ Migration candidate |
| `.shipkit/specs/active/*.json`, `.shipkit/plans/active/*.json` | ✓ Migrated to JSON |
| `.shipkit/architecture.json` | ✓ Migrated to JSON |
| `.shipkit/why.json` | ✓ Migrated to JSON |
| No `.shipkit/` output (NONE strategy) | ⊘ N/A |

**Report format**:
```
JSON ARTIFACT MIGRATION
───────────────────────
Migrated to JSON:     1/N skills (goals.json)
Candidates for JSON:  X skills
Correct as markdown:  Y skills
No output:           Z skills

Migration candidates:
  ✓ shipkit-project-status → .shipkit/status.json (migrated)
  ✓ shipkit-work-memory → .shipkit/progress.json (migrated)

Reference: install/skills/shipkit-goals/SKILL.md (JSON artifact pattern)
Convention: $schema, type, version, lastUpdated, source, summary
```

**Why this matters**: JSON artifacts are natively visualizable by external dashboards. Progressive migration ensures tooling gets richer data over time without requiring a big-bang rewrite.

---

### Step 9c: Claude Code Compatibility Audit (Always Run)

**Framework-wide check against current Claude Code changelog.**

Read `docs/development/claude-code-changelog.md` and validate:

#### 9b.1: Hook Event Coverage

**Check**: All hook events our hooks handle still exist in Claude Code

```
Current hook events (from changelog):
- SessionStart (v1.0.62)
- PreToolUse (v1.0.38) — supports additionalContext (v2.1.9)
- PostToolUse (v1.0.38)
- Stop (v1.0.38)
- SubagentStart (v2.0.43)
- SubagentStop (v1.0.41) — has agent_id, agent_transcript_path (v2.0.42)
- Notification (v2.0.37)
- PermissionRequest (v2.0.45)
- PreCompact (v1.0.48)
- TeammateIdle (v2.1.33)
- TaskCompleted (v2.1.33)

For each hook in install/shared/hooks/:
  Extract which events it handles (from settings.json hook config)
  If event NOT in known events list:
    → WARNING: Hook handles unknown event "{event}" - may be deprecated
```

---

#### 9b.2: Settings Schema Compatibility

**Check**: Our settings.json uses valid structure and fields

```
For install/settings/shipkit.settings.json:
  Validate known top-level keys:
  - permissions.allow — array of permission strings
  - hooks — hook configuration
  - env — environment variables (if any)

  Check permission string formats:
  - Skill({name}) — valid since v2.0.20
  - Bash({pattern}) — wildcard patterns valid since v2.1.0
  - mcp__{server}__{tool} — wildcard valid since v2.1.0

  If any permission uses unrecognized format:
    → WARNING: Permission "{perm}" uses unrecognized format
```

---

#### 9b.3: Framework-Wide Deprecated Pattern Scan

**Check**: Scan ALL skills and agents for deprecated patterns

```
Deprecated patterns to scan for across entire install/:
- ".claude.json" references (allowedTools/ignorePatterns removed v2.0.8)
- "includeCoAuthoredBy" (deprecated v2.0.62, use attribution)
- Legacy SDK entrypoint references (removed v1.0.123)
- Bash commands doing file operations (Read/Edit/Glob/Grep preferred since v2.1.0)

For each match found:
  → WARNING: {file} uses deprecated pattern: {pattern}
  → Suggestion: {replacement}
```

---

#### 9b.4: New Feature Adoption Summary

**Check**: Which newer Claude Code features the framework could leverage

```
Feature adoption report (INFO level):

Agent Memory (v2.1.33):
  Agents using `memory` field: {count}/{total}
  Agents that could benefit: [list]

Skill Context Fork (v2.1.0):
  Skills using `context: fork`: {count}/{total}

Frontmatter Hooks (v2.1.0):
  Skills/agents using inline `hooks`: {count}/{total}

YAML-style allowed-tools (v2.1.0):
  Skills using YAML lists: {count}/{total}

Plugin System (v2.0.12):
  Framework packaged as plugin: YES/NO
```

**Note**: This is informational only — no errors or warnings. Helps track modernization progress.

---

#### 9b.5: Changelog Version Drift Alert

**Check**: How far behind our last-verified version is

```
Read: docs/development/claude-code-changelog.meta.json → latestVersion
Read: .claude/skills/shipkit-framework-integrity/.integrity-state.json → lastVerifiedVersion (if exists)

If latestVersion != lastVerifiedVersion:
  Count versions between them
  Summarize key changes affecting framework:
    - New frontmatter fields
    - New hook events
    - Breaking changes
    - Deprecations

  → INFO: {N} new Claude Code versions since last integrity check
  → Key changes: [summary list]
```

**Store `lastVerifiedVersion` in state file after successful check.**

---

### Step 10: Save State & Generate Report

**Update state file**:
```python
def save_state(state, new_hashes, results):
    state["lastFullCheck"] = datetime.utcnow().isoformat() + "Z"
    state["fileHashes"] = new_hashes
    state["lastResults"] = results
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))
```

**Output format**:
```
============================================
SHIPKIT FRAMEWORK INTEGRITY REPORT
============================================
Timestamp: 2025-02-05T10:30:00Z
Mode: Incremental (15 files unchanged, 3 files checked)

MANIFEST ↔ DISK SYNC
─────────────────────
Skills on disk:     27
Skills in manifest: 27
Agents on disk:     6
Agents in manifest: 6

✓ All skills synced
✓ All agents synced

BROKEN REFERENCES
─────────────────
Files checked: 3 (24 skipped - unchanged)

Local References (references/foo.md → skill's own directory):
  ✗ shipkit-verify → references/quality-checklist.md (NOT FOUND)
  ✗ shipkit-preflight → templates/audit-template.md (NOT FOUND)

Shared References (shared/references/foo.md → install/shared/):
  ✓ All shared references valid

Cross-Skill References (shipkit-X/references/foo.md → other skill):
  ✓ All cross-skill references valid

CROSS-SKILL REFERENCES
──────────────────────
✓ All cross-skill references valid

HOOK VALIDATION
───────────────
✓ All 4 required hooks present
✓ Hook syntax valid
✓ No broken hook references in skills

INSTALLER INTEGRITY
───────────────────
✓ installers/install.py syntax valid
✓ installers/uninstall.py syntax valid
✓ All installer paths exist
✓ All manifest files valid JSON

7-FILE INTEGRATION
──────────────────
✓ File 1: All SKILL.md files exist
✓ File 2: Overview HTML complete
⚠ File 3: shipkit.md missing 1 skill
✓ File 4: Manifest valid
✓ File 5: Hooks valid
✓ File 6: Master routing complete
✓ File 7: Settings permissions complete

DOCUMENTATION COUNTS
────────────────────
README.md:      27 skills ✓
CLAUDE.md:      27 skills ✓
Overview HTML:  27 skills ✓

JSON ARTIFACT MIGRATION
───────────────────────
Migrated to JSON:     1 skill (goals.json)
Candidates for JSON:  3 skills
Correct as markdown:  12 skills
No output:           11 skills

⚠ Migration candidates:
  shipkit-project-status → structured health data
  shipkit-work-memory → session progress log

CLAUDE CODE COMPATIBILITY (v{claude_code_version})
───────────────────────────────────────────────────
✓ All hook events recognized
✓ Settings schema valid
⚠ 2 deprecated patterns found
ⓘ Feature adoption: 3/9 agents use memory field

============================================
SUMMARY
============================================
Errors:   2 (must fix before release)
Warnings: 1 (should fix)
Skipped:  24 files (unchanged since last check)

ERRORS:
1. [BROKEN] shipkit-verify references non-existent file
2. [BROKEN] shipkit-preflight references non-existent file

WARNINGS:
1. [DOCS] shipkit-new-skill not in shipkit.md

============================================
RESULT: FAIL (2 errors must be resolved)
============================================

State saved to: .claude/skills/shipkit-framework-integrity/.integrity-state.json
```

---

## Validation Rules Summary

| Check | Severity | Cached | Description |
|-------|----------|--------|-------------|
| VERSION missing | ERROR | No | `VERSION` file doesn't exist |
| VERSION invalid | ERROR | No | VERSION file empty or not valid semver |
| VERSION/tag mismatch | WARNING | No | VERSION doesn't match latest git tag |
| Orphan skill | ERROR | No | Skill directory exists but not in manifest |
| Ghost skill | ERROR | No | Skill in manifest but no directory |
| Broken reference | ERROR | Yes | SKILL.md references file that doesn't exist |
| Cross-skill ref invalid | ERROR | Yes | Skill references another skill that doesn't exist |
| Missing hook | ERROR | No | Required hook file missing |
| Hook syntax error | ERROR | Yes | Python file has syntax errors |
| Installer syntax error | ERROR | Yes | Installer Python files have syntax errors |
| Installer path missing | ERROR | No | Path referenced by installer doesn't exist |
| **Hook not in installer** | **ERROR** | No | Hook exists on disk but installer won't copy it |
| Invalid manifest JSON | ERROR | Yes | Manifest file has JSON syntax errors |
| Missing permission | ERROR | No | Skill not in settings.json allow list |
| Count mismatch | WARNING | No | Doc counts don't match manifest |
| Missing from routing | WARNING | No | Skill not in master routing table |
| Missing from docs | WARNING | No | Skill not in shipkit.md reference |
| Stale reference | WARNING | Yes | Reference exists but isn't actively used (triage needed) |
| Unknown hook event | WARNING | No | Hook handles event not in changelog's known events |
| Deprecated pattern | WARNING | No | Code uses pattern deprecated in changelog |
| Stale changelog | WARNING | No | Changelog >7 days old or missing |
| Version drift | INFO | No | New Claude Code versions since last check |
| Feature opportunity | INFO | No | Framework could leverage newer features |
| JSON migration candidate | WARNING | No | Skill outputs structured .md that should be .json |
| JSON convention missing | WARNING | No | Skill outputs .json but missing artifact convention |

---

## Command Line Options

```
/shipkit-framework-integrity [options]

Options:
  --full        Force full check, ignore cache
  --quick       Only check manifest sync and counts (fastest)
  --fix         Attempt to auto-fix simple issues
  --json        Output results as JSON
  --loop N      Run up to N iterations, re-checking after fixes (default: 3 if no N)
```

---

## Loop Mode

When invoked with `--loop N`, the skill runs iteratively — checking, fixing, and re-checking — until either zero errors/warnings remain or N iterations are exhausted.

**State file**: `.shipkit/framework-integrity-loop.local.md`

**Default completion promise**: "Framework integrity check reports zero errors and zero warnings"

**How it works**:
1. Parse `--loop N` from arguments (default N=3 if omitted)
2. Create state file with frontmatter (skill, iteration, max_iterations, completion_promise)
3. Run the normal integrity check
4. Update the Progress section in the state file with findings and fixes applied
5. If zero errors and zero warnings → delete state file, report success, stop
6. If issues remain → end response; the relentless stop hook blocks exit and re-prompts

**Example**:
```
/shipkit-framework-integrity --loop 3 --fix
```

This runs up to 3 iterations of check-fix-recheck. Combines with `--fix` for automated repair across passes (e.g., pass 1 fixes manifest sync, pass 2 fixes references revealed by the sync fix).

**Shared reference**: See `.claude/skills/_shared/loop-mode-reference.md` for state file format and protocol details.

---

## When This Skill Integrates with Others

### Before This Skill
- After refactoring skills or removing files
- After adding/removing skills or agents
- Before `git push` to main branch

### After This Skill
- Fix identified issues manually
- Re-run with `--full` to verify fixes
- Proceed with release/commit

### Related Skills
- `shipkit-dev-spec` → `shipkit-dev-plan` — Design and plan new skills/changes
- `shipkit-dev-review` — Reviews changes for quality after implementation

---

## Context Files This Skill Reads

**Core files**:
- `install/profiles/shipkit.manifest.json` — Source of truth for skills/agents
- `install/settings/shipkit.settings.json` — Permissions list
- `install/claude-md/shipkit.md` — Skill reference documentation
- `install/skills/shipkit-master/SKILL.md` — Routing table

**Installer files**:
- `installers/install.py` — Main Python installer
- `installers/uninstall.py` — Uninstaller

**All skill files**:
- `install/skills/shipkit-*/SKILL.md` — Each skill's definition
- `install/skills/shipkit-*/references/*` — Reference files
- `install/skills/shipkit-*/templates/*` — Template files

**All agent files**:
- `install/agents/shipkit-*.md` — Agent persona files

**Hook files**:
- `install/shared/hooks/*.py` — All hook files

**Documentation**:
- `README.md` — Skill count claims
- `CLAUDE.md` — Skill count claims
- `docs/generated/shipkit-overview.html` — HTML help

**Claude Code changelog** (auto-fetched if stale):
- `docs/development/claude-code-changelog.md` - Full changelog from GitHub
- `docs/development/claude-code-changelog.meta.json` - Freshness metadata
- `docs/development/fetch-changelog.sh` - Fetch script

**State file**:
- `.claude/skills/shipkit-framework-integrity/.integrity-state.json`

---

## Context Files This Skill Writes

**Write Strategy: STATE FILE ONLY**

- `.claude/skills/shipkit-framework-integrity/.integrity-state.json` — Caching state
- `.shipkit/framework-integrity-loop.local.md` — Loop mode state (only when `--loop N` used, deleted on completion)

This skill:
- Does NOT modify source files (unless `--fix` is used)
- Reports issues found
- User must fix issues manually (unless `--fix`)

---

## Success Criteria

Validation is complete when:
- [ ] Changelog freshness verified (fetched if stale >7 days)
- [ ] Manifest ↔ disk sync verified
- [ ] All SKILL.md files scanned for broken references (or skipped if unchanged)
- [ ] Cross-skill references validated
- [ ] All hooks present and syntax valid
- [ ] Installer syntax and paths valid
- [ ] 7-file integration consistency verified
- [ ] Documentation counts validated
- [ ] Claude Code compatibility audit complete
- [ ] State file updated with current hashes and lastVerifiedVersion
- [ ] Clear PASS/FAIL result with actionable items

---

## Example Session

```
User: "/shipkit-framework-integrity"

Claude:
Loading state file...
  Last check: 2025-02-04T15:00:00Z
  24 files unchanged, 3 files modified since last check

Running integrity check...

1. Checking manifest ↔ disk sync...
   ✓ 28 skills synced
   ✓ 6 agents synced

2. Scanning SKILL.md files for broken references...

   LOCAL REFERENCES (references/foo.md → skill's own directory):
   ✗ shipkit-ux-audit → references/common-patterns.md (NOT FOUND)
   ✗ shipkit-ux-audit → references/ux-principles.md (NOT FOUND)
   ✓ shipkit-spec → references/best-practices.md
   ✓ shipkit-master → references/file-freshness-logic.md

   SHARED REFERENCES (shared/references/foo.md → install/shared/):
   ✓ VERIFICATION-PROTOCOL.md exists (used by 5 skills)

   CROSS-SKILL REFERENCES (shipkit-X/references/foo.md):
   ✓ shipkit-plan → shipkit-spec/references/best-practices.md

3. Checking hooks...
   ✓ All 4 required hooks present
   ✓ Syntax valid
   ✓ All hooks covered by installer

4. Checking installer integrity...
   ✓ Installer syntax valid
   ✓ All paths exist

5. Validating 7-file integration...
   ✓ All integration files consistent

6. Checking documentation counts...
   ✓ All counts match (28 skills)

============================================
RESULT: FAIL (2 broken local references)

BROKEN LOCAL REFERENCES:
  shipkit-ux-audit/SKILL.md:
    ✗ references/common-patterns.md
    ✗ references/ux-principles.md

To fix: CREATE the missing files OR REMOVE the references from SKILL.md
(Use sub-agent triage to determine which action is appropriate)
============================================
```
