---
name: lite-plan
description: Creates focused implementation plans for POC/MVP features by reading existing context and generating step-by-step technical designs. Use when user asks to "plan how to build", "create implementation plan", or "design the approach" after a spec exists.
---

# plan-lite - Lightweight Implementation Planning

**Purpose**: Transform feature specifications into focused implementation plans that guide coding while staying lightweight for POC/MVP work.

---

## When to Invoke

**User triggers**:
- "Plan how to build this"
- "Create implementation plan"
- "How should we implement this feature?"
- "Design the technical approach"

**After**:
- `/lite-spec` has created specification for the feature
- Feature is ready for implementation planning

---

## Prerequisites

**Check before starting**:
- Spec exists: `.shipkit-lite/specs/active/[feature-name].md`
- Stack defined: `.shipkit-lite/stack.md` (from project-context-lite)

**Optional but helpful**:
- Architecture decisions: `.shipkit-lite/architecture.md`
- Type definitions: `.shipkit-lite/types.md`

---

## Process

### Step 1: Confirm Scope

**Before generating anything**, ask user 2-3 questions:

1. **Which spec are you planning?**
   - List available specs from `.shipkit-lite/specs/active/`
   - Let user choose

2. **Implementation approach?**
   - "What's your preferred approach?" (if multiple options exist)
   - "Any specific patterns you want to use?"

3. **Complexity level?**
   - "Quick POC plan (minimal steps)?"
   - "Detailed plan (more thorough)?"

**Why ask first**: Avoid token-heavy generation if user wants different approach.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# Required
.shipkit-lite/specs/active/[feature-name].md

# Stack info (tech choices)
.shipkit-lite/stack.md

# Past decisions (patterns established)
.shipkit-lite/architecture.md
```

**Optional context** (load if relevant):
```bash
# Type definitions (if data-heavy feature)
.shipkit-lite/types.md

# Component contracts (if building on existing)
.shipkit-lite/component-contracts.md

# Schema (if database changes needed)
.shipkit-lite/schema.md
```

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 3: Generate Implementation Plan

**Create plan file using Write tool**:

**Location**: `.shipkit-lite/plans/[feature-name]-plan.md`

**Plan structure**:

```markdown
# Implementation Plan - [Feature Name]

**Created**: [timestamp]
**Spec**: specs/active/[feature-name].md
**Status**: Planning

---

## Overview

**Goal**: [1-2 sentence summary]
**Complexity**: [Simple/Medium/Complex]
**Estimated effort**: [X hours/days]

---

## Tech Stack Alignment

**From stack.md:**
- Framework: [from stack.md]
- Database: [from stack.md]
- Key libraries: [from stack.md]

