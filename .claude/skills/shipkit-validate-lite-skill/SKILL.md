---
name: shipkit-validate-shipkit-skill
description: Validates a skill against quality standards and 7-file integration requirements. Reports issues and offers automated fixes. Use when checking if a skill is production-ready.
---

# shipkit-validate-shipkit-skill - Lite Skill Quality Validator

**Purpose**: Validate skills meet all quality standards and integration requirements

**What it does**: Checks SKILL.md quality, verifies 7-file integration, validates section markers, and offers automated fixes for common issues

---

## When to Invoke

**User says:**
- "Validate skill"
- "Check if [skill] is ready"
- "Audit shipkit-[skill-name]"
- "Is this skill complete?"
- "Quality check skill"

**Use when:**
- After creating a new skill
- Before committing changes to skill
- During skill maintenance/updates
- Troubleshooting why skill isn't working
- Checking section markers are in place

---

## Prerequisites

**Required**:
- Skill exists in `install/skills/shipkit-{skill-name}/`
- SKILL.md file exists

**Helpful context**:
- Understanding of quality standards → See `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md`
- Understanding of 7-file integration → See `claude-code-best-practices/SHIPKIT-7-FILE-INTEGRATION.md`
- Section markers → See `install/skills/_templates/`

---

## Process

### Step 0: Ensure Changelog Freshness

**Before running any checks, verify the Claude Code changelog is current.**

```
1. Check if docs/development/claude-code-changelog.meta.json exists
   If NOT exists → run: bash docs/development/fetch-changelog.sh

2. If exists, read fetchedAt timestamp
   If older than 7 days → run: bash docs/development/fetch-changelog.sh

3. Read latestVersion from meta.json
   Store as: claude_code_version (e.g., "2.1.34")
```

**Why**: Skills must align with current Claude Code capabilities. Stale changelog = stale validation.

---

### Step 1: Identify Skill to Validate

**Ask user**:
```
Which skill should I validate?

Options:
1. Specify skill name (e.g., "shipkit-spec", "shipkit-plan")
2. Validate all skills
3. List available skills first

→ [user choice]
```

**If user chooses "list"**:
```bash
ls -1 install/skills/shipkit-*/SKILL.md | sed 's|install/skills/||' | sed 's|/SKILL.md||'
```

**Store**: `skill_name` (e.g., "shipkit-spec")

---

### Step 2: Run Quality Checks

**Validation Categories**:

#### 2.1: YAML Frontmatter Validation

**Check**: `install/skills/{skill_name}/SKILL.md` frontmatter

```markdown
✓ YAML frontmatter check:
- [ ] Has `name` field
- [ ] Has `description` field
- [ ] name: lowercase, hyphens only, < 64 chars
- [ ] name: matches directory name
- [ ] name: starts with "shipkit-"
- [ ] description: third-person voice (not "I can" or "You can")
- [ ] description: includes WHAT and WHEN
- [ ] description: < 1024 chars
```

**Validation code**:
```python
import re
from pathlib import Path

def validate_frontmatter(skill_name):
    skill_md = Path(f'install/skills/{skill_name}/SKILL.md')
    content = skill_md.read_text()

    # Extract frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return ["ERROR: No YAML frontmatter found"]

    frontmatter = match.group(1)
    issues = []

    # Check name field
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        issues.append("ERROR: Missing 'name' field")
    else:
        name = name_match.group(1).strip()
        if name != skill_name:
            issues.append(f"ERROR: name '{name}' doesn't match directory '{skill_name}'")
        if not re.match(r'^shipkit-[a-z0-9-]+$', name):
            issues.append(f"ERROR: name '{name}' must start with 'shipkit-' and use lowercase/hyphens")
        if len(name) > 64:
            issues.append(f"ERROR: name '{name}' exceeds 64 chars")

    # Check description field
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    if not desc_match:
        issues.append("ERROR: Missing 'description' field")
    else:
        desc = desc_match.group(1).strip()
        if len(desc) > 1024:
            issues.append(f"WARNING: description exceeds 1024 chars ({len(desc)} chars)")
        if re.search(r'\b(I can|You can|I will|You should)\b', desc, re.IGNORECASE):
            issues.append("ERROR: description uses first/second person (must be third-person)")
        if not re.search(r'\bUse when\b', desc, re.IGNORECASE):
            issues.append("WARNING: description doesn't include 'Use when' trigger")

    return issues
```

---

#### 2.2: SKILL.md Quality Checks

**Check**: SKILL.md structure and content

