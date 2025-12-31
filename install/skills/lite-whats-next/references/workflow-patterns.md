# Workflow Intelligence Patterns

## Smart Routing Based on Context

**Context-aware suggestions (not just rule-based):**

**If user has been implementing for a while** (3+ commits, no docs):
→ Suggest: /lite-component-knowledge (before knowledge is lost)

**If user has multiple specs but no implementations**:
→ Suggest: /lite-implement (stop planning, start building)

**If user keeps creating specs without plans**:
→ Suggest: /lite-plan (complete the co-design phase)

**If components built but UX not audited**:
→ Suggest: /lite-ux-audit (check for missing UX best practices)

**If manual tasks detected but not tracked**:
→ Suggest: /lite-user-instructions (capture blocking tasks)

**If session ending or context getting long**:
→ Suggest: /lite-work-memory (log progress before losing context)

---

## Output Verbosity Levels

**Auto-invoked** (after skill via hook):
- Brief recommendation only
- Skip full pillar analysis (user just completed a skill, knows state)
- Format:
  ```
  ## What's Next? 🧭

  **Run: /lite-[skill-name]**

  **Why**: [One sentence rationale]

  **What this accomplishes**: [Brief outcome]
  ```

**Manual invocation** (user asks "what's next?"):
- Full analysis with pillar breakdown
- Show all gaps and alternatives
- Comprehensive state summary
- Format:
  ```
  ## What's Next? 🧭

  ### Project State Summary
  [5 pillar status with details]

  ### Recommended Next Step
  [Detailed rationale with alternatives]

  ### Critical Gaps
  [If any missing dependencies]
  ```

**Adaptive based on invocation method**

---

## What This Skill Eliminates

**From ALL 18 existing lite skills:**
- "Next steps" sections (50-100 lines each)
- Hardcoded workflow suggestions
- Fragile "after X do Y" logic

**From suggest-next-skill.py hook:**
- 80+ lines of detection logic
- Brittle file checking
- Hardcoded skill mappings

**Result**: Single source of truth for workflow intelligence

---

## Multi-Gap Priority Hierarchy

**When multiple critical gaps exist, prioritize:**

1. **Vision** (always first if missing)
   - Why: All decisions need strategic context
   - Suggest: /lite-why-project

2. **Understand Current** (need tech context)
   - Why: Can't plan features without knowing constraints
   - Suggest: /lite-project-context

3. **Co-design** (plan before building)
   - Why: Implementation needs clear requirements
   - Suggest: /lite-spec → /lite-plan

4. **Execute** (build the thing)
   - Why: Features need to be implemented
   - Suggest: /lite-implement

5. **Document** (capture knowledge)
   - Why: Knowledge decays without documentation
   - Suggest: /lite-component-knowledge, /lite-work-memory

**Example multi-gap scenario:**
```
Vision missing + Stack missing + No specs

Priority: Vision first
→ Suggest: /lite-why-project

Next session after vision:
→ Suggest: /lite-project-context

Then after stack:
→ Suggest: /lite-spec
```

---

## Staleness Detection Rules

**why.md stale** (>30 days old):
```
⚠️  Vision is 45 days old. Project may have evolved.
    Consider refreshing: /lite-why-project
```

**stack.md stale** (older than package.json mtime):
```
⚠️  Stack outdated (older than package.json).
    Dependencies may have changed.
    Refresh: /lite-project-context
```

**implementations.md stale** (older than most recent src/ changes):
```
⚠️  Documentation lags behind code.
    Update: /lite-component-knowledge
```

---

## Completion Detection

**When all 5 pillars complete:**
```
## What's Next? 🧭

### 🎉 All Pillars Complete!

✅ Vision defined (why.md)
✅ Current state understood (stack.md)
✅ Features co-designed (specs + plans)
✅ Implementation in progress (source code)
✅ Documentation current (implementations.md, architecture.md)

### Recommended Next Step

**Continue iterating**:
- New feature: /lite-spec → /lite-plan → /lite-implement
- Quality check: /lite-quality-confidence
- Team update: /lite-communications
- Session log: /lite-work-memory

### Or Maintain

- Update vision: /lite-why-project (if direction changed)
- Refresh stack: /lite-project-context (if dependencies updated)
- Health check: /lite-project-status (comprehensive gap analysis)
- UX audit: /lite-ux-audit (check for missing UX best practices)
```
