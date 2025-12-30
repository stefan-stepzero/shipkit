---
name: lite-whats-next
description: Analyzes project state across 5 pillars (Vision → Understand → Co-design → Execute → Document) and suggests next skill with rationale. Auto-invoked after every skill via Stop hook.
---

# lite-whats-next - Intelligent Workflow Guidance

**Purpose**: Analyze current project state, identify gaps, and suggest the next logical skill based on 5-pillar strategic framework.

**What it does**: Scans `.shipkit-lite/`, evaluates completion across pillars, detects workflow phase, suggests next skill with rationale.

---

## When to Invoke

**Auto-invoked**:
- After EVERY skill completes (via suggest-next-skill.py Stop hook)
- Mandatory per `lite.md` meta-rule

**Manual invocation**:
- User asks: "What should I do next?", "What's next?", "Where should I start?"
- User feels lost or unsure of next step

**Use cases**:
- Automatic workflow guidance after any skill
- Strategic planning ("what's the optimal order?")
- Gap detection ("what am I missing?")
- Getting unstuck ("I don't know what to do")

---

## Prerequisites

**Required**:
- `.shipkit-lite/` folder exists (created by any lite skill)

**Optional** (enhances analysis):
- `why.md` - Strategic vision (better suggestions)
- `stack.md` - Technical context (smarter routing)
- Any other context files (more accurate gap detection)

**This skill can run even on empty projects** - it detects the brand-new state and suggests `/lite-why-project` as starting point.

---

## The 5-Pillar Framework

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
- lite-prototyping (rapid UI mockups)
- lite-prototype-to-spec (extract prototype learnings to specs)
- lite-plan (implementation plans)
- lite-ux-coherence (ensure UX consistency)

**Outputs**:
- `.shipkit-lite/specs/active/*.md`
- `.shipkit-mockups/[name]/` (prototypes)
- Specs updated with UI/UX section (from prototype extraction)
- `.shipkit-lite/plans/*.md`
- UX analysis (console only, or appended to spec)

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
- lite-work-memory (log session progress)
- lite-communications (visual HTML reports)
- lite-document-artifact (structured docs)

**Outputs**:
- `.shipkit-lite/implementations.md`
- `.shipkit-lite/architecture.md`
- `.shipkit-lite/types.md`
- `.shipkit-lite/progress.md`
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
- progress.md (exists? session count?)
- communications/ (exists?)
- docs/ (exists? count files?)
```

**Also check:**
- `.shipkit-mockups/` (count prototype folders)
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
- ⏳ Partial: Some docs exist (implementations OR architecture OR progress)
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

**Phase 4: Prototyping/Implementation** (specs exist, ready to build)
- Has: Vision, Stack, Specs
- Missing: Plans, prototypes, or implementation incomplete
- Suggest: /lite-prototyping (if UI-heavy) OR /lite-plan OR /lite-implement

**Phase 5: Documentation** (code exists, docs missing)
- Has: Source code
- Missing: Documentation (implementations.md sparse)
- Suggest: /lite-component-knowledge OR /lite-work-memory

**Phase 6: Quality** (ready to ship)
- Has: Implementation complete
- Suggest: /lite-quality-confidence OR /lite-ux-coherence

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

**See `references/pillar-dependencies.md` for complete dependency rules.**

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

## Integration with suggest-next-skill.py Hook

**Hook is simple** (10 lines of logic):
```python
def main():
    # Directive to Claude (not suggestion to user)
    print("🤖 CLAUDE: Invoke /lite-whats-next now to provide workflow guidance")
    return 0
