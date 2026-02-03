---
name: shipkit-detect
description: Unified detection skill that scans artifacts after skill completion and creates work queues for follow-up skills. System skill - auto-triggered by router hook, not user-invocable.
---

# shipkit-detect - Automatic Detection & Queue Creation

**Purpose**: Scan artifacts created by parent skills, detect patterns, and create work queues for follow-up skills.

**Type**: System skill (auto-triggered by router hook)

**Trigger**: After parent skill writes to `.shipkit/.last-skill`

---

## How It Works

```
Parent Skill Completes
        ↓
Writes to .last-skill
        ↓
Router Hook Reads .last-skill
        ↓
Calls: shipkit-detect --mode={mapped-mode}
        ↓
Detection Runs → Queue Created
        ↓
Follow-up skill can process queue
```

---

## Detection Modes

| Mode | Triggered After | What It Scans | Queue Created | For Skill |
|------|-----------------|---------------|---------------|-----------|
| `services` | shipkit-spec | Spec for external services (Stripe, Supabase, etc.) | `fetch-integration-docs.md` | shipkit-integration-docs |
| `contracts` | shipkit-plan | Plan for data structures (types, interfaces, schemas) | `define-data-contracts.md` | shipkit-data-contracts |
| `changes` | (after implementation) | Recently modified components/routes | `components-to-document.md`, `routes-to-document.md` | (documentation - natural capability) |
| `ux-gaps` | shipkit-verify | Interactive components needing UX review | `ux-audit-needed.md` | shipkit-ux-audit |

---

## Mode: `services`

**Scans for external service mentions in specs.**

**Services detected:**
- Payment: Lemon Squeezy, Stripe, Paddle
- Database: Supabase, PlanetScale, Prisma
- AI: OpenAI, Anthropic, Replicate
- Storage: S3, Cloudflare R2, Uploadthing
- Email: Resend, SendGrid, Postmark
- Auth: Clerk, Auth0, NextAuth

**Creates:** `.shipkit/.queues/fetch-integration-docs.md`

**Queue format:**
```markdown
# Integration Docs Needed

## Pending
- [ ] Supabase
  - Mentioned in: specs/active/auth-flow.md
  - Keywords: supabase, auth, rls
  - Need: Current auth patterns, RLS examples
```

---

## Mode: `contracts`

**Scans for data structure definitions in plans.**

**Patterns detected:**
- TypeScript: `type X`, `interface X`
- Database: `CREATE TABLE`, schema definitions
- API: `POST /api/x`, `GET /api/x`
- Common entities: User, Post, Product, Order

**Creates:** `.shipkit/.queues/define-data-contracts.md`

**Queue format:**
```markdown
# Data Contracts To Define

## Pending
- [ ] User
  - Mentioned in: plans/auth-implementation.md
  - Layers: Database → API → Frontend
  - Need: Consistent shape across all layers
```

---

## Mode: `changes`

**Scans for recently modified files after implementation.**

**File patterns:**
- Components: `src/components/**/*.tsx`
- Routes: `src/app/**/route.ts`, `src/api/**/*.ts`
- Hooks: `src/hooks/**/*.ts`

**Time window:** Files modified in last 60 minutes

**Creates:**
- `.shipkit/.queues/components-to-document.md`
- `.shipkit/.queues/routes-to-document.md`

---

## Mode: `ux-gaps`

**Scans for interactive components needing UX review.**

**Patterns detected:**
- Forms with submit handlers
- Buttons with async actions
- Data fetching with loading states
- File upload components

**Threshold:** 3+ interactive components triggers audit

**Creates:** `.shipkit/.queues/ux-audit-needed.md`

---

## Invocation

**Via router hook (automatic):**
```bash
python .claude/skills/shipkit-detect/scripts/detect.py --mode=services
```

**Direct (for testing):**
```bash
python scripts/detect.py --mode=services
python scripts/detect.py --mode=contracts
python scripts/detect.py --mode=changes
python scripts/detect.py --mode=ux-gaps
```

---

## Adding New Detection Modes

To add a new detection type:

1. **Create scan script:** `scripts/scan_{mode}.py`
   ```python
   def scan():
       # Detection logic
       return detected_items

   def create_queue(items):
       # Queue creation logic
       pass
   ```

2. **Register in detect.py:**
   ```python
   MODES = {
       "services": scan_services,
       "contracts": scan_contracts,
       "changes": scan_changes,
       "ux-gaps": scan_ux_gaps,
       "new-mode": scan_new_mode,  # Add here
   }
   ```

3. **Update router mapping:**
   ```python
   # In after-skill-router.py
   TRIGGERS = {
       "shipkit-spec": "services",
       "shipkit-new-skill": "new-mode",  # Add here
   }
   ```

---

## Queue File Location

All queues are created in: `.shipkit/.queues/`

This folder is:
- Processed by follow-up skills when triggered
- Cleaned up when items completed

---

## Context Files This Skill Reads

| Mode | Reads |
|------|-------|
| services | `.shipkit/specs/active/*.md` |
| contracts | `.shipkit/plans/*.md` |
| changes | `src/components/**`, `src/app/**` (file modification times) |
| ux-gaps | `src/components/**` (interactive patterns) |

---

## Context Files This Skill Writes

| Mode | Writes |
|------|--------|
| services | `.shipkit/.queues/fetch-integration-docs.md` |
| contracts | `.shipkit/.queues/define-data-contracts.md` |
| changes | `.shipkit/.queues/components-to-document.md`, `routes-to-document.md` |
| ux-gaps | `.shipkit/.queues/ux-audit-needed.md` |

---

## Exit Codes

- `0` - Success (queue created or nothing to detect)
- `1` - Error (file not found, permissions issue)
- `2` - Invalid mode specified

---

**Remember**: This skill runs automatically. Users never invoke it directly. It's the invisible bridge between creation skills and documentation/verification skills.

---

## Prerequisites

**None - system skill.**

This skill is auto-triggered by the router hook after parent skills complete. Users never invoke it directly.

---

<!-- SECTION:success-criteria -->
## Success Criteria

Detection is complete when:
- [ ] Parent skill's `.last-skill` file read successfully
- [ ] Appropriate detection mode executed based on trigger mapping
- [ ] Relevant artifacts scanned (specs, plans, source files)
- [ ] Queue file created in `.shipkit/.queues/` (if items detected)
- [ ] Exit code returned (0 = success, 1 = error, 2 = invalid mode)
<!-- /SECTION:success-criteria -->

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- Shipkit v1.1.0 -->
