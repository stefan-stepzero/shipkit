# Example Status Outputs

Complete examples of status reports for different project states.

---

## Scenario 1: Healthy Project

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✓ Stack: documented (Next.js 14, Supabase, Tailwind)
  → Last updated: 3 hours ago

✓ Architecture: 8 decisions logged
  → Last updated: 1 day ago

✓ Implementations: 15 components documented
  → All large files documented

✓ Progress: 12 sessions logged
  → Last session: 2 hours ago

════════════════════════════════════════════════════

WORKFLOW STATUS

✓ Specs: 1 active (user-profile.md)
✓ Plans: 1 plan exists (user-profile-plan.md)
✓ Implementations: 3 components implemented
✓ User Tasks: 8 active, 12 completed

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

✓ Project is healthy!

Next: Continue implementing user-profile feature
      Run /lite-implement to continue coding

════════════════════════════════════════════════════
```

---

## Scenario 2: Stale Stack

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

⚠ Stack: outdated
  → Last updated: 5 days ago
  → package.json modified today (new dependencies added)
  → Run /lite-project-context to refresh

✓ Architecture: 3 decisions logged
✓ Implementations: 7 components documented
✓ Progress: 4 sessions logged

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Priority 1: Run /lite-project-context (stack is stale)

════════════════════════════════════════════════════
```

---

## Scenario 3: Workflow Gap

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✓ Stack: documented (Next.js 14, Supabase)
✓ Architecture: 6 decisions logged
⚠ Implementations: 10 components documented
  → 3 undocumented files >200 LOC
✓ Progress: 6 sessions logged

════════════════════════════════════════════════════

WORKFLOW STATUS

✓ Specs: 3 active
  • recipe-sharing.md
  • user-profile.md
  • notification-system.md

✗ Plans: 0 plans found
  → Specs exist but no implementation plans

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Priority 1: Run /lite-plan for recipe-sharing spec
Priority 2: After planning, run /lite-implement
Priority 3: Document large components with /lite-component-knowledge

════════════════════════════════════════════════════
```

---

## Scenario 4: Fresh Project

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✗ Directory not found: .shipkit-lite/

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Initialize project context:
→ Run /lite-project-context to scan codebase and generate:
  • stack.md (from package.json)
  • schema.md (from migrations)
  • Initial context files

════════════════════════════════════════════════════
```
