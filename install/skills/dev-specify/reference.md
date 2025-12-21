# Specification Writing Reference

Extended guidance for writing high-quality feature specifications using the dev-specify skill.

## Table of Contents

- Specification quality criteria
- ProdKit integration patterns
- Technical specification guidelines
- Writing for different audiences
- Common specification antipatterns

## Specification Quality Criteria

A high-quality spec is:

**Complete**: Answers all the key questions
- What problem are we solving?
- Who is this for?
- What does success look like?
- What are we NOT building?
- What could go wrong?

**Unambiguous**: Can be read by anyone and interpreted consistently
- Use precise language
- Define terms
- Provide examples
- Avoid "should", "could", "might" - be definitive

**Testable**: Clear acceptance criteria that can be verified
- Given/When/Then format
- Measurable outcomes
- Observable behaviors

**Prioritized**: Clear about what's critical vs. nice-to-have
- MUS Thave (P0), Should have (P1), Could have (P2)
- Justification for priority levels

## ProdKit Integration Patterns

When ProdKit artifacts exist, reference them to provide context:

### Strategic Context

**From `/strategic-thinking`:**
```markdown
## Business Context

This feature supports our value proposition: [Quote from business-canvas.md]

Target market segment: [Reference from business-canvas.md]
```

### User Context

**From `/personas`:**
```markdown
## Target Users

**Primary:** Sarah (Technical Product Manager persona)
- Goals: [from personas.md]
- Pain points: [from personas.md]
- Usage patterns: [from personas.md]
```

**From `/jobs-to-be-done`:**
```markdown
## Jobs to be Done

**Functional Job:** When [situation], I want to [motivation], so I can [outcome]

**Current Workflow:** [Reference current-state from JTBD]
**Pain Points:** [Reference pain points from JTBD]
```

### Design Context

**From `/brand-guidelines`:**
```markdown
## Brand Requirements

**Voice:** Professional but approachable (see brand/personality.md)
- Copy should be concise and action-oriented
- Error messages should be helpful, not technical

**Visual:** Clean, modern interface (see brand/visual-direction.md)
- Use primary brand color (#HEXCODE) for CTAs
- Follow 8px grid system
```

**From `/interaction-design`:**
```markdown
## User Journey

**Current Step:** [This feature] in overall journey
**Previous:** [What came before]
**Next:** [Where user goes after]

See design/future-state-journeys.md for complete flow.
```

### Requirements Context

**From `/user-stories`:**
```markdown
## User Stories Implemented

**US-003:** As a [user], I want [feature] so that [benefit]
- Acceptance Criteria: [from user-stories.md]
- Priority: High

**US-007:** As a [user], I want [feature] so that [benefit]
- Acceptance Criteria: [from user-stories.md]
- Priority: Medium
```

## Technical Specification Guidelines

### API Specifications

**RESTful Design Principles:**
- Use nouns for resources (`/users`, not `/getUsers`)
- HTTP verbs indicate action (GET, POST, PUT, DELETE)
- Hierarchical URLs for relationships (`/users/123/orders`)
- Plural resource names (`/products`, not `/product`)

**Comprehensive Documentation:**
- Every endpoint documented
- Every request parameter explained
- Every response field defined
- All error codes listed
- Example requests/responses provided

**Versioning Strategy:**
- URL-based (`/api/v1/`) or header-based
- Deprecation timeline (6 months notice)
- Migration guide for breaking changes

### UI Specifications

**Component-Based Thinking:**
- Break UI into reusable components
- Specify component props/configuration
- Document component states (loading, error, empty)
- Define responsive behavior

**Pixel-Perfect vs. Guidelines:**
- Exact specs for: Spacing, font sizes, colors, borders
- Guideline specs for: Content length, image dimensions
- Allow engineering judgment for: Minor adjustments, edge cases

**Interaction Design:**
- Every user action documented
- Every system response specified
- Loading states defined
- Error handling detailed

### Data Model Specifications

**Entity Definition:**
```markdown
### User Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Required, PK | Unique identifier |
| email | string | Required, unique, valid email | User's email address |
| created_at | timestamp | Required, auto | Account creation timestamp |
```

**Relationships:**
```
User (1) ───< (N) Orders
  │
  └──< (N) Addresses
```

**State Machines:**
```
[Created] ──register──> [Pending]
[Pending] ──verify──> [Active]
[Active] ──suspend──> [Suspended]
[Suspended] ──reactivate──> [Active]
```

## Writing for Different Audiences

### For Product Managers

**Focus on:**
- Business value and user impact
- Acceptance criteria
- Success metrics
- Trade-offs and decisions

**De-emphasize:**
- Implementation details
- Technical architecture
- Code-level specifics

### For Engineers

**Focus on:**
- Functional requirements
- Technical constraints
- API contracts
- Data models
- Performance requirements
- Error handling

**De-emphasize:**
- Business strategy
- Market positioning
- Long-term product vision

### For Designers

**Focus on:**
- User flows and scenarios
- UI components and interactions
- Visual design requirements
- Accessibility needs
- Responsive behavior

**De-emphasize:**
- Backend logic
- Database schema
- API implementation

### For QA

**Focus on:**
- Acceptance criteria (testable)
- Edge cases and error states
- Browser/device support
- Performance benchmarks

**De-emphasize:**
- Visual design details (unless testing UI)
- Business strategy

## Common Specification Antipatterns

### 1. Solution Instead of Problem

**Bad:**
```markdown
## Requirements

We need a Redis cache with 1000 connection pool...
```

