# File 3: Update install/claude-md/shipkit.md

**Purpose**: Add new skill invocation to the appropriate category section

**File**: `install/claude-md/shipkit.md`

---

## Step 1: Find Correct Category Section

**Sections in shipkit.md** (search for `**` headings):

1. **Project Setup** (lines ~27-30)
2. **Feature Development** (lines ~32-37)
3. **Documentation** (lines ~39-43)
4. **Quality & Process** (lines ~45-48)
5. **Utilities** (lines ~50-54)

**Match to user's category choice**:
- Category 1 (Meta/Infrastructure) → **Project Setup** section
- Category 2 (Decision & Design) → **Feature Development** section
- Category 3 (Implementation) → **Feature Development** section
- Category 4 (Documentation) → **Documentation** section
- Category 5 (Quality & Process) → **Quality & Process** section

---

## Step 2: Add Skill Invocation Line

**Format**:
```markdown
- `/shipkit-{skill-name}` - {purpose} → `{output_path}`
```

**Example existing entries**:
```markdown
**Feature Development:**
- `/shipkit-spec` - Write spec → `specs/active/[name].json`
- `/shipkit-architecture-memory` - Log decision → append to `architecture.json`
- `/shipkit-plan` - Create plan → `plans/active/[name].json`
- `/shipkit-implement` - Build feature with TDD guidance
```

**Add new entry** (in alphabetical order within section):
```markdown
**Feature Development:**
- `/shipkit-architecture-memory` - Log decision → append to `architecture.json`
- `/shipkit-NEW-SKILL` - {purpose} → `{output_path}`  <!-- NEW -->
- `/shipkit-plan` - Create plan → `plans/active/[name].json`
- `/shipkit-spec` - Write spec → `specs/active/[name].json`
- `/shipkit-implement` - Build feature with TDD guidance
```

---

## Step 3: Determine Output Path Format

**Based on output strategy** (from Step 1.5 of wizard):

**OVERWRITE**:
```markdown
- `/shipkit-why-project` - Define vision → `.shipkit/why.json`
```

**APPEND**:
```markdown
- `/shipkit-architecture-memory` - Log decision → append to `architecture.json`
```

**MULTIPLE**:
```markdown
- `/shipkit-spec` - Write spec → `specs/active/[name].json`
- `/shipkit-plan` - Create plan → `plans/active/[name].json`
```

**NONE** (no file output):
```markdown
- `/shipkit-implement` - Build feature with TDD guidance
```

---

## Step 4: Validate Entry

**Check**:
- [ ] Entry added to correct section
- [ ] Alphabetical order maintained within section
- [ ] Format matches existing entries
- [ ] Output path is accurate
- [ ] Purpose is concise (3-6 words)

---

## Examples by Category

### Example 1: Meta/Infrastructure Skill

**Category**: 1 (Meta/Infrastructure)
**Output**: OVERWRITE
**Path**: `.shipkit/project-overview.json`

**Add to Project Setup section**:
```markdown
**Project Setup:**
- `/shipkit-project-context` - Scan codebase, create stack.json
- `/shipkit-project-overview` - Generate overview → `.shipkit/project-overview.json`  <!-- NEW -->
- `/shipkit-project-status` - Health check, show gaps
- `/shipkit-why-project` - Define strategic vision (who/why/where)
```

---

### Example 2: Decision & Design Skill

**Category**: 2 (Decision & Design)
**Output**: MULTIPLE
**Path**: `.shipkit/decisions/[decision].json`

**Add to Feature Development section**:
```markdown
**Feature Development:**
- `/shipkit-architecture-memory` - Log decision → append to `architecture.json`
- `/shipkit-decision-log` - Record decision → `decisions/[decision].json`  <!-- NEW -->
- `/shipkit-plan` - Create plan → `plans/active/[name].json`
- `/shipkit-spec` - Write spec → `specs/active/[name].json`
```

---

### Example 3: Documentation Skill

**Category**: 4 (Documentation)
**Output**: APPEND
**Path**: `.shipkit/api-docs.json`

**Add to Documentation section**:
```markdown
**Documentation:**
- `/shipkit-api-docs` - Document API → append to `api-docs.json`  <!-- NEW -->
- `/shipkit-component-knowledge` - Document components → append to `implementations.json`
- `/shipkit-communications` - Create visual HTML from any lite content
- `/shipkit-document-artifact` - Create standalone doc → `docs/[category]/[name].json`
- `/shipkit-route-knowledge` - Document routes → append to `implementations.json`
```

---

### Example 4: Quality & Process Skill

**Category**: 5 (Quality & Process)
**Output**: NONE

**Add to Quality & Process section**:
```markdown
**Quality & Process:**
- `/shipkit-quality-confidence` - Pre-ship checks
- `/shipkit-security-review` - Security audit  <!-- NEW, no file output -->
- `/shipkit-user-instructions` - Track manual tasks → `user-tasks/active.json`
- `/shipkit-work-memory` - Log session → append to `progress.json`
```

---

## Common Mistakes

**❌ Adding to wrong section**
- Double-check category mapping

**❌ Incorrect arrow format**
- Use ` → ` (space-arrow-space)
- Not `->`or `->` or other variations

**❌ Not maintaining alphabetical order**
- Sort by skill name within each section

**❌ Missing output path**
- Always include unless output strategy is NONE

**❌ Inconsistent path format**
- Use placeholders: `[name]`, `[feature]`, `[component]`
- Match existing path conventions

---

## Report Format

After updating, report:

```
✓ File 3: Updated shipkit.md
  - Added to {Section Name} section
  - Entry: /shipkit-{skill-name} - {purpose} → {output_path}
  - Position: {alphabetically between X and Y}
```
