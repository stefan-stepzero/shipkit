# Implementation Planning - Examples

This file contains concrete examples of implementation plans for different types of features.

---

## Example 1: User Authentication (Backend Feature)

### Context
- **Spec**: Add user registration and login
- **Stack**: Node.js + TypeScript + PostgreSQL + Express
- **Constitution**: RESTful API, JWT auth, bcrypt passwords, 80% test coverage

### Plan Summary (plan.md excerpt)

```markdown
# Implementation Plan: User Authentication

**Feature**: 1-user-authentication
**Created**: 2024-01-15
**Spec**: `.shipkit/skills/dev-specify/outputs/specs/1-user-authentication/spec.md`

## Summary

Implement user registration and login with JWT-based authentication. Users can register with email/password, receive a token, and use it for authenticated requests.

## Technical Context

**Language/Framework**: TypeScript/Node.js 18 with Express
**Primary Dependencies**: Express, TypeORM, bcrypt, jsonwebtoken
**Storage**: PostgreSQL 15
**Testing**: Jest with Supertest
**Target Platform**: Node.js server
**Performance Goals**: <200ms p95 response time for auth endpoints
**Constraints**: Must support 1000 concurrent users
**Scale/Scope**: 10K registered users in first month

## Constitution Check

### Alignment with Standards

**Architectural Patterns**:
- [x] Controller → Service → Repository pattern
- [x] Dependency injection for services
- [x] Separate routes, controllers, services, models

**Technology Stack**:
- [x] Node.js 18 + TypeScript (approved)
- [x] PostgreSQL with TypeORM (approved)
- [x] bcrypt for password hashing (security standard)
- [x] JWT for stateless auth (approved)

**API Conventions**:
- [x] RESTful endpoints (/api/v1/auth/...)
- [x] JSON request/response
- [x] Standard HTTP codes (200, 400, 401, 500)

**Security Standards**:
- [x] Password validation (min 8 chars, complexity rules)
- [x] Bcrypt with cost factor 10
- [x] JWT with short expiry (15min access + 7day refresh)

### Violations & Justifications

*None - plan fully aligns with constitution*
```

### Research (research.md excerpt)

```markdown
# Technical Research: User Authentication

## Research Areas

### JWT Library Choice

**Question:** Which JWT library for Node.js?

**Options Considered:**

**Option A: jsonwebtoken**
- Pros: Most popular (26M weekly downloads), well-maintained, simple API
- Cons: Synchronous signing (blocking)
- Complexity: Low
- Team familiarity: High

**Option B: jose**
- Pros: Async operations, modern API, supports JWE
- Cons: Newer library, less community resources
- Complexity: Medium
- Team familiarity: Low

**Decision:** jsonwebtoken

**Rationale:**
- Team already familiar from previous projects
- Synchronous signing acceptable (< 1ms with RS256)
- Larger ecosystem (more Stack Overflow answers)
- Constitution doesn't require async operations

**Trade-offs Accepted:**
- Blocking operations (mitigated by fast crypto)
- Older API design (acceptable - stable and proven)

**Sources:**
- jsonwebtoken docs: https://github.com/auth0/node-jsonwebtoken
- Performance comparison: Signing 1000 tokens takes ~50ms
```

### Data Model (data-model.md excerpt)

```markdown
# Data Model: User Authentication

## Entities

### User

**Purpose:** Represents registered user with authentication credentials

**Fields:**
```
id: UUID, primary key, auto-generated
email: String, unique, required, max 255 chars, indexed
passwordHash: String, required (bcrypt, never expose)
firstName: String, optional, max 50 chars
lastName: String, optional, max 50 chars
createdAt: Timestamp, default now()
updatedAt: Timestamp, auto-update
lastLoginAt: Timestamp, nullable
```

**Constraints:**
- Unique: email (lowercase before save)
- Index: email (for login lookup <10ms)
- Validation: email must be RFC 5322 format
- Security: passwordHash uses bcrypt cost factor 10

**Relationships:**
- None (base authentication entity)

## Indexes

**Primary:**
- User.email (unique, btree) - Login lookup <10ms

## Validation

**Application-Level:**
- Email: RFC 5322 format, lowercase
- Password: Min 8 chars, 1 uppercase, 1 lowercase, 1 number

**Database-Level:**
- NOT NULL: email, passwordHash
- UNIQUE: email
- CHECK: email LIKE '%@%'
```

