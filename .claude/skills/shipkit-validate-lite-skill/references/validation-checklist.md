# Lite Skill Validation Checklist

**Purpose**: Comprehensive quality checklist for skills

**Use**: Referenced by shipkit-validate-shipkit-skill for validation logic

---

## Part 1: Official Claude Code Requirements

**Source**: `claude-code-best-practices/claude-code-references/skill-authoring-best-practice.md`

### YAML Frontmatter
- [ ] Has `---` YAML delimiters
- [ ] Has `name` field (required)
- [ ] Has `description` field (required)
- [ ] `name`: lowercase letters, numbers, hyphens only
- [ ] `name`: 1-64 characters
- [ ] `name`: does NOT start or end with hyphen
- [ ] `name`: does NOT contain consecutive hyphens (`--`)
- [ ] `name`: matches parent directory name
- [ ] `name`: starts with `shipkit-` prefix
- [ ] `description`: non-empty
- [ ] `description`: maximum 1024 characters
- [ ] `description`: third-person voice (NOT "I can" or "You can")
- [ ] `description`: includes WHAT the skill does
- [ ] `description`: includes WHEN to use it
- [ ] `description`: includes specific keywords for discovery

### File Structure
- [ ] SKILL.md exists
- [ ] SKILL.md is under 500 lines (target < 300 for lite)
- [ ] Uses forward slashes in paths (NOT backslashes)
- [ ] File references are one level deep from SKILL.md
- [ ] No deeply nested reference chains

---

## Part 2: Shipkit Quality Standards

**Source**: `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md`

### Required Sections
- [ ] "When to Invoke" section exists
- [ ] "Prerequisites" section exists
- [ ] "Process" section with numbered steps
- [ ] "When This Skill Integrates with Others" section
- [ ] "Context Files This Skill Reads" section
- [ ] "Context Files This Skill Writes" section
- [ ] "Success Criteria" section

### Cross-Referencing (Part 1.2)
- [ ] Has "When This Skill Integrates with Others" section
- [ ] Has "Before This Skill" subsection
- [ ] Has "After This Skill" subsection
- [ ] References include WHY each skill is needed (not just names)
- [ ] References include WHEN to invoke (conditions/triggers)
- [ ] NOT just generic lists - has causality
- [ ] Bidirectional references (if A → B, then B → A)

### JSON Artifact Convention
- [ ] If skill outputs structured data to `.shipkit/`, uses `.json` format (not `.md`)
- [ ] JSON output includes `$schema: "shipkit-artifact"` field
- [ ] JSON output includes `type`, `version`, `lastUpdated`, `source` fields
- [ ] JSON output includes `summary` object for dashboard rendering
- [ ] SKILL.md documents the complete JSON schema
- [ ] Reference implementation: `install/skills/shipkit-goals/SKILL.md`

**Skills that should remain markdown**: specs, plans, architecture decisions (narrative content).
**Skills that should migrate to JSON**: goals, project health, any structured/countable data.

### Quality Patterns

**For Artifact Skills** (Part 1.3):
- [ ] Output template includes quality checklist
- [ ] Checklist has clear binary checks (yes/no)
- [ ] Checklist organized by concern (Requirements, Completeness, Clarity)
- [ ] Checklist includes blocking reminder ("Before X, ensure...")
- [ ] Checklist embedded IN output file (not just SKILL.md)

**For Methodology Skills** (Part 1.4):
- [ ] Has "The Iron Law" section
- [ ] Iron Law is single memorable rule in ALL CAPS
- [ ] Iron Law includes explanation of WHY
- [ ] Iron Law includes consequences of breaking it
- [ ] Has "Red Flags" section
- [ ] Red Flags document 3+ common rationalizations
- [ ] Each Red Flag includes "Why dangerous" + "Reality" + "Instead"

### Logical Pathways Referenced

**Quick Exit Check** (Part 2.1):
- [ ] OVERWRITE/MULTIPLE skills check for recent output (< 5 min)
- [ ] Ask user "Use this or regenerate?" if recent
- [ ] Save tokens by avoiding redundant generation

