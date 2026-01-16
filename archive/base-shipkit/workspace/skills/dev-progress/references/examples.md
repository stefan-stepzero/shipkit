# Development Progress Examples

**Purpose:** Example progress documents at different stages of a project

**When to reference:** When creating progress.md and need formatting guidance

---

## Table of Contents

1. [Early Stage (1/9 complete)](#example-1-early-stage)
2. [Mid-Project (4/9 complete)](#example-2-mid-project)
3. [Late Stage (7/9 complete)](#example-3-late-stage)
4. [Out-of-Order Execution](#example-4-out-of-order-execution)
5. [Multiple Specs in Progress](#example-5-multiple-specs-in-progress)

---

## Example 1: Early Stage

**Project:** E-commerce Platform
**Stage:** Just completed first spec (infrastructure)

```markdown
# Development Progress

**Last Updated:** 2025-12-15 16:30
**Overall:** 1/9 specs complete (11%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-15
- Location: specs/001-core-infrastructure/
- Branch: feature/001-core-infrastructure (merged to main)
- Contains:
  - PostgreSQL database + migrations
  - JWT authentication scaffold
  - Express.js API framework
  - Email service (SendGrid)
  - Deployment pipeline (staging + production)

---

## Current 🔄

_No spec in progress yet_

---

## Next Up 📋

### Spec 2: User Authentication (US-001)
**From roadmap:** Blocks 80% of other features
**User Stories:** US-001
**Dependencies:** Spec 1 ✅
**Why next:** All user-facing features require auth

### Spec 3: Product Catalog + Search (US-002, US-007)
**From roadmap:** Core value, tightly coupled
**User Stories:** US-002, US-007
**Dependencies:** Spec 1 ✅, Spec 2 ⏳

### Spec 4: Shopping Cart + Checkout (US-003, US-004)
**From roadmap:** Purchase flow tightly coupled
**User Stories:** US-003, US-004
**Dependencies:** Spec 1 ✅, Spec 2 ⏳, Spec 3 ⏳

### Spec 5: Payment Integration (US-005)
**From roadmap:** High risk - validate early
**User Stories:** US-005
**Dependencies:** Spec 1 ✅, Spec 2 ⏳, Spec 4 ⏳

### Spec 6: Order History (US-006)
**From roadmap:** Depends on purchase flow
**User Stories:** US-006
**Dependencies:** Spec 1 ✅, Spec 2 ⏳, Spec 4 ⏳, Spec 5 ⏳

### Spec 7: Email Notifications (US-009)
**From roadmap:** Independent, can be parallel
**User Stories:** US-009
**Dependencies:** Spec 1 ✅, Spec 2 ⏳

### Spec 8: Admin Product Management (US-008)
**From roadmap:** Uses UI patterns from Spec 3
**User Stories:** US-008
**Dependencies:** Spec 1 ✅, Spec 2 ⏳, Spec 3 ⏳

### Spec 9: Analytics Dashboard (US-010)
**From roadmap:** Needs all data, goes last
**User Stories:** US-010
**Dependencies:** All previous specs

---

## Summary

- **Completed:** 1 spec
- **In Progress:** 0 specs
- **Remaining:** 8 specs
- **Total:** 9 specs
- **Progress:** 11%

---

## Next Action

**Start Spec 2:**
```bash
/dev-specify "User Authentication (US-001)"
```

**What Spec 2 unlocks:**
- All user-facing features (Specs 3-9)
- 80% of roadmap becomes buildable
- Critical path unblocked

**Expected timeline:**
- Spec 2 completes → 22% progress
- Spec 3 completes → 33% progress
- Spec 4 completes → 44% progress
```

**Key features:**
- Shows zero in-progress (between specs)
- Lists all remaining specs from roadmap
- Marks dependencies with ✅ (done) or ⏳ (waiting)
- Explains "why next" for immediate next spec
- Shows what completing next spec unlocks

---

## Example 2: Mid-Project

**Project:** E-commerce Platform
**Stage:** Halfway through, working on checkout

```markdown
# Development Progress

**Last Updated:** 2025-12-20 14:15
**Overall:** 4/9 specs complete (44%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-10
- Location: specs/001-core-infrastructure/
- Branch: feature/001-core-infrastructure (merged to main)

### Spec 2: User Authentication
- ✅ Merged: 2025-12-12
- Location: specs/002-user-authentication/
- Branch: feature/002-user-auth (merged to main)

### Spec 3: Product Catalog + Search
- ✅ Merged: 2025-12-15
- Location: specs/003-product-catalog-search/
- Branch: feature/003-catalog (merged to main)

### Spec 4: Shopping Cart + Checkout
- ✅ Merged: 2025-12-20 (today!)
- Location: specs/004-cart-checkout/
- Branch: feature/004-cart (merged to main)

---

## Current 🔄

_No spec in progress yet_

---

## Next Up 📋

### Spec 5: Payment Integration (US-005) ← START HERE
**From roadmap:** High risk - validate early
**User Stories:** US-005
**Dependencies:** Spec 1 ✅, Spec 2 ✅, Spec 4 ✅
**Why next:** All dependencies complete, highest risk remaining
**Unlocks:** Spec 6 (Order History)

### Spec 6: Order History (US-006)
**From roadmap:** Depends on purchase flow
**User Stories:** US-006
**Dependencies:** Spec 1 ✅, Spec 2 ✅, Spec 4 ✅, Spec 5 ⏳

### Spec 7: Email Notifications (US-009)
**From roadmap:** Independent, can be parallel
**User Stories:** US-009
**Dependencies:** Spec 1 ✅, Spec 2 ✅
**Note:** Could be built in parallel with Spec 5/6

### Spec 8: Admin Product Management (US-008)
**From roadmap:** Uses UI patterns from Spec 3
**User Stories:** US-008
**Dependencies:** Spec 1 ✅, Spec 2 ✅, Spec 3 ✅

### Spec 9: Analytics Dashboard (US-010)
**From roadmap:** Needs all data, goes last
**User Stories:** US-010
**Dependencies:** All previous specs

---

## Summary

- **Completed:** 4 specs
- **In Progress:** 0 specs
- **Remaining:** 5 specs
- **Total:** 9 specs
- **Progress:** 44%

---

## Velocity

- Spec 1: 3 days (Dec 7-10) [Infrastructure setup]
- Spec 2: 2 days (Dec 11-12) [Auth]
- Spec 3: 3 days (Dec 13-15) [Catalog + Search]
- Spec 4: 5 days (Dec 16-20) [Cart + Checkout]

**Note:** Velocity shown for context, not used for estimates

---

## Next Action

**Start Spec 5:**
```bash
/dev-specify "Payment Integration (US-005)"
```

**Critical:** Payment integration has external dependencies (Stripe)
- Validate API access
- Test webhook delivery
- Verify PCI compliance requirements
- Plan for failure scenarios

**After Spec 5 completes (56% progress):**
- Spec 6 (Order History) becomes buildable
- Specs 7 and 8 could be built in parallel (both dependencies met)
```

**Key features:**
- Shows multiple completed specs with dates
- Velocity section (informational only)
- Notes about parallel opportunities
- Flags high-risk next spec (payment)
- Shows percentage progress

---

## Example 3: Late Stage

**Project:** E-commerce Platform
**Stage:** Nearly done, working on analytics

```markdown
# Development Progress

**Last Updated:** 2025-12-28 10:45
**Overall:** 7/9 specs complete (78%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-10

### Spec 2: User Authentication
- ✅ Merged: 2025-12-12

### Spec 3: Product Catalog + Search
- ✅ Merged: 2025-12-15

### Spec 4: Shopping Cart + Checkout
- ✅ Merged: 2025-12-20

### Spec 5: Payment Integration
- ✅ Merged: 2025-12-22

### Spec 6: Order History
- ✅ Merged: 2025-12-23

### Spec 7: Email Notifications
- ✅ Merged: 2025-12-26

---

## Current 🔄

### Spec 8: Admin Product Management
- 🔄 Status: In development
- Location: specs/008-admin-product-management/
- Branch: feature/008-admin (active)
- Started: 2025-12-27
- Blocked by: None
- Progress indicators:
  - Spec created ✓
  - Plan created ✓
  - Tasks created ✓
  - Implementation: 60% (12/20 tasks complete)

---

## Next Up 📋

### Spec 9: Analytics Dashboard (US-010) ← FINAL SPEC
**From roadmap:** Needs all data, goes last
**User Stories:** US-010
**Dependencies:** All previous specs (8/9 complete ✅)
**After this:** Project roadmap complete! 🎉

---

## Summary

- **Completed:** 7 specs
- **In Progress:** 1 spec
- **Remaining:** 1 spec
- **Total:** 9 specs
- **Progress:** 78%

---

## Next Action

**Continue Spec 8:**
```bash
/dev-implement  # Continue working through tasks
```

**When Spec 8 done:**
```bash
/dev-specify "Analytics Dashboard (US-010)"
```

**🎯 Milestone:** After Spec 9, full roadmap complete!
```

**Key features:**
- Collapsed completed specs (less detail)
- Shows in-progress spec with task completion (60%)
- Final spec highlighted
- Milestone callout (roadmap completion)

---

## Example 4: Out-of-Order Execution

**Project:** E-commerce Platform
**Stage:** Built Spec 4 before Spec 3 (diverged from roadmap)

```markdown
# Development Progress

**Last Updated:** 2025-12-18 09:20
**Overall:** 3/9 specs complete (33%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-10

### Spec 2: User Authentication
- ✅ Merged: 2025-12-12

### Spec 4: Shopping Cart + Checkout ⚠️
- ✅ Merged: 2025-12-18
- **Note:** Completed before Spec 3 (out of roadmap order)
- **Impact:** Spec 4 mocks product data (Spec 3 not built yet)
- **TODO:** Integrate with real catalog when Spec 3 completes

---

## Current 🔄

_No spec in progress yet_

---

## Next Up 📋

### Spec 3: Product Catalog + Search (US-002, US-007) ← PRIORITY
**From roadmap:** Should have been before Spec 4
**User Stories:** US-002, US-007
**Dependencies:** Spec 1 ✅, Spec 2 ✅
**Why priority:** Spec 4 uses mocked product data, needs integration

### Spec 5: Payment Integration (US-005)
**From roadmap:** High risk - validate early
**User Stories:** US-005
**Dependencies:** Spec 1 ✅, Spec 2 ✅, Spec 4 ✅

[... remaining specs ...]

---

## Summary

- **Completed:** 3 specs (1 out of order)
- **In Progress:** 0 specs
- **Remaining:** 6 specs
- **Total:** 9 specs
- **Progress:** 33%

---

## Roadmap Divergence

**Original roadmap order:** 1 → 2 → 3 → 4 → 5 → ...
**Actual execution order:** 1 → 2 → 4 → [3 next] → ...

**Reason:** Business priority changed, needed checkout flow first

**Technical debt created:**
- Spec 4 uses mocked product data
- Integration work required when Spec 3 complete

---

## Next Action

**Build Spec 3 (priority):**
```bash
/dev-specify "Product Catalog + Search (US-002, US-007)"
```

**After Spec 3:**
- Integrate with Spec 4 (replace mocks with real catalog)
- Verify checkout flow with real product data
```

**Key features:**
- Flags out-of-order execution with ⚠️
- Explains reason for divergence
- Documents technical debt created
- Prioritizes getting back on track
- Shows impact on other specs

---

## Example 5: Multiple Specs in Progress

**Project:** E-commerce Platform
**Stage:** Two specs being built in parallel

```markdown
# Development Progress

**Last Updated:** 2025-12-21 15:00
**Overall:** 5/9 specs complete (56%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-10

### Spec 2: User Authentication
- ✅ Merged: 2025-12-12

### Spec 3: Product Catalog + Search
- ✅ Merged: 2025-12-15

### Spec 4: Shopping Cart + Checkout
- ✅ Merged: 2025-12-20

### Spec 5: Payment Integration
- ✅ Merged: 2025-12-21

---

## Current 🔄

### Spec 6: Order History (US-006)
- 🔄 Status: In development
- Location: specs/006-order-history/
- Branch: feature/006-orders (active)
- Started: 2025-12-21 (morning)
- Assignee: Team Member A
- Progress: 30% (6/20 tasks complete)

### Spec 7: Email Notifications (US-009)
- 🔄 Status: In development
- Location: specs/007-email-notifications/
- Branch: feature/007-emails (active)
- Started: 2025-12-21 (afternoon)
- Assignee: Team Member B
- Progress: 15% (3/20 tasks complete)
- **Note:** Independent of Spec 6, building in parallel

---

## Next Up 📋

### Spec 8: Admin Product Management (US-008)
**From roadmap:** Uses UI patterns from Spec 3
**User Stories:** US-008
**Dependencies:** Spec 1 ✅, Spec 2 ✅, Spec 3 ✅

### Spec 9: Analytics Dashboard (US-010)
**From roadmap:** Needs all data, goes last
**User Stories:** US-010
**Dependencies:** All previous specs (5/9 complete ✅)

---

## Summary

- **Completed:** 5 specs
- **In Progress:** 2 specs (parallel execution)
- **Remaining:** 2 specs
- **Total:** 9 specs
- **Progress:** 56%

---

## Parallel Execution Notes

**Why parallel:**
- Spec 6 and Spec 7 have no interdependencies
- Both only depend on Specs 1-5 (all complete)
- Team has capacity for parallel work

**Coordination:**
- Daily sync between Team Member A and B
- Merge Spec 6 first (started earlier)
- Merge Spec 7 after (reduce merge conflicts)

---

## Next Action

**Team Member A:**
```bash
/dev-implement  # Continue Spec 6 tasks
```

**Team Member B:**
```bash
/dev-implement  # Continue Spec 7 tasks
```

**When both complete:**
```bash
/dev-specify "Admin Product Management (US-008)"
```

**Progress projection:**
- When Spec 6 merges: 67% complete
- When Spec 7 merges: 78% complete
```

**Key features:**
- Lists multiple in-progress specs
- Shows assignees (team coordination)
- Shows task completion percentage per spec
- Explains why parallel execution is safe
- Coordination notes (merge order)

---

## Progress Document Best Practices

### 1. Keep it Current
- Update after every merge
- Auto-updated by /dev-finish is ideal

### 2. Show Context
- Merge dates for completed specs
- Task progress for in-progress specs
- Dependencies for upcoming specs

### 3. Flag Issues
- Out-of-order execution
- Technical debt created
- Blocked specs

### 4. Suggest Next Action
- Always tell user what to do next
- Specific command to run
- Context about why

### 5. Celebrate Milestones
- 50% complete
- Final spec started
- Roadmap complete

### 6. Keep History Light
- Don't need full spec details for completed specs
- Keep recent 2-3 specs verbose, older specs compact

---

## Common Patterns

### After Merge (between specs)
```markdown
## Current 🔄
_No spec in progress yet_

## Next Up 📋
### Spec N: [Next feature]
← START HERE
```

### During Development
```markdown
## Current 🔄
### Spec N: [Feature name]
- 🔄 Status: In development
- Progress: X% (Y/Z tasks complete)
```

### Project Complete
```markdown
## Summary
- **Progress:** 100% 🎉
- **Roadmap complete!**

## Next Steps
- Launch preparation
- Post-launch monitoring
- Feature refinement
```

---

## Using These Examples

1. **Match your stage** - Early, mid, late, or special case
2. **Copy structure** - Use sections: Completed, Current, Next Up, Summary
3. **Adapt details** - Add your project specifics
4. **Keep concise** - User wants quick status, not full history
5. **Actionable** - Always end with "What to do next"

**Remember:** Progress document is a living document. It should always reflect current state and guide next action.
