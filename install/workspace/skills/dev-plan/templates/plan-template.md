# Implementation Plan: [Feature Name]

**Spec:** [Link to spec.md]
**Created:** [Date]
**Last Updated:** [Date]

---

## Overview

**Feature Summary:**
[One paragraph from spec - what we're building]

**Technical Approach:**
[High-level technical strategy - how we'll build it]

---

## Architecture

### System Components

**[Component 1]:**
- Purpose: [What it does]
- Technology: [Language/framework from constitution]
- Responsibilities: [Key duties]

**[Component 2]:**
- Purpose: [What it does]
- Technology: [Language/framework from constitution]
- Responsibilities: [Key duties]

### Component Interactions

```
[User/Client] → [Component A] → [Component B] → [Data Store]
                      ↓
                [Component C]
```

[Describe data flow and component communication]

### Architecture Decisions

**Decision 1: [What was decided]**
- Options considered: [A, B, C]
- Chosen: [Option X]
- Rationale: [Why]
- Trade-offs: [What we gain/lose]

**Decision 2: [What was decided]**
- Options considered: [A, B, C]
- Chosen: [Option X]
- Rationale: [Why]
- Trade-offs: [What we gain/lose]

---

## Data Model

**See:** `data-model.md` for detailed schemas

**Key Entities:**
1. [Entity 1]: [Brief description]
2. [Entity 2]: [Brief description]
3. [Entity 3]: [Brief description]

**Relationships:**
- [Entity A] → [Entity B]: [Relationship type, cardinality]

---

## API Design

**See:** `contracts/` folder for detailed API contracts

### Endpoints

**[POST /api/resource]**
- Purpose: [What it does]
- Auth: [Required/Optional/None]
- Request: [Key fields]
- Response: [Key fields]
- Errors: [Key error codes]

**[GET /api/resource/:id]**
- Purpose: [What it does]
- Auth: [Required/Optional/None]
- Response: [Key fields]
- Errors: [Key error codes]

### Design Principles
- [Principle 1 from constitution, e.g., "REST, stateless"]
- [Principle 2 from constitution, e.g., "JSON responses"]
- [Principle 3, e.g., "Standard HTTP codes"]

---

## Technical Decisions

**See:** `research.md` for detailed technical research

### Key Decisions Summary

1. **[Decision area, e.g., "State Management"]**
   - Chosen: [Solution, e.g., "Redux Toolkit"]
   - Why: [Brief rationale]

2. **[Decision area, e.g., "Caching Strategy"]**
   - Chosen: [Solution, e.g., "Redis with 5min TTL"]
   - Why: [Brief rationale]

3. **[Decision area, e.g., "Database Choice"]**
   - Chosen: [Solution, e.g., "PostgreSQL"]
   - Why: [Brief rationale]

---

## Security Considerations

**Authentication:**
- Method: [From constitution, e.g., "JWT tokens"]
- Implementation: [How it's enforced]

**Authorization:**
- Model: [RBAC/ABAC/etc.]
- Enforcement: [Where checked]

**Data Protection:**
- At rest: [Encryption approach]
- In transit: [TLS, etc.]
- PII handling: [Specific measures]

**Vulnerabilities Addressed:**
- [OWASP concern 1]: [How mitigated]
- [OWASP concern 2]: [How mitigated]

---

## Performance Strategy

**Targets:** [From spec non-functional requirements]
- Response time: [e.g., "<200ms p95"]
- Throughput: [e.g., "1000 req/sec"]
- Concurrent users: [e.g., "10,000"]

**Optimization Techniques:**
1. **[Technique 1, e.g., "Database indexing"]**
   - Where: [Specific indexes]
   - Expected impact: [Improvement estimate]

2. **[Technique 2, e.g., "Caching"]**
   - What: [What to cache]
   - Where: [Redis/Memory/CDN]
   - TTL: [Duration]

3. **[Technique 3, e.g., "Lazy loading"]**
   - Where: [Components]
   - Why: [Benefit]

**Monitoring:**
- Metrics: [What to track]
- Alerts: [When to alert]
- Tools: [APM, logs]

---

## Error Handling

### Error Taxonomy

**Client Errors (4xx):**
- 400 Bad Request: [When, user message]
- 401 Unauthorized: [When, user message]
- 404 Not Found: [When, user message]
- 422 Validation Error: [When, user message]

**Server Errors (5xx):**
- 500 Internal: [When, user message, logging]
- 503 Unavailable: [When, user message, retry strategy]

### Recovery Strategies

**[Error type 1]:**
- Detection: [How we know it happened]
- User impact: [What user sees]
- Recovery: [Automatic retry? Manual intervention?]
- Logging: [What to log]

**[Error type 2]:**
- Detection: [How we know it happened]
- User impact: [What user sees]
- Recovery: [Automatic retry? Manual intervention?]
- Logging: [What to log]

---

## Testing Strategy

**From constitution:** [Testing requirements, e.g., "80% coverage, TDD"]

### Test Levels

**Unit Tests:**
- Coverage: [Target %]
- Focus: [Business logic, pure functions]
- Tools: [Jest/Vitest/pytest/etc.]

**Integration Tests:**
- Coverage: [What to test]
- Focus: [Component interactions, DB, external APIs]
- Tools: [Testing library]

**E2E Tests:**
- Coverage: [Critical user flows from spec]
- Focus: [Happy path + key error scenarios]
- Tools: [Playwright/Cypress/etc.]

### Test Data Strategy
- Fixtures: [Where stored]
- Factories: [How generated]
- Isolation: [DB per test? Transactions?]

---

## Deployment Strategy

**From constitution:** [CI/CD requirements]

### Environments
- Development: [Local setup]
- Staging: [Pre-prod environment]
- Production: [Live environment]

### Deployment Steps
1. [Step 1, e.g., "Run tests"]
2. [Step 2, e.g., "Build assets"]
3. [Step 3, e.g., "Database migrations"]
4. [Step 4, e.g., "Deploy to staging"]
5. [Step 5, e.g., "Smoke tests"]
6. [Step 6, e.g., "Deploy to production"]

### Rollback Plan
- Trigger: [When to rollback]
- Process: [How to rollback]
- Time: [Target rollback time]

---

## Dependencies

### External Libraries
- **[Library 1]**: [Version, purpose, license]
- **[Library 2]**: [Version, purpose, license]

### Internal Dependencies
- **[Component/Feature]**: [Why needed, impact if unavailable]

### Infrastructure
- **[Service, e.g., "Redis"]**: [Purpose, fallback if down]
- **[Service, e.g., "S3"]**: [Purpose, fallback if down]

---

## Migration & Compatibility

**Data Migration:**
- [If changing schemas] Migration strategy
- Backward compatibility approach
- Rollback procedure

**API Versioning:**
- [If changing APIs] Versioning strategy
- Deprecation timeline
- Client migration path

---

## Acceptance Criteria

**See:** `checklist.md` for detailed acceptance test checklist (if --with-checklist)

**Must Have:**
- [ ] All functional requirements from spec implemented
- [ ] All non-functional requirements met (performance, security)
- [ ] Tests pass (unit, integration, e2e)
- [ ] Code review completed
- [ ] Documentation updated

**Success Metrics:** [From spec]
- [Metric 1]: [Target]
- [Metric 2]: [Target]

---

## Open Questions & Risks

### Open Questions
- [Question 1]: [Why it matters, options, deadline to decide]
- [Question 2]: [Why it matters, options, deadline to decide]

### Technical Risks
1. **[Risk 1]**
   - Likelihood: [High/Medium/Low]
   - Impact: [High/Medium/Low]
   - Mitigation: [What we'll do]

2. **[Risk 2]**
   - Likelihood: [High/Medium/Low]
   - Impact: [High/Medium/Low]
   - Mitigation: [What we'll do]

---

## Timeline Estimate

**Note:** Estimates are for planning only, not commitments.

- Architecture setup: [X days]
- Core implementation: [X days]
- Testing: [X days]
- Documentation: [X days]
- Review & refinement: [X days]

**Total:** [X days]

**Confidence:** [High/Medium/Low]
**Assumptions:** [What could change this estimate]

---

## Next Steps

1. Review this plan with team
2. Resolve open questions
3. Create detailed tasks: `/dev-tasks`
4. Begin implementation: `/dev-implement`
