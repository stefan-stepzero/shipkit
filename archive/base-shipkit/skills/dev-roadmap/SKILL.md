---
name: dev-roadmap
description: "Create sequenced development plan from product user stories. Use after product discovery, before first dev-specify. Analyzes dependencies and sequences specs like a senior engineering manager would."
agent: dev-architect
---

# Development Roadmap

**Create an engineering-driven execution sequence for complex multi-feature projects.**

---

## Overview

Converts product user stories into a sequenced development plan, identifying foundational work and determining optimal spec order based on technical dependencies and execution logic.

**Core principle:** Foundation first, critical path prioritized, tightly coupled features grouped.

**This is NOT project management** - no timelines, no effort estimates, no Gantt charts. Pure technical sequencing.

---

## When to Use

**Triggers:**
- After product discovery complete (user stories exist)
- Before first `/dev-specify` on a greenfield project
- User says: "What order should I build these features?"
- User says: "Plan the development sequence"
- `/dev-roadmap`

**Don't use for:**
- Single feature projects (just run `/dev-specify`)
- Existing projects with established architecture (skip to `/dev-specify`)
- Projects with < 3 user stories (overhead not worth it)

---

## Prerequisites

**Required:**
- User stories (`.shipkit/skills/prod-user-stories/outputs/user-stories.md`)

**Recommended:**
- Technical constitution (`.shipkit/skills/dev-constitution/outputs/constitution.md`)
- Assumptions & risks (`.shipkit/skills/prod-assumptions-and-risks/outputs/assumptions-and-risks.md`)

---

## Process

### Step 1: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/dev-roadmap/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 2: Run Initialization Script

```bash
.shipkit/skills/dev-roadmap/scripts/create-roadmap.sh
```

**Script creates:**
- Output directory: `.shipkit/skills/dev-roadmap/outputs/`
- Empty roadmap.md from template
- Reports paths to Claude

---

### Step 3: Read Context

**Read these to understand the product:**

```bash
# Required
.shipkit/skills/prod-user-stories/outputs/user-stories.md
.shipkit/skills/dev-constitution/outputs/constitution.md

# Recommended (if available)
.shipkit/skills/prod-assumptions-and-risks/outputs/assumptions-and-risks.md
.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md
```

---

### Step 4: Analyze Like an Engineering Manager

**Think through technical execution logic:**

#### 1. Identify Foundation (What enables everything?)

**Ask:**
- "What infrastructure must exist before ANY feature can be built?"
- "What would block all features if missing?"

**Common foundation elements:**
- Database schema and migrations
- Authentication scaffold (middleware, session handling)
- API framework and routing
- Core domain models
- Deployment pipeline and environments
- Logging and monitoring setup

**Create:** Spec 0 or Spec 1 - "Core Infrastructure"

**Example:**
```
Spec 1: Core Infrastructure
Why first: All features depend on auth, database, and API framework
Contains:
  - PostgreSQL setup with migrations
  - JWT auth middleware
  - Express API with routing
  - Base domain models (User, Session)
  - Deployment to staging/prod
  - Error handling and logging
```

---

#### 2. Build Dependency Graph

**For each user story, ask:**
- "Does this story require another story's API/data/UI to work?"
- "Can this be built in parallel with others?"
- "Does this unlock other stories?"

**Common dependency patterns:**
- Dashboard features → require auth
- Reporting → requires data from core features
- Admin panels → require user management
- Notifications → require events from other features

**Document blocking dependencies:**
```
US-003 (Dashboard) depends on US-001 (Auth)
US-010 (Reports) depends on US-003, US-004 (needs their data)
US-015 (Admin) depends on US-001 (auth) and US-003 (user patterns)
```

---

#### 3. Group Tightly Coupled Features

**Ask:**
- "Which user stories share the same domain?"
- "Which stories would cause constant context switching if separated?"
- "Which stories share 80%+ of their code?"

**Grouping criteria:**
- Same database tables
- Same API endpoints
- Same UI screens/components
- Same technical risk area

**Example groupings:**
```
Group A: Auth stories (US-001, US-002) → Spec 2
Group B: Dashboard stories (US-003, US-004, US-005) → Spec 3
Group C: Reporting stories (US-010, US-011) → Spec 4
```

---

#### 4. Sequence by Engineering Logic

