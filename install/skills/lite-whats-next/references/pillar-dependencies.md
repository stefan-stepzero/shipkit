# Pillar Dependency Rules

## Strict Dependencies (Warn if Violated)

**lite-plan requires spec exists:**
```
⚠️  No spec found for this plan.
    Recommend: /lite-spec first
    Or: Proceed with plan based on description only
```

**lite-component-knowledge requires source code exists:**
```
❌ No components to document yet.
    Must implement first: /lite-implement
```

**lite-route-knowledge requires source code exists:**
```
❌ No routes to document yet.
    Must implement first: /lite-implement
```

---

## Recommended Dependencies (Suggest but Allow)

**lite-spec recommends why.md exists:**
```
⚠️  No vision defined (why.md missing).
    Recommend: /lite-why-project first for strategic context
    Or: Proceed with spec anyway
```

**lite-implement recommends plan exists:**
```
⚠️  No plan found for this spec.
    Recommend: /lite-plan first to break work into tasks
    Or: Proceed with implementation from spec only
```

**lite-architecture-memory recommends why.md exists:**
```
⚠️  No vision defined (why.md missing).
    Decisions align better with strategic context.
    Suggest: /lite-why-project first
```

**lite-ux-coherence recommends implementations.md exists:**
```
⚠️  No components documented yet.
    UX check works best with documented components.
    Suggest: /lite-component-knowledge first
```

---

## No Dependencies (Always Allowed)

**Meta/Infrastructure skills:**
- `/lite-why-project` - Can run anytime (defines vision)
- `/lite-project-context` - Can run anytime (scans current state)
- `/lite-project-status` - Can run anytime (health check)
- `/lite-whats-next` - Can run anytime (workflow guidance)

**Async/Utility skills:**
- `/lite-communications` - Can run anytime (generate reports)
- `/lite-user-instructions` - Can run anytime (track manual tasks)
- `/lite-work-memory` - Can run anytime (log session progress)
- `/lite-debug-systematically` - Can run anytime (troubleshooting)
- `/lite-integration-guardrails` - Can run anytime (service warnings)

**Documentation skills (if content exists):**
- `/lite-document-artifact` - Can run anytime (create standalone docs)
- `/lite-data-consistency` - Can run anytime (type checking)

---

## Dependency Check Algorithm

**When user invokes a skill:**

1. **Check strict dependencies**
   - If missing: Show ERROR, suggest prerequisite
   - User can override with explicit "proceed anyway"

2. **Check recommended dependencies**
   - If missing: Show WARNING, suggest optimal path
   - Allow user to proceed without blocking

3. **No dependencies**
   - Proceed immediately, no checks needed

**Example flow:**
```
User: "Run /lite-plan"

Check: Does spec exist for this feature?
- If YES: Proceed to /lite-plan
- If NO:
  WARN: "No spec found. Recommend /lite-spec first."
  ASK: "Proceed with plan anyway? (y/n)"
  - If y: Proceed to /lite-plan
  - If n: Suggest /lite-spec
```
