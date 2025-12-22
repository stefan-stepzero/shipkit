# Implementation Planning - Extended Reference

**Purpose**: This guide helps you create comprehensive implementation plans that translate feature specifications into actionable technical designs.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Planning Workflow](#planning-workflow)
4. [Constitution Compliance](#constitution-compliance)
5. [Constitution Check](#constitution-check)
6. [Architecture Decisions](#architecture-decisions)
7. [Performance Considerations](#performance-considerations)
8. [Security Planning](#security-planning)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Considerations](#deployment-considerations)
11. [Handoff to dev-tasks](#handoff-to-dev-tasks)
12. [Common Pitfalls](#common-pitfalls)
13. [Quality Checklist](#quality-checklist)
14. [Tips for Success](#tips-for-success)
15. [References](#references)

---

## Overview

The dev-plan skill bridges the gap between "what to build" (spec) and "how to execute" (tasks). It produces a complete technical blueprint that guides implementation while respecting established architectural standards.

**Input**: Feature specification (spec.md) + Technical constitution (constitution.md)
**Output**: Plan artifacts (plan.md, data-model.md, research.md, contracts/, quickstart.md)

---

## Core Principles

### 1. Constitution-Driven Design

**Every plan must align with the technical constitution.**

The constitution defines:
- Approved technology stack
- Architectural patterns
- Coding standards
- Testing requirements
- Performance targets
- Security standards

**Before making any technical decision, ask:**
- Does this align with constitution patterns?
- If not, is there a justified reason to deviate?
- Have I documented the violation and trade-off?

### 2. Research Before Design

**Don't guess unknowns - research them.**

If Technical Context has "NEEDS CLARIFICATION":
1. Stop design work
2. Enter Phase 0 (Research)
3. Web search, read docs, review examples
4. Document decisions in research.md
5. Resume design with concrete answers

**Red flags:**
- "We'll figure it out during implementation"
- "Probably works like X" (without verification)
- "Let's try Y and see" (without research)

### 3. Explicit Over Implicit

**Make everything explicit in the plan.**

- Don't assume readers know your reasoning
- Document trade-offs openly
- Explain WHY, not just WHAT
- Link to sources for technical decisions

---

## Planning Workflow

### Phase 0: Research & Unknowns

**Goal**: Resolve all "NEEDS CLARIFICATION" items before design.

**Process**:

1. **Scan Technical Context** for unknowns:
   - What language/framework? (if not in constitution)
   - What storage technology?
   - What testing approach?
   - What performance targets? (if not in spec)

2. **For each unknown, create research task**:
   - Question: What needs deciding?
   - Options: What are the alternatives?
   - Research: What sources to check?

3. **Execute research** (use web search, read docs):
   - Official documentation (highest priority)
   - Community best practices (Stack Overflow, GitHub)
   - Performance benchmarks (if relevant)
   - Team expertise (if available)

4. **Document in research.md**:
   - Decision made
   - Rationale (why this choice)
   - Alternatives considered (why rejected)
   - Trade-offs accepted
   - Sources cited

**Example research entry**:

```markdown
### State Management Solution

**Question:** How should we manage complex form state with multi-step wizard?

**Options Considered:**

**Option A: Redux Toolkit**
- Pros: Predictable state, time-travel debugging, large ecosystem
- Cons: Boilerplate overhead, learning curve, overkill for simple forms
- Complexity: Medium
- Team familiarity: High (used in 3 other projects)

**Option B: React Hook Form**
- Pros: Minimal re-renders, built-in validation, smaller bundle size
- Cons: Less suited for complex cross-step dependencies
- Complexity: Low
- Team familiarity: Medium (used once)

**Option C: Context + useReducer**
- Pros: No dependencies, simple, built into React
- Cons: Manual optimization needed, no devtools
- Complexity: Medium
- Team familiarity: High (React core concept)

**Decision:** React Hook Form + Context for shared wizard state

**Rationale:**
- Form validation is primary need (RHF excels here)
- Wizard state is simple (prev/next/current step) → Context sufficient
- Reduces bundle size vs Redux (spec requirement: <500KB initial load)
- Team can learn remaining 20% of RHF quickly

**Trade-offs Accepted:**
- Less sophisticated devtools than Redux
- Manual work for cross-step validation (acceptable - only 2 cases)

**Sources:**
- React Hook Form docs: https://react-hook-form.com/
- Performance comparison: https://github.com/bvaughn/react-form-benchmark
```

### Phase 1: Design & Contracts

**Goal**: Create detailed technical artifacts that guide implementation.

**Process**:

1. **Data Model Design** (data-model.md):

   **Start with entities from spec**:
   - Read functional requirements
   - Identify nouns → candidate entities
   - Identify relationships between entities
   - Define fields based on requirements
   - Add validation rules from spec
   - Consider state transitions (if applicable)

   **Example**:
   ```markdown
   ### User Entity

   **Purpose:** Represents authenticated user with profile

   **Fields:**
   ```
   id: UUID, primary key, auto-generated
   email: String, unique, required, indexed
   passwordHash: String, required (never expose in API)
   firstName: String, required, max 50 chars
   lastName: String, required, max 50 chars
   role: Enum ['user', 'admin'], default 'user'
   createdAt: Timestamp, default now()
   updatedAt: Timestamp, auto-update
   ```

   **Constraints:**
   - Unique: email (lowercase before save)
   - Index: email (for login lookup <10ms)
   - Validation: email must be RFC 5322 format
   - Security: passwordHash uses bcrypt (per constitution)

   **Relationships:**
   - Has many: Articles
   - Has many: Comments
   ```

   **Add indexes for performance**:
   - What queries will be frequent? (from spec user stories)
   - Index foreign keys for joins
   - Add composite indexes for common filters
   - Document expected query performance

2. **API Contract Generation** (contracts/):

   **Extract endpoints from requirements**:
   - Each user action → API endpoint
   - Follow REST or GraphQL conventions (from constitution)
   - Use standard HTTP methods (GET, POST, PUT, DELETE)
   - Define request/response shapes
   - Document error responses

   **OpenAPI example** (contracts/auth-api.yaml):
   ```yaml
   openapi: 3.0.0
   info:
     title: Authentication API
     version: 1.0.0
   paths:
     /api/v1/auth/login:
       post:
         summary: Authenticate user
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
         responses:
           '200':
             description: Login successful
             content:
               application/json:
                 schema:
                   type: object
                   properties:
                     token:
                       type: string
                     user:
                       $ref: '#/components/schemas/User'
           '401':
             description: Invalid credentials
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/Error'
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
           role:
             type: string
             enum: [user, admin]
       Error:
         type: object
         properties:
           code:
             type: string
           message:
             type: string
   ```

3. **Quickstart Guide** (quickstart.md):

   **Purpose**: Help developers build and test the feature

   **Contents**:
   - Prerequisites (what to install)
   - Installation instructions
   - How to run locally
   - How to test (manual + automated)
   - Example API calls (curl/http)
   - Expected responses
   - Common troubleshooting

   **Example structure**:
   ```markdown
   # Quickstart: User Authentication

   ## Prerequisites
   - Node.js 18+
   - PostgreSQL 15+
   - Redis (optional, for sessions)

   ## Setup
   ```bash
   # Install dependencies
   npm install

   # Setup database
   npm run db:migrate

   # Start services
   npm run dev
   ```

   ## Testing

   ### Register new user
   ```bash
   curl -X POST http://localhost:3000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Password123!","firstName":"Test","lastName":"User"}'
   ```

   Expected response:
   ```json
   {
     "token": "eyJhbGciOiJIUzI1NiIs...",
     "user": {
       "id": "550e8400-e29b-41d4-a716-446655440000",
       "email": "test@example.com",
       "firstName": "Test",
       "lastName": "User"
     }
   }
   ```
   ```

4. **Plan Document** (plan.md):

   **Purpose**: High-level technical blueprint

   **Key sections**:
   - **Summary**: 1-2 sentence feature overview
   - **Technical Context**: Stack, dependencies, constraints
   - **Constitution Check**: Alignment verification
   - **Architecture Overview**: Components, data flow
   - **Technical Decisions**: Key choices and trade-offs
   - **Security Considerations**: Auth, validation, PII
   - **Performance Strategy**: Targets, optimizations
   - **Testing Strategy**: TDD approach, coverage
   - **Deployment**: Environment vars, migrations, rollback

   **Keep it high-level**:
   - Don't include code samples (those go in templates/examples)
   - Focus on WHY and WHAT, not HOW
   - Reference other artifacts (data-model.md, contracts/)

---

## Constitution Compliance

### Before Planning

**Read the constitution first:**
- File: `.shipkit/skills/dev-constitution/outputs/constitution.md`
- Understand: Stack, patterns, standards, constraints

### During Planning

**Validate each decision against constitution:**
- Does this follow approved patterns?
- Are we using approved libraries?
- Do we meet security requirements?
- Are performance targets defined?

### Constitution Check Section

**In plan.md, document alignment:**

```markdown
## Constitution Check

### Alignment with Standards

**Architectural Patterns**:
- [x] Follows Controller → Service → Repository pattern
- [x] Respects module boundaries
- [x] Uses dependency injection

**Technology Stack**:
- [x] Node.js 18 with TypeScript (approved)
- [x] PostgreSQL 15 with TypeORM (approved)
- [x] Jest for testing (approved)

**Coding Standards**:
- [x] ESLint with Airbnb config
- [x] Prettier with 2-space indent
- [x] Absolute imports using @/ alias

**Testing Requirements**:
- [x] TDD approach planned
- [x] 80% coverage target (meets minimum)
- [x] Arrange-Act-Assert pattern

**API Conventions**:
- [x] RESTful design with resource URLs
- [x] JWT authentication (matches existing)
- [x] RFC 7807 error format

**Performance Requirements**:
- [x] Target: <200ms p95 response time (meets spec)
- [x] Database indexes for frequent queries
- [x] No N+1 query patterns

**Security Standards**:
- [x] Input validation with Joi
- [x] Bcrypt for password hashing
- [x] SQL injection prevention (parameterized queries)

### Violations & Justifications

*None - plan aligns with all constitution requirements*
```

**If there are violations:**

```markdown
### Violations & Justifications

| Constitution Rule | Violation | Why Needed | Alternative Rejected Because |
|-------------------|-----------|------------|------------------------------|
| Max 3 architectural layers | Adding 4th layer (API Gateway) | Need rate limiting + API key management | Implementing in controller would bloat code, harder to test |
| PostgreSQL only | Adding Redis for caching | Spec requires <100ms p95, DB alone can't meet it | Calculated caching needed for 200 req/s load |
```

**Justify violations clearly:**
- Why is this needed? (specific requirement from spec)
- What simpler alternative was considered?
- Why was it rejected? (concrete reason)

---

## Architecture Decisions

### Decision Framework

**For each significant choice, document:**

1. **Options Considered**: List 2-3 alternatives (minimum)
2. **Chosen Solution**: What you picked
3. **Rationale**: Why this over others
4. **Trade-offs**: What you're gaining/losing
5. **Reversibility**: How hard to change later

**Example**:

```markdown
**Decision: API Authentication Approach**

**Options Considered:**
- Option A: Session cookies
- Option B: JWT tokens
- Option C: OAuth2

**Chosen:** JWT tokens

**Rationale:**
- Stateless (enables horizontal scaling per spec)
- Mobile app support (spec requirement)
- Expires automatically (security best practice)
- Constitution specifies JWT as approved

**Trade-offs:**
- Can't revoke token before expiry (acceptable - use short expiry + refresh tokens)
- Slightly larger payload than session ID (acceptable - <1KB)

**Reversibility:** Medium
- Would require session store infrastructure
- Client code changes needed
- Estimate: 3-4 days to migrate
```

### Common Decision Areas

**Technology Choices:**
- State management (Redux, Context, Zustand, Jotai)
- Data fetching (fetch, axios, react-query, SWR)
- Validation (Joi, Yup, Zod, class-validator)
- Testing (Jest, Vitest, Testing Library)

**Architecture Patterns:**
- Layering (MVC, Clean Architecture, Hexagonal)
- Data access (Active Record, Repository, DAO)
- Dependency management (DI, Service Locator, Manual)

**Infrastructure:**
- Caching (Redis, Memcached, in-memory, CDN)
- Storage (SQL, NoSQL, Object Store, Files)
- Deployment (VMs, Containers, Serverless)

---

## Performance Considerations

### Define Targets (from spec)

**Response time:**
- p50: <Xms (median)
- p95: <Yms (95th percentile)
- p99: <Zms (99th percentile)

**Throughput:**
- Requests/second: X
- Concurrent users: Y

**Resource limits:**
- Max memory: X MB
- Max CPU: Y%
- Max storage: Z GB

### Plan Optimizations

**Database:**
- Indexes on frequent query fields
- Connection pooling (size based on load)
- Read replicas for read-heavy workloads
- Pagination for large result sets

**Caching:**
- What to cache: Frequent, expensive, static data
- Where: Redis, CDN, in-memory
- TTL: Based on data volatility
- Invalidation: Write-through, write-around

**Frontend:**
- Code splitting (lazy load routes/components)
- Image optimization (WebP, lazy load, CDN)
- Bundle size limits (from constitution)

### Monitoring Plan

**What to track:**
- Response times (p50, p95, p99)
- Error rates (by endpoint)
- Database query times
- Cache hit rates
- Resource usage (CPU, memory, disk)

**When to alert:**
- p95 exceeds target +20%
- Error rate >1%
- Cache hit rate <80%

---

## Security Planning

### Authentication

**Approach:** [From constitution]
- JWT, OAuth2, Session cookies, API keys

**Implementation:**
- Where to enforce (middleware, decorator, service)
- Token storage (HTTP-only cookies, localStorage, memory)
- Expiry policy (short-lived + refresh tokens)

### Authorization

**Model:**
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Custom (rules engine)

**Enforcement:**
- Where: Controller, service layer, database (RLS)
- How: Decorators, middleware, policy objects

### Input Validation

**What to validate:**
- Request parameters (query, path, body)
- File uploads (type, size, content)
- Headers (content-type, authorization)

**How to validate:**
- Schema validation (Joi, Yup, Zod)
- Sanitization (DOMPurify, validator.js)
- Whitelist over blacklist

### Data Protection

**At rest:**
- Encrypt sensitive fields (PII, secrets)
- Use database encryption (TDE)
- Secure key management (KMS, Vault)

**In transit:**
- TLS 1.2+ for all connections
- Certificate pinning (mobile apps)
- Secure headers (HSTS, CSP)

**PII Handling:**
- Minimize collection (only what's needed)
- Anonymize in logs
- Retention policy (delete after X days)
- Compliance (GDPR, CCPA)

---

## Testing Strategy

### TDD Approach

**For every task:**

1. **RED**: Write failing test first
   - Describe desired behavior
   - Run test → verify it fails
   - Commit to failing test before implementation

2. **GREEN**: Write minimal code to pass
   - Simplest implementation that works
   - No premature optimization
   - Run test → verify it passes

3. **REFACTOR**: Clean up while tests pass
   - Improve structure
   - Remove duplication
   - Run tests → verify still passing

### Test Levels

**Unit Tests:**
- **What**: Pure functions, business logic, models
- **Coverage**: 80%+ (from constitution)
- **Tools**: [From constitution, e.g., Jest, Vitest]
- **Speed**: <100ms per test file

**Integration Tests:**
- **What**: API endpoints, database operations, external APIs
- **Coverage**: All user-facing endpoints
- **Tools**: [Supertest, MSW, Test Containers]
- **Speed**: <5s per test file

**E2E Tests:**
- **What**: Critical user flows from spec
- **Coverage**: Happy path + key error scenarios
- **Tools**: [Playwright, Cypress, Selenium]
- **Speed**: <30s per test

### Test Data Strategy

**Fixtures:**
- Predefined test data (users.json, articles.json)
- Version controlled
- Loaded before tests

**Factories:**
- Generate random test data
- Libraries: faker.js, factory-bot
- Useful for fuzz testing

**Database Isolation:**
- Strategy 1: Transactions (rollback after test)
- Strategy 2: Separate DB per test file
- Strategy 3: In-memory database (SQLite)

---

## Deployment Considerations

### Environment Variables

**Document all required vars:**

```markdown
**Required:**
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Token signing key (32+ chars random)
- `REDIS_URL`: Redis connection string (optional)

**Optional:**
- `LOG_LEVEL`: debug|info|warn|error (default: info)
- `PORT`: Server port (default: 3000)
```

### Database Migrations

**Forward migration:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Rollback migration:**
```sql
DROP TABLE IF EXISTS users CASCADE;
```

**Testing:**
- Apply on staging first
- Verify data integrity
- Test rollback procedure
- Document expected downtime

### Rollback Plan

**When to rollback:**
- Critical bug discovered in production
- Performance degradation >20%
- Error rate >5%

**How to rollback:**
1. Revert to previous deployment
2. Run down migrations (if schema changed)
3. Monitor for stabilization
4. Post-mortem: What went wrong?

**Time target:** <10 minutes from decision to rollback complete

---

## Handoff to dev-tasks

**After planning is complete:**

1. Review all artifacts:
   - [ ] plan.md complete
   - [ ] research.md complete
   - [ ] data-model.md complete
   - [ ] contracts/ complete
   - [ ] quickstart.md complete
   - [ ] Constitution check passed

2. Run `/dev-tasks` to generate task breakdown

3. Tasks skill will:
   - Read this plan
   - Read spec.md
   - Read constitution.md
   - Generate dependency-ordered tasks
   - Include TDD test tasks
   - Mark parallel vs sequential execution

---

## Common Pitfalls

### 1. Skipping Research Phase

**Symptom:** "NEEDS CLARIFICATION" still in plan.md

**Problem:** Plan is incomplete, will cause rework during implementation

**Solution:** Don't skip Phase 0. Research unknowns thoroughly.

### 2. Constitution Violations Unjustified

**Symptom:** Using unapproved library without explanation

**Problem:** Technical debt, inconsistency with codebase

**Solution:** Either align with constitution OR document justification

### 3. Vague Architecture Decisions

**Symptom:** "We'll use the standard approach"

**Problem:** Ambiguous, different developers interpret differently

**Solution:** Be explicit. Name the pattern. Link to examples.

### 4. Missing Performance Targets

**Symptom:** No response time or throughput goals

**Problem:** Can't validate implementation success

**Solution:** Extract from spec. If missing, ask user for targets.

### 5. Security as Afterthought

**Symptom:** Security section says "TBD" or "Standard security"

**Problem:** Vulnerabilities discovered late

**Solution:** Plan security upfront. Validate, sanitize, encrypt, audit.

### 6. No Test Strategy

**Symptom:** "We'll write tests" without specifics

**Problem:** Tests skipped or incomplete

**Solution:** Define test levels, coverage targets, TDD approach

---

## Quality Checklist

Before considering plan complete:

- [ ] All "NEEDS CLARIFICATION" resolved
- [ ] Constitution check complete (violations justified)
- [ ] Technical decisions documented (options, rationale, trade-offs)
- [ ] Data model defined (entities, relationships, indexes)
- [ ] API contracts created (OpenAPI/GraphQL)
- [ ] Security considerations addressed
- [ ] Performance targets defined
- [ ] Testing strategy planned (TDD, levels, coverage)
- [ ] Deployment steps documented
- [ ] Quickstart guide created
- [ ] References to spec and constitution included

---

## Tips for Success

**Start with unknowns:**
- Front-load research (Phase 0)
- Don't guess, investigate
- Document sources

**Think dependencies:**
- What needs to exist first?
- What can be built in parallel?
- Where are integration points?

**Design for testing:**
- How will you test this?
- Can components be tested in isolation?
- What's the happy path? Error cases?

**Favor simplicity:**
- Complexity has a cost
- Choose boring technology (proven patterns)
- Justify anything novel

**Document trade-offs:**
- Every decision has pros/cons
- Be honest about what you're sacrificing
- Explain why it's acceptable

---

## References

- **Spec Template**: `.shipkit/skills/dev-specify/templates/spec-template.md`
- **Constitution Template**: `.shipkit/skills/dev-constitution/templates/constitution-template.md`
- **OpenAPI Specification**: https://swagger.io/specification/
- **GraphQL Schema Language**: https://graphql.org/learn/schema/
- **C4 Model** (architecture diagrams): https://c4model.com/
- **ADR Template** (architecture decisions): https://github.com/joelparkerhenderson/architecture-decision-record
