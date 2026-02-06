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
- `/shipkit-spec` - Write spec → `specs/active/[name].md`
- `/shipkit-architecture-memory` - Log decision → append to `architecture.md`
- `/shipkit-plan` - Create plan → `plans/[name].md`
- `/shipkit-implement` - Build feature with TDD guidance
```

**Add new entry** (in alphabetical order within section):
```markdown
**Feature Development:**
- `/shipkit-architecture-memory` - Log decision → append to `architecture.md`
- `/shipkit-NEW-SKILL` - {purpose} → `{output_path}`  <!-- NEW -->
- `/shipkit-plan` - Create plan → `plans/[name].md`
- `/shipkit-spec` - Write spec → `specs/active/[name].md`
- `/shipkit-implement` - Build feature with TDD guidance
```

---

## Step 3: Determine Output Path Format

**Based on output strategy** (from Step 1.5 of wizard):

**OVERWRITE**:
```markdown
- `/shipkit-why-project` - Define vision → `.shipkit/why.md`
```

**APPEND**:
```markdown
- `/shipkit-architecture-memory` - Log decision → append to `architecture.md`
```

**MULTIPLE**:
```markdown
- `/shipkit-spec` - Write spec → `specs/active/[name].md`
- `/shipkit-plan` - Create plan → `plans/[name].md`
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
**Path**: `.shipkit/project-overview.md`

**Add to Project Setup section**:
```markdown
**Project Setup:**
- `/shipkit-project-context` - Scan codebase, create stack.md
- `/shipkit-project-overview` - Generate overview → `.shipkit/project-overview.md`  <!-- NEW -->
- `/shipkit-project-status` - Health check, show gaps
- `/shipkit-why-project` - Define strategic vision (who/why/where)
```

---

### Example 2: Decision & Design Skill

**Category**: 2 (Decision & Design)
**Output**: MULTIPLE
**Path**: `.shipkit/decisions/[decision].md`

**Add to Feature Development section**:
```markdown
**Feature Development:**
- `/shipkit-architecture-memory` - Log decision → append to `architecture.md`
- `/shipkit-decision-log` - Record decision → `decisions/[decision].md`  <!-- NEW -->
- `/shipkit-plan` - Create plan → `plans/[name].md`
- `/shipkit-spec` - Write spec → `specs/active/[name].md`
```

---

### Example 3: Documentation Skill

**Category**: 4 (Documentation)
**Output**: APPEND
**Path**: `.shipkit/api-docs.md`

**Add to Documentation section**:
```markdown
**Documentation:**
- `/shipkit-api-docs` - Document API → append to `api-docs.md`  <!-- NEW -->
- `/shipkit-component-knowledge` - Document components → append to `implementations.md`
- `/shipkit-communications` - Create visual HTML from any lite content
- `/shipkit-document-artifact` - Create standalone doc → `docs/[category]/[name].md`
- `/shipkit-route-knowledge` - Document routes → append to `implementations.md`
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
- `/shipkit-user-instructions` - Track manual tasks → `user-tasks/active.md`
- `/shipkit-work-memory` - Log session → append to `progress.md`
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
