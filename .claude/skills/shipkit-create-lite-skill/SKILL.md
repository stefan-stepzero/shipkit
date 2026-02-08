---
name: shipkit-create-shipkit-skill
description: Interactive wizard to create new skills with automatic 7-file integration. Scaffolds SKILL.md from templates based on skill type and updates all integration files. Use when adding a new skill to Shipkit.
---

# shipkit-create-shipkit-skill - New Lite Skill Wizard

**Purpose**: Create a new skill with automatic 7-file integration

**What it does**: Interactive wizard that scaffolds a new skill, generates SKILL.md from appropriate template based on skill type, updates all 7 integration files, and adds standard section markers

---

## When to Invoke

**User says:**
- "Create a new skill"
- "Add a skill for [feature]"
- "Scaffold a skill"
- "New skill for lite"
- "Build a skill"

**Use when:**
- Starting a new skill from scratch
- Want automated 7-file integration
- Need correct template based on skill type

---

## Prerequisites

**Required understanding:**
- Lite vs full skills → See `claude-code-best-practices/SHIPKIT-DESIGN-PHILOSOPHY.md`
- 7-file integration system → See `claude-code-best-practices/SHIPKIT-7-FILE-INTEGRATION.md`
- Quality standards → See `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md`

**No file prerequisites** - this is a creation skill

---

## Process

### Step 0: Ensure Changelog Freshness

**Before scaffolding, verify Claude Code changelog is current so generated skills use valid patterns.**

```
1. Check if docs/development/claude-code-changelog.meta.json exists
   If NOT exists → run: bash docs/development/fetch-changelog.sh

2. If exists, read fetchedAt timestamp
   If older than 7 days → run: bash docs/development/fetch-changelog.sh

3. Read latestVersion from meta.json
   Store as: claude_code_version (e.g., "2.1.34")
```

**Why**: New skills must use current frontmatter fields and patterns. Scaffolding against a stale understanding of Claude Code = broken skills.

**Current valid skill frontmatter fields** (from changelog):
- `name` (required) — since v2.0.20
- `description` (required) — since v2.0.20
- `context` — since v2.1.0 (supports `fork` for sub-agent execution)
- `agent` — since v2.1.0 (specifies agent type)
- `hooks` — since v2.1.0 (lifecycle hooks in frontmatter)
- `user-invocable` — since v2.1.0 (opt-out from slash menu with `false`)
- `allowed-tools` — YAML-style lists since v2.1.0
- `argument-hint` — since v1.0.54
- `skills` — since v2.0.43 (auto-load skills for subagents)

**Use these fields when generating YAML frontmatter in Step 3.**

---

### Step 1: Gather Information (Interactive Wizard)

**Ask user these questions in sequence:**

#### 1.1: Skill Name
```
What should this skill be called? (without 'shipkit-' prefix)
Examples: spec, plan, communications, architecture-memory, user-stories

→ [user input]
```

**Process:**
- Store user input
- Add `shipkit-` prefix automatically
- Verify skill doesn't already exist in `install/skills/`
- If exists: Ask user to choose different name or confirm overwrite

---

#### 1.2: Purpose
```
What does this skill do? (one sentence)
This will be used in the description field and documentation.

Example: "Creates user stories with acceptance criteria from feature descriptions"

→ [user input]
```

**Store for:** YAML frontmatter description, documentation

---

#### 1.3: Category
```
Which category does this skill belong to?

1. Meta/Infrastructure - project-context, project-status, shipkit-master
2. Decision & Design - spec, architecture-memory, ux-coherence, data-consistency
3. Implementation - plan, implement
4. Documentation - component-knowledge, route-knowledge, document-artifact, communications
5. Quality & Process - quality-confidence, work-memory, debug-systematically

Choose 1-5:
```

**Use for:**
- Determining section in overview.html
- Determining section in shipkit.md
- Determining routing table in master

---