**Patterns from architecture.md:**
- [Pattern 1 we're following]
- [Pattern 2 we're following]

---

## Implementation Steps

### Phase 1: Setup
- [ ] [Setup task 1]
- [ ] [Setup task 2]

### Phase 2: Core Implementation
- [ ] [Core task 1]
- [ ] [Core task 2]
- [ ] [Core task 3]

### Phase 3: Integration
- [ ] [Integration task 1]
- [ ] [Integration task 2]

### Phase 4: Testing
- [ ] [Test task 1]
- [ ] [Test task 2]

---

## Data Model Changes

**New/Modified entities:**
- [Entity 1]: [description]
- [Entity 2]: [description]

**Database changes needed:**
- [ ] [Migration 1]
- [ ] [Migration 2]

---

## File Structure

**New files to create:**
```
[file-path-1]
[file-path-2]
```

**Files to modify:**
```
[file-path-1]
[file-path-2]
```

---

## Key Decisions

**Decision 1**: [What was decided]
- **Why**: [Rationale]
- **Alternative**: [What we didn't choose]

**Decision 2**: [What was decided]
- **Why**: [Rationale]

---

## Acceptance Criteria

From spec.md:
- [ ] [AC 1]
- [ ] [AC 2]
- [ ] [AC 3]

---

## Potential Gotchas

- [Gotcha 1]: [How to avoid]
- [Gotcha 2]: [How to avoid]

---

## Next Steps

After plan approval:
1. Run `/lite-implement` to start coding
2. Follow TDD-lite approach
3. Document as you build

---

## References

- Spec: .shipkit-lite/specs/active/[feature-name].md
- Stack: .shipkit-lite/stack.md
- Architecture: .shipkit-lite/architecture.md
```

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it:

"This plan establishes [pattern/choice]. Should I log this to architecture-memory-lite?"

If yes, suggest:
```
/lite-architecture-memory
```

---

### Step 5: Suggest Next Step

**Output to user**:
```
✅ Implementation plan created

📁 Location: .shipkit-lite/plans/[feature-name]-plan.md

📋 Summary:
  • [X] implementation steps
  • [Y] files to create/modify
  • [Z] database changes

🎯 Complexity: [Simple/Medium/Complex]
⏱️  Estimated: [X hours/days]

👉 Next: /lite-implement
   Start coding following this plan

Ready to start implementing?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Step-by-step implementation guide
- ✅ References existing context (stack, architecture)
- ✅ File structure planning
- ✅ Key technical decisions

**Not included** (vs full dev-plan):
- ❌ Research phase (no unknowns investigation)
- ❌ API contracts (OpenAPI/GraphQL schemas)
- ❌ Detailed data model design
- ❌ Performance benchmarks
- ❌ Security threat modeling
- ❌ Deployment planning

**Philosophy**: Good enough plan to start coding, not exhaustive design doc.

---

## Integration with Other Skills

**Before plan-lite**:
- `/lite-spec` - Creates feature specification
- `/lite-project-context` - Generates stack.md, schema.md
- `/lite-architecture-memory` - Logs past decisions

**After plan-lite**:
- `/lite-implement` - Executes the plan with TDD-lite
- `/lite-architecture-memory` - Logs significant decisions (optional)

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit-lite/specs/active/[feature].md` - Feature requirements
- `.shipkit-lite/stack.md` - Tech stack info

**Conditionally reads**:
- `.shipkit-lite/architecture.md` - Past decisions
- `.shipkit-lite/types.md` - Type definitions
- `.shipkit-lite/schema.md` - Database schema

---

## Context Files This Skill Writes

**Creates**:
- `.shipkit-lite/plans/[feature]-plan.md` - Implementation plan

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**:
- Each plan is feature-specific and tied to a single spec
- Plans are generated on-demand when user invokes `/lite-plan`
- If user re-plans the same feature, they want a fresh plan based on current context
- Old plans become stale as specs, stack, or architecture evolve
- No historical value: planning is forward-looking, not a historical record
- Checkboxes track implementation progress, but that state belongs in implementation tracking, not the plan itself

**Behavior**:
- If `.shipkit-lite/plans/[feature]-plan.md` exists, completely replace it
- Use Write tool (after Read) to overwrite with new content
- No archiving needed - plans are regenerated artifacts, not historical documents
- User can always re-generate by re-running `/lite-plan`

**When to re-plan**:
- Spec changed significantly (use `/lite-spec` to update, then re-run `/lite-plan`)
- Tech stack changed (stack.md updated, need new plan)
- Architecture patterns changed (architecture.md updated, need aligned plan)

**Never modifies**:
- Specs, stack, architecture (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-plan`
2. shipkit-master-lite tells Claude to read this SKILL.md
3. Claude asks user which spec to plan
4. Claude reads only relevant spec + stack
5. Claude optionally reads architecture/types if needed
6. Claude generates plan
7. Context loaded: ~1500-2500 tokens (focused)

**Not loaded unless needed**:
- Other specs
- Implementation docs
- User tasks
- Progress logs

---

## Success Criteria

Plan is complete when:
- [ ] All implementation steps identified
- [ ] File structure defined
- [ ] Database changes documented
- [ ] Key decisions explained
- [ ] References existing patterns from architecture.md
- [ ] Respects tech stack from stack.md
- [ ] Acceptance criteria from spec included

---

## Tips for Effective Planning

**Keep it focused**:
- Plan ONE feature at a time
- 10-20 steps maximum for POC
- Don't over-design

**Reference context**:
- Check stack.md for approved tech
- Check architecture.md for established patterns
- Reuse existing components when possible

**Make it actionable**:
- Specific file paths
- Clear task descriptions
- Checkboxes for tracking

**When to upgrade to full /dev-plan**:
- Complex integrations requiring research
- API contracts needed
- Security-critical features
- Performance requirements
- Multi-service coordination

---

**Remember**: This is a POC/MVP plan. Get something working, then refine. Don't spend hours planning what you could learn in minutes of coding.
