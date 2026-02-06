# Bug Prevention Infrastructure Specification

**Created:** 2025-12-30
**Updated:** 2025-12-31 (Phases 2-6 IMPLEMENTED)
**Purpose:** Redesign skill architecture to automatically prevent common vibe coding errors through reference material and milestone-based checks

**STATUS: Phases 2-7 COMPLETE** ✅
- ✅ Phase 2: Queue Infrastructure created (.shipkit/.queues/)
- ✅ Phase 3: 5 Detection skills created and functional
- ✅ Phase 4: Milestone hook implemented (Stop hook chain)
- ✅ Phase 5: Consumer skills updated with queue-reading (Step 0)
- ✅ Phase 6: Session documentation hook added (shipkit-work-memory auto-invoke)
- ✅ Phase 7: shipkit-whats-next queue-awareness (COMPLETE - Step 0 added, priority system implemented)

---

## Key Clarifications

**✅ The 8 Integration Files (Part 1):**
Every skill rename/creation requires updating:
1. SKILL.md frontmatter
2. HTML overview page
3. Claude.md skill list
4. Manifest JSON
5. Hook file (optional)
6. Master routing table
7. Settings permissions
8. shipkit-whats-next mentions (**CRITICAL** for skill discovery)

**✅ Detection Scripts Architecture (Part 3):**
- Detection logic = Skills in `install/skills/` (Option A)
- Marked as "system" skills in manifest (hidden from user)
- Follows best practice: skills can call scripts

**✅ shipkit-whats-next Role (Part 2):**
- Ultimate workflow orchestrator (queue-aware)
- Automatic mode: SessionStop hook invokes it
- Manual mode: User calls when confused about workflow state

---

## Executive Summary

**Current Problem:**
- Bug prevention skills exist but require manual invocation
- Users forget to run them → bugs occur
- No infrastructure for detecting when preventative checks needed
- shipkit-whats-next is too generic (tries to cover all workflow states)

**Proposed Solution:**
- Rename skills to reflect bug-prevention purpose
- Create milestone-specific hooks that trigger at key workflow points
- Implement detection/queue infrastructure for automatic skill triggering
- Generate living reference material that prevents future bugs

---

## Part 1: Skill Renaming Strategy

### Renamed Skills (Better Clarity)

| Current Name | New Name | Why |
|--------------|----------|-----|
| `shipkit-integration-guardrails` | `shipkit-integration-docs` | Fetches CURRENT integration patterns, not just security |
| `shipkit-data-consistency` | `shipkit-data-contracts` | Validates data shape contracts, prevents type mismatches |
| `shipkit-ux-coherence` | `shipkit-ux-audit` | Audits UX best practices (loading states, errors, a11y) |
| `shipkit-component-knowledge` | **Keep as-is** | Name is clear - documents component contracts |
| `shipkit-route-knowledge` | **Keep as-is** | Name is clear - documents API/route contracts |

### The 8 Integration Files (CRITICAL for Every Skill)

When renaming or creating a skill, ALL 8 files must be updated:

**File 1: SKILL.md**
- Location: `install/skills/{skill-name}/SKILL.md`
- Update: YAML frontmatter `name:` field
- Example: `name: shipkit-integration-docs`

**File 2: HTML Overview**
- Location: `help/shipkit-shipkit-overview.html`
- Update: Find skill in milestone section, update `<h4>/shipkit-integration-guardrails</h4>` → `<h4>/shipkit-integration-docs</h4>`
- Update: Skill description text to match new purpose

**File 3: Claude.md Skill List**
- Location: `install/claude-md/shipkit.md`
- Update: Find line like `- \`/shipkit-integration-guardrails\` - Description`
- Change to: `- \`/shipkit-integration-docs\` - Fetch current integration patterns`

**File 4: Manifest Definition**
- Location: `install/profiles/shipkit.manifest.json`
- Update: Find `"shipkit-integration-guardrails"` in `skills.definitions` array
- Change to: `"shipkit-integration-docs"`

**File 5: Hook File (Optional)**
- Location: `install/shared/hooks/suggest-next-skill.py`
- Update: Only if skill has detection logic in hook
- Most skills don't need this updated

