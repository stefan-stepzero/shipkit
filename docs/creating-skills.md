# Creating Skills

Guide for contributors who want to create new Shipkit skills.

---

## The Skill Value Test

Before creating a skill, it must pass this test:

**A skill is valuable if it does ONE of these:**
1. **Forces human decisions to be explicit** — Vision, trade-offs, priorities, domain knowledge
2. **Creates persistence Claude lacks** — Institutional memory that survives sessions

**A skill is redundant if:** Claude does it well without instruction.

| Needs a Skill | No Skill Needed |
|---------------|-----------------|
| Define project vision | Debug this error |
| Capture architecture decisions | Implement the login |
| Create feature specs | Write unit tests |
| Document integration patterns | Refactor this code |

**Litmus test:** "If I just asked Claude to do this without a skill, would it work?"
- YES → Don't create the skill
- NO (requires human input or persistence) → Create the skill

---

## Skill Structure

Every skill needs one file:

```
install/skills/shipkit-[name]/
└── SKILL.md
```

Optional supporting files:
```
install/skills/shipkit-[name]/
├── SKILL.md                    # Required
├── references/                 # Optional: Reference material
│   └── patterns.md
└── scripts/                    # Optional: Automation scripts
    └── detect.py
```

---

## SKILL.md Format

```yaml
---
name: shipkit-[name]
description: "What it does. Triggers: 'keyword1', 'keyword2', 'when to use'."
---

# shipkit-[name] - Title

**Purpose**: One sentence describing what problem this skill solves.

---

## When to Invoke

**User triggers:**
- "user says this"
- "user asks for that"

**Suggested after:**
- `/shipkit-other-skill` - When that skill completes

---

## Prerequisites

**Required:**
- `.shipkit/file.md` - What must exist

**Optional but helpful:**
- `.shipkit/other.md` - Nice to have

---

## Process

### Step 1: [Action]

[Description of what happens]

**Questions asked:**
- Question 1?
- Question 2?

### Step 2: [Action]

[Description]

### Step 3: [Generate Output]

**Creates:** `.shipkit/output.md`

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `.shipkit/x.md` | Why it's read |

---

## Context Files This Skill Writes

| File | Strategy | Purpose |
|------|----------|---------|
| `.shipkit/y.md` | CREATE/APPEND/REPLACE | What it contains |

---

## Success Criteria

Skill is complete when:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Output file created

---

## After Completion

**Suggested next:** `/shipkit-next-skill` - Why

**Natural capabilities** (no skill needed): Implementation, debugging, testing.
```

---

## Key Requirements

### 1. Naming

- **Prefix:** All skills use `shipkit-` prefix
- **Format:** Lowercase, hyphens only
- **Max length:** 64 characters
- **Directory must match name**

Good: `shipkit-architecture-memory`
Bad: `architecture_memory`, `ArchMemory`

### 2. Description

Must be:
- **Third-person** ("Creates..." not "I create...")
- **Include WHAT and WHEN**
- **Under 1024 characters**

Good:
```yaml
description: "Logs architecture decisions with rationale. Use when making significant technical choices."
```

Bad:
```yaml
description: "I can help you log decisions"     # Wrong POV
description: "Logs decisions"                   # Missing WHEN
```

### 3. Size Limits

- **Target:** < 300 lines
- **Maximum:** 500 lines
- **Reason:** Every line competes with conversation context

If your skill exceeds 300 lines:
- Move examples to `references/`
- Move scripts to `scripts/`
- Keep SKILL.md focused on workflow

### 4. Prerequisites

Skills should check prerequisites before running:

```markdown
## Prerequisites

**Required:**
- `.shipkit/why.md` - Vision must be defined first

**If missing:**
Run `/shipkit-why-project` first to define project vision.
```

### 5. Context Files

Document what the skill reads and writes:

**Reads:**
```markdown
## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `.shipkit/why.md` | Understand project constraints |
| `.shipkit/stack.md` | Know what technologies are in use |
```

