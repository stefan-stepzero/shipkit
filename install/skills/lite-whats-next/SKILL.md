---
name: lite-whats-next
description: Analyzes project state across 4 pillars (Vision → Understand → Co-design → Execute → Document) and suggests next skill with rationale. Auto-called after every skill via hook.
---

# lite-whats-next - Intelligent Workflow Guidance

**Purpose**: Analyze current project state, identify gaps, and suggest the next logical skill based on 4-pillar strategic framework.

**What it does**: Scans `.shipkit-lite/`, evaluates completion across pillars, detects workflow phase, suggests next skill with rationale.

---

## When to Invoke

**Auto-invoked**:
- After EVERY skill completes (via suggest-next-skill.py hook)

**Manual invocation**:
- User asks: "What should I do next?", "What's next?", "Where should I start?"
- User feels lost or unsure of next step

**Use cases**:
- Automatic workflow guidance after any skill
- Strategic planning ("what's the optimal order?")
- Gap detection ("what am I missing?")
- Getting unstuck ("I don't know what to do")

---

## The 4-Pillar Framework

**Order**: Vision → Understand → Co-design → Execute → Document

### Pillar 1: Vision (C1)
**Goal**: Know WHY and WHERE you're going

**Skills**:
- lite-why-project (who/why/where/how)

**Outputs**:
- `.shipkit-lite/why.md`

---

### Pillar 2: Understand Current (A)
**Goal**: Know WHERE you are technically

**Skills**:
- lite-project-context (scan stack)
- lite-project-status (health check)

**Outputs**:
- `.shipkit-lite/stack.md`
- Status report (no file, console only)

---

### Pillar 3: Co-design Future (C2)
**Goal**: PLAN what to build

**Skills**:
- lite-spec (feature specifications)
- lite-plan (implementation plans)

**Outputs**:
- `.shipkit-lite/specs/active/*.md`
- `.shipkit-lite/plans/*.md`

---

### Pillar 4: Execute (D)
**Goal**: BUILD the features

**Skills**:
- lite-implement (TDD implementation)
- lite-quality-confidence (pre-ship verification)
- lite-user-instructions (track manual tasks)

**Outputs**:
- Source code (src/, app/, components/)
- `.shipkit-lite/user-tasks/active.md`

---

### Pillar 5: Document Current (B)
**Goal**: CAPTURE what was built

**Skills**:
- lite-component-knowledge (document components)
- lite-route-knowledge (document routes)
- lite-architecture-memory (log decisions)
- lite-data-consistency (capture types)
- lite-communications (visual HTML reports)
- lite-document-artifact (structured docs)

**Outputs**:
- `.shipkit-lite/implementations.md`
- `.shipkit-lite/architecture.md`
- `.shipkit-lite/types.md`
- `.shipkit-lite/docs/**/*.md`
- `.shipkit-lite/communications/latest.html`

---

## Process

### Step 1: Scan Project State

**Check all .shipkit-lite/ files:**

```
Read/Check:
- why.md (exists?)
- stack.md (exists?)
- specs/active/ (count files)
- plans/ (count files)
- implementations.md (exists? line count?)
- architecture.md (exists? entry count?)
- types.md (exists?)
- user-tasks/active.md (exists? task count?)
- communications/ (exists?)
- docs/ (exists? count files?)
```

**Also check:**
- Source code existence (src/, app/, components/ folders)
- Git status (uncommitted changes?)

---

### Step 2: Evaluate Each Pillar

**Pillar 1: Vision - Check completion:**
- ✅ Complete: why.md exists
- ⚠️ Stale: why.md older than 30 days (suggest update)
- ❌ Missing: why.md doesn't exist

**Pillar 2: Understand Current - Check completion:**
- ✅ Complete: stack.md exists and fresh
- ⚠️ Stale: stack.md older than package.json
- ❌ Missing: stack.md doesn't exist

**Pillar 3: Co-design Future - Check completion:**
- ✅ Complete: Has specs AND plans
- ⏳ In Progress: Has specs but missing plans (or vice versa)
- ❌ Missing: No specs or plans