#### 1.4: Primary Type (Determines Quality Pattern)
```
What type of skill is this?

1. Artifact - Creates structured deliverables (specs, plans, docs, decision logs)
   → Template will include quality checklist section
   Examples: spec, plan, why-project, architecture-memory, component-knowledge

2. Methodology - Teaches a process or discipline (TDD, debugging, verification)
   → Template will include Iron Laws + Red Flags sections
   Examples: implement, debug-systematically, quality-confidence, ux-coherence

3. Utility - Supporting function (scanning, transforming, routing, clarifying)
   → Template will have basic structure only
   Examples: project-status, communications, clarify, shipkit-master

Choose 1, 2, or 3:
```

**Store as:** `skill_type` (artifact|methodology|utility)

**Determines:** Which template to use, which quality patterns to include

---

#### 1.5: Output Strategy (If Skill Creates Files)
```
How does this skill write output?

1. OVERWRITE - Creates/replaces a single file each time
   Examples: goals.json, why.json, latest.html
   → Will apply Quick Exit Check + File Exists Workflow patterns

2. APPEND - Adds entries to an ongoing file
   Examples: architecture.json, implementations.json
   → Will apply Duplicate Detection pattern

3. MULTIPLE - Creates a separate file per invocation
   Examples: specs/active/[feature].json, plans/active/[feature].json
   → Will apply Quick Exit Check pattern

4. NONE - No file output (guidance/reporting only)
   Examples: implement (guidance), project-status (reporting)
   → No file patterns needed

Choose 1, 2, 3, or 4:
```

**Store as:** `output_strategy` (overwrite|append|multiple|none)

**Determines:** Which logical pathways (Part 2) to include

---

#### 1.5b: Output Format (If OVERWRITE or MULTIPLE)
```
What format should the output file use?

1. JSON - Structured data following the Shipkit Artifact Convention
   Use for: Goals, status, structured data that dashboards can visualize
   → Output as .json with required fields: $schema, type, version, lastUpdated, source, summary
   → RECOMMENDED for new artifact skills

2. Markdown - Human-readable document
   Use for: Specs, plans, architecture decisions, narrative content
   → Output as .md with standard sections

Choose 1 or 2:
```

**Store as:** `output_format` (json|markdown)

**If JSON**: The generated SKILL.md will include the Shipkit Artifact Convention:
```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

**Reference implementation**: See `install/skills/shipkit-goals/SKILL.md` for a complete JSON artifact skill.

---

#### 1.6: Output Location (If Not NONE)
```
Where does this skill write output?

Use placeholders for dynamic parts:
- [feature] for feature name
- [component] for component name
- [name] for generic name

Examples (JSON artifacts):
- .shipkit/goals.json
- .shipkit/project-health.json

Examples (Markdown - narrative content only):
- .shipkit/specs/active/[feature].json (now JSON)
- .shipkit/communications/latest.html

→ [user input]
```

**Store as:** `output_path`

**Use for:** Detection logic in hook, documentation

---

#### 1.7: Routing Keywords (3-5 phrases)
```
What keywords should route to this skill?
Provide 3-5 natural phrases users might say.

These will be added to the master routing table.

Examples for shipkit-spec:
- "create spec", "specification", "spec for", "write spec"

Examples for shipkit-communications:
- "visualize", "HTML report", "visual communication", "create presentation"

Enter keywords (comma-separated):
→ [user input]
```

**Parse:** Split by comma, trim whitespace
**Store as:** `keywords` array

---

#### 1.8: Advanced Frontmatter (Optional)
```
Does this skill need any advanced Claude Code features?

1. context: fork - Run in a forked sub-agent context (v2.1.0)
   Use for: Skills that should run isolated from main conversation
2. agent: {agent-name} - Execute as a specific agent persona (v2.1.0)
   Use for: Skills that need a specialized agent context
3. hooks - Define lifecycle hooks (PreToolUse, PostToolUse, Stop) (v2.1.0)
   Use for: Skills that need tool-level middleware
4. user-invocable: false - Hide from slash command menu (v2.1.0)
   Use for: System skills that shouldn't be directly invoked
5. None needed (default)

