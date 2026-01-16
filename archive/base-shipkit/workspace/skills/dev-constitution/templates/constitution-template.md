# [PROJECT_NAME] Technical Constitution

**Created:** [CREATION_DATE]
**Last Updated:** [LAST_UPDATE_DATE]
**Version:** [VERSION]
**Product Stage:** [POC | MVP | Established]

---

## Core Architectural Decisions

### Domain Model
[DOMAIN_MODEL_DESCRIPTION]
<!-- Example:
- **Entities:** User, Project, Task, Comment
- **Naming:** PascalCase entities, camelCase properties
- **Patterns:** Repository for data access, Service layer for business logic
- **Relationships:** Explicit foreign keys, cascading deletes defined
-->

### Technology Stack
[TECH_STACK_DESCRIPTION]
<!-- Example:
- **Backend:** Node.js with TypeScript, Express framework
- **Database:** PostgreSQL 15+ with TypeORM
- **Frontend:** React 18+ with TypeScript, Vite bundler
- **Testing:** Vitest for unit tests, Playwright for E2E
-->

### API Conventions
[API_CONVENTIONS_DESCRIPTION]
<!-- Example:
- **Style:** RESTful with resource-based URLs
- **Versioning:** URL-based (e.g., `/api/v1/users`)
- **Authentication:** JWT tokens with refresh token rotation
- **Error format:** RFC 7807 Problem Details
-->

---

## Coding Standards

### Language & Style
[CODING_STANDARDS_DESCRIPTION]
<!-- Example:
- **TypeScript:** Strict mode enabled, no `any` types
- **Linting:** ESLint with Airbnb config
- **Formatting:** Prettier with 2-space indent
- **Imports:** Absolute imports using path aliases
-->

### Testing Requirements
[TESTING_REQUIREMENTS_DESCRIPTION]
<!-- Example:
- **Coverage:** Minimum 80% line coverage
- **TDD:** Required for all new features
- **Test structure:** Arrange-Act-Assert pattern
- **Mocking:** Minimal - prefer real implementations
-->

---

## Performance Requirements

[PERFORMANCE_REQUIREMENTS_DESCRIPTION]
<!-- Example:
- **API response:** p95 < 200ms for read operations
- **Database queries:** N+1 queries prohibited
- **Bundle size:** < 500KB initial load (gzipped)
- **Monitoring:** Datadog APM and logging required
-->

---

## Security Standards

[SECURITY_STANDARDS_DESCRIPTION]
<!-- Example:
- **Input validation:** All user input validated and sanitized
- **SQL injection:** Parameterized queries only, no string concatenation
- **XSS protection:** Content Security Policy enforced
- **Secrets:** Environment variables only, never committed to git
- **Authentication:** OAuth 2.0 with PKCE for public clients
-->

---

## Deployment Constraints

[DEPLOYMENT_CONSTRAINTS_DESCRIPTION]
<!-- Example:
- **Platform:** Docker containers on AWS ECS
- **CI/CD:** GitHub Actions with staging → production promotion
- **Monitoring:** Datadog APM, CloudWatch logs
- **Rollback:** Blue-green deployment pattern
- **Database migrations:** Reversible migrations required
-->

---

## Development Workflow

### Branching Strategy
[BRANCHING_STRATEGY_DESCRIPTION]
<!-- Example:
- **Pattern:** Feature branches from main (e.g., `001-feature-name`)
- **Naming:** Numeric prefix + kebab-case description
- **Lifetime:** Short-lived (merge within 1-2 days)
- **Protection:** Main branch requires PR + passing tests
-->

### Code Review Requirements
[CODE_REVIEW_REQUIREMENTS_DESCRIPTION]
<!-- Example:
- **Required:** One approval from team member
- **Checks:** All tests pass, no linting errors, coverage maintained
- **Scope:** Review for spec compliance + code quality
- **Self-review:** Author must review own PR before requesting review
-->

### CI/CD Pipeline
[CI_CD_PIPELINE_DESCRIPTION]
<!-- Example:
- **On PR:** Linting, type checking, unit tests, E2E tests
- **On merge to main:** Deploy to staging automatically
- **Production:** Manual approval after staging validation
- **Rollback:** Automated rollback if health checks fail
-->

---

## Non-Negotiables

### Must Have
[MUST_HAVE_LIST]
<!-- Example:
- Tests pass before merge (no exceptions)
- Security vulnerabilities addressed (high/critical = blocking)
- Performance budgets respected (API < 200ms, bundle < 500KB)
- Accessibility: WCAG 2.1 AA compliance for all UI
-->

### Must Avoid
[MUST_AVOID_LIST]
<!-- Example:
- No direct database queries in controllers/routes
- No business logic in frontend components
- No synchronous blocking operations in API handlers
- No storing sensitive data in frontend state/localStorage
- No feature flags older than 90 days (clean up or promote)
-->

---

## Product-Driven Constraints

### Product Stage Implications
[PRODUCT_STAGE_IMPLICATIONS]
<!-- Example for POC:
- **Speed > Quality:** Fast iteration, minimal infrastructure
- **Technical debt OK:** Document for future cleanup
- **Testing:** Critical paths only, no coverage targets
- **Monitoring:** Basic error logging sufficient

Example for MVP:
- **Balance:** Pragmatism with sustainability
- **Technical debt:** Acceptable if tracked and timeboxed
- **Testing:** 60%+ coverage, E2E for happy paths
- **Monitoring:** Basic metrics (errors, latency, usage)

Example for Established:
- **Reliability:** Optimize for uptime and maintainability
- **Technical debt:** Minimize, address continuously
- **Testing:** 80%+ coverage, comprehensive E2E
- **Monitoring:** Full observability (traces, metrics, logs)
-->

### Scale Requirements
[SCALE_REQUIREMENTS_DESCRIPTION]
<!-- Example:
- **Target users:** 10,000 concurrent users by Q4
- **Data growth:** 100K records/month
- **Geographic:** US + EU (GDPR compliance)
- **Availability:** 99.9% uptime (8.76 hours downtime/year max)
-->

### Compliance & Legal
[COMPLIANCE_REQUIREMENTS_DESCRIPTION]
<!-- Example:
- **GDPR:** Data portability, right to deletion, consent tracking
- **SOC2:** Access logs, encryption at rest/transit, audit trails
- **CCPA:** Privacy policy, opt-out mechanisms
- **PCI-DSS:** (if applicable) Use certified payment processors
-->

---

## Governance

### Amendment Process
[AMENDMENT_PROCESS_DESCRIPTION]
<!-- Example:
- **Proposal:** Document change rationale and impact
- **Review:** Team discussion (async or sync)
- **Approval:** Consensus required for major changes
- **Migration:** Update all affected specs, plans, and code
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)
-->

### Compliance Review
[COMPLIANCE_REVIEW_DESCRIPTION]
<!-- Example:
- **Frequency:** Every PR checks constitution compliance
- **Scope:** Spec compliance review + code quality review
- **Enforcement:** Automated checks where possible (linting, tests)
- **Exceptions:** Documented with justification and expiry date
-->

---

**Generated from product artifacts:**
[PRODUCT_ARTIFACTS_LIST]
<!-- Example:
- `.shipkit/skills/prod-user-stories/outputs/user-stories.md`
- `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`
- `.shipkit/skills/prod-success-metrics/outputs/success-metrics.md`
-->

**NOTE:** This constitution was automatically generated from product discovery. Sections marked with `[PLACEHOLDER]` need review and refinement before proceeding to feature development.