### Contracts (contracts/auth-api.yaml excerpt)

```yaml
openapi: 3.0.0
info:
  title: Authentication API
  version: 1.0.0
paths:
  /api/v1/auth/register:
    post:
      summary: Register new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                firstName:
                  type: string
                  maxLength: 50
                lastName:
                  type: string
                  maxLength: 50
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  refreshToken:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'
        '400':
          description: Validation error
        '409':
          description: Email already exists
  /api/v1/auth/login:
    post:
      summary: Login existing user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: Login successful
        '401':
          description: Invalid credentials
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
        firstName:
          type: string
        lastName:
          type: string
```

---

## Example 2: Product Catalog (Full-Stack Feature)

### Context
- **Spec**: Display searchable product catalog with filters
- **Stack**: React + TypeScript (frontend) + Node.js + PostgreSQL (backend)
- **Constitution**: REST API, React functional components, Redux for state, Tailwind CSS

### Plan Summary (plan.md excerpt)

```markdown
# Implementation Plan: Product Catalog

## Summary

Build searchable product catalog with filtering (category, price range, availability). Backend provides paginated REST API, frontend displays products with filters and search.

## Technical Context

**Language/Framework**: TypeScript/React 18 (frontend), TypeScript/Node.js (backend)
**Primary Dependencies**: React, Redux Toolkit, TailwindCSS, Express, TypeORM
**Storage**: PostgreSQL 15 + Elasticsearch (for search)
**Testing**: Vitest (frontend), Jest (backend), Playwright (E2E)
**Target Platform**: Modern browsers (Chrome/Firefox/Safari latest)
**Performance Goals**: <100ms search, <50ms filter, <2s initial load
**Constraints**: 10K products, 1000 concurrent users
**Scale/Scope**: Desktop + mobile responsive

## Constitution Check

### Violations & Justifications

| Constitution Rule | Violation | Why Needed | Alternative Rejected Because |
|-------------------|-----------|------------|------------------------------|
| PostgreSQL only | Adding Elasticsearch | Spec requires fuzzy search with <100ms response | PostgreSQL full-text search tested at 500ms with 10K products |
| No additional state management | Using Redux Toolkit | Complex filter state shared across 5 components | Context causes excessive re-renders (tested: 12 renders per filter change) |
```

### Research (research.md excerpt)

```markdown
## Research Areas

### Search Implementation

**Question:** How to achieve <100ms fuzzy search on 10K products?

**Options Considered:**

**Option A: PostgreSQL Full-Text Search**
- Pros: No additional infrastructure, ACID guarantees
- Cons: Slower (500ms tested), limited fuzzy search
- Complexity: Low
- Performance: ❌ Does not meet spec

**Option B: Elasticsearch**
- Pros: Fast (<50ms tested), powerful fuzzy search, faceted search
- Cons: Additional infrastructure, eventual consistency
- Complexity: Medium
- Performance: ✅ Exceeds spec requirement

**Option C: Algolia (SaaS)**
- Pros: Fastest (<10ms), managed service, typo tolerance
- Cons: Cost ($1/month per 1K records), vendor lock-in
- Complexity: Low
- Performance: ✅ Far exceeds spec

**Decision:** Elasticsearch

**Rationale:**
- Meets <100ms requirement with margin (50ms avg)
- Self-hosted (constitution prefers open source)
- Faceted search useful for filters (category counts)
- Team has Elasticsearch experience from other project

**Trade-offs Accepted:**
- Operational complexity (need to run/monitor ES cluster)
- Eventual consistency (acceptable - products update infrequently)

**Proof of Concept:**
- Indexed 10K products in local ES instance
- Ran 100 search queries: avg 47ms, p95 72ms
- Tested fuzzy search: "laptop" matches "labtop", "laptpo"
```

### Data Model (data-model.md excerpt)