**File 6: Master Routing Table**
- Location: `install/skills/shipkit-master/SKILL.md`
- Update: Find routing table entry (markdown table row)
- Change: `| "integration guardrails", "check integration" | \`/shipkit-integration-guardrails\` |`
- To: `| "integration docs", "fetch integration patterns" | \`/shipkit-integration-docs\` |`

**File 7: Settings Permissions**
- Location: `install/settings/shipkit.settings.json`
- Update: Find `"Skill(shipkit-integration-guardrails)"` in `permissions.allow` array
- Change to: `"Skill(shipkit-integration-docs)"`

**File 8: shipkit-whats-next Integration (CRITICAL)**
- Location: `install/skills/shipkit-whats-next/SKILL.md`
- Update: Find all mentions of skill name
- Update: Pillar categorization if skill purpose changed
- Update: Special Relationships section with When/Why/Trigger
- **WHY CRITICAL:** If skill not mentioned here, workflow brain won't suggest it!

### Renaming Checklist (Per Skill)

For each renamed skill, verify all 8 files updated:

- [ ] File 1: SKILL.md frontmatter `name:` updated
- [ ] File 2: HTML overview skill name and description updated
- [ ] File 3: Claude.md skill list entry updated
- [ ] File 4: Manifest JSON array entry updated
- [ ] File 5: Hook file updated (if applicable, usually skip)
- [ ] File 6: Master routing table entry updated
- [ ] File 7: Settings permission string updated
- [ ] File 8: shipkit-whats-next mentions updated

**Implementation:**
1. Rename skill directories: `install/skills/shipkit-integration-guardrails/` → `install/skills/shipkit-integration-docs/`
2. Update all 8 integration files using checklist above
3. Update cross-references in other skills (check "When This Skill Integrates with Others" sections)
4. Test skill invocation: `/shipkit-integration-docs` should work

---

## Part 2: Milestone-Specific Hook Architecture

### Problem with Current shipkit-whats-next

**Current:** One monolithic skill tries to handle all workflow states
- After spec? After plan? After implementation? During implementation?
- Too complex, too many conditionals
- Can't trigger preventative checks at the RIGHT moment

### Proposed: Milestone-Specific Hooks

**Create hidden hook skills that trigger at specific workflow milestones:**

```
POST-SPEC HOOK (shipkit-post-spec-check)
├─ Triggers after: /shipkit-spec completes
├─ Checks: Does spec mention external services?
├─ Creates queue: .queues/fetch-integration-docs.md
└─ Suggests: "Run /shipkit-integration-docs before implementation"

POST-PLAN HOOK (shipkit-post-plan-check)
├─ Triggers after: /shipkit-plan completes
├─ Checks: Does plan define new data structures?
├─ Creates queue: .queues/define-data-contracts.md
└─ Suggests: "Run /shipkit-data-contracts to define types before coding"

POST-IMPLEMENT HOOK (shipkit-post-implement-check)
├─ Triggers after: /shipkit-implement completes
├─ Checks: What was built? Components? Routes? Integrations?
├─ Creates queues:
│   ├─ .queues/components-to-document.md
│   ├─ .queues/routes-to-document.md
│   └─ .queues/integrations-used.md
└─ Suggests: "Document changes to prevent future bugs"

PRE-SHIP HOOK (shipkit-pre-ship-check)
├─ Triggers before: /shipkit-quality-confidence runs
├─ Checks: Missing UX patterns? Undocumented integrations?
├─ Creates queue: .queues/ux-audit-needed.md
└─ Suggests: "Run /shipkit-ux-audit before shipping"
```

### Implementation Strategy

**Option A: SessionStop Hook (Simple)**
```json
// .claude/settings.json
"hooks": {
  "SessionStop": {
    "skill": "shipkit-milestone-detector"
  }
}
```

**Option B: Skill-Level Hooks (Precise)**
Each skill declares its own post-completion hook in SKILL.md:
```yaml
---
name: shipkit-spec
on_completion: shipkit-post-spec-check
---
```

