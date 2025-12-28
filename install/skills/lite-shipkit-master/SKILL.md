---
name: lite-shipkit-master
description: Orchestrator that enforces skill usage, manages intelligent context loading at session start, and routes user requests to appropriate lite skills. Auto-loaded via session-start hook.
---

# shipkit-master-lite - Lightweight Orchestration & Routing

**Purpose**: Session orchestrator that checks file freshness, loads context efficiently, and routes user requests to appropriate lite skills based on keywords and project state.

**Role**: THE master orchestrator for Shipkit Lite. Loaded automatically at every session start via `.claude/hooks/session-start.sh`.

---

## When This Skill Loads

**Auto-invoked**:
- Every session start (via session-start.sh hook)
- Hook outputs this SKILL.md to Claude's context

**Manual invocation**:
- When user asks: "What should I do?", "Help me decide next steps", "What's available?"

---

## Core Responsibilities

1. **File Freshness Checking** - Determine if cached context is stale
2. **Lazy Context Loading** - Load only what's needed for current task
3. **Request Routing** - Match user intent to appropriate lite skill
4. **Context Mapping** - Tell Claude which files to read for each skill
5. **Next Step Suggestions** - Guide workflow progression

---

## File Freshness Checking Logic

### Purpose
Avoid loading stale context or wasting tokens regenerating fresh context.

### How It Works

**On session start, check if `.shipkit-lite/stack.md` is fresh:**

```bash
# Get timestamps (Unix epoch seconds)
STACK_TIME=$(stat -c %Y .shipkit-lite/stack.md 2>/dev/null || echo "0")
PACKAGE_TIME=$(stat -c %Y package.json 2>/dev/null || echo "0")
ENV_TIME=$(stat -c %Y .env.example 2>/dev/null || echo "0")

# Logic:
if [ ! -f .shipkit-lite/stack.md ]; then
  → stack.md missing → Suggest: /lite-project-context to create it
elif [ $STACK_TIME -lt $PACKAGE_TIME ]; then
  → stack.md older than package.json → Suggest: /lite-project-context to refresh
elif [ $STACK_TIME -lt $ENV_TIME ]; then
  → stack.md older than .env.example → Suggest: /lite-project-context to refresh
else
  → stack.md is fresh → Load cached stack.md (~100 tokens)
fi
```

**Apply same logic to other context files:**

| Context File | Compare Against | If Stale, Suggest |
|--------------|-----------------|-------------------|
| `.shipkit-lite/stack.md` | `package.json`, `.env.example` | `/lite-project-context` |
| `.shipkit-lite/schema.md` | `migrations/*`, `prisma/schema.prisma` | `/lite-project-context` |
| `.shipkit-lite/architecture.md` | N/A (append-only) | N/A |

**Token savings:**
- Fresh context: Load from cache (~100-200 tokens)
- Stale context: Suggest regeneration (~1,500 tokens to regenerate)

---

## Session Start Behavior

### What Happens at Session Start

**Hook execution (`.claude/hooks/session-start.sh`):**
```bash
#!/bin/bash
# Session start hook for Shipkit Lite

echo "🚀 Shipkit Lite Session Starting..."
echo ""

# 1. Load master orchestrator
cat .claude/skills/lite-shipkit-master/SKILL.md

# 2. Check and load stack.md (if fresh)
if [ -f .shipkit-lite/stack.md ]; then
  STACK_TIME=$(stat -c %Y .shipkit-lite/stack.md)
  PACKAGE_TIME=$(stat -c %Y package.json 2>/dev/null || echo "0")

  if [ $STACK_TIME -gt $PACKAGE_TIME ]; then
    echo "📚 Loading cached stack..."
    cat .shipkit-lite/stack.md
  else
    echo "⚠️  Stack may be stale. Run /lite-project-context to refresh."
  fi
else
  echo "📝 No stack.md found. Run /lite-project-context to scan project."
fi

# 3. Load architecture.md (if exists, always fresh since append-only)
if [ -f .shipkit-lite/architecture.md ]; then
  echo "🏗️  Loading architecture decisions..."
  cat .shipkit-lite/architecture.md
fi

echo ""
echo "✅ Ready. Use /lite-project-status to see project health."
echo ""
```

**Total tokens at session start: ~400-600**

- shipkit-master-lite SKILL.md: ~200 tokens
- stack.md (if fresh): ~100 tokens
- architecture.md (if exists): ~100-200 tokens
- Hook messages: ~50 tokens