**File Exists Workflow** (Part 2.2):
- [ ] OVERWRITE skills offer View/Update/Replace/Cancel
- [ ] Read existing file before overwriting
- [ ] Archive old version if replacing (Part 2.5)

**Duplicate Detection** (Part 2.4):
- [ ] APPEND skills check for similar entries
- [ ] Search last N entries for duplicates
- [ ] Ask "Update existing or add new?" if found

---

## Part 3: Lite Design Philosophy

**Source**: `claude-code-best-practices/SHIPKIT-DESIGN-PHILOSOPHY.md`

### Lite Characteristics
- [ ] SKILL.md targets < 300 lines
- [ ] Asks 3-5 questions maximum (not 10-20)
- [ ] Generates 1-2 page outputs (not 5-10)
- [ ] Focuses on happy path only
- [ ] Skips edge cases, error handling (unless critical)
- [ ] Uses single examples.md (not references/ folder)
- [ ] Completes in 10-20 minutes
- [ ] Never reads constitution (assumes POC mode)

### File Structure (Lite)
- [ ] Has SKILL.md (required)
- [ ] Has templates/ folder (if artifact skill)
- [ ] Has scripts/ folder (if script-driven)
- [ ] Has examples.md at root (NOT in references/)
- [ ] Does NOT have references/ folder (use single examples.md)

---

## Part 4: 7-File Integration

**Source**: `claude-code-best-practices/SHIPKIT-7-FILE-INTEGRATION.md`

### File 1: SKILL.md
- [ ] Exists at `install/skills/shipkit-{skill-name}/SKILL.md`
- [ ] YAML frontmatter valid
- [ ] All required sections present

### File 2: help/shipkit-shipkit-overview.html
- [ ] Skill listed in correct category section
- [ ] Entry format: `<li><strong>shipkit-{skill-name}</strong> - {2-4 word description}</li>`
- [ ] Skill count incremented (stat-number)
- [ ] In alphabetical order within category

### File 3: install/claude-md/shipkit.md
- [ ] Skill listed in correct section
- [ ] Entry format: `- /shipkit-{skill-name} - {purpose} → {output_path}`
- [ ] In alphabetical order within section
- [ ] Output path format matches output strategy

### File 4: install/profiles/shipkit.manifest.json
- [ ] Skill in `skills.definitions` array
- [ ] JSON syntax valid (no trailing commas)
- [ ] Entry format: `"shipkit-{skill-name}"`

### File 5: install/shared/hooks/suggest-next-skill.py
- [ ] Python syntax valid (`python -m py_compile`)
- [ ] Optional: Detection logic added (if deterministic next step)
- [ ] Optional: Suggestion message added

### File 6: install/skills/shipkit-master/SKILL.md
- [ ] Skill in routing table
- [ ] Entry in correct category table
- [ ] Keywords quoted and comma-separated
- [ ] Context files specified
- [ ] Format: `| "keyword1", "keyword2" | /shipkit-{skill} | context-files |`

### File 7: install/settings/shipkit.settings.json
- [ ] Skill permission in `permissions.allow` array
- [ ] JSON syntax valid
- [ ] Entry format: `"Skill(shipkit-{skill-name})"`

---

## Part 4b: Claude Code Compatibility

**Source**: `docs/development/claude-code-changelog.md` (auto-fetched from GitHub)

### Changelog Freshness
- [ ] `docs/development/claude-code-changelog.meta.json` exists
- [ ] `fetchedAt` is within 7 days
- [ ] If stale or missing: run `bash docs/development/fetch-changelog.sh`

### Skill Frontmatter Compatibility
Known valid fields (update as changelog evolves):
- [ ] `name` — since v2.0.20
- [ ] `description` — since v2.0.20
- [ ] `context` — since v2.1.0 (supports `fork`)
- [ ] `agent` — since v2.1.0
- [ ] `hooks` — since v2.1.0
- [ ] `user-invocable` — since v2.1.0
- [ ] `allowed-tools` — since v2.0.20 (YAML-style lists since v2.1.0)
- [ ] `argument-hint` — since v1.0.54
- [ ] `skills` — since v2.0.43