**Recommendation:** Option A is simpler - one SessionStop hook that detects which skill just completed and routes to appropriate milestone check.

---

## Part 3: Detection & Queue Infrastructure

### Queue File System

**Location:** `.shipkit/.queues/` (hidden from user, drives automation)

**Queue Files:**

```
.shipkit/
  .queues/
    # Created by milestone hooks, consumed by preventative skills

    fetch-integration-docs.md
    ├─ Created by: shipkit-post-spec-check (detects service mentions)
    ├─ Format: List of services needing current docs
    └─ Consumed by: shipkit-integration-docs

    define-data-contracts.md
    ├─ Created by: shipkit-post-plan-check (detects data structures)
    ├─ Format: List of types/interfaces to define
    └─ Consumed by: shipkit-data-contracts

    components-to-document.md
    ├─ Created by: shipkit-post-implement-check (detects new components)
    ├─ Format: List of component files with modification times
    └─ Consumed by: shipkit-component-knowledge

    routes-to-document.md
    ├─ Created by: shipkit-post-implement-check (detects new routes)
    ├─ Format: List of route files with modification times
    └─ Consumed by: shipkit-route-knowledge

    ux-audit-needed.md
    ├─ Created by: shipkit-pre-ship-check (threshold: N features built)
    ├─ Format: List of interactive components to audit
    └─ Consumed by: shipkit-ux-audit

    integrations-used.md
    ├─ Created by: shipkit-post-implement-check (code analysis)
    ├─ Format: List of service integrations in codebase
    └─ Consumed by: shipkit-integration-docs
```

### Queue File Format

**Example: `.queues/fetch-integration-docs.md`**
```markdown
# Integration Docs Needed

**Created:** 2025-12-30 14:32
**Reason:** Spec mentions Stripe webhooks

## Pending

- [ ] Stripe webhooks (mentioned in spec: payment-flow.md)
  - File: src/api/webhooks/stripe.ts
  - Need: Webhook signature verification pattern

- [ ] Supabase RLS policies (mentioned in plan: auth-plan.md)
  - File: src/lib/supabase/policies.sql
  - Need: Current RLS policy patterns for user data

## Completed

- [x] OpenAI API (docs fetched 2025-12-28)
```

### Detection Scripts (Hidden Skills in install/skills/)

**DECISION: Option A - Detection scripts are skills**

Detection logic lives in `install/skills/` as proper skills (not shared scripts). This follows best practice for allowing skills to call scripts.

**Why skills not shared scripts:**
- Skills can invoke other skills easily
- Follows existing architecture pattern
- Can be tested/debugged like any skill
- Marked as "system" skills in manifest (hidden from user lists)

### Detection Scripts (Hidden Skills)

**shipkit-post-spec-check** (hidden skill)
```python
#!/usr/bin/env python3
# Purpose: Detect services mentioned in spec, create integration docs queue

import re
from pathlib import Path

def detect_services_in_spec(spec_path):
    """Detect service mentions in spec"""
    spec_content = Path(spec_path).read_text()

    services = {
        'stripe': ['stripe', 'payment', 'webhook'],
        'supabase': ['supabase', 'postgres', 'rls', 'auth'],
        'openai': ['openai', 'gpt', 'embedding', 'llm'],
        's3': ['s3', 'bucket', 'upload', 'storage'],
    }

    detected = []
    for service, keywords in services.items():
        if any(kw in spec_content.lower() for kw in keywords):
            detected.append(service)

    return detected

def create_integration_queue(services, spec_path):
    """Create queue file for integration docs"""
    queue_path = Path('.shipkit/.queues/fetch-integration-docs.md')
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Integration Docs Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Services mentioned in spec: {spec_path}

## Pending

"""

    for service in services:
        content += f"- [ ] {service.capitalize()} integration\n"
        content += f"  - Mentioned in: {spec_path}\n"
        content += f"  - Need: Current best practices and patterns\n\n"

    queue_path.write_text(content)
    print(f"✓ Created integration docs queue with {len(services)} services")

if __name__ == '__main__':
    # Run after shipkit-spec completes
    latest_spec = find_latest_spec('.shipkit/specs/active/')
    services = detect_services_in_spec(latest_spec)

    if services:
        create_integration_queue(services, latest_spec)
        print(f"\n💡 Suggestion: Run /shipkit-integration-docs to fetch current patterns")
```