```markdown
✓ SKILL.md quality check:
- [ ] File length < 500 lines (target < 300 for lite)
- [ ] Has "When to Invoke" section
- [ ] Has "Prerequisites" section
- [ ] Has "Process" section with clear steps
- [ ] Has "When This Skill Integrates with Others" section
- [ ] Has "Context Files This Skill Reads" section
- [ ] Has "Context Files This Skill Writes" section
- [ ] Cross-references use forward slashes (not backslashes)
- [ ] Cross-references are one level deep
```

**Validation code**:
```python
def validate_skill_md_quality(skill_name):
    skill_md = Path(f'install/skills/{skill_name}/SKILL.md')
    content = skill_md.read_text()
    lines = content.splitlines()

    issues = []

    # Check line count
    if len(lines) > 500:
        issues.append(f"WARNING: SKILL.md has {len(lines)} lines (limit: 500)")

    # Check required sections
    required_sections = [
        "When to Invoke",
        "Prerequisites",
        "Process",
        "When This Skill Integrates with Others",
        "Context Files This Skill Reads",
        "Context Files This Skill Writes"
    ]

    for section in required_sections:
        if section not in content:
            issues.append(f"ERROR: Missing required section: '{section}'")

    # Check for backslashes in paths
    if '\\' in content and 'install\\skills' in content:
        issues.append("ERROR: Uses backslashes in paths (must use forward slashes)")

    return issues
```

---

#### 2.3: Cross-Reference Validation

**Check**: "When This Skill Integrates with Others" section quality

```markdown
✓ Cross-reference check:
- [ ] Has "Before This Skill" subsection
- [ ] Has "After This Skill" subsection
- [ ] References are bidirectional (if A → B, then B → A)
- [ ] References include WHY and WHEN (not just skill names)
- [ ] No generic lists (must have causality/triggers)
```

**See**: `SKILL-QUALITY-AND-PATTERNS.md` Part 1.2

---

#### 2.4: Quality Pattern Validation

**Check**: Skill includes appropriate quality patterns based on type

**Artifact skills**:
```markdown
✓ Artifact quality check:
- [ ] Has quality checklist in output template
- [ ] Checklist has clear binary checks
- [ ] Checklist organized by concern (Requirements, Completeness, Clarity)
- [ ] Checklist includes blocking reminder before next step
```

**Methodology skills**:
```markdown
✓ Methodology quality check:
- [ ] Has "The Iron Law" section
- [ ] Iron Law is memorable single rule in ALL CAPS
- [ ] Has "Red Flags" section
- [ ] Red Flags document common rationalizations
- [ ] Red Flags provide alternatives
```

**See**: `SKILL-QUALITY-AND-PATTERNS.md` Part 1.3-1.4

---

### Step 3: Validate 7-File Integration

**Check all 7 integration files**:

#### 3.1: File 1 - SKILL.md Exists

```bash
[ -f install/skills/{skill_name}/SKILL.md ] && echo "✓" || echo "✗ MISSING"
```

---

#### 3.2: File 2 - Overview.html Entry

**Check**: `help/shipkit-shipkit-overview.html`

```python
def validate_overview_html(skill_name):
    html_path = Path('help/shipkit-shipkit-overview.html')
    html = html_path.read_text()

    issues = []

    # Check if skill is listed
    if f'<strong>{skill_name}</strong>' not in html:
        issues.append(f"ERROR: {skill_name} not found in overview.html")

    # Check skill count (count all <strong>shipkit-*</strong> entries)
    skill_count = len(re.findall(r'<strong>shipkit-\w+</strong>', html))
    stat_match = re.search(r'<span class="stat-number">(\d+)</span>', html)
    if stat_match:
        displayed_count = int(stat_match.group(1))
        if displayed_count != skill_count:
            issues.append(f"WARNING: Skill count shows {displayed_count} but found {skill_count} skills")

    return issues
```

---

#### 3.3: File 3 - shipkit.md Entry

**Check**: `install/claude-md/shipkit.md`

```python
def validate_claude_md(skill_name):
    md_path = Path('install/claude-md/shipkit.md')
    md = md_path.read_text()

    issues = []

    # Check if skill is listed
    if f'/{skill_name}` -' not in md:
        issues.append(f"ERROR: /{skill_name} not found in shipkit.md")

    return issues
```

---

#### 3.4: File 4 - Manifest Entry

**Check**: `install/profiles/shipkit.manifest.json`

```python
import json