```markdown
## Entities

### Product

**Purpose:** Represents sellable product in catalog

**Fields:**
```
id: UUID, primary key
sku: String, unique, required, max 50 chars, indexed
name: String, required, max 200 chars
description: Text, optional
categoryId: UUID, foreign key → Category.id
price: Decimal(10,2), required
currency: String(3), required, default 'USD'
inStock: Boolean, default true, indexed
stockCount: Integer, default 0
imageUrl: String, optional
createdAt: Timestamp
updatedAt: Timestamp
```

**Indexes:**
- sku (unique, btree) - Product lookup
- categoryId (btree) - Filter by category
- (inStock, categoryId) (composite) - Available products by category
- price (btree) - Price range filters

### Category

**Fields:**
```
id: UUID, primary key
name: String, unique, required
slug: String, unique, required, indexed
parentCategoryId: UUID, nullable, self-reference
```

**Relationships:**
- Category has many Products
- Category can have parent Category (nested categories)

## Elasticsearch Index

**products index mapping:**
```json
{
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "sku": { "type": "keyword" },
      "name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "fuzzy": {
            "type": "text",
            "analyzer": "trigram"
          }
        }
      },
      "description": { "type": "text" },
      "categoryId": { "type": "keyword" },
      "categoryName": { "type": "keyword" },
      "price": { "type": "scaled_float", "scaling_factor": 100 },
      "inStock": { "type": "boolean" }
    }
  }
}
```

**Sync strategy:**
- On product create/update → index to Elasticsearch (async)
- On product delete → remove from Elasticsearch
- Nightly full reindex (catch any missed updates)
```

---

## Example 3: Payment Integration (External Service Integration)

### Context
- **Spec**: Integrate Stripe for payment processing
- **Stack**: Node.js + Express + PostgreSQL
- **Constitution**: RESTful API, idempotent operations, webhook verification

### Plan Summary (plan.md excerpt)

```markdown
# Implementation Plan: Stripe Payment Integration

## Summary

Integrate Stripe for credit card payments. Support checkout flow, payment confirmation, and refunds. Handle webhooks for asynchronous payment updates.

## Security Considerations

**Authentication:**
- Stripe API key stored in environment variable (never committed)
- Webhook signature verification using Stripe's library

**Authorization:**
- Only authenticated users can create payments
- Users can only view their own payments
- Admins can issue refunds

**Data Protection:**
- Never store credit card numbers (handled by Stripe)
- Store only Stripe payment intent ID
- Log payment attempts with PII redacted

**Webhooks:**
- Verify webhook signature before processing
- Idempotent event handling (track processed events)
- Replay attack prevention (timestamp validation)

## Error Handling

### Payment Failures

**Client Errors (4xx):**
- 400 Bad Request: Invalid amount, currency
- 401 Unauthorized: Missing/invalid API key
- 402 Payment Required: Card declined
- 404 Not Found: Payment intent not found

**Server Errors (5xx):**
- 500 Internal: Stripe API error
- 503 Unavailable: Stripe API down (retry with backoff)

**Recovery Strategy:**

**Declined card:**
- User message: "Card declined. Please try another payment method."
- Log: Payment attempt, error code, user ID
- Recovery: User retries with different card

**Stripe API timeout:**
- User message: "Payment is processing. Check status in a moment."
- Log: Timeout, payment intent ID
- Recovery: Poll payment intent status, update async via webhook
```

### Research (research.md excerpt)

```markdown
### Idempotency Strategy

**Question:** How to handle duplicate payment requests (e.g., user clicks "Pay" twice)?

**Options Considered:**

**Option A: Idempotency keys (Stripe native)**
- Pros: Built into Stripe API, prevents duplicate charges
- Cons: Requires generating unique key per request
- Complexity: Low

**Option B: Database transaction locks**
- Pros: Prevents concurrent requests
- Cons: Doesn't prevent duplicate charge if Stripe call succeeds but response lost
- Complexity: Medium

**Option C: Request deduplication cache (Redis)**
- Pros: Fast, prevents backend work
- Cons: Cache miss still allows duplicates
- Complexity: Medium

**Decision:** Idempotency keys + database status check

**Implementation:**
```javascript
// Generate idempotency key from order ID + timestamp
const idempotencyKey = `order-${orderId}-${Date.now()}`;

// Stripe API call with idempotency key
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
}, {
  idempotencyKey,
});

// Store payment intent with status
await db.payments.create({
  orderId,
  stripePaymentIntentId: paymentIntent.id,
  status: 'processing',
});
```

**Trade-offs:**
- Idempotency key generation logic in backend
- Acceptable: Simple timestamp-based approach
```

---

## Example 4: Real-Time Notifications (WebSocket Feature)

