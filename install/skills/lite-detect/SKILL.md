---
name: lite-detect
description: Unified detection skill that scans artifacts after skill completion and creates work queues for follow-up skills. System skill - auto-triggered by router hook, not user-invocable.
---

# lite-detect - Automatic Detection & Queue Creation

**Purpose**: Scan artifacts created by parent skills, detect patterns, and create work queues for follow-up skills.

**Type**: System skill (auto-triggered by router hook)

**Trigger**: After parent skill writes to `.shipkit-lite/.last-skill`

---

## How It Works

```
Parent Skill Completes
        ↓
Writes to .last-skill
        ↓
Router Hook Reads .last-skill
        ↓
Calls: lite-detect --mode={mapped-mode}
        ↓
Detection Runs → Queue Created
        ↓
Follow-up skill can process queue
```

---

## Detection Modes

| Mode | Triggered After | What It Scans | Queue Created | For Skill |
|------|-----------------|---------------|---------------|-----------|
| `services` | lite-spec | Spec for external services (Stripe, Supabase, etc.) | `fetch-integration-docs.md` | lite-integration-docs |
| `contracts` | lite-plan | Plan for data structures (types, interfaces, schemas) | `define-data-contracts.md` | lite-data-contracts |
| `changes` | lite-implement | Recently modified components/routes | `components-to-document.md`, `routes-to-document.md` | lite-component-knowledge, lite-route-knowledge |
| `ux-gaps` | lite-quality-confidence | Interactive components needing UX review | `ux-audit-needed.md` | lite-ux-audit |

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

**Creates:** `.shipkit-lite/.queues/fetch-integration-docs.md`

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

**Creates:** `.shipkit-lite/.queues/define-data-contracts.md`

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
- `.shipkit-lite/.queues/components-to-document.md`
- `.shipkit-lite/.queues/routes-to-document.md`

---

## Mode: `ux-gaps`

**Scans for interactive components needing UX review.**

**Patterns detected:**
- Forms with submit handlers
- Buttons with async actions
- Data fetching with loading states
- File upload components

**Threshold:** 3+ interactive components triggers audit

**Creates:** `.shipkit-lite/.queues/ux-audit-needed.md`

---

## Invocation

**Via router hook (automatic):**
```bash
python .claude/skills/lite-detect/scripts/detect.py --mode=services
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
       "lite-spec": "services",
       "lite-new-skill": "new-mode",  # Add here
   }
   ```

---

## Queue File Location

All queues are created in: `.shipkit-lite/.queues/`

This folder is:
- Scanned by lite-whats-next for suggestions
- Processed by follow-up skills
- Cleaned up when items completed

---

## Context Files This Skill Reads

| Mode | Reads |
|------|-------|
| services | `.shipkit-lite/specs/active/*.md` |
| contracts | `.shipkit-lite/plans/*.md` |
| changes | `src/components/**`, `src/app/**` (file modification times) |
| ux-gaps | `src/components/**` (interactive patterns) |

---

## Context Files This Skill Writes

| Mode | Writes |
|------|--------|
| services | `.shipkit-lite/.queues/fetch-integration-docs.md` |
| contracts | `.shipkit-lite/.queues/define-data-contracts.md` |
| changes | `.shipkit-lite/.queues/components-to-document.md`, `routes-to-document.md` |
| ux-gaps | `.shipkit-lite/.queues/ux-audit-needed.md` |

---

## Exit Codes

- `0` - Success (queue created or nothing to detect)
- `1` - Error (file not found, permissions issue)
- `2` - Invalid mode specified

---

**Remember**: This skill runs automatically. Users never invoke it directly. It's the invisible bridge between creation skills and documentation/verification skills.