def validate_manifest(skill_name):
    manifest_path = Path('install/profiles/shipkit.manifest.json')
    manifest = json.loads(manifest_path.read_text())

    issues = []

    # Check if skill is in definitions
    if skill_name not in manifest['skills']['definitions']:
        issues.append(f"ERROR: {skill_name} not in shipkit.manifest.json definitions")

    # Validate JSON syntax
    try:
        json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        issues.append(f"ERROR: JSON syntax error in manifest: {e}")

    return issues
```

---

#### 3.5: File 5 - Hook Entry (Optional)

**Check**: `install/shared/hooks/shipkit-after-skill-router.py`

**Note**: Not all skills need hook detection - this is OPTIONAL. Only needed if skill triggers detection.

```python
def validate_hook(skill_name):
    hook_path = Path('install/shared/hooks/shipkit-after-skill-router.py')
    hook = hook_path.read_text()

    # This is optional - just check Python syntax
    import subprocess
    result = subprocess.run(
        ['python', '-m', 'py_compile', str(hook_path)],
        capture_output=True
    )

    if result.returncode != 0:
        return [f"ERROR: Python syntax error in shipkit-after-skill-router.py: {result.stderr.decode()}"]

    return []  # No issues - hook is optional
```

---

#### 3.6: File 6 - Master Routing Entry

**Check**: `install/skills/shipkit-master/SKILL.md`

```python
def validate_master_routing(skill_name):
    master_path = Path('install/skills/shipkit-master/SKILL.md')
    master = master_path.read_text()

    issues = []

    # Check if skill is in routing table
    if f'/{skill_name}' not in master:
        issues.append(f"ERROR: {skill_name} not found in master routing table")

    return issues
```

---

#### 3.7: File 7 - Settings Permission

**Check**: `install/settings/shipkit.settings.json`

```python
def validate_settings(skill_name):
    settings_path = Path('install/settings/shipkit.settings.json')
    settings = json.loads(settings_path.read_text())

    issues = []

    # Check if skill permission exists
    permission = f'Skill({skill_name})'
    if permission not in settings['permissions']['allow']:
        issues.append(f"ERROR: {permission} not in settings.json allow list")

    # Validate JSON syntax
    try:
        json.loads(settings_path.read_text())
    except json.JSONDecodeError as e:
        issues.append(f"ERROR: JSON syntax error in settings: {e}")

    return issues
```

---

#### 3.8: Section Markers Validation

**Check**: SKILL.md has standard section markers

```python
def validate_section_markers(skill_name):
    skill_path = Path(f'install/skills/{skill_name}/SKILL.md')
    content = skill_path.read_text()

    issues = []

    # Check for after-completion section marker
    if '<!-- SECTION:after-completion -->' not in content:
        issues.append(f"WARNING: {skill_name} missing <!-- SECTION:after-completion --> marker")

    # Check for proper closing tags
    if '<!-- SECTION:after-completion -->' in content:
        if '<!-- /SECTION:after-completion -->' not in content:
            issues.append(f"ERROR: {skill_name} has unclosed after-completion section")

    # Optional: check for success-criteria section
    if '<!-- SECTION:success-criteria -->' in content:
        if '<!-- /SECTION:success-criteria -->' not in content:
            issues.append(f"ERROR: {skill_name} has unclosed success-criteria section")

    return issues
