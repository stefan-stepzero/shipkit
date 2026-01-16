# Technical Constitution Reference

## Purpose

The technical constitution defines **high-level** architecture, design, and coding principles for your product. It's consumed by all dev skills (specify, plan, tasks, implement) to ensure consistency.

**Key principle:** LEAN and HIGH-LEVEL. Details emerge through the dev workflow.

---

## What Goes in a Constitution

### 1. Technical Principles (Architecture, Design, Code Quality)

**Architecture principles** - How systems are organized:
- Monolith vs microservices
- Layering/separation of concerns
- Data flow patterns
- Scaling approach

**Design principles** - How code is structured:
- Composition over inheritance
- Dependency injection
- SOLID principles relevant to your stack
- Error handling philosophy

**Code quality principles** - What good code looks like:
- Readability standards
- DRY/KISS/YAGNI priorities
- Comment/documentation approach
- Naming conventions

### 2. Constraints & Non-Negotiables

**Must have:**
- Security requirements
- Compliance needs
- Performance targets
- Accessibility standards

**Must avoid:**
- Known anti-patterns for your stack
- Deprecated technologies
- Over-engineering traps
- Common footguns

### 3. Tech Stack

List core technologies with **brief** rationale:
- Language/framework (why this one?)
- Database (why this one?)
- Infrastructure (why this setup?)

**Match product stage:**
- POC: Speed over scalability
- MVP: Balance pragmatism with quality
- Established: Optimize for maintenance

### 4. Quality Standards

**Testing:**
- Minimum coverage (e.g., 80% for critical paths)
- Required test types (unit, integration, e2e)
- TDD/test-after policy

**Performance:**
- Key metrics (latency, throughput)
- Acceptable ranges
- Monitoring approach

**Security:**
- Authentication/authorization approach
- Data protection requirements
- Vulnerability scanning

### 5. Development Workflow

**Branching:** Feature branches? Trunk-based?
**Reviews:** Who reviews? What's required?
**CI/CD:** What checks must pass?
**Documentation:** What must be documented?

---

## Token Efficiency Strategies

**Target: <500 words total**

### Be Concise
❌ **Verbose:**
> "We believe that readability is of paramount importance and should be the primary consideration when writing code. Therefore, developers should always prioritize clear, self-documenting code that can be easily understood by other team members."

✅ **Concise:**
> "Readability first. Self-documenting code preferred."

### Use Lists, Not Prose
❌ **Wordy:**
> "Our architecture follows a three-tier pattern where the presentation layer communicates with the business logic layer, which in turn interacts with the data access layer. This separation ensures that concerns are properly isolated."

✅ **Bulleted:**
> **Architecture:** Three-tier (presentation → logic → data). Strict layer boundaries.

### Link, Don't Explain
❌ **Redundant:**
> "SOLID principles should be followed. Specifically, the Single Responsibility Principle states that a class should have only one reason to change. The Open/Closed Principle..."

✅ **Reference:**
> **Design:** Follow SOLID principles (especially SRP, DIP).

### Defer Details
❌ **Too specific:**
> "All API endpoints must return JSON responses with the following structure: { status: 'success' | 'error', data: any, message: string, timestamp: ISO8601 }. Errors should use HTTP status codes 400 for client errors..."

✅ **High-level:**
> **API:** REST, JSON responses. Standard HTTP codes. (Details in API contracts via dev-plan)

---

## Extracting from Product Artifacts

### From User Stories
**Extract:**
- Tech stack hints (mobile app → React Native?)
- Performance needs (real-time collaboration?)
- Security requirements (payment processing?)
- Accessibility needs (mentioned users?)

**Example:**
User story mentions "Works offline" → Constitution includes "Offline-first architecture" principle

### From Strategy (Business Canvas)
**Extract:**
- Product stage (POC/MVP/Established)
- Scale expectations
- Cost constraints
- Time-to-market pressure

**Example:**
Strategy says "Launch in 6 weeks" → Constitution emphasizes "Speed over perfection. Pragmatic choices."

### From Success Metrics
**Extract:**
- Performance targets
- Reliability requirements
- Scalability needs

**Example:**
Metric: "99.9% uptime" → Constitution includes "Fault tolerance required. Circuit breakers, retries."

### From Assumptions & Risks
**Extract:**
- Technical risks to mitigate
- Constraints to encode