**Good:**
```markdown
## Problem

API response times exceed 500ms for dashboard queries, causing poor UX.

## Requirements

- Dashboard queries must return in < 200ms (p95)
- Solution should scale to 10k concurrent users

## Suggested Approach

Consider caching strategy (Redis, application-level, CDN).
```

### 2. Vague Acceptance Criteria

**Bad:**
```markdown
- System should be fast
- UI should look good
- Errors should be handled properly
```

**Good:**
```markdown
- API responds in < 200ms for 95% of requests under normal load (1000 req/min)
- UI matches design mockups in Figma (link: ...)
- All errors display user-friendly message + log technical details + notify on-call
```

### 3. Missing Context

**Bad:**
```markdown
Add OAuth login.
```

**Good:**
```markdown
## Context

60% of users abandon signup due to complex registration form (analytics link).
Competitor analysis shows OAuth reduces signup time by 40%.

## Requirement

Add OAuth login via Google and GitHub to reduce signup friction.

## Success Metrics

- Signup completion rate increases from 40% to 60%
- Time-to-first-login decreases from 3min to 30sec
```

### 4. Scope Creep in Disguise

**Bad:**
```markdown
## Requirements

1. User login
2. Password reset
3. Two-factor authentication
4. Social login (Google, Facebook, Twitter, LinkedIn)
5. Single sign-on
6. Biometric authentication
7. Session management across devices
```

**Good:**
```markdown
## Requirements (MVP)

1. Email/password login
2. Password reset via email link

## Out of Scope (Future Phases)

- Phase 2: Two-factor authentication
- Phase 3: Social login (Google, GitHub)
- Not planned: Biometric, SSO
```

### 5. Assuming Implementation

**Bad:**
```markdown
Use PostgreSQL for user table. Store passwords with bcrypt.
```

**Good:**
```markdown
## Requirements

- Store user credentials securely (industry-standard hashing)
- Support 100k users with < 10ms query latency

## Suggested Approach

PostgreSQL with bcrypt is recommended, but alternative RDBMS acceptable if meets performance requirements.
```

## Specification Templates by Feature Type

### CRUD Feature Template

See `templates/spec-template.md` - focuses on data operations

**Key sections:**
- Data model (entity definition)
- CRUD operations (Create, Read, Update, Delete specs)
- Validation rules
- Permissions (who can create/read/update/delete)

### Integration Feature Template

See `templates/api-spec-template.md` - focuses on external systems

**Key sections:**
- Integration partner details
- Authentication/authorization
- Data mapping (our schema ↔ their schema)
- Error handling (what if partner is down?)
- Rate limits and retries

### UI Feature Template

See `templates/ui-spec-template.md` - focuses on user interface

**Key sections:**
- Visual design (layouts, components, styles)
- User interactions (clicks, hovers, keyboard)
- Responsive behavior
- Loading/error/empty states

### Background Job Template

**Key sections:**
- Trigger (what starts the job?)
- Schedule (cron, interval, event-based)
- Processing logic
- Retry/failure handling
- Monitoring and alerts

## Specification Review Checklist

Before finalizing a spec, verify:

**Completeness:**
- [ ] Problem statement is clear
- [ ] Success criteria are defined
- [ ] Functional requirements are listed
- [ ] Non-functional requirements are specified
- [ ] Acceptance criteria are testable
- [ ] Edge cases are considered
- [ ] Dependencies are identified
- [ ] Out-of-scope items are listed

**Clarity:**
- [ ] No ambiguous language
- [ ] Technical terms are defined
- [ ] Examples are provided
- [ ] Diagrams illustrate complex concepts

**Feasibility:**
- [ ] Engineering reviewed for technical feasibility
- [ ] Design reviewed for UX feasibility
- [ ] Product reviewed for business viability
- [ ] Security/compliance reviewed if applicable

**Traceability:**
- [ ] Links to user stories (from ProdKit)
- [ ] Links to design mocks/prototypes
- [ ] Links to related specs
- [ ] Links to market analysis (if applicable)

## Advanced Specification Techniques

### Specifying by Example

Instead of abstract requirements, show concrete examples:

**Example: Search Feature**

```markdown
## Search Behavior

### Example 1: Exact Match

Query: "red shoes"
Results: Items with both "red" AND "shoes" in title/description
Order: Relevance score DESC

### Example 2: Partial Match

Query: "sho"
Results: Items matching "sho*" (shoes, shorts, shopping)
Order: Popularity

### Example 3: No Results

Query: "xyzabc"
Result: Empty state with suggestions for popular categories
```

### Specifying with Decision Tables

For complex conditional logic:

| Condition 1 | Condition 2 | Condition 3 | Result |
|-------------|-------------|-------------|--------|
| User is admin | Item is published | - | Show edit button |
| User is admin | Item is draft | - | Show publish button |
| User is owner | Item is draft | - | Show edit button |
| User is viewer | - | - | No action buttons |

### Specifying State Transitions

For features with complex states:

```
graph TD
    Draft -->|publish| Review
    Review -->|approve| Published
    Review -->|reject| Draft
    Published -->|unpublish| Draft
    Published -->|archive| Archived
    Archived -->|restore| Draft
```

(Include actual diagram or clear description)

## Resources

**Internal:**
- Constitution: `.claude/constitutions/core.md`
- ProdKit artifacts: `.prodkit/`
- Previous specs: `.devkit/specs/`

**External:**
- RFC format: https://www.ietf.org/standards/rfcs/
- API design guide: https://cloud.google.com/apis/design
- WCAG accessibility: https://www.w3.org/WAI/WCAG21/quickref/

---

This reference guide helps you write specs that are complete, clear, and actionable. For specific examples, see `examples.md`.
