# Framework Integrity Checklist

**Purpose**: Comprehensive checklist for Shipkit framework integrity validation

**Use**: Referenced by shipkit-framework-integrity for validation logic

---

## Part 0: Version File

### VERSION Sync
- [ ] `install/VERSION` exists
- [ ] VERSION contains valid semver (e.g., `1.3.0`)
- [ ] VERSION matches latest git release tag (if tags exist)

**Why this matters**: The VERSION file is the single source of truth for Shipkit releases. During installation, this version is:
- Written to `_shipkit` key in user's `.claude/settings.json`
- Inserted into CLAUDE.md markers: `<!-- BEGIN Shipkit v{VERSION} -->`

If VERSION is stale, users will get incorrect version markers after update.

---

## Part 1: Manifest ↔ Disk Sync

### Skills Sync
- [ ] Every directory in `install/skills/shipkit-*/` has manifest entry
- [ ] Every manifest skill entry has corresponding directory
- [ ] No orphan skills (disk only)
- [ ] No ghost skills (manifest only)

### Agents Sync
- [ ] Every file in `install/agents/shipkit-*.md` has manifest entry
- [ ] Every manifest agent entry has corresponding file
- [ ] No orphan agents (disk only)
- [ ] No ghost agents (manifest only)

---

## Part 2: Reference Integrity

### File References in SKILL.md
- [ ] All `references/*.md` paths resolve
- [ ] All `templates/*.md` paths resolve
- [ ] All `install/skills/...` paths resolve
- [ ] All `install/agents/...` paths resolve
- [ ] All `docs/...` paths resolve

### Cross-Skill References
- [ ] All `/shipkit-{name}` command references point to existing skills
- [ ] All "After This Skill" entries reference existing skills
- [ ] All "Before This Skill" entries reference existing skills
- [ ] All `install/skills/shipkit-{name}` paths resolve