**Ordering principles (in priority order):**

**a) Foundation always first**
- Database, auth, API framework
- Nothing else can proceed without it

**b) Riskiest/most uncertain next**
- Unknown technical territory? Do it early.
- External API integration? Validate it works ASAP.
- New tech stack? Prove it out before building on it.
- **Reason:** Fail fast. Learn what you don't know.

**c) Critical path before parallel work**
- Blocking dependencies first
- Things that unlock other work
- **Reason:** Unblock maximum future work.

**d) Tightly coupled together**
- Keep related features in adjacent specs
- **Reason:** Minimize context switching.

**e) Independent work can be sequenced flexibly**
- No dependencies? Consider priority, risk, or user value.
- **Reason:** Flexibility for future parallel work.

**Example sequence:**
```
Spec 1: Core Infrastructure (foundation - enables all)
Spec 2: Auth (US-001, US-002) (blocks 60% of features)
Spec 3: Dashboard (US-003, US-004, US-005) (core value, tightly coupled)
Spec 4: External API Integration (US-007) (risky - validate early)
Spec 5: Reporting (US-010, US-011) (independent, can be parallel)
Spec 6: Admin Panel (US-015, US-016) (uses patterns from Spec 3)
```

---

### Step 5: Write the Roadmap

**Output to:**
```
.shipkit/skills/dev-roadmap/outputs/roadmap.md
```

**Format:**
```markdown
# Development Roadmap

## Foundation

### Spec 1: Core Infrastructure
**Why first:** All features depend on database, auth scaffold, API framework

**Contains:**
- PostgreSQL database with migrations
- JWT authentication middleware
- Express.js API routing framework
- User and Session models
- Deployment pipeline (staging + production)
- Error handling and logging

**Dependencies:** None (foundation)

---

## Feature Sequence

### Spec 2: User Authentication (US-001, US-002)
**Why next:** Blocks 60% of other features (dashboard, profile, admin)

**Contains:**
- User signup and login flows
- Session management
- Password reset
- Profile management

**Dependencies:** Spec 1

---

### Spec 3: User Dashboard (US-003, US-004, US-005)
**Why next:** Core user value, tightly coupled features

**Contains:**
- Dashboard UI layout
- Data display widgets
- Basic user actions (create, update, delete)
- Real-time updates

**Dependencies:** Spec 1, Spec 2

---

### Spec 4: External Payment Integration (US-007)
**Why next:** High technical risk - validate early before building dependent features

**Contains:**
- Lemon Squeezy integration
- Payment flow
- Webhook handling
- Transaction history

**Dependencies:** Spec 1, Spec 2

---

### Spec 5: Reporting (US-010, US-011)
**Why next:** Independent of other features, validates data layer

**Contains:**
- Report generation engine
- Export to PDF/CSV
- Scheduled reports
- Report templates

**Dependencies:** Spec 1, Spec 2

---

### Spec 6: Admin Panel (US-015, US-016)
**Why next:** Uses UI patterns established in Spec 3

**Contains:**
- User management (CRUD)
- System settings
- Audit logs
- Role management

**Dependencies:** Spec 1, Spec 2, Spec 3 (for UI patterns)

---

## Total: 6 Specs

Progress tracking: Use /dev-progress after each spec completes
```

---

### Step 6: Review with User

**Present the roadmap and ask:**
- "Does this sequence make engineering sense?"
- "Any dependencies I missed?"
- "Any stories that should be grouped differently?"

**Refine based on feedback.**

---

## What This Enables

**After roadmap exists:**

1. **Clear execution path**
   - "Build Spec 1, then 2, then 3..."
   - No guessing what to spec next

2. **Dependency awareness**
   - Know what blocks what
   - Avoid building things in wrong order

3. **Progress tracking**
   - `/dev-progress` tracks completion through roadmap
   - Know how far through the plan you are

4. **Team coordination** (future)
   - Specs 5 and 6 could be parallel
   - Roadmap shows which specs are independent

---

## Next Steps

**After roadmap created:**

```bash
# Start with Spec 1 (foundation)
/dev-specify "Core Infrastructure: database, auth scaffold, API framework"
/dev-plan
/dev-tasks
/dev-implement
/dev-finish
  → auto-calls /dev-progress (updates tracking)

# Then Spec 2 (next in roadmap)
/dev-specify "User Authentication (US-001, US-002)"
... continue through roadmap
```

