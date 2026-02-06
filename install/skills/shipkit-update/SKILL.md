---
name: shipkit-update
description: Install or update Shipkit from GitHub. Detects existing installations, archives them safely, and intelligently merges user content with new version.
user_invocable: true
arguments:
  - name: repo
    description: GitHub repo (default: stefan-stepzero/shipkit or configured repo)
    required: false
---

# shipkit-update - Install & Update Shipkit

**Purpose**: One skill to install Shipkit fresh or update an existing installation. Archives previous versions safely and intelligently merges user content.

**Role**: Bootstrap/update skill. Can be fetched directly from GitHub even before Shipkit is installed.

---

## Why This Skill Exists

**Updates are tricky without version tracking and safe migration.**

This skill provides:
1. **Detection** - Finds all Shipkit variants (current + legacy naming)
2. **Safe archiving** - Never deletes, always preserves
3. **Clean install** - Fresh framework files from source
4. **Intelligent merge** - Claude merges user content into new structure

---

## When to Invoke

**User-invoked:**
- "Install Shipkit" / "Update Shipkit" / "Upgrade Shipkit"
- `/shipkit-update` (explicit)
- "Reinstall Shipkit from GitHub"

**Bootstrap scenario:**
- User pastes GitHub link + "install this"
- Claude fetches this skill directly and executes

---

## Prerequisites

**For installation:**
- Access to GitHub (WebFetch or gh CLI)
- Write access to project root

**For update:**
- Existing Shipkit installation (any version)

---

## Process

### Step 0: Request Permissions Upfront

**Get user approval once at the start, then run without interruptions.**

Present to user:
```
To update Shipkit, I need permission to:

1. **Fetch from GitHub** — Download installer and VERSION file
2. **Run Python script** — Execute the installer (installs skills, agents, hooks)
3. **Modify files** — Update .claude/, .shipkit/, and CLAUDE.md

This will:
- Archive your current installation (nothing deleted)
- Install fresh framework files
- Preserve your specs, plans, progress, and other user content

Proceed? [y/n]
```

**If approved:** Continue without further permission prompts.
**If declined:** Stop and explain what manual steps user can take.

---

### Step 1: Detect Existing Installation

**Scan for ALL Shipkit variants:**

```
Detection targets:
├── .shipkit/                    # Current context folder
├── .shipkit-lite/               # Legacy context folder
├── .claude/
│   ├── skills/shipkit-*/        # Current skills
│   ├── skills/lite-*/           # Legacy skills
│   ├── agents/shipkit-*.md      # Current agents
│   ├── agents/lite-*.md         # Legacy agents
│   ├── hooks/shipkit-*.py       # Current hooks
│   ├── hooks/lite-*.py          # Legacy hooks
│   ├── rules/shipkit.md         # Framework rules (replace on update)
│   ├── settings.json            # Main settings (check _shipkit key)
│   └── settings.local.json      # Local overrides (check for stale refs)
├── CLAUDE.md                    # Root (user-editable, merge carefully)
└── **/CLAUDE.md                 # Subfolders (check for Shipkit sections)
```

**Version detection:**
- Grep for `Shipkit v` pattern in all found files
- Check `_shipkit` key in JSON files
- Look for legacy markers: `Shipkit-Lite`, `lite-`, `BEGIN Shipkit-Lite`
- Record highest version found

**Output:**
```
Detected Shipkit installation:
- Version: v1.0.0 (from 12 files)
- Context folder: .shipkit/
- Skills: 15 found (shipkit-* prefix)
- Agents: 6 found
- CLAUDE.md: Has Shipkit section (with markers / without markers)
- settings.json: Has _shipkit key
- settings.local.json: Found (has stale lite-* refs / clean)
- User content: why.md, architecture.md, 3 specs
```

---

### Step 2: Archive Existing Installation

**Always archive before any changes.**