**Example:**
Risk: "Team unfamiliar with GraphQL" → Constitution says "REST API. Stick to team's strengths."

---

## Examples by Product Stage

### POC Constitution (Minimal)
```markdown
## Technical Principles
**Architecture:** Monolith. Ship fast.
**Design:** Simple > clever.
**Code Quality:** Readable, tested critical paths only.

## Constraints
**Must Have:** Works end-to-end.
**Must Avoid:** Premature optimization.

## Tech Stack
- Python/Flask: Fast prototyping
- SQLite: Zero setup
- Heroku: One-click deploy

## Quality Standards
**Testing:** Critical user flows only.
**Performance:** "Good enough" for demo.
**Security:** Basic (auth, HTTPS).

## Development Workflow
**Branching:** Main only.
**Reviews:** Optional.
**CI/CD:** Deploy to staging on push.
```

### MVP Constitution (Balanced)
```markdown
## Technical Principles
**Architecture:** Layered monolith. Clear boundaries for future splitting.
**Design:** Composition over inheritance. Explicit dependencies.
**Code Quality:** Self-documenting. Comments for "why", not "what".

## Constraints
**Must Have:** 99% uptime, sub-200ms p95 latency.
**Must Avoid:** Framework lock-in, vendor lock-in.

## Tech Stack
- Node.js/Express: Team expertise
- PostgreSQL: Relational data, proven reliability
- AWS ECS: Managed containers

## Quality Standards
**Testing:** 80% coverage, TDD for business logic.
**Performance:** Monitor p50/p95/p99, <200ms target.
**Security:** OWASP top 10, automated scans.

## Development Workflow
**Branching:** Feature branches, squash merge.
**Reviews:** Required, 1 approval.
**CI/CD:** Tests + lint + security scan must pass.
```

### Established Constitution (Optimized)
```markdown
## Technical Principles
**Architecture:** Microservices, event-driven. Domain boundaries.
**Design:** SOLID, DDD patterns. Interface-first.
**Code Quality:** Production-grade. Defensive coding.

## Constraints
**Must Have:** 99.99% uptime, GDPR compliance, SOC2.
**Must Avoid:** Tight coupling, synchronous dependencies.

## Tech Stack
- Go: Performance, concurrency
- PostgreSQL + Redis: Persistence + caching
- Kubernetes: Orchestration, zero-downtime deploys

## Quality Standards
**Testing:** 90% coverage, contract tests, chaos engineering.
**Performance:** p99 <100ms, autoscale 10x.
**Security:** Zero-trust, encryption at rest/transit, pen tests.

## Development Workflow
**Branching:** Trunk-based, feature flags.
**Reviews:** 2 approvals, automated checks.
**CI/CD:** Blue-green deploys, automated rollback.
```

---

## Common Mistakes

### ❌ Too Detailed
Including specific API routes, database schemas, file structures → These emerge in dev-plan, not constitution.

### ❌ Too Generic
"Write good code" → Useless. Be specific to your product/stack.

### ❌ Too Long
>1000 words → Will consume too many tokens in every dev skill invocation.

### ❌ Not Product-Aware
Ignoring product stage, user stories, constraints → Constitution should be grounded in product reality.

---

## Usage in Dev Workflow

**Dev skills that read constitution:**
1. `dev-specify` - Checks technical constraints when creating spec
2. `dev-plan` - Validates architecture/design choices against principles
3. `dev-tasks` - Ensures tasks align with quality standards
4. `dev-implement` - Follows coding principles, testing standards

**When to update constitution:**
- Product stage changes (POC → MVP → Established)
- Major technical decision (switching frameworks, adding services)
- New constraints (compliance requirements, performance needs)
- Team lessons learned (add anti-pattern to "Must Avoid")

**How to update:**
Run `/dev-constitution --update` → Script auto-archives old version → Claude guides update conversation.

---

## Quick Checklist

Before finalizing constitution, verify:
- [ ] <500 words total (lean!)
- [ ] Grounded in product artifacts (not generic)
- [ ] Product stage-appropriate (POC/MVP/Established)
- [ ] Actionable principles (not platitudes)
- [ ] Clear constraints and non-negotiables
- [ ] Tech stack with rationale
- [ ] Measurable quality standards
- [ ] Defined development workflow