---

## Constraints

**DO:**
- ✅ Identify foundation (infrastructure that enables all features)
- ✅ Analyze technical dependencies (what blocks what)
- ✅ Group tightly coupled features (same domain/tables/code)
- ✅ Sequence by engineering logic (foundation → risky → critical path)
- ✅ Document "why" for each sequence decision

**DON'T:**
- ❌ Estimate effort or timelines (not project management)
- ❌ Assign work to people (not resource planning)
- ❌ Create Gantt charts or burndowns (not scheduling)
- ❌ Optimize for "business priority" alone (technical logic first)
- ❌ Ignore technical dependencies for business reasons

---

## Red Flags

**Stop if you see:**
- Specs that depend on future specs (circular dependency)
- Foundation work spread across multiple specs (should be Spec 1)
- Single user story split across specs (keep together)
- Roadmap organized by "priority" ignoring dependencies (wrong)
- Timeline or effort estimates added (out of scope)

---

## Example: E-commerce Platform

**User stories (summary):**
- US-001: User registration/login
- US-002: Product catalog
- US-003: Shopping cart
- US-004: Checkout flow
- US-005: Payment processing (Lemon Squeezy)
- US-006: Order history
- US-007: Product search
- US-008: Admin product management
- US-009: Email notifications
- US-010: Analytics dashboard

**Roadmap:**
```
Spec 1: Core Infrastructure (DB, auth scaffold, API, email service)
Spec 2: User Auth (US-001) - blocks everything
Spec 3: Product Catalog + Search (US-002, US-007) - tightly coupled
Spec 4: Shopping Cart + Checkout (US-003, US-004) - tightly coupled
Spec 5: Payment Integration (US-005) - risky, validate early
Spec 6: Order History (US-006) - needs Spec 4, Spec 5
Spec 7: Email Notifications (US-009) - independent, can be parallel
Spec 8: Admin Panel (US-008) - uses patterns from Spec 3
Spec 9: Analytics Dashboard (US-010) - needs all data, goes last
```

**Why this sequence:**
- Spec 1: Foundation enables everything
- Spec 2: Auth blocks all user features
- Spec 3: Core value (browse products)
- Spec 4: Purchase flow (tightly coupled to cart)
- Spec 5: Payment is risky - validate before building dependencies
- Spec 6: Requires Spec 4 + 5 to work
- Spec 7: Independent, could be parallel with Spec 6
- Spec 8: Reuses UI patterns from Spec 3
- Spec 9: Needs data from all features, naturally goes last

---

## Quick Reference

| Step | Action | Output |
|------|--------|--------|
| 1. Foundation | Identify infrastructure that enables all features | Spec 1: Core Infrastructure |
| 2. Dependencies | Build dependency graph (what blocks what) | Documented blocking relationships |
| 3. Grouping | Group tightly coupled features | Batched user stories into specs |
| 4. Sequencing | Order by: foundation → risky → critical path → independent | Numbered spec sequence with "why" |
| 5. Document | Write roadmap.md with sequence + rationale | `.shipkit/skills/dev-roadmap/outputs/roadmap.md` |

---

## Success Criteria

A good roadmap has:

1. ✅ Clear foundation spec (Spec 1)
2. ✅ No circular dependencies (A needs B needs A)
3. ✅ Tightly coupled features grouped together
4. ✅ "Why next" rationale for each spec
5. ✅ Dependencies explicitly listed
6. ✅ 3-10 specs (not too granular, not too coarse)
7. ✅ Pure engineering logic (no PM fluff)

---

## Integration with Other Skills

**Called after:**
- `/prod-user-stories` - Provides the features to sequence

**Calls before starting:**
- None (reads existing artifacts)

**Enables:**
- `/dev-specify` - Know which spec to create first
- `/dev-progress` - Track execution through roadmap

**Typical flow:**
```
/prod-user-stories
  → user-stories.md created
/dev-constitution
  → constitution.md created
/dev-roadmap
  → roadmap.md created (sequence of 6 specs)
/dev-specify "Spec 1: Core Infrastructure"
  ... (through pipeline)
/dev-finish
  → auto-calls /dev-progress
  → "1/6 complete. Next: Spec 2"
```