**Pillar 4: Execute - Check completion:**
- ✅ Complete: Source code exists, plans completed
- ⏳ In Progress: Source code exists, plans exist
- ❌ Not Started: No source code yet

**Pillar 5: Document Current - Check completion:**
- ✅ Complete: implementations.md exists with content
- ⏳ Partial: Some docs exist (implementations OR architecture)
- ❌ Missing: No documentation of current state

---

### Step 3: Determine Current Phase

**Based on pillar states, identify workflow phase:**

**Phase 1: Project Setup** (nothing exists)
- Missing: Vision, Stack
- Suggest: /lite-why-project

**Phase 2: Technical Discovery** (vision exists, no stack)
- Has: Vision
- Missing: Stack
- Suggest: /lite-project-context

**Phase 3: Planning** (vision + stack exist, no specs)
- Has: Vision, Stack
- Missing: Specs
- Suggest: /lite-spec

**Phase 4: Implementation** (specs exist, need plans or implementation)
- Has: Vision, Stack, Specs
- Missing: Plans or implementation incomplete
- Suggest: /lite-plan OR /lite-implement

**Phase 5: Documentation** (code exists, docs missing)
- Has: Source code
- Missing: Documentation (implementations.md sparse)
- Suggest: /lite-component-knowledge

**Phase 6: Quality** (ready to ship)
- Has: Implementation complete
- Suggest: /lite-quality-confidence

---

### Step 4: Check Dependencies & Warn

**Before suggesting skill, check if dependencies exist:**

**lite-spec dependencies:**
- Recommended: why.md (vision)
- Warning if missing: "No vision defined. Recommend /lite-why-project first, but can proceed."

**lite-plan dependencies:**
- Required: spec must exist
- Warning if missing: "No spec found. Create spec first with /lite-spec, or proceed without?"

**lite-implement dependencies:**
- Recommended: plan exists
- Warning if missing: "No plan found. Recommend /lite-plan first, but can proceed."

**lite-component-knowledge dependencies:**
- Required: Source code exists
- Error if missing: "No components to document yet. Implement first."

---

### Step 5: Generate Recommendation

**Output format:**

```markdown
## What's Next? 🧭

{IF GAPS DETECTED IN CRITICAL PILLARS:}
### ⚠️  Critical Gaps

- Vision missing: No why.md found
- Stack unknown: No stack.md found

{END IF}

---

### Recommended Next Step

**Run: /lite-{skill-name}**

**Why**: {Rationale based on pillar analysis}

{IF DEPENDENCY WARNING:}
⚠️  **Note**: {Dependency warning message}
{END IF}

**What this accomplishes**:
- {Pillar}: {Progress made}
- {Outcome}: {User benefit}

---

### Alternative Paths

**If you prefer to**:
- {Alternative goal}: Run /lite-{alternative-skill}
- {Another goal}: Run /lite-{another-skill}

---

### Project State Summary

**Pillar 1: Vision** {✅/⏳/❌}
  {Status details}

**Pillar 2: Understand Current** {✅/⏳/❌}
  {Status details}

**Pillar 3: Co-design Future** {✅/⏳/❌}
  {Status details}

**Pillar 4: Execute** {✅/⏳/❌}
  {Status details}

**Pillar 5: Document Current** {✅/⏳/❌}
  {Status details}
```

---

## Example Scenarios

### Scenario 1: Brand New Project

**State**: Nothing exists

**Analysis**:
- Pillar 1 (Vision): ❌ Missing (no why.md)
- Pillar 2 (Understand): ❌ Missing (no stack.md)
- Pillar 3 (Co-design): ❌ Missing (no specs)
- Pillar 4 (Execute): ❌ Not started
- Pillar 5 (Document): ❌ Missing

**Recommendation**:
```
Run: /lite-why-project

Why: Starting a project without vision leads to aimless decisions.
     Define who/why/where first, then everything else aligns.

What this accomplishes:
- Pillar 1: Vision defined
- Outcome: Claude knows your goals for better suggestions
```

