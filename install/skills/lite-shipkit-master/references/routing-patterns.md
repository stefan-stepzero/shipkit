# Routing Patterns and Logic

Decision tree, context loading instructions, and post-routing suggestions.

---

## Routing Logic - Decision Tree

```
User sends message
    ↓
Does it contain meta keywords ("status", "scan", "help")?
    YES → Route to meta skill
    NO  → Continue
    ↓
Does it contain decision keywords ("decide", "architecture", "UX", "integration")?
    YES → Route to decision skill
    NO  → Continue
    ↓
Does it contain implementation keywords ("spec", "plan", "implement", "build")?
    YES → Route to implementation skill
    NO  → Continue
    ↓
Does it contain documentation keywords ("document", "docs", "component")?
    YES → Route to documentation skill
    NO  → Continue
    ↓
Does it contain quality keywords ("quality", "ship", "checklist", "task", "progress")?
    YES → Route to quality/process skill
    NO  → Continue
    ↓
Ambiguous intent
    ↓
Ask clarifying question:
  "Did you mean to:
   1. Create a spec for this? (/lite-spec)
   2. Plan implementation? (/lite-plan)
   3. Start coding? (/lite-implement)"
```

---

## Context Loading Instructions for Claude

**When shipkit-master-lite routes to a skill:**

### Pattern 1: Meta Skills (Glob-Based)

```
User: "What's the project status?"

shipkit-master-lite:
1. Route: /lite-project-status
2. Load context:
   - Glob: .shipkit-lite/specs/active/*.md
   - Glob: .shipkit-lite/plans/*.md
   - Read: .shipkit-lite/implementations.md
   - Read: .shipkit-lite/progress.md
3. Invoke: project-status-lite
```

### Pattern 2: Implementation Skills (Focused)

```
User: "Plan the recipe sharing feature"

shipkit-master-lite:
1. Route: /lite-plan
2. Load context (in order):
   - Read: .shipkit-lite/specs/active/recipe-sharing.md
   - Read: .shipkit-lite/stack.md
   - Read: .shipkit-lite/architecture.md (if exists)
3. Invoke: plan-lite
4. plan-lite asks user questions before generating
```

### Pattern 3: Documentation Skills (Append)

```
User: "Document the RecipeCard component"

shipkit-master-lite:
1. Route: /lite-component-knowledge
2. Load context:
   - Read: .shipkit-lite/implementations.md
   - Read: .shipkit-lite/stack.md
3. Invoke: component-knowledge-lite
4. Skill appends to implementations.md
```

---

## What to Suggest After Completion

**shipkit-master-lite doesn't "complete" - it routes.**

**But after routing, suggest next skill based on what was invoked:**

### After Meta Skills

| Just Ran | Suggest Next |
|----------|--------------|
| `/lite-project-status` | Contextual based on what's missing (e.g., "No specs exist, run /lite-spec?") |
| `/lite-project-context` | "Context refreshed. Ready to spec features? Run /lite-spec" |

### After Decision Skills

| Just Ran | Suggest Next |
|----------|--------------|
| `/lite-architecture-memory` | "Decision logged. Continue with current task." |
| `/lite-spec` | "Spec created. Plan it? Run /lite-plan" |

### After Implementation Skills

| Just Ran | Suggest Next |
|----------|--------------|
| `/lite-spec` | "/lite-plan" |
| `/lite-plan` | "/lite-implement" |
| `/lite-implement` | "/lite-quality-confidence OR /lite-component-knowledge" |

### After Documentation Skills

| Just Ran | Suggest Next |
|----------|--------------|
| `/lite-component-knowledge` | "Documentation updated. Continue implementing?" |
| `/lite-work-memory` | "Progress logged. Session complete." |

---

## Ambiguous Intent Handling

**If user request doesn't match clear keywords:**

1. **Ask clarifying question:**
   "Do you want to [option A] or [option B]?"

2. **Examples:**
   - "Document this" → Component or route? Ask.
   - "Fix this" → Debug or implement? Ask.
   - "Create X" → Spec, plan, or implement? Ask.

3. **Default to simplest skill:**
   - If POC → Suggest implement directly
   - If Greenfield → Suggest spec → plan → implement chain

---

## Missing Context Handling

**If required context is missing:**

```
❌ Cannot run /lite-plan - No spec exists

Options:
1. Create spec first: /lite-spec
2. Plan without spec (not recommended)

Proceed?
```

---

## Common Routing Patterns

### Pattern 1: First-Time Setup
```
User: [starts session]
→ shipkit-master-lite: "No stack.md found"
→ Suggest: /lite-project-context
→ User runs it
→ Suggest: /lite-project-status
```

### Pattern 2: Feature Development
```
User: "Build recipe sharing"
→ Check: Does spec exist?
→ NO → Suggest: /lite-spec first
→ YES → Route to /lite-plan
→ After plan → Suggest /lite-implement
```

### Pattern 3: Documentation Update
```
User: "Document the UserCard component"
→ Route: /lite-component-knowledge
→ Load: implementations.md, stack.md
→ Skill appends documentation
→ Suggest: Continue implementing
```

### Pattern 4: Decision Logging
```
User: "We decided to use Zustand for state"
→ Route: /lite-architecture-memory
→ Load: architecture.md
→ Skill appends decision
→ Suggest: Continue current task
```

---

## Tips for Effective Routing

**For Claude Code users:**

1. **Always check freshness first** - Don't waste tokens on stale context
2. **Load incrementally** - Only what's needed for current task
3. **Route precisely** - Match keywords to skills accurately
4. **Ask when unclear** - Better to clarify than guess wrong
5. **Suggest next steps** - Keep workflow moving forward

**When user says something vague:**
- Don't assume intent
- Present 2-3 most likely options
- Let user choose

**When prerequisites are missing:**
- Don't fail silently
- Explain what's missing
- Suggest prerequisite skill
- Offer to proceed anyway (with warning)