**What's NOT loaded at session start:**
- Specs
- Plans
- Implementations
- User tasks
- Types
- Schema
- Component contracts

→ These load ON DEMAND when relevant skill is invoked.

---

## Skill Routing Table

**Match user intent to appropriate lite skill:**

### Meta/Infrastructure Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "What should I do?", "Show status", "Project health" | `/lite-project-status` | All .shipkit-lite/ files (glob scan) |
| "Scan project", "Generate stack", "Refresh context", "What's my tech stack?" | `/lite-project-context` | package.json, .env.example, migrations/ |
| "Help", "What skills exist?", "What can you do?" | List all lite skills | None |

### Decision & Design Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Log this decision", "Architecture choice", "Why did we choose X?" | `/lite-architecture-memory` | .shipkit-lite/architecture.md |
| "UX guidance", "Design patterns", "ADHD principles" | `/lite-ux-coherence` | .shipkit-lite/architecture.md (UX section) |
| "Stripe integration", "Supabase help", "Service warning" | `/lite-integration-guardrails` | .shipkit-lite/stack.md (determine services) |
| "Type consistency", "Update types", "Data contracts" | `/lite-data-consistency` | .shipkit-lite/types.md, component-contracts.md |

### Implementation Workflow Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec this feature", "Create specification", "Write requirements" | `/lite-spec` | .shipkit-lite/specs/active/ |
| "Plan this", "How to implement?", "Create plan" | `/lite-plan` | specs/, stack.md, architecture.md |
| "Build this", "Start coding", "Implement" | `/lite-implement` | plans/, specs/, stack.md |

### Documentation Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Document component", "How does X work?", "Component docs" | `/lite-component-knowledge` | .shipkit-lite/implementations.md |
| "Document route", "API endpoint docs", "Route docs" | `/lite-route-knowledge` | .shipkit-lite/implementations.md |
| "Create docs", "Write guide", "Documentation" | `/lite-document-artifact` | .shipkit-lite/docs/ |

### Process & Quality Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Pre-ship checklist", "Ready to ship?", "Quality check" | `/lite-quality-confidence` | implementations.md, specs/ |
| "Create task", "Track TODO", "User tasks" | `/lite-user-instructions` | .shipkit-lite/user-tasks/active.md |
| "Log progress", "Session summary", "What did we do?" | `/lite-work-memory` | .shipkit-lite/progress.md |

### Ambiguous Intent

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

## Context Loading Table

**Which context files to load for each skill:**