**shipkit-post-implement-check** (hidden skill)
```python
#!/usr/bin/env python3
# Purpose: Detect new components/routes, create documentation queues

from pathlib import Path
import os

def find_modified_components(since_minutes=60):
    """Find components modified in last N minutes"""
    import time
    cutoff = time.time() - (since_minutes * 60)

    components = []
    for file in Path('src/components').rglob('*.tsx'):
        if os.path.getmtime(file) > cutoff:
            components.append(file)

    return components

def find_modified_routes(since_minutes=60):
    """Find routes modified in last N minutes"""
    import time
    cutoff = time.time() - (since_minutes * 60)

    routes = []
    for file in Path('src/app').rglob('route.ts'):
        if os.path.getmtime(file) > cutoff:
            routes.append(file)

    return routes

def create_documentation_queues(components, routes):
    """Create queue files for documentation"""

    # Components queue
    if components:
        queue = Path('.shipkit/.queues/components-to-document.md')
        content = f"""# Components To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** New/modified components detected

## Pending

"""
        for comp in components:
            mtime = datetime.fromtimestamp(os.path.getmtime(comp))
            content += f"- [ ] {comp}\n"
            content += f"  - Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n\n"

        queue.write_text(content)
        print(f"✓ Created component docs queue with {len(components)} items")

    # Routes queue
    if routes:
        queue = Path('.shipkit/.queues/routes-to-document.md')
        content = f"""# Routes To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** New/modified routes detected

## Pending

"""
        for route in routes:
            mtime = datetime.fromtimestamp(os.path.getmtime(route))
            content += f"- [ ] {route}\n"
            content += f"  - Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n\n"

        queue.write_text(content)
        print(f"✓ Created route docs queue with {len(routes)} items")

if __name__ == '__main__':
    # Run after shipkit-implement completes
    components = find_modified_components(since_minutes=60)
    routes = find_modified_routes(since_minutes=60)

    create_documentation_queues(components, routes)

    if components or routes:
        print(f"\n💡 Suggestion: Run /shipkit-component-knowledge or /shipkit-route-knowledge to document changes")
```

---

## Part 4: Reference Material System

### Purpose: Bug Prevention Through Living Documentation

**Core Insight:** Each preventative skill generates reference material that Claude reads during FUTURE implementations to prevent bugs.

### Reference Material Locations

```
.shipkit/
  references/
    integrations/
      stripe-webhooks.md          # Current Stripe webhook patterns
      supabase-auth.md            # Current Supabase auth patterns
      openai-api.md               # Current OpenAI API patterns

    contracts/
      data-contracts.md           # Data shape contracts across layers
      api-contracts.md            # API request/response schemas

    components/
      UserCard.md                 # UserCard component contract
      LoginForm.md                # LoginForm component contract

    routes/
      api-auth-login.md           # POST /api/auth/login contract
      api-posts.md                # POST /api/posts contract

    ux/
      ux-checklist.md             # UX best practices reference
      ux-patterns.md              # Established UX patterns in project
```

### Reference Material Format

**Example: `references/integrations/stripe-webhooks.md`**
```markdown
# Stripe Webhook Integration Reference

**Last fetched:** 2025-12-30 from stripe.com/docs/webhooks
**Stripe API version:** 2024-11-20.acacia

---

## Current Correct Pattern

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function POST(request: Request) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  // ✓ MUST verify signature (security critical)
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET  // ← Often forgotten!
  );

  // ✓ Handle event types
  switch (event.type) {
    case 'payment_intent.succeeded':
      // Handle successful payment
      break;
    case 'payment_intent.failed':
      // Handle failed payment
      break;
  }

  return Response.json({ received: true });
}
```

---

## Common Mistakes (Prevent These!)

❌ **Forgetting signature verification:**
```typescript
// DON'T DO THIS - Security vulnerability!
const event = JSON.parse(body);  // Unverified webhook
```