```

**Why this matters:**
- Section markers enable batch updates via `scripts/skill-sections.py`
- Guardrails in after-completion replace mandatory skill chaining
- Standardization across all skills

---

### Step 3b: Claude Code Compatibility Checks

**Check skill against current Claude Code changelog** (`docs/development/claude-code-changelog.md`):

#### 3b.1: Frontmatter Field Validation

**Check**: Skill uses valid, current frontmatter fields

```markdown
✓ Frontmatter compatibility check:
- [ ] `name` — valid since v2.0.20
- [ ] `description` — valid since v2.0.20
- [ ] `context: fork` — valid since v2.1.0 (if used)
- [ ] `agent` — valid since v2.1.0 (if used)
- [ ] `hooks` — valid since v2.1.0 (if used)
- [ ] `user-invocable` — valid since v2.1.0 (if used)
- [ ] `allowed-tools` — YAML-style lists valid since v2.1.0
- [ ] No unrecognized frontmatter fields
```

**Known valid skill frontmatter fields** (as of changelog):
`name`, `description`, `context`, `agent`, `hooks`, `user-invocable`, `allowed-tools`, `argument-hint`, `skills`

**Flag**: Any frontmatter field NOT in this list → WARNING: Unrecognized field

---

#### 3b.2: Agent Frontmatter Validation (if skill references agents)

**Check**: Any agent files referenced by the skill use current fields

```markdown
✓ Agent compatibility check (if applicable):
- [ ] `model` — valid since v2.0.64
- [ ] `permissionMode` — valid since v2.0.43
- [ ] `disallowedTools` — valid since v2.0.30
- [ ] `memory` — valid since v2.1.33 (user/project/local scope)
- [ ] `tools` — supports Task(agent_type) restriction since v2.1.33
- [ ] `hooks` — valid since v2.1.0
- [ ] `skills` — valid since v2.0.43
```

---

#### 3b.3: Deprecated Pattern Detection

**Check**: Skill doesn't use patterns that have been deprecated or superseded

```markdown
✓ Deprecated pattern check:
- [ ] NOT using .claude.json allowedTools (removed v2.0.8, use settings.json)
- [ ] NOT using .claude.json ignorePatterns (removed v2.0.8, use settings.json)
- [ ] NOT referencing legacy SDK entrypoint (removed v1.0.123)
- [ ] NOT using Bash for file operations where dedicated tools exist (v2.1.0+ guidance)
- [ ] NOT using includeCoAuthoredBy (deprecated v2.0.62, use attribution setting)
```

---

#### 3b.4: Feature Opportunity Check

**Check**: Skill could benefit from newer Claude Code features it doesn't use

```markdown
⚡ Feature opportunity check (INFO level, not blocking):
- [ ] Could skill benefit from `context: fork`? (v2.1.0 — runs in sub-agent)
- [ ] Could skill benefit from `memory` on its agent? (v2.1.33 — persistent memory)
- [ ] Could skill benefit from `hooks` in frontmatter? (v2.1.0 — lifecycle hooks)
- [ ] Could skill use YAML-style allowed-tools? (v2.1.0 — cleaner declarations)
- [ ] Is skill description under 2% of context budget? (v2.1.32 — scales with context)
```

**Note**: These are suggestions, not errors. Report as INFO level.

---

### Step 4: Report Results

**Generate validation report**:

```
============================================
Validation Report: {skill_name}
============================================

✓ YAML Frontmatter
  ✓ name: {name}
  ✓ description: {desc_preview}...

✓ SKILL.md Quality
  ✓ Length: {line_count} lines (< 500)
  ✓ All required sections present
  ✓ Cross-references valid

⚠ Quality Patterns
  ✓ Has quality checklist (artifact)
  ✗ Missing Iron Law section (methodology)

✓ 7-File Integration
  ✓ File 1: SKILL.md exists
  ✓ File 2: Listed in overview.html
  ✓ File 3: Listed in shipkit.md
  ✓ File 4: In manifest.json
  ⊘ File 5: Hook optional (not modified)
  ✓ File 6: In master routing
  ✓ File 7: Permission in settings.json

✓ Section Markers
  ✓ Has <!-- SECTION:after-completion --> marker

✓ Claude Code Compatibility (changelog v{claude_code_version})
  ✓ All frontmatter fields recognized
  ✓ No deprecated patterns
  ⓘ Could benefit from `context: fork` (v2.1.0)

============================================
RESULT: {PASS/FAIL with X issues}
============================================

Issues found:
1. [ERROR] Missing Iron Law section (methodology skill)
2. [WARNING] Description doesn't include "Use when"
3. [ERROR] Not listed in master routing table

Fixes available:
→ Run `/shipkit-fix-shipkit-skill {skill_name}` to auto-fix issues
→ Or manually fix issues above
```

---

### Step 5: Offer Fixes

**For each issue, offer automated fix**:

```
Found 3 issues. Offer fixes? (y/n)

If yes:
1. ERROR: Missing master routing
   → Add these keywords to routing table: [suggest based on description]
   → Add to {category} table

2. WARNING: Skill count mismatch (overview.html shows 17, found 18)
   → Update count to 18

3. ERROR: Missing settings permission
   → Add "Skill({skill_name})" to shipkit.settings.json