### Excluded from Validation
- URLs (http://, https://)
- Placeholder paths with `{variables}`
- User project paths (.shipkit/ context files - templates for user projects)

### Broken Reference Triage
Before creating a missing reference file, determine if it's actually needed:

| Usage Pattern | Necessary? | Action |
|---------------|------------|--------|
| `Read: references/X.md` | YES | Create file |
| `Load references/X.md` | YES | Create file |
| `**See:** references/X.md` | MAYBE | Check if content inline |
| `See references/X.md for...` | MAYBE | Check if content inline |
| Mentioned in passing | NO | Remove reference |

**Decision process**:
1. Is reference actively loaded by skill logic?
   - YES → Create the file
   - NO → Go to step 2
2. Does similar content exist elsewhere (inline, other skill)?
   - YES → Remove reference, content already available
   - NO → Decide: create minimal file OR remove aspirational reference

---

## Part 3: Hook Validation

### Required Hooks
- [ ] `install/shared/hooks/shipkit-session-start.py` exists
- [ ] `install/shared/hooks/shipkit-after-skill-router.py` exists
- [ ] `install/shared/hooks/shipkit-track-skill-usage.py` exists
- [ ] `install/shared/hooks/shipkit-relentless-stop-hook.py` exists

### Hook Syntax
- [ ] All `.py` files in `install/shared/hooks/` pass `python -m py_compile`
- [ ] No import errors for standard library modules

### Hook References in Skills
- [ ] Skills mentioning hooks reference hooks that exist
- [ ] Hook filenames in skills match actual hook files

---

## Part 4: Installer Integrity

### Installer Files
- [ ] `installers/install.py` exists
- [ ] `installers/uninstall.py` exists
- [ ] Both pass `python -m py_compile`

### Installer Path References
The installer requires these paths to exist:
- [ ] `install/shared` — Shared files (hooks, scripts)
- [ ] `install/shared/hooks` — Hook files
- [ ] `install/skills` — Skill definitions
- [ ] `install/agents` — Agent personas
- [ ] `install/settings` — Settings templates
- [ ] `install/claude-md` — CLAUDE.md templates
- [ ] `install/profiles` — Manifest files
- [ ] `docs/generated` — HTML documentation

### Installer Coverage (CRITICAL)
**Hooks are hardcoded in the installer** - they must be manually synced!

- [ ] All hooks in `install/shared/hooks/` are listed in installer's `install_shared_core()`
- [ ] No hooks in installer that don't exist on disk
- [ ] When adding a new hook: update `installers/install.py`

**Current hardcoded hooks** (check these match disk):
```python
shutil.copy2(hooks_src / "shipkit-session-start.py", ...)
shutil.copy2(hooks_src / "shipkit-after-skill-router.py", ...)
shutil.copy2(hooks_src / "shipkit-track-skill-usage.py", ...)
shutil.copy2(hooks_src / "shipkit-relentless-stop-hook.py", ...)
```

### Manifest Validity
- [ ] `install/profiles/shipkit.manifest.json` exists
- [ ] Valid JSON syntax
- [ ] Has `skills.mandatory` (array)
- [ ] Has `skills.optional` (object with category arrays)
- [ ] Has `agents` (array)
- [ ] All other `.manifest.json` files are valid JSON

---

## Part 5: 7-File Integration Consistency

### File 1: SKILL.md
- [ ] Every skill has `SKILL.md` file
- [ ] SKILL.md is readable (no encoding issues)

### File 2: Overview HTML
- [ ] `docs/generated/shipkit-overview.html` exists
- [ ] Each manifest skill listed in HTML
- [ ] Skill count in HTML matches manifest count
- [ ] No stale/removed skills still listed

### File 3: shipkit.md
- [ ] `install/claude-md/shipkit.md` exists
- [ ] Each user-invocable skill listed (except shipkit-detect)
- [ ] Format: `/{skill-name}` with description
- [ ] No stale/removed skills still listed

### File 4: Manifest
- [ ] `install/profiles/shipkit.manifest.json` exists
- [ ] Valid JSON syntax
- [ ] All referenced skills exist on disk

### File 5: Hooks
- [ ] All required hooks present
- [ ] All hooks have valid Python syntax
- [ ] settings.json hook configuration references valid files

### File 6: Master Routing
- [ ] `install/skills/shipkit-master/SKILL.md` exists
- [ ] Each skill has routing entry (except detect, master)
- [ ] Routing keywords are relevant to skill purpose
- [ ] No stale/removed skills still listed

### File 7: Settings Permissions
- [ ] `install/settings/shipkit.settings.json` exists
- [ ] Valid JSON syntax
- [ ] Each manifest skill has `Skill({skill-name})` permission
- [ ] No permissions for non-existent skills

---

## Part 6: Documentation Accuracy

### Skill Counts
- [ ] README.md skill count matches manifest
- [ ] CLAUDE.md skill count matches manifest
- [ ] Overview HTML skill count matches manifest
- [ ] All three counts are consistent with each other

### Skill Lists
- [ ] README.md skill list is current
- [ ] CLAUDE.md Appendix skill list is current
- [ ] No removed skills still listed anywhere
- [ ] No new skills missing from lists

---

## Part 6b: Claude Code Compatibility

**Source**: `docs/development/claude-code-changelog.md` (auto-fetched from GitHub)

### Changelog Freshness
- [ ] `docs/development/claude-code-changelog.meta.json` exists
- [ ] `fetchedAt` is within 7 days
- [ ] If stale or missing: run `bash docs/development/fetch-changelog.sh`

### Hook Event Coverage
Known hook events (update as changelog evolves):
- [ ] SessionStart (v1.0.62)
- [ ] PreToolUse (v1.0.38, additionalContext v2.1.9)
- [ ] PostToolUse (v1.0.38)
- [ ] Stop (v1.0.38)
- [ ] SubagentStart (v2.0.43)
- [ ] SubagentStop (v1.0.41)
- [ ] Notification (v2.0.37)
- [ ] PermissionRequest (v2.0.45)
- [ ] PreCompact (v1.0.48)
- [ ] TeammateIdle (v2.1.33)
- [ ] TaskCompleted (v2.1.33)

### Settings Schema
- [ ] Permission string formats are valid
- [ ] Skill() permissions use correct syntax
- [ ] Bash() permissions use valid wildcard patterns (v2.1.0+)
- [ ] MCP tool permissions use valid patterns (v2.1.0+)

### Deprecated Pattern Scan
Scan all files in install/ for:
- [ ] No `.claude.json` allowedTools references (removed v2.0.8)
- [ ] No `.claude.json` ignorePatterns references (removed v2.0.8)
- [ ] No `includeCoAuthoredBy` references (deprecated v2.0.62)
- [ ] No legacy SDK entrypoint references (removed v1.0.123)

### Feature Adoption Tracking
- [ ] Agent `memory` field usage counted
- [ ] Skill `context: fork` usage counted
- [ ] Frontmatter `hooks` usage counted
- [ ] YAML-style `allowed-tools` usage counted

### Version Drift
- [ ] `lastVerifiedVersion` tracked in state file
- [ ] Delta between last verified and current reported
- [ ] Key changes affecting framework summarized

---

## Part 7: Caching & State

### State File
Location: `.claude/skills/shipkit-framework-integrity/.integrity-state.json`

- [ ] State file created/updated after each run
- [ ] File hashes stored for incremental checking
- [ ] Last check timestamp recorded
- [ ] Previous results stored for unchanged files

### Caching Rules
- **Always re-check**: Manifest sync, counts, cross-cutting concerns
- **Cache per-file**: SKILL.md references, hook syntax, installer syntax
- **Skip if unchanged**: Files with matching hash since last check

---

## Severity Classification

### ERROR (Must Fix Before Release)

| Issue | Example | Cached |
|-------|---------|--------|
| Orphan skill | Directory exists, not in manifest | No |
| Ghost skill | In manifest, no directory | No |
| Broken reference | SKILL.md references non-existent file | Yes |
| Cross-skill ref invalid | Skill references non-existent skill | Yes |
| Missing required hook | `shipkit-session-start.py` not found | No |
| Hook syntax error | Python won't compile | Yes |
| Installer syntax error | `install.py` won't compile | Yes |
| Installer path missing | Required install path doesn't exist | No |
| Invalid manifest JSON | Manifest file malformed | Yes |
| Missing permission | Skill not in settings.json | No |

### WARNING (Should Fix)

| Issue | Example | Cached |
|-------|---------|--------|
| Count mismatch | README says 28, manifest has 27 | No |
| Missing from routing | Skill not in master routing | No |
| Missing from docs | Skill not in shipkit.md | No |
| Stale documentation | Removed skill still listed | No |

### INFO (Optional)

| Issue | Example |
|-------|---------|
| File unchanged | Skipped validation (cached) |
| Verbose skill | Over 300 lines (note only) |

---

## Quick Commands

### Full integrity check
```
/shipkit-framework-integrity
```

### Force full check (ignore cache)
```
/shipkit-framework-integrity --full
```

### Quick check (manifest + counts only)
```
/shipkit-framework-integrity --quick
```

### Clear cache
```bash
rm .claude/skills/shipkit-framework-integrity/.integrity-state.json
```

---

## Pass/Fail Criteria

### PASS
- Zero ERRORs
- WARNINGs acceptable (logged but not blocking)

### FAIL
- Any ERROR present
- Must resolve all ERRORs before release

---

## Common Issues After Refactoring

| Issue | Fix |
|-------|-----|
| Removed skill still in manifest | Remove from `shipkit.manifest.json` |
| New skill not in settings | Add `Skill({name})` to `shipkit.settings.json` |
| Reference to deleted file | Remove reference or recreate file |
| Skill count outdated | Update README.md, CLAUDE.md, overview HTML |
| Renamed skill, old name lingers | Search and replace old name in all 7 files |
| Hook renamed/removed | Update skills that reference the hook |
| Cross-skill reference broken | Update or remove the reference |

---

## Integration with Other Checks

| Check | Tool | Scope |
|-------|------|-------|
| Single skill quality | `shipkit-validate-lite-skill` | One skill |
| Framework integrity | `shipkit-framework-integrity` | All skills + integration |
| Pre-commit | Git hooks | Changed files only |
| CI/CD | GitHub Actions | Full repo |

---

## Validation Script Reference

### Key Paths
```python
PATHS = {
    "manifest": "install/profiles/shipkit.manifest.json",
    "settings": "install/settings/shipkit.settings.json",
    "claude_md": "install/claude-md/shipkit.md",
    "master": "install/skills/shipkit-master/SKILL.md",
    "overview": "docs/generated/shipkit-overview.html",
    "installer": "installers/install.py",
    "uninstaller": "installers/uninstall.py",
    "hooks": "install/shared/hooks",
    "skills": "install/skills",
    "agents": "install/agents",
    "state": ".claude/skills/shipkit-framework-integrity/.integrity-state.json"
}
```

### Required Hooks
```python
REQUIRED_HOOKS = [
    "shipkit-session-start.py",
    "shipkit-after-skill-router.py",
    "shipkit-track-skill-usage.py",
    "shipkit-relentless-stop-hook.py"
]
```

### Installer Required Paths
```python
INSTALLER_PATHS = [
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