---

### Scenario 2: Vision + Stack, No Specs

**State**: why.md and stack.md exist, no specs

**Analysis**:
- Pillar 1 (Vision): ✅ Complete
- Pillar 2 (Understand): ✅ Complete
- Pillar 3 (Co-design): ❌ Missing
- Pillar 4 (Execute): ❌ Not started
- Pillar 5 (Document): ❌ Missing

**Recommendation**:
```
Run: /lite-spec

Why: You know your vision and tech stack. Time to plan your first feature.

What this accomplishes:
- Pillar 3: Co-design initiated
- Outcome: Clear feature spec guides implementation
```

---

### Scenario 3: Code Exists, No Docs

**State**: Source code in src/, no implementations.md

**Analysis**:
- Pillar 1 (Vision): ✅ Complete
- Pillar 2 (Understand): ✅ Complete
- Pillar 3 (Co-design): ✅ Complete (2 specs, 2 plans)
- Pillar 4 (Execute): ⏳ In Progress
- Pillar 5 (Document): ❌ Missing (no implementations.md)

**Recommendation**:
```
Run: /lite-component-knowledge

Why: You've built components but haven't documented them.
     Document now (2 min) vs trying to remember later (20 min).

What this accomplishes:
- Pillar 5: Document current state
- Outcome: Future you (or teammates) can understand your code

Alternative Paths:
- Continue building: /lite-implement (if rushing)
- Ship current feature: /lite-quality-confidence
```

---

### Scenario 4: Spec Exists, No Plan

**State**: specs/active/recipe-sharing.md exists, no plan

**Analysis**:
- Pillar 3 (Co-design): ⏳ Partial (spec exists, plan missing)

**Recommendation**:
```
Run: /lite-plan

Why: You have a spec but no implementation plan.
     Planning helps break work into manageable tasks.

What this accomplishes:
- Pillar 3: Co-design complete
- Outcome: Clear roadmap from spec to implementation
```

---

### Scenario 5: Missing Dependencies Warning

**State**: User just ran /lite-plan but no spec exists

**Recommendation**:
```
Run: /lite-spec

⚠️  Note: You created a plan without a spec. Consider creating
          a spec first for better alignment.

Why: Plans work best when based on clear specifications.

What this accomplishes:
- Pillar 3: Proper co-design flow (spec → plan)
- Outcome: Implementation has clear requirements

Alternative Paths:
- Proceed anyway: /lite-implement (use plan as-is)
```

---

## Integration with suggest-next-skill.py Hook

**Old hook** (80+ lines):
```python
# Detect which skill just ran
# Check 8+ file locations
# Map to 8+ different suggestions
```

**New hook** (10 lines):
```python
def main():
    # Just invoke lite-whats-next skill
    # Let the skill do all intelligence
    print()
    print("---")
    print()
    # Skill outputs recommendation
    return 0
```

**Massive simplification**: Hook delegates to skill

---

## Workflow Intelligence

**lite-whats-next enforces optimal flow:**

1. **Vision first** - Can't plan features without knowing why
2. **Understand before planning** - Need to know tech constraints
3. **Spec before plan** - Clear requirements before breakdown
4. **Plan before implement** - Know the approach before coding
5. **Implement before document** - Can't document what doesn't exist
6. **Document before next feature** - Capture knowledge while fresh

**But allows flexibility**:
- Warns about missing dependencies
- Suggests optimal path
- Allows user to override

---

## Context Files This Skill Reads

**Scans entire `.shipkit-lite/` folder:**
- `why.md`
- `stack.md`
- `architecture.md`
- `implementations.md`
- `types.md`
- `specs/active/*.md`
- `plans/*.md`
- `user-tasks/active.md`
- `communications/latest.html`
- `docs/**/*.md`

**Also checks:**
- Source code folders (src/, app/, components/)
- Git status

**Reads everything to build complete picture**

---

## Context Files This Skill Writes