❌ **Using old API (pre-2024):**
```typescript
// Old pattern (deprecated):
stripe.webhooks.construct(body, sig)

// New pattern (current):
stripe.webhooks.constructEvent(body, sig, secret)
```

❌ **Not handling webhook retries:**
- Stripe retries failed webhooks
- Use idempotency keys to prevent duplicate processing

---

## Testing Webhooks

**Stripe CLI (recommended):**
```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
stripe trigger payment_intent.succeeded
```

**Test events:**
- Use Stripe test mode event types
- Verify signature even in test mode

---

## Environment Variables Required

```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...  # Get from Stripe Dashboard → Webhooks
```

---

**Next update due:** When Stripe API version changes or new webhook events added
```

**Example: `references/contracts/data-contracts.md`**
```markdown
# Data Contracts Reference

**Last updated:** 2025-12-30

---

## User Data Contract

**Database schema:**
```sql
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Backend API returns:**
```typescript
// GET /api/users/:id
{
  userId: string,      // user_id converted to string
  email: string,
  createdAt: string    // ISO 8601 format
}
```

**Frontend expects:**
```typescript
interface User {
  userId: string;      // ✓ Matches API
  email: string;       // ✓ Matches API
  createdAt: string;   // ✓ Matches API (convert to Date client-side if needed)
}
```

**Common mistake:**
```typescript
// ❌ DON'T expect Date object from API
interface User {
  createdAt: Date;  // Wrong! API returns string
}

// ✓ Correct approach
const user: User = await fetchUser(id);
const createdDate = new Date(user.createdAt);  // Convert client-side
```

---

## Post Data Contract

**Database schema:**
```sql
CREATE TABLE posts (
  post_id INTEGER PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  content TEXT,
  metadata JSONB
);
```

**Backend API expects (POST /api/posts):**
```typescript
{
  userId: string,      // Required
  content: string,     // Required
  metadata?: object    // Optional
}
```

**Backend API returns:**
```typescript
{
  postId: string,
  userId: string,
  content: string,
  metadata: object | null,
  createdAt: string
}
```

**Frontend contract:**
```typescript
// Request
interface CreatePostRequest {
  userId: string;
  content: string;
  metadata?: Record<string, any>;
}

// Response
interface Post {
  postId: string;
  userId: string;
  content: string;
  metadata: Record<string, any> | null;
  createdAt: string;
}
```

---

**Update triggers:**
- Database migrations → Revalidate contracts
- API schema changes → Update this file
- Type errors in production → Investigate contract mismatch
```

### How Claude Uses References During Implementation

**Before coding a Stripe webhook:**
```
Claude: "Let me check references/integrations/stripe-webhooks.md for current patterns"
↓
Reads: "MUST use constructEvent with signature verification"
↓
Codes: Uses correct pattern, avoids common mistakes
↓
Result: No security vulnerability, no bugs
```

**Before integrating with UserCard component:**
```
Claude: "Let me check references/components/UserCard.md for props contract"
↓
Reads: "Expects 'profile' prop (changed from 'user' on 2025-12-28)"
↓
Codes: <UserCard profile={data} />
↓
Result: No prop type errors
```

---

## Part 5: Skill Workflow Integration

### Updated Skill Purposes

**shipkit-integration-docs** (renamed from shipkit-integration-guardrails)
```yaml
Purpose: Fetch CURRENT integration patterns for external services
Trigger: Queue file exists (.queues/fetch-integration-docs.md)
Input: Queue file listing services
Output: references/integrations/{service}.md
Prevents: Coding against outdated docs, missing security patterns
```

**shipkit-data-contracts** (renamed from shipkit-data-consistency)
```yaml
Purpose: Validate and document data shape contracts across layers
Trigger: Queue file exists (.queues/define-data-contracts.md)
Input: Database schema, API responses, component props
Output: references/contracts/data-contracts.md
Prevents: Type mismatches between DB → Backend → Frontend
```