**Create archive folder:**
```
.shipkit-archive/
└── {YYYYMMDD-HHMMSS}/
    ├── context/                     # From .shipkit/ or .shipkit-lite/
    │   └── [entire .shipkit/ contents]
    ├── skills/                      # All shipkit-* and lite-* skills
    ├── agents/                      # All shipkit-* and lite-* agents
    ├── hooks/                       # All shipkit-* and lite-* hooks
    ├── CLAUDE.md.backup             # Full backup of root CLAUDE.md
    ├── settings.json.backup         # Full backup of settings
    └── MANIFEST.md                  # What was archived + versions
```

**MANIFEST.md format:**
```markdown
# Shipkit Archive Manifest
Archived: 2024-01-15 14:30:00
Previous version: v1.0.0
Upgrading to: v1.1.0

## Archived Framework Files
- 15 skills (shipkit-* prefix)
- 7 agents
- 2 hooks
- settings.json entries

## Archived Context (entire .shipkit/ folder)
All files preserved in context/ subfolder.

## Other Backups
- CLAUDE.md (full backup)
- settings.json (full backup)

## Version Map
| File | Version |
|------|---------|
| shipkit-master/SKILL.md | v1.0.0 |
| shipkit-spec/SKILL.md | v1.0.0 |
| settings.json (_shipkit) | v1.0.0 |
| CLAUDE.md | v1.0.0 (or "no markers") |
...

## Notes
- settings.local.json was NOT archived (user's local file)
- Original files preserved here if merge needs review
```

---

### Step 3: Fetch and Run Python Installer

**Source repository:**
- Default: `https://github.com/stefan-stepzero/shipkit` (or user-configured)
- Branch: `main`

**Step 3a: Fetch VERSION to know target version:**
```bash
curl -sL https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/install/VERSION
```
Store this for reporting (e.g., "Updating to v1.3.0").

**Step 3b: Fetch and run the Python installer:**
```bash
# Download installer to temp location
curl -sL https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/installers/install.py -o /tmp/shipkit-install.py

# Run installer with --from-github flag
# - Downloads repo zip, extracts, installs
# - -y for non-interactive (we already got permission in Step 0)
# - --claude-md skip (Claude will do intelligent merge in Step 4)
python /tmp/shipkit-install.py --from-github -y --claude-md skip

# Clean up
rm /tmp/shipkit-install.py
```

**What the installer handles (with `--from-github`):**
1. Downloads entire repo as zip from GitHub
2. Extracts to temp directory
3. Installs:
   - Skills → `.claude/skills/shipkit-*/`
   - Agents → `.claude/agents/`
   - Hooks → `.claude/hooks/`
   - Settings → `.claude/settings.json` (preserves existing)
   - Templates → `.shipkit/templates/`
   - HTML Overview → `.shipkit/shipkit-overview.html`
4. Cleans up temp files automatically

**Why use the installer:**
- Single source of truth for "what to install"
- Handles file copying, permissions, platform differences
- Tested and maintained separately
- Claude focuses on intelligence (detection, archiving, merging user content)

---

### Step 4: Intelligent Merge (CLAUDE.md)

**This is where Claude uses judgment, not rigid rules.**

#### Scenario A: Fresh install (no existing CLAUDE.md)
→ Create CLAUDE.md with full Shipkit template (with BEGIN/END markers)

#### Scenario B: Existing CLAUDE.md WITH markers
```
<!-- BEGIN Shipkit v*.*.* -->
...old shipkit content...
<!-- END Shipkit v*.*.* -->
```
→ Replace content between markers with new template
→ Update version in markers
→ Preserve everything outside markers

#### Scenario C: Existing CLAUDE.md WITHOUT markers (legacy or manual)

**Claude analyzes and merges intelligently:**

1. Read new Shipkit template (canonical structure)
2. Read old CLAUDE.md content
3. For each piece of old content, determine:
   - Is it old Shipkit instruction? → Drop (replaced by new)
   - Is it user preference? → Add to "Working Preferences" section
   - Is it project-specific knowledge? → Add to "Project Learnings" section
   - Is it unrelated to Shipkit? → Preserve below END marker

**Judgment calls Claude makes:**