### Agent Frontmatter Compatibility
- [ ] `model` — since v2.0.64
- [ ] `permissionMode` — since v2.0.43
- [ ] `disallowedTools` — since v2.0.30
- [ ] `memory` — since v2.1.33 (scope: user/project/local)
- [ ] `tools` — since v2.1.33 (supports Task(agent_type) restriction)
- [ ] `hooks` — since v2.1.0
- [ ] `skills` — since v2.0.43

### Deprecated Patterns
- [ ] NOT using `.claude.json` allowedTools (removed v2.0.8)
- [ ] NOT using `.claude.json` ignorePatterns (removed v2.0.8)
- [ ] NOT referencing legacy SDK entrypoint (removed v1.0.123)
- [ ] NOT using `includeCoAuthoredBy` (deprecated v2.0.62, use `attribution`)
- [ ] NOT using Bash for file ops where dedicated tools exist (v2.1.0+ guidance)

### Feature Opportunities (INFO)
- [ ] Could benefit from `context: fork`? (v2.1.0)
- [ ] Could benefit from agent `memory` field? (v2.1.33)
- [ ] Could benefit from frontmatter `hooks`? (v2.1.0)
- [ ] Could use YAML-style `allowed-tools`? (v2.1.0)
- [ ] Description within 2% context budget? (v2.1.32)

---

## Part 5: Content Quality

### Terminology
- [ ] Consistent terminology throughout
- [ ] No mixing synonyms (e.g., "API endpoint" vs "URL" vs "path")

### Examples
- [ ] Concrete examples (not abstract placeholders)
- [ ] Input/output pairs shown
- [ ] Examples are realistic

### Workflows
- [ ] Clear numbered steps
- [ ] Checkboxes for multi-step processes
- [ ] Conditional branching clearly marked

### Common Mistakes Avoided
- [ ] No Windows-style paths (backslashes)
- [ ] No time-sensitive information
- [ ] No vague names ("helper", "utils")
- [ ] No first/second person in description
- [ ] No deeply nested references

---

## Validation Script Usage

**This checklist is implemented in validation scripts**:

```python
# Example validation function
def validate_lite_skill(skill_name):
    results = {
        "official": validate_official_requirements(skill_name),
        "quality": validate_quality_standards(skill_name),
        "philosophy": validate_lite_philosophy(skill_name),
        "integration": validate_7_file_integration(skill_name)
    }
    return results
```

---

## Pass/Fail Criteria

### PASS
All ERROR items resolved, WARNINGS acceptable

### FAIL
Any ERROR items present

### Severity Levels

**ERROR** (must fix):
- Missing required sections
- Invalid YAML frontmatter
- Missing from integration files
- Broken bidirectional references
- First/second person in description
- Missing quality patterns (checklist or Iron Laws)

**WARNING** (should fix):
- Over 500 lines (target < 300)
- Over 1024 char description
- Missing "Use when" in description
- No examples provided
- Complex cross-reference chains

**INFO** (optional):
- Could add more examples
- Could improve naming
- Could expand documentation

---

## Quick Reference

| Check | Pass If | Fail If |
|-------|---------|---------|
| YAML frontmatter | Valid, third-person, includes WHAT+WHEN | Missing fields, first-person |
| SKILL.md length | < 500 lines (< 300 ideal) | > 500 lines |
| Cross-references | Bidirectional with WHY/WHEN | Generic lists, no causality |
| Quality patterns | Has checklist (artifact) OR Iron Laws (methodology) | Missing patterns |
| 7-file integration | All 7 files updated | Missing from any file |
| File structure | Uses lite conventions | Uses full skill patterns |

---

**Use this checklist**: Run `/shipkit-validate-shipkit-skill {skill-name}` to automate validation