**shipkit-ux-audit** (renamed from shipkit-ux-coherence)
```yaml
Purpose: Audit for missing UX best practices
Trigger: Queue file exists (.queues/ux-audit-needed.md) OR pre-ship
Input: Implemented components (from implementations.md)
Output: references/ux/ux-checklist.md + suggested fixes
Prevents: Missing loading states, error handling, accessibility
```

**shipkit-component-knowledge** (no rename)
```yaml
Purpose: Document component contracts to prevent future integration bugs
Trigger: Queue file exists (.queues/components-to-document.md)
Input: Component source files
Output: references/components/{ComponentName}.md
Prevents: Using wrong props, outdated component APIs
```

**shipkit-route-knowledge** (no rename)
```yaml
Purpose: Document API/route contracts to prevent integration bugs
Trigger: Queue file exists (.queues/routes-to-document.md)
Input: Route/API source files
Output: references/routes/{route-name}.md
Prevents: Wrong HTTP methods, missing parameters, auth errors
```

---

## Part 6: Implementation Phases

### Phase 1: Rename Skills ✅ COMPLETE
- [x] Rename shipkit-integration-guardrails → shipkit-integration-docs
- [x] Rename shipkit-data-consistency → shipkit-data-contracts
- [x] Rename shipkit-ux-coherence → shipkit-ux-audit
- [x] Update all 8 integration files for each renamed skill
- [x] Update cross-references in SKILL.md files
- [x] Update overview.html with new names

### Phase 2: Create Queue Infrastructure ✅ COMPLETE
- [x] Create `.shipkit/.queues/` directory
- [x] Define queue file formats (markdown templates)
- [x] Create .gitignore entry for .queues/ (ephemeral files)

### Phase 3: Create Detection Scripts (Hidden Skills) ✅ COMPLETE
- [x] Create shipkit-post-spec-check (Python script in install/skills/)
- [x] Create shipkit-post-plan-check (Python script in install/skills/)
- [x] Create shipkit-post-implement-check (Python script in install/skills/)
- [x] Create shipkit-pre-ship-check (Python script in install/skills/)
- [x] Test each detection script individually
- [x] Mark as "system" skills in manifest.json

### Phase 4: Create Milestone Hook ✅ COMPLETE
- [x] Create shipkit-milestone-detector (Stop hook coordinator)
- [x] Logic: Detect which skill just completed → Route to appropriate check
- [x] Update install/settings/shipkit.settings.json to add Stop hook
- [x] Fix: Remove invalid matcher, add $CLAUDE_PROJECT_DIR paths, add stdin reading

### Phase 5: Update Consumer Skills ✅ COMPLETE
- [x] Update shipkit-integration-docs to read fetch-integration-docs.md queue (Step 0 added)
- [x] Update shipkit-data-contracts to read define-data-contracts.md queue (Step 0 added)
- [x] Update shipkit-ux-audit to read ux-audit-needed.md queue (Step 0 added)
- [x] Update shipkit-component-knowledge to read components-to-document.md queue (Step 0 added)
- [x] Update shipkit-route-knowledge to read routes-to-document.md queue (Step 0 added)

### Phase 6: Session Documentation ✅ COMPLETE (Added)
- [x] Add prompt hook to auto-invoke shipkit-work-memory for session continuity
- [x] Smart conditional logic (only document significant work)
- [x] Integrate into Stop hook chain (milestone → docs → next-skill)

### Phase 7: Update shipkit-whats-next ✅ COMPLETE
- [x] Add queue file checking logic (Step 0 added)
- [x] Suggest skills when queues exist (priority table created)
- [x] Show queue contents in suggestions (recommendation format defined)
- [x] Document queue-aware behavior in Special Relationships section
- [x] Update "Context Files This Skill Reads" to include .queues/

### Phase 8: Create Reference Material System ⏸️ DEFERRED
- [ ] Create `.shipkit/references/` directory structure
- [ ] Design reference material templates
- [ ] Update skills to output to references/ folder
- [ ] Update shipkit-implement to read references/ before coding

---

## Part 7: Success Criteria

### Bug Prevention Metrics

**Objective:** Reduce common vibe coding errors by 80%

**Measured by:**
1. **Integration bugs:**
   - Before: "Used old Stripe API, webhooks failed"
   - After: references/integrations/stripe-webhooks.md prevents this

