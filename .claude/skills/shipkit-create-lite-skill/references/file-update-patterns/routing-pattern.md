# File 6: Update install/skills/shipkit-master/SKILL.md

**Purpose**: Add routing keywords to the master skill's routing table

**File**: `install/skills/shipkit-master/SKILL.md`

---

## Step 1: Find Routing Table Section

**Search for**: `## Skill Routing Table`

**Structure**:
```markdown
## Skill Routing Table

**Match user intent to appropriate skill:**

### Meta/Infrastructure Keywords
| User Says | Route To | Load Context |
|-----------|----------|--------------|
...

### Decision & Design Keywords
| User Says | Route To | Load Context |
...

### Implementation Keywords
...

### Documentation Keywords
...

### Quality & Process Keywords
...
```

---

## Step 2: Determine Correct Table

**Match to user's category choice** (from Step 1.3 of wizard):

1. Category 1 (Meta/Infrastructure) → **Meta/Infrastructure Keywords** table
2. Category 2 (Decision & Design) → **Decision & Design Keywords** table
3. Category 3 (Implementation) → **Implementation Keywords** table
4. Category 4 (Documentation) → **Documentation Keywords** table
5. Category 5 (Quality & Process) → **Quality & Process Keywords** table

---

## Step 3: Add Row to Routing Table

**Format**:
```markdown
| "{keyword1}", "{keyword2}", "{keyword3}" | `/shipkit-{skill-name}` | {context-files} |
```

**Use keywords from wizard** (Step 1.7):
- User provided 3-5 keywords
- Format as comma-separated quoted strings

**Specify context files to load**:
- What files should Claude read when this skill is invoked?
- Examples: `stack.json`, `specs/active/*.json`, `architecture.json`, etc.

---

## Step 4: Example Additions by Category

### Example 1: Decision & Design

**Skill**: `shipkit-user-stories`
**Keywords**: "user stories", "requirements", "acceptance criteria"
**Context**: User stories files

**Add to Decision & Design table**:

```markdown
### Decision & Design Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec", "Specification", "Requirements", "Feature spec" | `/shipkit-spec` | stack.json, schema.json |
| "Log decision", "Architectural choice", "Decision record" | `/shipkit-architecture-memory` | architecture.json |
| "User stories", "Requirements", "Acceptance criteria" | `/shipkit-user-stories` | specs/active/*.json, why.json |  <-- NEW
| "UX check", "Consistent UI", "UX patterns" | `/shipkit-ux-coherence` | implementations.json |
```

---

### Example 2: Documentation

**Skill**: `shipkit-api-documentation`
**Keywords**: "API docs", "document endpoints", "API reference"
**Context**: Implementation files

**Add to Documentation table**:

```markdown
### Documentation Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "API docs", "Document endpoints", "API reference" | `/shipkit-api-documentation` | implementations.json, routes/*.ts |  <-- NEW
| "Document component", "Component docs", "How this works" | `/shipkit-component-knowledge` | implementations.json |
| "Document route", "Route docs", "Endpoint docs" | `/shipkit-route-knowledge` | implementations.json, routes/*.ts |
```

---

### Example 3: Meta/Infrastructure

**Skill**: `shipkit-dependency-audit`
**Keywords**: "check dependencies", "audit packages", "outdated packages"
**Context**: Package files

**Add to Meta/Infrastructure table**:

```markdown
### Meta/Infrastructure Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Check dependencies", "Audit packages", "Outdated packages" | `/shipkit-dependency-audit` | package.json, requirements.txt |  <-- NEW
| "Scan project", "Generate stack", "Refresh context" | `/shipkit-project-context` | package.json, .env.example |
| "Show status", "Project health" | `/shipkit-project-status` | All .shipkit/ files |
```

---

### Example 4: Implementation

**Skill**: `shipkit-refactor`
**Keywords**: "refactor", "improve code", "clean up"
**Context**: Implementation and architecture files

**Add to Implementation table**:

```markdown
### Implementation Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Create plan", "Implementation plan", "How to build" | `/shipkit-plan` | specs/active/*.json, stack.json |
| "Refactor", "Improve code", "Clean up" | `/shipkit-refactor` | architecture.json, implementations.json |  <-- NEW
| "Implement", "Build feature", "Code this", "Start coding" | `/shipkit-implement` | plans/active/*.json, specs/active/*.json |
```

---

### Example 5: Quality & Process

**Skill**: `shipkit-code-review`
**Keywords**: "review code", "check quality", "code feedback"
**Context**: Recent changes

**Add to Quality & Process table**:

```markdown
### Quality & Process Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Review code", "Check quality", "Code feedback" | `/shipkit-code-review` | git diff, architecture.json |  <-- NEW
| "Quality check", "Ready to ship?", "Pre-launch" | `/shipkit-quality-confidence` | specs/active/*.json, implementations.json |
| "Debug", "Fix bug", "Something's wrong" | `/shipkit-debug-systematically` | None (systematic process) |
```

---

## Step 5: Context Files Guidelines

**Common patterns**:

**Always read if exists**:
- `stack.json` - Tech stack context
- `architecture.json` - Past decisions

**Skill-specific**:
- Spec skills → Read `specs/active/*.json`
- Plan skills → Read `specs/active/*.json`, `stack.json`
- Implement skills → Read `plans/active/*.json`, `specs/active/*.json`
- Documentation skills → Read `implementations.json`
- UX skills → Read `implementations.json`, `specs/active/*.json`

**None**:
- Process/methodology skills (implement, debug)
- Utility skills that scan everything

---

## Step 6: Validate Table Formatting

**Check**:
- [ ] Pipes (`|`) are aligned
- [ ] Keywords are quoted and comma-separated
- [ ] Skill name uses `/shipkit-` prefix
- [ ] Context files are realistic and exist
- [ ] Row is in logical order (not necessarily alphabetical)

**Markdown table syntax**:
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Content  | Content  | Content  |
```

---

## Complete Before/After Example

**Before** (Decision & Design table):
```markdown
### Decision & Design Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec", "Specification", "Requirements" | `/shipkit-spec` | stack.json, schema.json |
| "Log decision", "Architectural choice" | `/shipkit-architecture-memory` | architecture.json |
| "UX check", "Consistent UI" | `/shipkit-ux-coherence` | implementations.json |
| "Types", "Schema", "Data model" | `/shipkit-data-consistency` | types.json, schema.json |
```

**After** (adding shipkit-user-stories):
```markdown
### Decision & Design Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec", "Specification", "Requirements" | `/shipkit-spec` | stack.json, schema.json |
| "Log decision", "Architectural choice" | `/shipkit-architecture-memory` | architecture.json |
| "User stories", "Requirements list", "Acceptance criteria" | `/shipkit-user-stories` | specs/active/*.json, why.json |  <-- NEW
| "UX check", "Consistent UI" | `/shipkit-ux-coherence` | implementations.json |
| "Types", "Schema", "Data model" | `/shipkit-data-consistency` | types.json, schema.json |
```

---

## Common Mistakes

**❌ Forgetting to quote keywords**
```markdown
| User stories, Requirements | ... |  <-- ERROR: No quotes
```

**❌ Breaking table alignment**
```markdown
| "Keyword" | `/skill` | Context |
|--|--|  <-- ERROR: Missing third separator
```

**❌ Using wrong skill prefix**
```markdown
| "Keyword" | `shipkit-skill` | ... |  <-- ERROR: Missing /
| "Keyword" | `/skill` | ... |     <-- ERROR: Missing shipkit-
```

**❌ Unrealistic context files**
```markdown
| "Keyword" | `/shipkit-spec` | all-files.md, everything.md |  <-- ERROR: These don't exist
```

**❌ Too many keywords in one cell**
```markdown
| "Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5", "Keyword6" | ... |
    <-- Too long, hard to read
```

---

## Report Format

After updating, report:

```
✓ File 6: Updated master routing
  - Added to {Category} Keywords table
  - Keywords: "{keyword1}", "{keyword2}", "{keyword3}"
  - Routes to: /shipkit-{skill-name}
  - Context: {context-files}
```