Choose (comma-separated for multiple, or 5 for none):
```

**Store as:** `advanced_frontmatter` - dict of selected fields
**Use for:** YAML frontmatter generation in Step 3

---

#### 1.9: Prerequisites (Optional)
```
Does this skill require other files to exist first?

Examples:
- shipkit-plan requires shipkit-spec (hard requirement)
- shipkit-spec optionally uses stack.json (soft requirement)
- shipkit-project-status has no requirements

Options:
1. Hard requirement (blocks if missing): [skill-name or file-path]
2. Soft requirement (optional but helpful): [skill-name or file-path]
3. No requirements

→ [user choice + input if applicable]
```

**Store as:** `prerequisites` object with `hard` and `soft` arrays

---

### Step 2: Select and Load Template

**Template selection logic:**

```
template_name = f"{skill_type}-{output_strategy}.md"

Examples:
- artifact + multiple → artifact-multiple-template.md
- artifact + append → artifact-append-template.md
- methodology + none → methodology-template.md
- utility + overwrite → utility-overwrite-template.md
```

**Load template from:** `references/templates/{template_name}`

**If template doesn't exist:** Use fallback based on skill_type only

**Templates contain:**
- YAML frontmatter placeholders
- Section structure appropriate for type
- Quality pattern placeholders (checklist or Iron Laws)
- Logical pathway references appropriate for output strategy

**See:** `references/templates/` for all available templates

---

### Step 3: Generate SKILL.md from Template

**Process:**
1. Read template file
2. Replace placeholders with user answers from Step 1
3. Generate SKILL.md content

**Placeholder mapping:**
```
{{SKILL_NAME}} → shipkit-{user_input_1.1}
{{DESCRIPTION}} → {user_input_1.2}
{{CATEGORY}} → {user_input_1.3}
{{OUTPUT_PATH}} → {user_input_1.6}
{{KEYWORDS}} → {user_input_1.7 as list}
{{PREREQUISITES}} → {user_input_1.8 formatted}
```

**Write to:** `install/skills/shipkit-{skill-name}/SKILL.md`

**Show preview:**
```
Generated SKILL.md preview (first 30 lines):

---
name: shipkit-user-stories
description: Creates user stories with acceptance criteria from feature descriptions
---

# shipkit-user-stories - User Story Generator

...

Looks good? (y/n/edit)
```

**If edit:** Allow user to modify before writing
**If no:** Cancel and exit
**If yes:** Proceed to Step 4

---

### Step 4: Update 7 Integration Files

**For each file, use pattern from `references/file-update-patterns/`**

**Show progress:**
```
Updating integration files...