### Context
- **Spec**: Real-time notifications when user receives messages
- **Stack**: Node.js + Express + Socket.io + Redis
- **Constitution**: WebSocket for real-time, Redis for pub/sub

### Plan Summary (plan.md excerpt)

```markdown
# Implementation Plan: Real-Time Notifications

## Architecture

### System Components

**WebSocket Server (Socket.io):**
- Purpose: Maintain persistent connections with clients
- Technology: Socket.io (WebSocket + polling fallback)
- Responsibilities: Client connection management, message delivery

**Redis Pub/Sub:**
- Purpose: Distribute notifications across server instances
- Technology: Redis 7
- Responsibilities: Message broker for horizontal scaling

**Notification Service:**
- Purpose: Business logic for creating notifications
- Technology: Node.js service
- Responsibilities: Validate, persist, publish notifications

### Component Interactions

```
[Client Browser] ←WebSocket→ [Socket.io Server 1] ←Redis Pub/Sub→ [Notification Service]
                                      ↓
                              [PostgreSQL Notifications]
                                      ↑
[Client Browser] ←WebSocket→ [Socket.io Server 2] ←Redis Pub/Sub→ [Same DB]
```

**Data Flow:**
1. User A sends message to User B
2. Message service creates notification
3. Notification service:
   - Persists to PostgreSQL
   - Publishes to Redis topic: `notifications:user:${userId}`
4. All Socket.io servers subscribed to topic receive event
5. Server with User B's connection emits notification via WebSocket
6. User B's browser displays notification

### Scalability

**Horizontal Scaling:**
- Multiple Socket.io servers behind load balancer
- Sticky sessions (same user → same server)
- Redis pub/sub broadcasts to all servers

**Connection Limits:**
- Each server: 10K concurrent connections
- Target: 50K users → 5 servers minimum

**Fallback for Lost Connections:**
- Client reconnects → fetch missed notifications from DB
- Cursor-based pagination for efficient sync
```

### Performance Strategy (plan.md excerpt)

```markdown
## Performance Strategy

**Targets:**
- Connection latency: <100ms
- Message delivery: <50ms after publish
- Missed notifications fetch: <200ms

**Optimization Techniques:**

1. **Redis Pub/Sub for Distribution**
   - Where: Cross-server message broadcast
   - Expected impact: 10ms message propagation
   - Alternative rejected: Database polling (500ms latency)

2. **Binary Protocol (MessagePack)**
   - What: Serialize notifications as MessagePack
   - Where: WebSocket messages
   - Expected impact: 60% smaller payload vs JSON
   - Alternative: JSON (slower parsing, larger size)

3. **Connection Pooling**
   - What: Reuse Redis connections
   - Pool size: 10 connections per server
   - Expected impact: Eliminate connection overhead

**Monitoring:**
- Metrics:
  - Active WebSocket connections per server
  - Message delivery latency (publish → client receive)
  - Redis pub/sub queue depth
  - Notification delivery success rate
- Alerts:
  - Message latency >100ms for 5 minutes
  - Failed deliveries >1% of total
  - Redis connection failures
```

---

## Example 5: Data Export (Background Job Feature)

### Context
- **Spec**: Export user data to CSV (GDPR compliance)
- **Stack**: Node.js + Bull (job queue) + Redis
- **Constitution**: Background jobs for long-running tasks, email notification on completion

### Plan Summary (plan.md excerpt)

```markdown
# Implementation Plan: Data Export

## Technical Context

**Language/Framework**: TypeScript/Node.js 18
**Primary Dependencies**: Bull (job queue), csv-writer, nodemailer
**Storage**: PostgreSQL (data source), S3 (export storage)
**Testing**: Jest with Bull mocks
**Target Platform**: Node.js background workers
**Performance Goals**: Export 100K records in <5 minutes
**Constraints**: GDPR 30-day response time, max 1GB file size
**Scale/Scope**: 10K users, avg 1K records per user

## Architecture

### Components

**Export API:**
- Endpoint: POST /api/v1/exports
- Creates export job, returns job ID
- Response: 202 Accepted

**Job Queue (Bull + Redis):**
- Queues export requests
- Processes serially (1 export at a time to avoid DB overload)
- Retry failed jobs (3 attempts with exponential backoff)

**Export Worker:**
- Fetches user data from PostgreSQL
- Streams to CSV file
- Uploads to S3 with expiring link (7 days)
- Sends email with download link

**S3 Storage:**
- Temporary storage for export files
- Pre-signed URLs for secure download
- Lifecycle policy: Delete after 7 days

### Data Flow

```
[User requests export] → [API creates job] → [Job queued in Redis]
                              ↓
                      [Worker picks up job]
                              ↓
                    [Stream data from PostgreSQL]
                              ↓
                      [Write CSV incrementally]
                              ↓
                      [Upload to S3]
                              ↓
                [Generate pre-signed URL]
                              ↓
              [Email user with download link]