**Writes:**
```markdown
## Context Files This Skill Writes

| File | Strategy | Purpose |
|------|----------|---------|
| `.shipkit/architecture.md` | APPEND | Add decision without overwriting history |
| `.shipkit/specs/active/*.md` | CREATE | New spec file per feature |
```

Write strategies:
- **CREATE** — New file each time
- **APPEND** — Add to existing (preserve history)
- **REPLACE** — Overwrite entirely

### 6. Success Criteria

Clear, checkable criteria:

```markdown
## Success Criteria

Skill is complete when:
- [ ] User answered clarifying questions
- [ ] Output file created at correct location
- [ ] File contains required sections
- [ ] User knows suggested next step
```

### 7. After Completion

Always suggest next steps:

```markdown
## After Completion

**Suggested next:** `/shipkit-plan` - Create implementation plan from this spec

**Natural capabilities** (no skill needed):
- Implementation
- Debugging
- Testing
- Code documentation
```

---

## Integration Checklist

When adding a new skill, update these files:

### 1. Create the skill
```
install/skills/shipkit-[name]/SKILL.md
```

### 2. Add to manifest
`install/profiles/shipkit.manifest.json`:
```json
{
  "skills": {
    "optional": {
      "Category Name": [
        {"name": "shipkit-[name]", "desc": "What it does"}
      ]
    }
  }
}
```

### 3. Add to CLAUDE.md template
`install/claude-md/shipkit.md`:
```markdown
| When... | Use |
|---------|-----|
| [trigger condition] | `/shipkit-[name]` |
```

### 4. Update master skill
`install/skills/shipkit-master/SKILL.md` — Add to skill list

### 5. Update documentation
`docs/skill-reference.md` — Add skill entry

---

## Common Patterns

### Ask Before Loading

Don't load all context speculatively. Ask first:

```markdown
### Step 1: Clarify Scope

Before loading any context, ask:
1. Which feature are you working on?
2. What's the main question/decision?

**Then** load only relevant context.
```

### Progressive Disclosure

Start simple, add detail only if needed:

```markdown
### Step 2: Generate Initial Output

Create minimal version first.

### Step 3: Expand If Needed

Ask: "Should I add more detail to any section?"

Only expand sections user requests.
```

### Append-Only for History

For decision logs, always append:

```markdown
## Context Files This Skill Writes

| File | Strategy | Purpose |
|------|----------|---------|
| `.shipkit/architecture.md` | APPEND | Preserve decision history |
```

### Reference External Docs

For integration patterns, fetch live:

```markdown
### Step 2: Fetch Current Patterns

Use WebFetch to get current documentation:
- Check official docs
- Extract security patterns
- Cache in `references/`
```

---

## Testing Your Skill

1. **Install in test project:**
   ```bash
   mkdir test-project && cd test-project
   python ../sg-shipkit/installers/install.py
   ```

2. **Invoke the skill:**
   ```
   /shipkit-[name]
   ```

3. **Verify:**
   - Does it ask the right questions?
   - Does it create the right files?
   - Is output useful?
   - Does it suggest logical next step?

4. **Check context budget:**
   - Skill + loaded context < 2500 tokens
   - Output is appropriately sized

---

## Anti-Patterns to Avoid

### 1. Skills for Natural Capabilities
❌ Creating a skill for debugging, implementing, or testing
✅ These are natural capabilities — just ask Claude

### 2. Loading Everything
❌ Loading all context files at skill start
✅ Ask questions first, load only what's needed

### 3. Giant Output
❌ 10-page specifications
✅ 1-2 page focused documents

### 4. No Clear Completion
❌ Skill that runs indefinitely
✅ Clear success criteria and "done" state

### 5. Overwriting History
❌ Replacing architecture decisions
✅ Appending new decisions, preserving history

---

## Submitting Your Skill

1. Fork the repo
2. Create branch: `skill/shipkit-[name]`
3. Add skill following this guide
4. Update integration files (manifest, docs)
5. Test in clean project
6. Submit PR using the template

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full details.