| Skill | Always Load | Conditionally Load |
|-------|-------------|-------------------|
| `/lite-project-status` | Glob .shipkit-lite/** | N/A |
| `/lite-project-context` | package.json | .env.example, migrations/, prisma/schema.prisma |
| `/lite-architecture-memory` | .shipkit-lite/architecture.md | N/A |
| `/lite-spec` | .shipkit-lite/specs/active/ | stack.md (tech choices), architecture.md (patterns) |
| `/lite-plan` | specs/active/[feature].md, stack.md | architecture.md, types.md, schema.md |
| `/lite-implement` | plans/[feature].md, stack.md | specs/, types.md, implementations.md |
| `/lite-component-knowledge` | .shipkit-lite/implementations.md | stack.md (to reference tech) |
| `/lite-route-knowledge` | .shipkit-lite/implementations.md | stack.md (to reference framework) |
| `/lite-quality-confidence` | implementations.md | specs/active/ (acceptance criteria) |
| `/lite-user-instructions` | .shipkit-lite/user-tasks/active.md | N/A |
| `/lite-work-memory` | .shipkit-lite/progress.md | N/A |

**Token budget per skill invocation: ~1500-2500 tokens**

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

## Special Behaviors

### 1. Enforce Skill Usage

**shipkit-master-lite prevents manual file editing:**

If user tries to manually edit `.shipkit-lite/` files:
```
❌ "Don't edit .shipkit-lite/ files manually!"

Use the appropriate skill instead:
  • .shipkit-lite/stack.md → /lite-project-context
  • .shipkit-lite/specs/* → /lite-spec
  • .shipkit-lite/plans/* → /lite-plan
  • .shipkit-lite/implementations.md → /lite-component-knowledge or /lite-route-knowledge
  • .shipkit-lite/architecture.md → /lite-architecture-memory
```

**Exception**: User can read files manually anytime.

---

### 2. Progressive Disclosure

**Never load all context at once.**

**Bad approach:**
```
Session start → Load everything (~5000 tokens)
```

**Good approach (Shipkit Lite way):**
```
Session start → Load master + stack + architecture (~400 tokens)
User asks to plan → Load relevant spec + stack (~1500 tokens)
User asks to implement → Load plan + stack (~1500 tokens)
```

**Total context across 3 interactions: ~3400 tokens**
vs.
**Loading everything upfront: ~5000 tokens**

**Savings:** 32% fewer tokens, better focus.

---

### 3. Freshness Warnings

**Output examples:**

```
⚠️  stack.md is older than package.json
    Dependencies may have changed.
    Run /lite-project-context to refresh.

✅ stack.md is fresh (newer than package.json)
```

```
⚠️  schema.md is older than migrations/
    Database schema may have changed.
    Run /lite-project-context to refresh.

✅ schema.md is fresh
```

---

### 4. Missing Context Handling

**If required context is missing:**

```
❌ Cannot run /lite-plan - No spec exists

Options:
1. Create spec first: /lite-spec
2. Plan without spec (not recommended)

Proceed?
```

---

## Integration with Other Skills

**shipkit-master-lite is the hub:**

```
            shipkit-master-lite
                    |
      ┌─────────────┼─────────────┐
      |             |             |
   Meta Skills  Implementation  Documentation
      |             |             |
project-status  spec-lite    component-knowledge
project-context plan-lite    route-knowledge
                implement    document-artifact
```

**All skills flow through shipkit-master-lite routing.**

---

## Success Criteria

shipkit-master-lite is working correctly when:

- [ ] Session starts load ~400 tokens (not thousands)
- [ ] File freshness is checked accurately
- [ ] User requests route to correct skills
- [ ] Context loads on demand (not upfront)
- [ ] Ambiguous requests trigger clarifying questions
- [ ] Manual edits to .shipkit-lite/ are discouraged
- [ ] Next skill suggestions are contextual

---

## Example Session Flow

### Session 1: Fresh Start

```
[Session starts - hook runs]

🚀 Shipkit Lite Session Starting...

📝 No stack.md found. Run /lite-project-context to scan project.

✅ Ready. Use /lite-project-status to see project health.

---

User: "Scan my project"

Claude (via shipkit-master-lite):
• Routing to: /lite-project-context
• Loading: package.json, .env.example
• [project-context-lite executes]
• Generated: .shipkit-lite/stack.md

✅ Project context created

Next: /lite-project-status to see overall health
```

### Session 2: Continuing Work

```
[Session starts - hook runs]

🚀 Shipkit Lite Session Starting...

📚 Loading cached stack...
[stack.md contents - ~100 tokens]

🏗️  Loading architecture decisions...
[architecture.md contents - ~150 tokens]

✅ Ready. Use /lite-project-status to see project health.

---

User: "Plan the recipe sharing feature"

Claude (via shipkit-master-lite):
• Routing to: /lite-plan
• Loading context:
  - .shipkit-lite/specs/active/recipe-sharing.md
  - .shipkit-lite/stack.md (already loaded)
  - .shipkit-lite/architecture.md (already loaded)
• [plan-lite executes]

✅ Plan created: .shipkit-lite/plans/recipe-sharing-plan.md

Next: /lite-implement to start coding
```

### Session 3: Stale Context

```
[Session starts - hook runs]

🚀 Shipkit Lite Session Starting...

⚠️  Stack may be stale. Run /lite-project-context to refresh.
    (stack.md is older than package.json)

✅ Ready.

---

User: "Refresh context"

Claude (via shipkit-master-lite):
• Routing to: /lite-project-context
• [Regenerates stack.md with updated dependencies]

✅ Context refreshed

Next: Continue your work
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

---

## Common Patterns

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

## Token Budget Summary

**Session start:**
- Hook messages: ~50 tokens
- shipkit-master-lite SKILL.md: ~200 tokens
- stack.md (if fresh): ~100 tokens
- architecture.md (if exists): ~150 tokens
- **Total: ~500 tokens**

**Per skill invocation:**
- Skill SKILL.md: ~200 tokens
- Context files: ~1000-2000 tokens
- **Total: ~1200-2200 tokens**

**Compared to loading everything upfront:**
- All skills loaded: ~3000 tokens
- All context loaded: ~4000 tokens
- **Total upfront: ~7000 tokens**

**Savings: 85-90% token reduction at session start**

---

**Remember:** shipkit-master-lite is the traffic controller. It routes efficiently, loads lazily, and keeps the workflow moving. Every session starts here. Every request flows through here.