✓ File 1: SKILL.md created
⏳ File 2: Updating overview.html...
```

---

#### 4.1: File 2 - Update help/shipkit-shipkit-overview.html

**Pattern:** See `references/file-update-patterns/overview-pattern.md`

**Steps:**
1. Read `help/shipkit-shipkit-overview.html`
2. Find `<span class="stat-number">XX</span>` → increment by 1
3. Find correct category section based on user_input_1.3
4. Add new list item:
   ```html
   <li><strong>{skill-name}</strong> - {2-4 word description from purpose}</li>
   ```
5. Write updated file

**Report:** `✓ File 2: Updated overview.html (count + Documentation section)`

---

#### 4.2: File 3 - Update install/claude-md/shipkit.md

**Pattern:** See `references/file-update-patterns/claude-md-pattern.md`

**Steps:**
1. Read `install/claude-md/shipkit.md`
2. Find section matching category from Step 1.3
3. Add line in alphabetical order:
   ```markdown
   - `/shipkit-{skill-name}` - {purpose} → `{output_path}`
   ```
4. Write updated file

**Report:** `✓ File 3: Updated shipkit.md (Decision & Design section)`

---

#### 4.3: File 4 - Update install/profiles/shipkit.manifest.json

**Pattern:** See `references/file-update-patterns/manifest-pattern.md`

**Steps:**
1. Read and parse `install/profiles/shipkit.manifest.json`
2. Add `"shipkit-{skill-name}"` to `skills.definitions` array as last item
3. Validate JSON syntax
4. Write updated file

**Report:** `✓ File 4: Updated manifest.json (added to definitions)`

---

#### 4.4: File 5 - Update install/shared/hooks/shipkit-after-skill-router.py (Optional)

**Pattern:** See `references/file-update-patterns/hook-pattern.md`

**When needed:** Only if the new skill should trigger detection after another skill completes.

**Steps:**
1. Read `install/shared/hooks/shipkit-after-skill-router.py`
2. Add mapping to `SKILL_TO_MODE` dict if skill triggers detection
3. Validate Python syntax with `python -m py_compile`
4. Write updated file

**Report:** `✓ File 5: Updated shipkit-after-skill-router.py (optional trigger mapping)`

**Note:** Most skills don't need hook updates. The hook is for automatic detection chaining only.

---

#### 4.5: File 6 - Update install/skills/shipkit-master/SKILL.md

**Pattern:** See `references/file-update-patterns/routing-pattern.md`

**Steps:**
1. Read `install/skills/shipkit-master/SKILL.md`
2. Find routing table for category from Step 1.3
3. Add row with keywords from Step 1.7
4. Write updated file

**Report:** `✓ File 6: Updated master routing (3 keywords)`

---

#### 4.6: File 7 - Update install/settings/shipkit.settings.json

**Pattern:** See `references/file-update-patterns/settings-pattern.md`

**Steps:**
1. Read and parse `install/settings/shipkit.settings.json`
2. Add `"Skill(shipkit-{skill-name})"` to `allow` array
3. Validate JSON syntax
4. Write updated file

**Report:** `✓ File 7: Updated settings.json (added permission)`

---

### Step 5: Create references/ Folder Structure

**Create placeholder README in references/:**
```markdown
# shipkit-{skill-name} References

## Purpose
Extended documentation and examples for shipkit-{skill-name}.

## Contents
- `examples.md` - Concrete usage examples
- `guide.md` - Extended tips and best practices
- `scenarios.md` - Full scenario walkthroughs

## When to Use
Move content here if SKILL.md exceeds 500 lines.
```

**Write to:** `install/skills/shipkit-{skill-name}/references/README.md`

---

### Step 6: Final Summary and Next Steps

**Show complete summary:**
```
✅ Created shipkit-{skill-name}

Files created:
✓ install/skills/shipkit-{skill-name}/SKILL.md
✓ install/skills/shipkit-{skill-name}/references/README.md

Files updated:
✓ File 2: help/shipkit-shipkit-overview.html
✓ File 3: install/claude-md/shipkit.md
✓ File 4: install/profiles/shipkit.manifest.json
⊘ File 5: install/shared/hooks/shipkit-after-skill-router.py (optional)
✓ File 6: install/skills/shipkit-master/SKILL.md
✓ File 7: install/settings/shipkit.settings.json

Next steps:
1. Review SKILL.md and refine:
   - Fill in "When This Skill Integrates with Others" section
   - Add specific cross-references to related skills
   - Refine process steps if needed

2. Add examples (optional):
   - Create references/examples.md if helpful

3. Validate the skill:
   Run: /shipkit-validate-shipkit-skill shipkit-{skill-name}

4. Test manually:
   - Try invoking /shipkit-{skill-name}
   - Verify it works as expected

5. Commit when satisfied:
   git add install/skills/shipkit-{skill-name}/
   git add help/shipkit-shipkit-overview.html
   git add install/claude-md/shipkit.md
   git add install/profiles/shipkit.manifest.json
   git add install/skills/shipkit-master/SKILL.md
   git add install/settings/shipkit.settings.json
   git commit -m "Add shipkit-{skill-name}"