2. **Data contract bugs:**
   - Before: "Expected Date but got string, runtime error"
   - After: references/contracts/data-contracts.md prevents this

3. **Component integration bugs:**
   - Before: "Used wrong prop name, component errored"
   - After: references/components/{Name}.md prevents this

4. **UX gaps:**
   - Before: "Forgot loading state, button clickable during async"
   - After: shipkit-ux-audit catches this pre-ship

### User Experience Goals

1. **Automatic detection:** User doesn't need to remember to run preventative skills
2. **Timely suggestions:** Skills suggested at the RIGHT milestone (not too early/late)
3. **Living documentation:** References stay fresh, prevent future bugs
4. **Zero manual work:** Queues created automatically, user just approves

---

## Part 8: File Structure Overview

```
sg-shipkit/
  install/
    skills/
      # Renamed skills (user-facing)
      shipkit-integration-docs/          # Renamed from shipkit-integration-guardrails
        SKILL.md
        scripts/
          fetch-docs.py
        templates/
          integration-reference.md

      shipkit-data-contracts/            # Renamed from shipkit-data-consistency
        SKILL.md
        scripts/
          validate-contracts.py
        templates/
          data-contract.md

      shipkit-ux-audit/                  # Renamed from shipkit-ux-coherence
        SKILL.md
        scripts/
          audit-ux.py
        templates/
          ux-checklist.md

      # System skills (hidden from user, marked in manifest)
      shipkit-post-spec-check/
        SKILL.md
        scripts/
          detect-services.py         # Scans spec for service mentions

      shipkit-post-plan-check/
        SKILL.md
        scripts/
          detect-data-structures.py  # Scans plan for data definitions

      shipkit-post-implement-check/
        SKILL.md
        scripts/
          detect-changes.py          # Scans modified files

      shipkit-pre-ship-check/
        SKILL.md
        scripts/
          check-readiness.py         # Checks for UX audit needs

      # Milestone coordinator (system skill)
      shipkit-milestone-detector/
        SKILL.md
        scripts/
          route-to-check.py          # SessionStop hook logic

.shipkit/
  .queues/                           # Ephemeral queue files
    fetch-integration-docs.md
    define-data-contracts.md
    components-to-document.md
    routes-to-document.md
    ux-audit-needed.md

  references/                        # Living reference material
    integrations/
      stripe-webhooks.md
      supabase-auth.md
    contracts/
      data-contracts.md
    components/
      UserCard.md
      LoginForm.md
    routes/
      api-auth-login.md
    ux/
      ux-checklist.md
```

---

## Part 9: Open Questions & Decisions

### ✅ Decided

1. **Detection script location:** ✅ Option A - Skills in `install/skills/`
   - Detection logic as proper skills, marked as system skills
   - Follows best practice for script organization

2. **shipkit-whats-next role:** ✅ Queue-aware ultimate orchestrator
   - Automatic mode: SessionStop hook invokes it
   - Manual mode: User calls `/shipkit-whats-next` when confused
   - Reads queue files and suggests pending work

### ❓ Still Open

1. **SessionStop hook frequency:**
   - Does SessionStop fire after EVERY skill?
   - Or only at session end?
   - May need to test actual behavior

2. **Queue file lifespan:**
   - When do we clear completed queue items?
   - Archive old queues or delete immediately?
   - Git-ignore .queues/ folder (ephemeral)?

3. **Reference freshness:**
   - How often re-fetch integration docs?
   - Version pinning for external docs?
   - Add "last fetched" timestamps to references

4. **System skill marking:**
   - How to mark detection skills as "system" in manifest?
   - Should they appear in `/help` or be completely hidden?

---

## Next Steps

1. **Review this spec** - Does the architecture make sense?
2. **Decide on hook strategy** - SessionStop vs skill-level hooks?
3. **Prototype detection script** - Test shipkit-post-implement-check first?
4. **Create reference templates** - Design one integration reference as example?
5. **Begin implementation** - Start with Phase 1 (renaming)?

---

**END OF SPECIFICATION**
