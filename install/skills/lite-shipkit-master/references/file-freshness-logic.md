# File Freshness Checking Logic

Detailed implementation of timestamp-based freshness detection to avoid loading stale context.

---

## Purpose

Avoid loading stale context or wasting tokens regenerating fresh context.

---

## How It Works

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

## Freshness Warning Examples

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

## Token Budget Impact

**Session start with fresh context:**
- Hook messages: ~50 tokens
- shipkit-master-lite SKILL.md: ~200 tokens
- stack.md (cached): ~100 tokens
- architecture.md (cached): ~150 tokens
- **Total: ~500 tokens**

**Session start with stale context:**
- Hook messages: ~50 tokens
- shipkit-master-lite SKILL.md: ~200 tokens
- Freshness check + regeneration: ~1,500 tokens
- **Total: ~1,750 tokens**

**Savings: 71% token reduction by detecting staleness early**