Would you like to validate now? (y/n)
```

**If yes:** Invoke `/shipkit-validate-shipkit-skill shipkit-{skill-name}` (if that skill exists)
**If no:** Exit

---

## When This Skill Integrates with Others

### After shipkit-create-shipkit-skill

**Natural next step:**
- `/shipkit-validate-shipkit-skill` - Validate the created skill meets all quality standards
  - **Trigger:** User says "yes" to validation prompt, or manually runs validation
  - **Why:** Ensure the generated skill is production-ready

**Manual refinement:**
- Edit SKILL.md to fill in TODOs and add specific details
- Add cross-references to related skills
- Add examples if needed

### Before shipkit-create-shipkit-skill

**Optional preparation:**
- Review `SHIPKIT-DESIGN-PHILOSOPHY.md` to understand lite approach
- Review existing skills for patterns to follow
- Decide on skill purpose and scope

**No hard prerequisites** - can be run immediately

### Related Skills

- `/shipkit-create-core-skill` - For creating full skills instead of lite
- `/shipkit-validate-shipkit-skill` - For validating created skills
- `/shipkit-audit-repo` - For checking overall repository health

---

## Context Files This Skill Reads

**Templates:**
- `references/templates/artifact-*.md` - Templates for artifact skills
- `references/templates/methodology-*.md` - Templates for methodology skills
- `references/templates/utility-*.md` - Templates for utility skills

**Patterns:**
- `references/file-update-patterns/*.md` - How to update each integration file

**Claude Code changelog** (auto-fetched if stale):
- `docs/development/claude-code-changelog.md` - Full changelog from GitHub
- `docs/development/claude-code-changelog.meta.json` - Freshness metadata
- `docs/development/fetch-changelog.sh` - Fetch script

**Integration files (to update):**
- `help/shipkit-shipkit-overview.html`
- `install/claude-md/shipkit.md`
- `install/profiles/shipkit.manifest.json`
- `install/shared/hooks/shipkit-after-skill-router.py` (optional)
- `install/skills/shipkit-master/SKILL.md`
- `install/settings/shipkit.settings.json`

---

## Context Files This Skill Writes

**Creates:**
- `install/skills/shipkit-{skill-name}/SKILL.md` - Main skill file
  - **Write Strategy:** CREATE (new file)
  - **Behavior:** Fails if file already exists (unless user confirms overwrite)
  - **Why:** Prevent accidental overwriting of existing skills

- `install/skills/shipkit-{skill-name}/references/README.md` - References folder structure
  - **Write Strategy:** CREATE
  - **Behavior:** Creates placeholder README
  - **Why:** Prepares folder for future examples/guides

**Updates (all APPEND):**
- `help/shipkit-shipkit-overview.html` - Adds skill to list, increments count
- `install/claude-md/shipkit.md` - Adds skill to category section
- `install/profiles/shipkit.manifest.json` - Adds to definitions array
- `install/skills/shipkit-master/SKILL.md` - Adds routing keywords
- `install/settings/shipkit.settings.json` - Adds skill permission

**Optional:**
- `install/shared/hooks/shipkit-after-skill-router.py` - Only if skill triggers detection

---

## References

**Templates**: See `references/templates/` for:
- All skill type templates (artifact, methodology, utility)
- Templates by output strategy (overwrite, append, multiple, none)

**File Update Patterns**: See `references/file-update-patterns/` for:
- Detailed instructions for updating each of the 7 files
- JSON/Python syntax validation rules
- Examples of additions

**Examples**: See `references/examples/` for:
- Complete example generated skills
- Before/after comparisons

**Quality Standards** (reference but don't duplicate):
- `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md` - Universal quality standards
- `claude-code-best-practices/SHIPKIT-7-FILE-INTEGRATION.md` - 7-file integration system
- `claude-code-best-practices/SHIPKIT-DESIGN-PHILOSOPHY.md` - Lite philosophy and approach

---

## Section Markers

**All new skills should include standard section markers:**

```markdown
<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->
```

**Why section markers:**
- Enable batch updates across all skills via `scripts/skill-sections.py`
- Standardize guardrails across skills
- Replace mandatory skill chaining with guardrails

**Validation:**
After creation, run:
```bash
/shipkit-validate-shipkit-skill shipkit-{skill-name}
```