```

## Error Handling

### Job Failures

**Database timeout:**
- Detection: Query exceeds 30s
- User impact: Export fails
- Recovery: Retry job (3 attempts)
- Logging: Error, user ID, row count processed

**S3 upload failure:**
- Detection: S3 API error
- User impact: Export created but not accessible
- Recovery: Retry upload, fallback to email attachment (if <10MB)
- Logging: Error, file size, bucket name

**Out of memory:**
- Detection: Node.js heap limit exceeded
- User impact: Export fails for large datasets
- Recovery: Batch processing (10K records per chunk)
- Logging: Error, user ID, memory usage

### User Notifications

**Success email:**
```
Subject: Your data export is ready
Body:
Your requested data export is now available for download:

[Download Link] (expires in 7 days)

This file contains all your data as of [timestamp].
```

**Failure email:**
```
Subject: Your data export failed
Body:
We encountered an error processing your export request.

Error: [User-friendly error message]

Please try again or contact support if the issue persists.
```
```

---

## Common Patterns Across Examples

### 1. Constitution Alignment
- Every example checks constitution first
- Violations are justified explicitly
- Trade-offs are documented

### 2. Research Before Design
- Unknowns identified early
- Options evaluated with pros/cons
- Decisions backed by evidence (benchmarks, docs)

### 3. Explicit Architecture
- Components named clearly
- Data flow diagrammed
- Integration points documented

### 4. Security Upfront
- Authentication/authorization planned
- Input validation defined
- PII handling specified

### 5. Performance Targets
- Specific metrics (p95 <Xms)
- Optimization techniques listed
- Monitoring plan included

### 6. Error Handling
- Failure modes identified
- Recovery strategies defined
- User impact considered

### 7. Testing Strategy
- TDD approach specified
- Test levels defined (unit, integration, E2E)
- Coverage targets set

### 8. Deployment Planning
- Environment variables documented
- Migration strategy defined
- Rollback procedure included

---

## Anti-Patterns to Avoid

### ❌ Vague Decisions
**Bad**: "We'll use the standard approach for auth"
**Good**: "JWT tokens with 15min expiry + 7day refresh, using jsonwebtoken library"

### ❌ Unresolved Unknowns
**Bad**: "Database choice: TBD"
**Good**: "PostgreSQL 15 - chosen for ACID guarantees and team expertise"

### ❌ No Alternatives Considered
**Bad**: "Using Redis for caching"
**Good**: "Compared Redis vs Memcached vs in-memory. Chose Redis for persistence and pub/sub support."

### ❌ Missing Justification for Constitution Violations
**Bad**: *Adds Elasticsearch without explanation*
**Good**: "Adding Elasticsearch (violates PostgreSQL-only rule) because full-text search requires <100ms response and PostgreSQL tested at 500ms with 10K records."

### ❌ Performance Without Numbers
**Bad**: "Should be fast enough"
**Good**: "Target <200ms p95 response time, achieving <150ms in local benchmark"

### ❌ Security Checklist Mentality
**Bad**: "✅ Security considered"
**Good**: "Input validation with Joi schema, SQL injection prevention via parameterized queries, bcrypt for passwords with cost factor 10"

---

## Summary

**Key Takeaways:**

1. **Start with constitution** - Align or justify deviations
2. **Research unknowns** - Don't guess, investigate
3. **Be explicit** - Name patterns, tools, approaches
4. **Show your work** - Document options, rationale, trade-offs
5. **Plan for failure** - Error handling, monitoring, rollback
6. **Test-driven** - Define testing strategy upfront
7. **Security first** - Not an afterthought

These examples demonstrate comprehensive planning that sets up implementation for success.
