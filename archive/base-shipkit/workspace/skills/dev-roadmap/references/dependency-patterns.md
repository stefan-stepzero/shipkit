# Common Dependency Patterns

**Purpose:** Recognize common technical dependency patterns when sequencing features

**When to reference:** When analyzing user stories and unsure what blocks what

---

## Table of Contents

1. [Authentication Dependencies](#authentication-dependencies)
2. [Data Pipeline Dependencies](#data-pipeline-dependencies)
3. [UI Component Dependencies](#ui-component-dependencies)
4. [Integration Dependencies](#integration-dependencies)
5. [Testing Dependencies](#testing-dependencies)

---

## Authentication Dependencies

### Pattern: Auth Blocks All User Features

**What blocks:**
- Any feature requiring user identity
- Any feature with access control
- Any feature with personalization
- Any feature storing user data

**Example:**
```
Auth blocks:
  - User profiles
  - Shopping carts
  - Saved preferences
  - Order history
  - Dashboard
  - Admin panels
```

**Exception:** Public features (landing pages, product catalog browse, search)

---

### Pattern: Multi-Tenancy is Architectural

**What blocks:**
- ALL features in multi-tenant apps
- Data isolation requires tenant context
- Can't retrofit multi-tenancy later

**Example:**
```
Multi-tenant auth blocks:
  - Organization management
  - Team collaboration
  - Resource sharing
  - Billing per organization
  - Access control per tenant
```

**Decision point:** Spec 1 or Spec 2 (can't be later)

---

### Pattern: Role-Based Access Control (RBAC)

**What blocks:**
- Admin features
- Feature flags per role
- Granular permissions
- Audit logs

**Example:**
```
RBAC blocks:
  - Admin CRUD operations
  - Approval workflows
  - Report access control
  - System configuration
```

**Tip:** Implement basic RBAC early, refine later

---

## Data Pipeline Dependencies

### Pattern: Database Schema Blocks CRUD

**What blocks:**
- Any feature reading/writing that entity
- Migrations must exist first
- Schema changes require careful sequencing

**Example:**
```
Product schema blocks:
  - Product catalog
  - Shopping cart (references products)
  - Order history (references products)
  - Search (indexes products)
  - Admin product management
```

**Tip:** Get core entities in Spec 1, evolve schema in subsequent specs

---

### Pattern: Data Source Blocks Analysis

**What blocks:**
- Reporting requires data ingestion
- Analytics requires events/metrics
- Dashboards require data connections

**Example:**
```
Data ingestion blocks:
  - Custom reports
  - Real-time dashboards
  - Data exports
  - Scheduled reports
  - Alerting
```

**Sequence:** Data ingestion → Analysis features

---

### Pattern: Event Streaming Blocks Reactive Features

**What blocks:**
- Webhooks
- Real-time notifications
- Audit trails
- Activity feeds
- Integrations

**Example:**
```
Event bus blocks:
  - Webhook delivery
  - Email notifications
  - Push notifications
  - Third-party integrations
  - Audit logs
```

**Decision:** Event infrastructure in Spec 1 if many reactive features

---

## UI Component Dependencies

### Pattern: Design System Blocks Consistency

**What blocks:**
- Consistent UI across features
- Reusable components
- Accessibility standards
- Brand compliance

**Example:**
```
Component library blocks:
  - All UI features (if consistency required)

Component library enables:
  - Faster feature development
  - Consistent UX
```

**Decision:**
- **Option A:** Design system in Spec 1 (slower start, consistent later)
- **Option B:** Build one feature first, extract patterns (faster start, refactor later)

**For POCs/MVPs:** Option B (extract patterns later)
**For mature products:** Option A (consistency matters)

---

### Pattern: Navigation Structure Blocks Discoverability

**What blocks:**
- Features that need to be accessible
- User flows between features
- Information architecture

**Example:**
```
Navigation blocks:
  - All features (they need to be reachable)

Can be built incrementally:
  - Spec 1: Basic nav structure
  - Spec N: Add new feature to nav
```

**Tip:** Navigation scaffolding in Spec 1, extend per feature

---

### Pattern: Established UI Patterns Enable Reuse

**What enables:**
- Admin panels after user-facing CRUD
- Similar features benefit from patterns

**Example:**
```
Product management UI (Spec 3) enables:
  - Category management (uses same CRUD pattern)
  - Admin product editing (reuses product forms)
  - Inventory management (similar table patterns)
```

**Sequence:** First instance → Refine → Reuse pattern

---

## Integration Dependencies

### Pattern: Payment Integration Blocks Monetization

**What blocks:**
- Checkout completion
- Subscription management
- Invoice generation
- Refunds

**Example:**
```
Stripe integration blocks:
  - Order completion
  - Recurring billing
  - Payment methods management
  - Transaction history
```

**Risk:** High (external dependency, compliance)
**Sequence:** Early (Spec 3-5) to validate, before building dependencies

---

### Pattern: Third-Party APIs Block Dependent Features

**What blocks:**
- Features using that API
- Features requiring that data

**Example:**
```
Google Maps API blocks:
  - Location search
  - Nearby results
  - Route planning
  - Store locator

SendGrid API blocks:
  - Transactional emails
  - Email notifications
  - Marketing campaigns
```

**Risk:** Medium-High (rate limits, auth, schema changes)
**Sequence:** Validate integration early (Spec 2-4)

---

### Pattern: OAuth Integration Blocks Social Features

**What blocks:**
- Social login
- Social sharing
- Import from social networks
- Calendar integrations

**Example:**
```
Google OAuth blocks:
  - "Sign in with Google"
  - Google Calendar sync
  - Gmail integration

Facebook OAuth blocks:
  - "Sign in with Facebook"
  - Share to Facebook
  - Import Facebook events
```

**Sequence:** OAuth in Spec 2 (auth phase), social features later

---

## Testing Dependencies

### Pattern: Test Infrastructure Blocks Quality

**What blocks:**
- Automated testing
- CI/CD confidence
- Regression prevention

**Example:**
```
Test setup blocks:
  - Unit tests
  - Integration tests
  - E2E tests
  - CI/CD pipeline
```

**Decision:**
- **Must have in Spec 1:** Test framework setup, CI/CD
- **Per feature:** Tests for that feature
- **Later:** E2E test infrastructure (after core features)

---

### Pattern: Test Data Blocks Integration Tests

**What blocks:**
- Integration tests
- E2E tests
- Manual QA
- Demo environments

**Example:**
```
Test data blocks:
  - Full workflow testing
  - Demo to stakeholders
  - Load testing
  - Performance testing
```

**Sequence:** After core features (Spec 3-4), before dependent features

---

## Dependency Analysis Questions

When reviewing user stories, ask these questions:

### 1. Data Dependencies
- Does this feature read/write data from another feature?
- Does this feature require a specific schema to exist?
- Does this feature aggregate data from multiple sources?

**If YES:** Dependency on the feature that creates that data

---

### 2. Auth/Access Dependencies
- Does this feature require user identity?
- Does this feature have different behavior per role?
- Does this feature require multi-tenant isolation?

**If YES:** Dependency on auth/RBAC

---

### 3. API/Integration Dependencies
- Does this feature call external APIs?
- Does this feature integrate with third-party services?
- Does this feature require webhooks/events from elsewhere?

**If YES:** Dependency on that integration or event system

---

### 4. UI Dependencies
- Does this feature reuse UI patterns from another feature?
- Does this feature require components from a design system?
- Does this feature need to be in the navigation?

**If YES:** Consider if pattern should be established first

---

### 5. Business Logic Dependencies
- Does this feature trigger actions in another feature?
- Does this feature require calculations from another feature?
- Does this feature extend functionality of another feature?

**If YES:** Dependency on that feature's business logic

---

## Dependency Graph Example

**Project:** E-commerce platform

```
                    ┌─────────────────┐
                    │   Spec 1: Core  │
                    │  Infrastructure │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Spec 2: Auth   │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
 ┌────────▼────────┐ ┌──────▼───────┐ ┌────────▼────────┐
 │ Spec 3: Catalog │ │ Spec 4: Cart │ │ Spec 7: Emails  │
 │   + Search      │ │  + Checkout  │ │  (independent)  │
 └────────┬────────┘ └──────┬───────┘ └─────────────────┘
          │                  │
          └─────────┬────────┘
                    │
          ┌─────────▼────────┐
          │ Spec 5: Payment  │
          │   (risky early)  │
          └─────────┬────────┘
                    │
          ┌─────────▼────────┐
          │ Spec 6: Orders   │
          └─────────┬────────┘
                    │
          ┌─────────▼────────┐
          │ Spec 8: Admin    │
          └──────────────────┘
```

**Legend:**
- Arrows = "blocks" or "enables"
- Spec 7 independent (no arrows from others)
- Spec 5 early despite not being critical path (high risk)

---

## Special Cases

### Circular Dependencies (Fix Required)

**Problem:**
```
Feature A needs Feature B's data
Feature B needs Feature A's data
```

**Solutions:**
1. **Extract shared logic to earlier spec**
   ```
   Spec N: Shared data model
   Spec N+1: Feature A (uses shared model)
   Spec N+2: Feature B (uses shared model)
   ```

2. **One feature doesn't actually need the other**
   - Re-examine requirements
   - Often one direction is sufficient

3. **Staged implementation**
   ```
   Spec N: Feature A (basic)
   Spec N+1: Feature B (basic)
   Spec N+2: Feature A + B integration
   ```

---

### Optional Dependencies (Design Decision)

**Pattern:** Feature A works without Feature B, but better with it

**Example:**
```
Product catalog works without search
But search makes it much better
```

**Decision:**
- **Sequence separately:** Catalog first, search later (faster initial delivery)
- **Sequence together:** Catalog + search in same spec (better UX from start)

**POC/MVP:** Separate (validate core first)
**Mature product:** Together (quality matters)

---

### Parallel Dependencies (Team Coordination)

**Pattern:** Two features depend on same foundation, but not each other

**Example:**
```
Spec 1: Core Infrastructure
  ├→ Spec 2: Feature A (needs Spec 1)
  └→ Spec 3: Feature B (needs Spec 1, independent of A)
```

**Opportunity:** Specs 2 and 3 could be built in parallel by different team members

**Roadmap note:** Document this in "Dependencies" field

---

## Using Dependency Patterns

1. **Read user stories** - Understand what each feature does
2. **Identify data needs** - What does it read/write?
3. **Identify auth needs** - Who can access it?
4. **Identify integration needs** - What external systems?
5. **Identify UI needs** - What patterns does it reuse?
6. **Draw dependency graph** - Visualize what blocks what
7. **Sequence by graph** - Topological sort (dependencies first)
8. **Consider risk** - Move risky items earlier
9. **Consider coupling** - Group tightly related features

**Remember:** Technical dependencies trump business priority. You can't build what depends on things that don't exist yet.