```

**All intelligence lives in this skill** - the hook just triggers invocation.

**Massive simplification**: Hook delegates to skill instead of containing logic.

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

**See `references/workflow-patterns.md` for smart routing logic.**

---

## When This Skill Integrates with Others

### Before This Skill

**All 18 other lite skills** - This skill is invoked AFTER them
- **When**: After ANY lite skill completes
- **Why**: Provide intelligent workflow guidance based on project state
- **Trigger**: Stop hook fires after Claude finishes response

**This is the workflow brain** - it analyzes what was just done and suggests what's next.

### After This Skill

**The skill it recommends** - Suggests next logical step
- **When**: This skill analyzes project state and identifies gaps
- **Why**: Enforce optimal workflow order (Vision → Understand → Co-design → Execute → Document)
- **Trigger**: User chooses to follow recommendation (or overrides)

**Example flow**:
```
User completes /lite-spec
→ Stop hook fires
→ /lite-whats-next invoked
→ Analyzes: spec exists, no plan
→ Recommends: /lite-plan
→ User runs /lite-plan
```

### Special Relationships

**lite-project-status** - Complementary gap detection
- **When**: User asks "what's the status?" or "where are we?"
- **Why**: lite-project-status gives detailed health check, lite-whats-next gives workflow guidance
- **Difference**: Status = comprehensive gaps, Whats-next = next single action

**lite-why-project** - First skill suggested for new projects
- **When**: No .shipkit-lite/ files exist
- **Why**: Vision provides strategic context for all future decisions
- **Trigger**: Brand new project detected

**lite-prototyping** - Suggested for UI-heavy features after spec exists
- **When**: Spec exists and feature has significant UI/UX component
- **Why**: Validate UI decisions before committing to full implementation
- **Trigger**: Spec mentions UI, user wants to "see it" before building

**lite-prototype-to-spec** - Suggested after prototype iteration complete
- **When**: Prototype exists in .shipkit-mockups/ and user says "done prototyping"
- **Why**: Preserve validated UI/UX patterns before prototype is deleted
- **Trigger**: User completed prototype iteration, ready to document learnings

**lite-work-memory** - Often suggested at session end
- **When**: User has been working for a while, no recent progress log
- **Why**: Capture knowledge before ending session
- **Trigger**: Context window getting large, or explicit "end session"

**lite-ux-coherence** - Suggested when UX divergence detected
- **When**: Multiple features implemented with different patterns
- **Why**: Early UX audit prevents costly refactoring later
- **Trigger**: 3+ components exist, no recent UX check

**lite-user-instructions** - Suggested when blockers detected
- **When**: Implementation stalled, or manual tasks mentioned
- **Why**: Track blocking tasks so they don't get forgotten
- **Trigger**: User mentions "need to configure X" or "waiting on Y"

---

## Context Files This Skill Reads

**Scans entire `.shipkit-lite/` folder:**
- `why.md`
- `stack.md`
- `architecture.md`
- `implementations.md`
- `types.md`
- `progress.md`
- `specs/active/*.md`
- `plans/*.md`
- `user-tasks/active.md`
- `communications/latest.html`
- `docs/**/*.md`

**Also checks:**
- `.shipkit-mockups/` (prototype folders)
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

## Manual Invocation Benefits

**User can run `/lite-whats-next` anytime to:**
- Get unstuck ("I don't know what to do")
- Check gaps ("Am I missing something?")
- See big picture ("Where am I in the workflow?")
- Plan next session ("What should I focus on today?")

**Always helpful, never annoying**

---

## Common Scenarios

**See `references/common-scenarios.md` for 8 detailed scenarios:**
- Scenario 1: Brand New Project
- Scenario 2: Vision + Stack, No Specs
- Scenario 3: Code Exists, No Docs
- Scenario 4: Spec Exists, No Plan
- Scenario 5: Missing Dependencies Warning
- Scenario 6: Just Completed Implementation
- Scenario 7: UX Inconsistency Detected
- Scenario 8: Spec Exists, UI Uncertain (→ prototyping)

---

## Workflow Patterns

**See `references/workflow-patterns.md` for:**
- Smart routing based on context
- Output verbosity levels (auto vs manual invocation)
- What this skill eliminates (hardcoded suggestions)
- Multi-gap priority hierarchy
- Staleness detection rules
- Completion detection

---

## Pillar Dependencies

**See `references/pillar-dependencies.md` for:**
- Strict dependencies (block if missing)
- Recommended dependencies (warn if missing)
- No-dependency skills (always allowed)
- Dependency check algorithm

---

**Remember**: This skill is the workflow brain. It analyzes, suggests, warns, but never blocks. Vision first, then understand, co-design, execute, document. Optimal flow with user flexibility.
