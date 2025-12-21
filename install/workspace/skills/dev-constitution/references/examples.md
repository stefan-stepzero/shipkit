# Technical Constitution Examples

Three complete examples showing constitutions at different product stages.

---

## Example 1: POC - AI Meeting Summarizer

**Context:** Early prototype, 2-week sprint, proving concept

### Technical Constitution

**Product:** MeetingMind AI
**Stage:** POC
**Last Updated:** 2025-01-15

#### 1. Technical Principles

**Architecture:**
- Single-service monolith
- Synchronous, request-response only
- No distributed systems

**Design:**
- Flat module structure
- Direct dependencies OK for POC
- Optimize for iteration speed

**Code Quality:**
- Readable over clever
- TODO comments allowed
- Tech debt acceptable if documented

#### 2. Constraints & Non-Negotiables

**Must Have:**
- End-to-end working demo
- API key security (env vars)
- Basic error handling

**Must Avoid:**
- Over-engineering
- Premature abstractions
- Complex state management

#### 3. Tech Stack

**Core Technologies:**
- Python 3.11: Fast prototyping, great AI libs
- FastAPI: Modern, auto-docs, async support
- OpenAI API: GPT-4 for summarization
- SQLite: Zero-config persistence

**Rationale:** Speed to demo. Use team's Python expertise. Avoid infrastructure complexity.

#### 4. Quality Standards

**Testing:**
- Manual testing acceptable
- Automated tests for critical path only (upload → summarize → download)

**Performance:**
- <30s for 1hr meeting (acceptable for demo)
- No load testing required

**Security:**
- HTTPS only
- API keys in environment
- No public exposure (demo only)

#### 5. Development Workflow

**Branching:** Main only, commit directly
**Reviews:** Pair programming optional
**CI/CD:** None (manual deploy to demo env)
**Documentation:** README with setup steps

---

## Example 2: MVP - SaaS Task Manager

**Context:** Launching to first 100 customers, 3-month runway

### Technical Constitution

**Product:** TaskFlow Pro
**Stage:** MVP
**Last Updated:** 2025-01-15

#### 1. Technical Principles

**Architecture:**
- Modular monolith with clear domain boundaries
- Prepare for future microservices split
- Event bus for internal communication

**Design:**
- Dependency injection for testability
- Repository pattern for data access
- Service layer for business logic
- SOLID principles (especially SRP, OCP)

**Code Quality:**
- Self-documenting code preferred
- Comments explain "why", not "what"
- No dead code or commented-out blocks
- Consistent naming conventions

#### 2. Constraints & Non-Negotiables

**Must Have:**
- 99% uptime target
- <200ms API response time (p95)
- GDPR compliance (EU users)
- Mobile-responsive UI

**Must Avoid:**
- Framework lock-in (use standard interfaces)
- N+1 database queries
- Blocking operations in request path
- Tight coupling between domains

#### 3. Tech Stack

**Core Technologies:**
- TypeScript/Node.js: Type safety + team expertise
- Next.js: SSR, SEO, built-in API routes
- PostgreSQL: ACID, complex queries, proven
- Redis: Session store, caching
- AWS ECS: Managed containers, no K8s complexity

**Rationale:** Balanced pragmatism with quality. TypeScript prevents bugs. PostgreSQL handles relational data well. ECS simpler than K8s for MVP scale.

#### 4. Quality Standards

**Testing:**
- 80% code coverage minimum
- TDD for business logic
- Integration tests for API endpoints
- E2E tests for critical user flows

**Performance:**
- Monitor p50/p95/p99 latency
- Database query <50ms target
- CDN for static assets
- Lazy loading for heavy UI components

**Security:**
- OWASP Top 10 compliance
- Automated dependency scanning (Snyk)
- Input validation on all endpoints
- Rate limiting on auth endpoints

#### 5. Development Workflow

**Branching:** Feature branches, squash merge to main
**Reviews:** Required, 1 approval, automated checks must pass
**CI/CD:**
- Tests + lint + type check must pass
- Deploy to staging on PR
- Manual promotion to production
**Documentation:** API docs (OpenAPI), architecture diagrams

---

## Example 3: Established - Fintech Platform

**Context:** 50K daily active users, regulated industry, 10-person team

### Technical Constitution

**Product:** PayStream
**Stage:** Established
**Last Updated:** 2025-01-15

#### 1. Technical Principles

**Architecture:**
- Microservices with domain-driven design
- Event-driven architecture (async communication)
- API gateway for external traffic
- CQRS where read/write patterns differ

**Design:**
- Interface segregation (small, focused contracts)
- Hexagonal architecture (ports & adapters)
- Immutable data structures where possible
- Fail fast with circuit breakers

**Code Quality:**
- Production-grade only (no shortcuts)
- Defensive programming (validate everything)
- Explicit error types (no silent failures)
- Comprehensive logging (structured JSON)

#### 2. Constraints & Non-Negotiables