**None** - This skill is read-only analysis

**Never modifies files** - Only suggests next action

---

## Success Criteria

Recommendation is helpful when:
- [ ] Scanned all .shipkit-lite/ files
- [ ] Evaluated all 5 pillars accurately
- [ ] Detected current workflow phase correctly
- [ ] Suggested next skill with clear rationale
- [ ] Warned about missing dependencies (if any)
- [ ] Provided alternative paths
- [ ] Showed project state summary

---

## Special Behaviors

### Multi-Gap Scenarios

**If multiple critical gaps exist:**
```
Vision missing + Stack missing
→ Suggest: /lite-why-project (vision first always)

Spec exists + Plan missing + Docs missing
→ Suggest: /lite-plan (complete co-design before documenting)
```

**Priority hierarchy:**
1. Vision (always first if missing)
2. Understand Current (need tech context)
3. Co-design (plan before building)
4. Execute (build the thing)
5. Document (capture knowledge)

---

### Staleness Detection

**Files can become stale:**

**why.md stale** (>30 days old):
```
⚠️  Vision is 45 days old. Consider refreshing: /lite-why-project
```

**stack.md stale** (older than package.json):
```
⚠️  Stack outdated (older than package.json). Refresh: /lite-project-context
```

**Suggests updates when appropriate**

---

### Completion Detection

**When all pillars complete:**
```
## What's Next? 🧭

### 🎉 All Pillars Complete!

✅ Vision defined
✅ Current state understood
✅ Features co-designed
✅ Implementation in progress
✅ Documentation current

### Recommended Next Step

**Continue iterating**:
- New feature: /lite-spec → /lite-plan → /lite-implement
- Quality check: /lite-quality-confidence
- Team update: /lite-communications

### Or Maintain

- Update vision: /lite-why-project
- Refresh stack: /lite-project-context
- Health check: /lite-project-status
```

---

## Pillar Dependency Rules

**Strict dependencies** (warn if violated):
- lite-plan requires spec exists
- lite-component-knowledge requires source code exists

**Recommended dependencies** (suggest but allow):
- lite-spec recommends why.md exists
- lite-implement recommends plan exists
- lite-architecture-memory recommends why.md exists

**No dependencies** (always allowed):
- lite-why-project (can run anytime)
- lite-project-context (can run anytime)
- lite-project-status (can run anytime)
- lite-communications (can run anytime)

---

## Smart Routing Based on Context

**If user has been implementing for a while** (3+ commits, no docs):
→ Suggest: /lite-component-knowledge (before knowledge is lost)

**If user has multiple specs but no implementations**:
→ Suggest: /lite-implement (stop planning, start building)

**If user keeps creating specs without plans**:
→ Suggest: /lite-plan (complete the co-design phase)

**Context-aware, not just rule-based**

---

## Manual Invocation Benefits

**User can run `/lite-whats-next` anytime to:**
- Get unstuck ("I don't know what to do")
- Check gaps ("Am I missing something?")
- See big picture ("Where am I in the workflow?")
- Plan next session ("What should I focus on today?")

**Always helpful, never annoying**

---

## Output Verbosity Levels

**Auto-invoked** (after skill via hook):
- Brief recommendation only
- Skip full pillar analysis (user just completed a skill, knows state)

**Manual invocation** (user asks "what's next?"):
- Full analysis with pillar breakdown
- Show all gaps and alternatives
- Comprehensive state summary

**Adaptive based on invocation method**

---

## This Skill Eliminates

**From ALL 18 existing skills:**
- "Next steps" sections (50-100 lines each)
- Hardcoded workflow suggestions
- Fragile "after X do Y" logic

**From suggest-next-skill.py hook:**
- 80+ lines of detection logic
- Brittle file checking
- Hardcoded skill mappings

**Result**: Single source of truth for workflow

---

**Remember**: This skill is the workflow brain. It analyzes, suggests, warns, but never blocks. Vision first, then understand, co-design, execute, document. Optimal flow with user flexibility.
