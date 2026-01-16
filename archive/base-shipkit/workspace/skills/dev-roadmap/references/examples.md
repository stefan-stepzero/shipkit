# Development Roadmap Examples

**Purpose:** Real-world roadmap examples for different types of projects

**When to reference:** When creating a roadmap and need inspiration for sequencing patterns

---

## Table of Contents

1. [E-commerce Platform](#example-1-e-commerce-platform)
2. [SaaS Analytics Dashboard](#example-2-saas-analytics-dashboard)
3. [Mobile App with Backend](#example-3-mobile-app-with-backend)
4. [API-First Architecture](#example-4-api-first-architecture)
5. [Legacy System Migration](#example-5-legacy-system-migration)

---

## Example 1: E-commerce Platform

### User Stories (Summary)
- US-001: User registration/login
- US-002: Product catalog browsing
- US-003: Shopping cart
- US-004: Checkout flow
- US-005: Payment processing (Stripe)
- US-006: Order history
- US-007: Product search
- US-008: Admin product management
- US-009: Email notifications
- US-010: Analytics dashboard

### Roadmap

```
Spec 1: Core Infrastructure
Why: Foundation enables everything
Contains:
  - PostgreSQL database + migrations
  - JWT authentication scaffold
  - Express.js API framework
  - Email service (SendGrid integration)
  - Deployment pipeline (staging + production)
  - Error tracking (Sentry)
Dependencies: None

Spec 2: User Authentication (US-001)
Why: Blocks 80% of other features
Contains:
  - User registration and login
  - Session management
  - Password reset flow
  - Email verification
Dependencies: Spec 1

Spec 3: Product Catalog + Search (US-002, US-007)
Why: Core value, tightly coupled (same data model)
Contains:
  - Product listing and detail pages
  - Category navigation
  - Full-text search (Elasticsearch)
  - Product filtering and sorting
Dependencies: Spec 1, Spec 2

Spec 4: Shopping Cart + Checkout (US-003, US-004)
Why: Purchase flow is tightly coupled, critical path
Contains:
  - Add/remove items from cart
  - Cart persistence
  - Checkout form
  - Order creation
Dependencies: Spec 1, Spec 2, Spec 3

Spec 5: Payment Integration (US-005)
Why: High risk - validate early before building dependencies
Contains:
  - Stripe integration
  - Payment processing
  - Webhook handling
  - Transaction logging
Dependencies: Spec 1, Spec 2, Spec 4

Spec 6: Order History (US-006)
Why: Depends on purchase flow completion
Contains:
  - Order listing
  - Order details view
  - Order status tracking
  - Download invoices
Dependencies: Spec 1, Spec 2, Spec 4, Spec 5

Spec 7: Email Notifications (US-009)
Why: Independent feature, can be parallel with Spec 6
Contains:
  - Order confirmation emails
  - Shipping notifications
  - Password reset emails
  - Welcome emails
Dependencies: Spec 1, Spec 2

Spec 8: Admin Product Management (US-008)
Why: Uses UI patterns established in Spec 3
Contains:
  - Product CRUD operations
  - Category management
  - Inventory tracking
  - Bulk operations
Dependencies: Spec 1, Spec 2, Spec 3

Spec 9: Analytics Dashboard (US-010)
Why: Needs data from all features, naturally goes last
Contains:
  - Sales metrics
  - User behavior analytics
  - Revenue charts
  - Export to CSV
Dependencies: Spec 1, Spec 2, Spec 3, Spec 4, Spec 5, Spec 6
```

**Total: 9 specs**

**Key patterns:**
- Foundation first (Spec 1)
- Auth second (blocks everything)
- Core value early (Spec 3 - browsing products)
- Risky integration validated early (Spec 5 - payment)
- Dependent features after their dependencies (Spec 6 after 4+5)
- Independent work can be parallel (Spec 6 and 7)
- Analytics last (needs all data)

---

## Example 2: SaaS Analytics Dashboard

### User Stories (Summary)
- US-001: User registration/login
- US-002: Data source connections (SQL, APIs)
- US-003: Dashboard builder
- US-004: Custom visualizations
- US-005: Scheduled reports
- US-006: Team collaboration
- US-007: API access
- US-008: Billing integration

### Roadmap

```
Spec 1: Core Infrastructure
Why: Foundation
Contains:
  - Database (PostgreSQL + TimescaleDB for metrics)
  - Auth scaffold
  - API framework
  - Job queue (Redis + Bull)
  - File storage (S3)
Dependencies: None

Spec 2: User Auth + Multi-tenancy (US-001)
Why: Blocks everything, multi-tenancy is architectural
Contains:
  - User registration/login
  - Organization model
  - Role-based access
  - Tenant isolation
Dependencies: Spec 1

Spec 3: Data Source Connections (US-002)
Why: High risk, core value - validate early
Contains:
  - SQL database connectors (Postgres, MySQL)
  - REST API connector
  - Connection testing
  - Data ingestion pipeline
Dependencies: Spec 1, Spec 2

Spec 4: Dashboard Builder (US-003)
Why: Core product value
Contains:
  - Dashboard CRUD
  - Drag-and-drop layout
  - Widget library
  - Query builder
Dependencies: Spec 1, Spec 2, Spec 3

Spec 5: Custom Visualizations (US-004)
Why: Extends dashboard functionality
Contains:
  - Chart types (line, bar, pie, etc.)
  - Custom SQL queries
  - Data transformations
  - Interactive filters
Dependencies: Spec 1, Spec 2, Spec 3, Spec 4

Spec 6: Scheduled Reports (US-005)
Why: Independent of dashboard UI
Contains:
  - Report scheduling
  - Email delivery
  - PDF generation
  - Report history
Dependencies: Spec 1, Spec 2, Spec 3

Spec 7: Team Collaboration (US-006)
Why: Independent feature, can be parallel with others
Contains:
  - Dashboard sharing
  - Comments and annotations
  - Activity feed
  - Notifications
Dependencies: Spec 1, Spec 2, Spec 4

Spec 8: API Access (US-007)
Why: Independent, enables integrations
Contains:
  - REST API for dashboards
  - API key management
  - Rate limiting
  - API documentation
Dependencies: Spec 1, Spec 2, Spec 4

Spec 9: Billing Integration (US-008)
Why: Last - product must work before charging
Contains:
  - Stripe billing
  - Subscription plans
  - Usage tracking
  - Invoice generation
Dependencies: Spec 1, Spec 2
```

**Total: 9 specs**

**Key patterns:**
- Multi-tenancy in Spec 2 (architectural decision early)
- Risky data connectors validated early (Spec 3)
- Core product value built incrementally (Specs 4, 5)
- Multiple independent features (Specs 6, 7, 8 can be parallel)
- Billing last (product validated first)

---

## Example 3: Mobile App with Backend

### User Stories (Summary)
- US-001: User onboarding
- US-002: Profile management
- US-003: Feed of content
- US-004: Create/share content
- US-005: Push notifications
- US-006: In-app messaging
- US-007: Location-based features

### Roadmap

```
Spec 1: Backend Infrastructure
Why: Mobile app needs API first
Contains:
  - Node.js API (Express)
  - MongoDB database
  - Firebase Cloud Messaging setup
  - AWS deployment
  - CDN for media (CloudFront)
Dependencies: None

Spec 2: Mobile App Scaffold + Auth (US-001)
Why: Foundation for all mobile features
Contains:
  - React Native setup
  - Navigation structure
  - User registration/login
  - Token management
  - Onboarding flow
Dependencies: Spec 1

Spec 3: Profile Management (US-002)
Why: Simple, establishes patterns
Contains:
  - Profile viewing
  - Profile editing
  - Avatar upload
  - Settings screen
Dependencies: Spec 1, Spec 2

Spec 4: Content Feed (US-003)
Why: Core product value
Contains:
  - Feed API endpoint
  - Feed UI (infinite scroll)
  - Pull-to-refresh
  - Content caching
Dependencies: Spec 1, Spec 2

Spec 5: Content Creation (US-004)
Why: Tightly coupled with feed
Contains:
  - Create content form
  - Media upload (photos/videos)
  - Content moderation
  - Share functionality
Dependencies: Spec 1, Spec 2, Spec 4

Spec 6: Push Notifications (US-005)
Why: Independent feature, enables engagement
Contains:
  - FCM integration
  - Notification triggers
  - Notification UI
  - Notification preferences
Dependencies: Spec 1, Spec 2

Spec 7: In-App Messaging (US-006)
Why: Independent, can be parallel
Contains:
  - Message threads
  - Real-time chat (Socket.io)
  - Message notifications
  - Media sharing in messages
Dependencies: Spec 1, Spec 2

Spec 8: Location-Based Features (US-007)
Why: Independent, requires permissions testing
Contains:
  - Location permissions
  - Nearby content
  - Location tagging
  - Map view
Dependencies: Spec 1, Spec 2, Spec 4
```

**Total: 8 specs**

**Key patterns:**
- Backend API first (mobile needs it)
- Mobile scaffold + auth together (foundation)
- Simple feature first to establish patterns (profile)
- Core value early (feed + creation)
- Independent features can be parallel (Specs 6, 7, 8)

---

## Example 4: API-First Architecture

### User Stories (Summary)
- US-001: API authentication
- US-002: User management API
- US-003: Resource CRUD APIs
- US-004: Search API
- US-005: Webhooks
- US-006: Admin dashboard
- US-007: API documentation
- US-008: Rate limiting

### Roadmap

```
Spec 1: Core API Infrastructure
Why: Foundation for API product
Contains:
  - FastAPI framework
  - PostgreSQL database
  - Redis for caching/rate limiting
  - OpenAPI schema generation
  - Deployment (Docker + K8s)
Dependencies: None

Spec 2: API Authentication (US-001)
Why: Blocks all other APIs
Contains:
  - OAuth 2.0 flows
  - API key management
  - JWT tokens
  - Refresh token rotation
Dependencies: Spec 1

Spec 3: User Management API (US-002)
Why: Foundation for multi-tenant system
Contains:
  - User CRUD endpoints
  - Organization management
  - Role-based access control
  - Audit logging
Dependencies: Spec 1, Spec 2

Spec 4: Resource CRUD APIs (US-003)
Why: Core product functionality
Contains:
  - RESTful CRUD endpoints
  - Pagination
  - Filtering and sorting
  - Nested resources
Dependencies: Spec 1, Spec 2, Spec 3

Spec 5: Search API (US-004)
Why: High value, uses established patterns
Contains:
  - Full-text search (Elasticsearch)
  - Advanced filtering
  - Faceted search
  - Search analytics
Dependencies: Spec 1, Spec 2, Spec 4

Spec 6: Webhooks (US-005)
Why: Independent, enables integrations
Contains:
  - Webhook subscriptions
  - Event delivery
  - Retry logic
  - Webhook logs
Dependencies: Spec 1, Spec 2

Spec 7: Rate Limiting (US-008)
Why: Protect API from abuse
Contains:
  - Token bucket algorithm
  - Per-key limits
  - Rate limit headers
  - Quota management
Dependencies: Spec 1, Spec 2

Spec 8: API Documentation (US-007)
Why: After APIs are stable
Contains:
  - Interactive docs (Swagger UI)
  - Code examples
  - Getting started guide
  - API changelog
Dependencies: All previous specs (documents them)

Spec 9: Admin Dashboard (US-006)
Why: Internal tool, can be simple
Contains:
  - User management UI
  - API usage metrics
  - Webhook management
  - System health dashboard
Dependencies: Spec 1, Spec 2, Spec 3
```

**Total: 9 specs**

**Key patterns:**
- API infrastructure first
- Auth second (blocks everything)
- Core APIs built incrementally (Specs 3, 4, 5)
- Independent features parallel (Specs 6, 7)
- Documentation after APIs stable (Spec 8)
- Internal admin tool last (lower priority)

---

## Example 5: Legacy System Migration

### User Stories (Summary)
- US-001: New authentication system
- US-002: Data migration pipeline
- US-003: Feature parity - reports
- US-004: Feature parity - admin
- US-005: New UI framework
- US-006: Dual-write system
- US-007: Cutover automation

### Roadmap

```
Spec 1: New System Infrastructure
Why: Foundation for migration target
Contains:
  - Modern stack (React + Node.js)
  - PostgreSQL database
  - Authentication service
  - Deployment pipeline
  - Monitoring/alerting
Dependencies: None

Spec 2: Data Migration Pipeline (US-002)
Why: HIGH RISK - validate early
Contains:
  - ETL pipeline
  - Data validation
  - Migration scripts
  - Rollback procedures
  - Data reconciliation
Dependencies: Spec 1

Spec 3: Authentication Migration (US-001)
Why: Blocks user access to new system
Contains:
  - SSO integration
  - User migration
  - Session compatibility
  - Fallback to old auth
Dependencies: Spec 1, Spec 2

Spec 4: Dual-Write System (US-006)
Why: Enables gradual migration
Contains:
  - Write to both systems
  - Consistency checks
  - Conflict resolution
  - Monitoring dual-write health
Dependencies: Spec 1, Spec 2, Spec 3

Spec 5: Feature Parity - Reports (US-003)
Why: Most critical feature
Contains:
  - Rebuild key reports
  - Match old report logic
  - Visual parity
  - Export functionality
Dependencies: Spec 1, Spec 2, Spec 4

Spec 6: Feature Parity - Admin (US-004)
Why: Second most critical
Contains:
  - Admin CRUD operations
  - User management
  - System configuration
  - Audit logs
Dependencies: Spec 1, Spec 2, Spec 3, Spec 4

Spec 7: New UI Framework (US-005)
Why: After feature parity proven
Contains:
  - Component library
  - Responsive design
  - Accessibility improvements
  - Modern UX patterns
Dependencies: Spec 1, Spec 5, Spec 6

Spec 8: Cutover Automation (US-007)
Why: Last - after everything tested
Contains:
  - Cutover scripts
  - DNS switching
  - Database cutover
  - Rollback procedures
  - Post-cutover validation
Dependencies: All previous specs
```

**Total: 8 specs**

**Key patterns:**
- New infrastructure first
- **Data migration EARLY** (highest risk in migrations)
- Auth migration before features (critical dependency)
- Dual-write enables gradual migration (Spec 4)
- Feature parity before UX improvements (validate logic first)
- Cutover last (after thorough testing)

---

## Common Sequencing Patterns

### Pattern: Foundation First
**Always Spec 1:**
- Database setup
- Authentication scaffold
- API framework
- Deployment pipeline
- Monitoring/logging

### Pattern: Auth Blocks Everything
**Always Spec 2 (or part of Spec 1):**
- Most features require auth
- Multi-tenancy is architectural
- Get it right early

### Pattern: Risky Early
**Spec 2-4 range:**
- External integrations (payment, APIs)
- Data migrations
- New technologies
- Complex algorithms
**Why:** Fail fast, learn unknowns early

### Pattern: Tightly Coupled Together
**Adjacent specs:**
- Shopping cart + checkout
- Product catalog + search
- Feed + content creation
**Why:** Minimize context switching

### Pattern: Independent Features Parallel
**No strict sequence:**
- Email notifications
- Analytics/reporting
- Admin tools
- API documentation
**Why:** Can be built in any order

### Pattern: Dependent Features After Dependencies
**Logical:**
- Order history after checkout + payment
- Dashboard after data connections
- Admin panel after core features
**Why:** Can't build without prerequisites

### Pattern: Analytics/Reporting Last
**Usually final spec:**
- Needs data from all features
- Lower priority than core functionality
- Can iterate after launch

---

## Anti-Patterns to Avoid

### ❌ Business Priority Over Technical Dependencies
**Wrong:**
```
Spec 1: High-value feature A
Spec 2: Medium-value feature B (depends on A)
Spec 3: Auth (A and B both need it)
```
**Right:**
```
Spec 1: Core Infrastructure + Auth
Spec 2: Feature A
Spec 3: Feature B
```

### ❌ Single User Story Split Across Specs
**Wrong:**
```
Spec 3: Shopping cart (part 1)
Spec 5: Shopping cart (part 2)
```
**Right:**
```
Spec 3: Shopping cart (complete)
```

### ❌ Foundation Work Spread Across Specs
**Wrong:**
```
Spec 1: Database
Spec 3: Auth
Spec 5: API framework
```
**Right:**
```
Spec 1: Core Infrastructure (database + auth + API)
```

### ❌ Circular Dependencies
**Wrong:**
```
Spec 2 depends on Spec 4
Spec 4 depends on Spec 2
```
**Fix:** One of them doesn't actually need the other, or extract shared code to earlier spec

---

## Using These Examples

1. **Find similar project type** - E-commerce, SaaS, mobile app, API, migration
2. **Identify patterns** - Foundation, auth, risky early, tightly coupled
3. **Adapt to your context** - Your tech stack, your risks, your dependencies
4. **Don't copy blindly** - Understand the "why" behind each sequence decision

**Remember:** These are examples, not templates. Your roadmap should reflect YOUR project's unique technical dependencies.