**Must Have:**
- 99.99% uptime SLA
- SOC2 Type II compliance
- PCI DSS for card data
- Audit trail for all transactions
- Multi-region failover

**Must Avoid:**
- Synchronous service-to-service calls
- Shared databases across services
- Mutable shared state
- Single points of failure

#### 3. Tech Stack

**Core Technologies:**
- Go: Performance, concurrency, small binaries
- gRPC: Type-safe service communication
- PostgreSQL: ACID for financial transactions
- Redis: Distributed cache, session store
- Kafka: Event streaming, audit log
- Kubernetes: Orchestration, zero-downtime deploys
- AWS: Multi-region, managed services

**Rationale:** Go's concurrency fits event-driven model. gRPC enforces contracts. PostgreSQL's ACID guarantees critical for money. Kafka provides event sourcing for audit. K8s enables sophisticated deployment strategies.

#### 4. Quality Standards

**Testing:**
- 90% code coverage
- TDD required
- Contract tests for all service boundaries
- Chaos engineering (monthly game days)
- Canary testing in production

**Performance:**
- p99 <100ms for API calls
- Horizontal autoscaling (2-20 pods per service)
- Database connection pooling
- Query optimization (no full table scans)
- Load testing before major releases

**Security:**
- Zero-trust networking
- Encryption at rest and in transit
- Secret rotation (30-day cycle)
- Penetration testing (quarterly)
- Security code review for auth changes
- Automated vulnerability scanning

#### 5. Development Workflow

**Branching:** Trunk-based development with feature flags
**Reviews:** 2 approvals required, CODEOWNERS enforced
**CI/CD:**
- Full test suite + static analysis
- Automated security scan (SAST/DAST)
- Blue-green deployments
- Automated rollback on error rate spike
- Deploy windows (business hours only)
**Documentation:**
- RFC process for architectural changes
- Runbooks for operational procedures
- OpenAPI specs for all APIs
- Architecture decision records (ADRs)

---

## Key Differences by Stage

| Aspect | POC | MVP | Established |
|--------|-----|-----|-------------|
| **Length** | ~200 words | ~350 words | ~500 words |
| **Architecture** | Simple monolith | Modular monolith | Microservices |
| **Testing** | Manual + critical path | 80% coverage, TDD | 90% coverage, chaos tests |
| **Performance** | "Good enough" | Monitored, <200ms | SLA-driven, <100ms |
| **Security** | Basic (HTTPS, env vars) | OWASP, automated scans | Compliance, pen tests |
| **Deployment** | Manual | Automated to staging | Blue-green, canaries |
| **Trade-off** | Speed > everything | Balance | Reliability > speed |

---

## Anti-Examples (What NOT to Do)

### ❌ Too Generic (Useless)

```markdown
## Technical Principles
- Write clean code
- Follow best practices
- Be pragmatic
- Test your code
```

**Why bad:** Could apply to any project. Gives no actual guidance.

### ❌ Too Detailed (Wrong Level)

```markdown
## API Response Format
All endpoints return:
{
  "status": "success" | "error",
  "data": { ... },
  "pagination": {
    "page": number,
    "perPage": number,
    "total": number
  },
  "meta": {
    "requestId": string,
    "timestamp": ISO8601
  }
}
```

**Why bad:** This belongs in API specs (dev-plan), not constitution.

### ❌ Not Product-Aware (Disconnected)

```markdown
## Tech Stack
- Microservices architecture
- Kubernetes orchestration
- GraphQL APIs
- Event sourcing with CQRS
```

**Why bad:** No rationale. Might be over-engineering for a POC.

### ❌ Too Long (Token Waste)

A 2000-word constitution that explains every design pattern, lists every library version, includes code examples...

**Why bad:** Wastes tokens in every dev skill invocation. Details belong in references or emerge through workflow.

---

## Template Usage Tips

### Fill Every Section Meaningfully

❌ **Lazy:**
```markdown
## 1. Technical Principles
**Architecture:** TBD
**Design:** TBD
**Code Quality:** TBD
```

✅ **Useful:**
```markdown
## 1. Technical Principles
**Architecture:** Monolith for now. Split when team >5 or services >3.
**Design:** Composition over inheritance. Interfaces for testing.
**Code Quality:** Readable > clever. No magic.
```

### Use Rationale to Ground Decisions

❌ **No context:**
```markdown
**Tech Stack:**
- React
- PostgreSQL
- Docker
```

✅ **Justified:**
```markdown
**Tech Stack:**
- React: Team expertise + rich ecosystem
- PostgreSQL: Relational data + complex queries
- Docker: Consistent dev/prod environments
```

### Match Product Stage

❌ **POC with enterprise requirements:**
```markdown
**Stage:** POC
**Quality Standards:**
- 99.99% uptime
- SOC2 compliance
- Automated canary deployments
```

✅ **POC-appropriate:**
```markdown
**Stage:** POC
**Quality Standards:**
- Works for demo
- Basic error handling
- Manual testing OK
```