Apply all fixes? (y/n/selective)
```

---

## Validation Checklist Reference

**Complete checklist** (see `references/validation-checklist.md`):

### Official Claude Code Requirements
- [ ] YAML frontmatter valid
- [ ] name: lowercase, hyphens, < 64 chars, starts with "shipkit-"
- [ ] description: third-person, includes WHAT + WHEN, < 1024 chars
- [ ] SKILL.md < 500 lines
- [ ] Forward slashes in paths (not backslashes)

### Claude Code Compatibility (from changelog)
- [ ] All frontmatter fields are recognized and current
- [ ] No deprecated patterns used (.claude.json allowedTools, legacy SDK, etc.)
- [ ] Agent frontmatter fields valid if agents referenced
- [ ] Feature opportunities noted (INFO level)

### Shipkit Quality Standards (Part 1)
- [ ] Has "When This Skill Integrates with Others" section
- [ ] Cross-references are bidirectional with WHY and WHEN
- [ ] Has quality checklist (artifact) OR Iron Laws + Red Flags (methodology)
- [ ] References are one level deep
- [ ] Prerequisites clearly stated

### 7-File Integration
- [ ] File 1: SKILL.md exists
- [ ] File 2: Listed in help/shipkit-shipkit-overview.html
- [ ] File 3: Listed in install/claude-md/shipkit.md
- [ ] File 4: In install/profiles/shipkit.manifest.json
- [ ] File 5: Hook updated if needed (optional)
- [ ] File 6: In install/skills/shipkit-master/SKILL.md routing
- [ ] File 7: Permission in install/settings/shipkit.settings.json

### Section Markers
- [ ] Has `<!-- SECTION:after-completion -->` marker
- [ ] Section properly closed with `<!-- /SECTION:after-completion -->`

---

## When This Skill Integrates with Others

### After shipkit-validate-shipkit-skill
- `/shipkit-fix-shipkit-skill` - Apply automated fixes to issues found
  - **Trigger**: Validation found fixable issues
  - **Why**: Automate corrections instead of manual edits

### Before shipkit-validate-shipkit-skill
- `/shipkit-create-shipkit-skill` - Creates skill to validate
  - **Natural flow**: Create → Validate → Fix → Commit

### Related Skills
- `/shipkit-create-shipkit-skill` - Create new skills
- `/shipkit-audit-repo` - Audit entire repo health (validates ALL skills)

---

## Context Files This Skill Reads

**Validation targets (7 files)**:
- `install/skills/{skill-name}/SKILL.md` - Main skill file
- `help/shipkit-shipkit-overview.html` - Overview page
- `install/claude-md/shipkit.md` - Skill invocations
- `install/profiles/shipkit.manifest.json` - Manifest definitions
- `install/shared/hooks/shipkit-after-skill-router.py` - Hook file (optional)
- `install/skills/shipkit-master/SKILL.md` - Master routing
- `install/settings/shipkit.settings.json` - Permissions

**Section templates**:
- `install/skills/_templates/after-completion.md` - Standard guardrails section
- `install/skills/_templates/success-criteria.md` - Standard checklist

**Quality standards**:
- `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md` - Universal standards
- `claude-code-best-practices/SHIPKIT-7-FILE-INTEGRATION.md` - Integration checklist

**Claude Code changelog** (auto-fetched if stale):
- `docs/development/claude-code-changelog.md` - Full changelog from GitHub
- `docs/development/claude-code-changelog.meta.json` - Freshness metadata
- `docs/development/fetch-changelog.sh` - Fetch script

---

## Context Files This Skill Writes

**Write Strategy: NONE** (Validation skill, no file output)

**This skill:**
- ❌ Does not create or modify files
- ✅ Reads files to validate structure
- ✅ Reports issues found
- ✅ Offers fixes (via separate fix skill)

**To apply fixes**: Use `/shipkit-fix-shipkit-skill {skill-name}` (separate skill)

---

## Success Criteria

Validation is complete when:
- [ ] Changelog freshness verified (fetched if stale >7 days)
- [ ] All quality checks run
- [ ] All 7-file integration checks run
- [ ] Claude Code compatibility checks run
- [ ] Clear report generated with PASS/FAIL
- [ ] Issues listed with severity (ERROR/WARNING/INFO)
- [ ] Fixes offered for each issue
- [ ] User knows next steps

---

## Example Validation Session

```
User: "/shipkit-validate-shipkit-skill shipkit-spec"

Claude:
1. Read install/skills/shipkit-spec/SKILL.md
2. Run quality checks:
   ✓ YAML frontmatter valid
   ✓ 287 lines (< 500)
   ✓ All required sections
   ⚠ Cross-references missing "why" context
3. Run integration checks:
   ✓ All 7 files updated
4. Generate report:
   RESULT: PASS with 1 warning
5. Offer fix:
   "Update cross-references to include 'why'? (y/n)"
```

---

**Remember**: This skill VALIDATES only. Use `/shipkit-fix-shipkit-skill` to apply fixes.