| Old Content | Action |
|-------------|--------|
| "Always use TypeScript strict mode" | → Working Preferences |
| "This project uses Prisma for ORM" | → Project Learnings |
| "Run /lite-spec for specifications" | → Drop (old command) |
| "Check .shipkit-lite/ for context" | → Drop (old path) |
| "Never commit .env files" | → Project Learnings |
| Company coding standards section | → Preserve below END marker |
| Old Shipkit skill reference tables | → Drop (replaced) |

4. Write merged CLAUDE.md with proper markers
5. Archive has original if user wants to review

**For subfolder CLAUDE.md files:**
- Same logic applies
- Check each `**/CLAUDE.md` found during detection
- Merge each one individually

---

### Step 5: Intelligent Merge (settings.json)

**Same principle: Claude merges with judgment.**

1. Read new Shipkit settings template
2. Read old `.claude/settings.json`
3. Merge intelligently:

| Section | Action |
|---------|--------|
| `_shipkit` | → Update to new version |
| `permissions.allow` with `Skill(shipkit-*)` | → Replace with new skill list |
| `permissions.allow` with `Skill(lite-*)` | → Remove (legacy) |
| `permissions.allow` (other entries) | → **Preserve** (user's custom permissions) |
| `permissions.deny` | → Merge (keep user's, add Shipkit's) |
| `hooks.SessionStart` with shipkit paths | → Replace with new |
| `hooks.SessionStart` (other entries) | → **Preserve** (user's custom hooks) |
| `hooks.Stop` | → Same logic |
| `skills`, `workspace` sections | → Replace with new |
| Any other keys | → **Preserve** (user's additions) |

4. Write valid JSON
5. Archive has original backup

**Example preservation:**
```json
// Old settings.json had:
"permissions": {
  "allow": [
    "Skill(shipkit-spec)",        // ← Replace (Shipkit)
    "Skill(lite-plan)",           // ← Remove (legacy)
    "WebFetch(domain:myapi.com)", // ← PRESERVE (user)
    "Bash(terraform:*)"           // ← PRESERVE (user)
  ]
}

// New merged settings.json:
"permissions": {
  "allow": [
    "Skill(shipkit-spec)",        // New Shipkit
    "Skill(shipkit-plan)",        // New Shipkit (renamed)
    ...all new shipkit skills...
    "WebFetch(domain:myapi.com)", // Preserved
    "Bash(terraform:*)"           // Preserved
  ]
}
```

---

### Step 6: Handle settings.local.json

**Do NOT modify this file.** It's the user's local overrides.

**But warn if stale patterns detected:**

Scan for:
- `lite-*` references
- Old Shipkit version markers
- Paths to `.shipkit-lite/`

**If found, output warning:**
```
⚠ settings.local.json contains outdated references:
  - "Skill(lite-spec)" → should be "Skill(shipkit-spec)"
  - Path ".shipkit-lite/" → should be ".shipkit/"

This file was NOT modified (it's your local config).
Consider updating these references manually.
```

---

### Step 7: Migrate User Content

**Principle: Migrate everything EXCEPT known framework/transient files.**

This approach is future-proof — new user content files automatically migrate without needing to update this list.

**DON'T migrate (framework - install fresh):**
```
├── templates/          # Framework templates from install
└── queues/             # Transient task queues, start empty
```

**DON'T migrate (purely auto-generated):**
```
├── schema.md           # Auto-generated from migrations
└── env-requirements.md # Auto-generated from .env files
```

**MIGRATE: Everything else in `.shipkit/`**

This includes (but is not limited to):
- `why.md` - Vision document
- `architecture.md` - Architecture decisions
- `stack.md` - Tech stack (may have manual annotations)
- `specs/**` - Feature specifications (active and implemented)
- `plans/**` - Implementation plans
- `progress.md` - Session history
- `archives/**` - Progress archives
- `codebase-index.json` - Navigation index
- `product-discovery.md` - User personas and journeys
- `types.md` - Data contracts
- `implementations.md` - Component/route documentation
- `user-tasks/**` - User task lists
- `production-readiness.md` - Audit reports
- `audits/**` - Audit history
- `ux-decisions.md` - UX decision log
- `communications/**` - Generated HTML reports
- `status.md` - Health snapshots
- Any other user-created files

**Note on stack.md:** While initially auto-generated, users often add manual notes and decisions. Migrating preserves this context. If user wants fresh detection, they can run `/shipkit-project-context` after update.

**Migration process:**
1. List all files in archived `.shipkit/` context folder
2. Exclude: `templates/`, `queues/`, `schema.md`, `env-requirements.md`
3. Copy everything else to new `.shipkit/`
4. Report what was migrated
5. Note that schema.md/env-requirements.md can be regenerated if needed

---

## Output Format

**Fresh install (no previous):**
```
✓ Shipkit installed

Installed:
- 29 skills → .claude/skills/shipkit-*/
- 7 agents → .claude/agents/
- 5 hooks → .claude/hooks/
- Framework rules → .claude/rules/shipkit.md
- Settings created
- CLAUDE.md created (user-editable sections)
- HTML Overview → .shipkit/shipkit-overview.html

💡 Open .shipkit/shipkit-overview.html in your browser for a skill reference guide

Next: Run /shipkit-project-context to scan your codebase
```

**Update (with merge):**
```
✓ Shipkit updated v1.0.0 → v1.1.0

Archived to: .shipkit-archive/20240115-143000/
- Full backup preserved (see MANIFEST.md)

Installed fresh:
- 29 skills, 7 agents, 2 hooks

Merged intelligently:
- CLAUDE.md: Shipkit section updated, your preferences preserved
- settings.json: Shipkit entries updated, your custom permissions preserved

Migrated user content:
- why.md ✓
- architecture.md ✓
- stack.md ✓
- specs/ (3 files) ✓
- product-discovery.md ✓
- types.md ✓
- [... all other user files ...]

Not migrated (purely auto-generated):
- schema.md, env-requirements.md
  ℹ️  Run /shipkit-project-context to regenerate if needed

⚠ settings.local.json has stale refs (see above)

Ready to use. Review merged files, archive has originals.
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| GitHub fetch fails | "Cannot reach {repo}. Check network/URL." |
| No write permission | "Cannot write to project. Check permissions." |
| Invalid JSON in settings | "settings.json has syntax errors. Fix manually or restore from archive." |
| Version same as installed | "Already at v1.1.0. Force reinstall? [y/n]" |
| Archive subfolder exists | Append seconds to timestamp to make unique |

---

## Context Files This Skill Reads

**Detection:**
- `.shipkit/**` - Current context folder
- `.shipkit-lite/**` - Legacy context folder
- `.claude/skills/shipkit-*/**` - Current skills
- `.claude/skills/lite-*/**` - Legacy skills
- `.claude/agents/*.md` - Installed agents
- `.claude/hooks/*.py` - Installed hooks
- `.claude/settings.json` - Main settings
- `.claude/settings.local.json` - Local overrides (scan only)
- `CLAUDE.md` - Root instructions
- `**/CLAUDE.md` - Subfolder instructions

**From GitHub:**
- `install/VERSION` - Target version (fetched to report version)
- `installers/install.py` - Python installer (fetched and executed)

The installer handles fetching and installing:
- Skills, agents, hooks, settings, templates, CLAUDE.md template

---

## Context Files This Skill Writes

**Archive (creates):**
- `.shipkit-archive/{timestamp}/` - Full archive folder
- `.shipkit-archive/{timestamp}/MANIFEST.md` - What was archived
- `.shipkit-archive/{timestamp}/context/` - Entire .shipkit/ contents
- `.shipkit-archive/{timestamp}/CLAUDE.md.backup` - Original CLAUDE.md
- `.shipkit-archive/{timestamp}/settings.json.backup` - Original settings

**Install (creates/overwrites):**
- `.shipkit/` - Context folder structure
- `.shipkit/templates/` - Fresh templates
- `.claude/skills/shipkit-*/` - All skills
- `.claude/agents/shipkit-*.md` - All agents
- `.claude/hooks/shipkit-*.py` - All hooks
- `.claude/rules/shipkit.md` - Framework rules (always replaced)

**Merge (modifies):**
- `.claude/settings.json` - Merged settings
- `CLAUDE.md` - Merged with markers
- `**/CLAUDE.md` - Any subfolder CLAUDE.md files

**Does NOT modify:**
- `.claude/settings.local.json` - User's local file (warn only)

---

## GitHub Repository Structure Expected

```
{repo}/
├── installers/
│   └── install.py                       # Python installer (fetched and run)
├── install/
│   ├── VERSION                          # e.g., "1.3.0"
│   ├── profiles/
│   │   └── shipkit.manifest.json        # What to install
│   ├── skills/
│   │   └── shipkit-*/SKILL.md           # All skills
│   ├── agents/
│   │   └── shipkit-*.md                 # All agents
│   ├── shared/hooks/
│   │   └── shipkit-*.py                 # All hooks
│   ├── rules/
│   │   └── shipkit.md                   # Framework rules (replace on update)
│   ├── settings/
│   │   └── shipkit.settings.json        # Settings template
│   ├── templates/
│   │   └── *.md                         # Template files
│   └── claude-md/
│       └── shipkit.md                   # CLAUDE.md template (user-editable)
├── docs/
│   └── generated/
│       └── shipkit-overview.html        # Skill reference (browser viewable)
```

---

## Configuration

**Default repository** (can be overridden):
```
SHIPKIT_REPO=https://github.com/stefan-stepzero/shipkit
```

**Override via argument:**
```
/shipkit-update repo:myorg/my-shipkit-fork
```

---

## When This Skill Integrates with Others

### After shipkit-update

| Skill | When to Use | Why |
|-------|-------------|-----|
| `/shipkit-project-context` | After fresh install | Scan codebase and generate stack.md |
| `/shipkit-why-project` | After fresh install (new project) | Define project vision if not migrated |
| `/shipkit-codebase-index` | After update | Refresh navigation index |

### Before shipkit-update

This skill is typically the **first skill run** — it bootstraps or updates the entire framework. No prerequisites.

### Related Skills

- `/shipkit-project-status` — Check project health after update
- `/shipkit-verify` — Verify the update completed correctly

---

<!-- SECTION:after-completion -->
## After Completion

**Post-update checklist:**

1. **Review merged files** — Check CLAUDE.md and settings.json look correct
2. **Check archive** — Originals in `.shipkit-archive/{timestamp}/` if needed
3. **Test a skill** — Try `/shipkit-project-status` to verify installation works
4. **Optional refresh** — Run `/shipkit-project-context` if you want fresh stack detection

**If something looks wrong:**
- Archive has all original files
- Restore specific files manually if needed
- Report issues for future improvements
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Permissions requested upfront (single approval, no interruptions)
- [ ] Detects all Shipkit variants (current + legacy naming)
- [ ] Archives completely before any modifications
- [ ] MANIFEST.md accurately records what was archived with versions
- [ ] Python installer fetched and executed successfully
- [ ] Framework files installed fresh match VERSION
- [ ] CLAUDE.md merged intelligently (user content preserved)
- [ ] settings.json merged intelligently (user permissions preserved)
- [ ] settings.local.json untouched (warning if stale)
- [ ] User context files migrated (including stack.md)
- [ ] No data loss possible (archive has everything)
<!-- /SECTION:success-criteria -->

---

## Security Notes

- Only fetches from specified GitHub repository
- Executes Python installer from trusted repo (user approved in Step 0)
- Installer only copies files — no network calls, no data exfiltration
- Archives are local, never uploaded
- settings.local.json never modified (privacy)

---

## Key Principle

**Archive first, merge with judgment, user reviews result.**

Claude uses intelligence to merge, not rigid find-replace rules. The archive is the safety net — if the merge isn't perfect, the original is always available.