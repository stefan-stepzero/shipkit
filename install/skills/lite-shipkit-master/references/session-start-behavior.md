# Session Start Behavior

Detailed hook implementation and token budget for session initialization.

---

## Hook Execution

**`.claude/hooks/session-start.sh` implementation:**

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

---

## What Gets Loaded at Session Start

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

## Progressive Disclosure Strategy

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

## Example Session Flows

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

## Token Budget Comparison

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
