# Goal Templates Reference

This reference provides stage-appropriate goal templates for the `/shipkit-goals` skill. Goals are proposed based on current project stage, detected capabilities, and project type.

---

## Stage Definitions

Read `currentState` from `why.json` and map to stage:

| Stage | Description | Typical Duration |
|-------|-------------|------------------|
| **POC** | Proving the concept works. Happy path only. Throwaway code acceptable. | Days to weeks |
| **MVP** | Minimum viable for first real users. Core flow complete, basic polish. | Weeks to months |
| **Production** | Ready for sustained use. Hardened, monitored, documented. | Ongoing |
| **Scale** | Growth mode. Multi-tenant, enterprise features, performance optimized. | Ongoing |

**Mapping from why.json `currentState`:**

```
"starting" / "idea" / "POC"     → POC stage
"MVP" / "alpha" / "prototype"   → MVP stage
"beta" / "production" / "live"  → Production stage
"growth" / "scale" / "enterprise" → Scale stage
```

---

## Goal Templates by Stage

Each stage has goals across four lenses. Not all lenses apply to all project types.

### POC → MVP Goals

**Objective:** Go from "it works for me" to "first users can use it"

#### Technical Lens
| Goal | Success Criteria |
|------|------------------|
| Core flow works end-to-end | Happy path completes without manual intervention |
| Basic error handling | Errors caught, user sees message (not stack trace) |
| Deployable to hosted environment | Can run outside localhost |
| Environment config separated | No hardcoded secrets or URLs |

#### Product/UX Lens
| Goal | Success Criteria |
|------|------------------|
| First-run experience exists | New user knows what to do on arrival |
| Core action is obvious | Primary CTA visible within 5 seconds |
| Loading states present | User knows when something is happening |
| Mobile not broken | Core flow works on phone (if web) |

#### Growth Lens (if applicable)
| Goal | Success Criteria |
|------|------------------|
| Self-serve signup works | User can start without manual intervention |
| Value delivered in first session | User accomplishes something meaningful |

#### Operational Lens
| Goal | Success Criteria |
|------|------------------|
| README explains what this is | New person understands purpose in 30 seconds |
| How to run locally documented | Developer can start contributing |

---

### MVP → Production Goals

**Objective:** Go from "first users" to "sustainable product"

#### Technical Lens
| Goal | Success Criteria |
|------|------------------|
| Auth hardened | Session expiry, rate limiting, brute force prevention |
| Error recovery exists | Retry logic, graceful degradation for non-critical features |
| Input validation complete | All user inputs validated, sanitized |
| CI/CD pipeline | Automated build, test, deploy |
| Health check endpoint | Monitoring can verify app is alive |

#### Product/UX Lens
| Goal | Success Criteria |
|------|------------------|
| Onboarding flow complete | User guided through first key actions |
| Empty states guide users | No dead-ends when data is missing |
| Confirmation on destructive actions | Delete/remove requires explicit confirm |
| Error messages are actionable | User knows what to do, not just what failed |
| Form validation inline | Errors shown at field level, not just on submit |

#### Growth Lens (if applicable)
| Goal | Success Criteria |
|------|------------------|
| Activation metric defined | Know what action = "activated user" |
| User can invite others | Viral loop possible |
| Feedback channel exists | Users can report issues, request features |

#### Operational Lens
| Goal | Success Criteria |
|------|------------------|
| User-facing documentation | Help docs or FAQ for common questions |
| Error logging with context | Can debug user-reported issues |
| Support channel defined | Users know where to get help |
| Backup strategy documented | Know how to recover from data loss |

---

### Production → Scale Goals

**Objective:** Go from "sustainable" to "growth-ready"

#### Technical Lens
| Goal | Success Criteria |
|------|------------------|
| Performance benchmarked | Know current limits, have baseline metrics |
| Database queries optimized | N+1 eliminated, indexes on common queries |
| Caching strategy implemented | Reduced redundant computation/fetches |
| Rate limiting on all endpoints | Protected from abuse |
| Audit logging | Security-relevant actions tracked |

#### Product/UX Lens
| Goal | Success Criteria |
|------|------------------|
| Power user features | Keyboard shortcuts, bulk actions, saved preferences |
| Notification preferences | Users control what they receive |
| Data export available | Users can get their data out |

#### Growth Lens
| Goal | Success Criteria |
|------|------------------|
| Referral/invite tracking | Know where users come from |
| Onboarding optimization | Multiple paths for different user types |
| Self-serve upgrade flow | Users can upgrade plan without talking to sales |

#### Operational Lens
| Goal | Success Criteria |
|------|------------------|
| Monitoring & alerting | Know when things break before users tell you |
| Runbooks for common issues | On-call can resolve without escalation |
| SLA defined | Users know what to expect |
| Incident response process | Know how to handle outages |

---

### Scale → Enterprise Goals

**Objective:** Go from "growth" to "enterprise-ready"

#### Technical Lens
| Goal | Success Criteria |
|------|------------------|
| Multi-tenancy | Data isolation between customers |
| SSO/SAML support | Enterprise auth integration |
| Role-based access control | Granular permissions |
| API rate limits per customer | Fair usage enforcement |

#### Product/UX Lens
| Goal | Success Criteria |
|------|------------------|
| Admin dashboard | Customer admins can manage their org |
| Bulk operations | Handle large data sets efficiently |
| White-labeling (if applicable) | Customer branding options |

#### Growth Lens
| Goal | Success Criteria |
|------|------------------|
| Sales-assist flow | Demo accounts, trial extensions |
| Usage analytics for customers | Customers see their own metrics |

#### Operational Lens
| Goal | Success Criteria |
|------|------------------|
| SLA guarantees | Contractual uptime commitments |
| Compliance certifications | SOC2, GDPR, HIPAA as needed |
| Dedicated support tier | Enterprise support offering |
| Custom contracts | Legal/procurement ready |

---

## Concept Modifiers

When `codebase-index.json` shows specific concepts, add relevant goals:

### If `concepts.auth` exists

| Stage | Add Goals |
|-------|-----------|
| MVP → Prod | Session expiry configured, Rate limiting on auth endpoints, Password requirements enforced |
| Prod → Scale | Account lockout after failed attempts, Auth audit logging |

### If `concepts.payments` exists

| Stage | Add Goals |
|-------|-----------|
| MVP → Prod | Webhook signature verification, Failed payment handling, Subscription state synced |
| Prod → Scale | Dunning flow (failed payment recovery), Invoice/receipt generation |

### If `concepts.database` exists

| Stage | Add Goals |
|-------|-----------|
| MVP → Prod | Backup strategy documented, Migrations run automatically, Cascade deletes configured |
| Prod → Scale | Read replicas (if needed), Query performance monitoring |

### If `concepts.email` exists

| Stage | Add Goals |
|-------|-----------|
| MVP → Prod | Transactional emails work, Unsubscribe link present |
| Prod → Scale | Email deliverability monitoring, Template management |

### If `concepts.api` exists (public API)

| Stage | Add Goals |
|-------|-----------|
| MVP → Prod | API authentication, Consistent error format, Basic rate limiting |
| Prod → Scale | API versioning, API documentation (OpenAPI), Per-customer rate limits |

---

## Project Type Variations

Adjust lens weights based on project type:

### SaaS Web App
- All lenses apply
- Growth lens high priority
- Operational lens high priority

### CLI Tool
- Technical lens: focus on install, cross-platform
- Product/UX lens: focus on help text, error messages, progress output
- Growth lens: low priority (maybe package manager distribution)
- Operational lens: focus on docs, changelog, version management

### Library/Package
- Technical lens: focus on API design, backwards compatibility, test coverage
- Product/UX lens: focus on DX (developer experience), examples, error messages
- Growth lens: low priority
- Operational lens: focus on docs, changelog, migration guides

### API Service
- Technical lens: high priority (reliability, performance)
- Product/UX lens: focus on DX, API design, error responses
- Growth lens: depends on business model
- Operational lens: high priority (uptime, monitoring)

### Internal Tool
- Technical lens: moderate (works > perfect)
- Product/UX lens: moderate (usable > beautiful)
- Growth lens: not applicable
- Operational lens: focus on handoff docs, maintainability

---

## Using This Reference

The `/shipkit-goals` skill should:

1. **Read context:**
   - `why.json` → `currentState` → determine stage
   - `why.json` → `vision`, `problem` → understand direction
   - `codebase-index.json` → `concepts` → detect capabilities

2. **Select templates:**
   - Pick goals for current stage → next stage transition
   - Apply concept modifiers based on detected capabilities
   - Adjust lens weights based on project type

3. **Propose goals:**
   - Present 5-10 goals across relevant lenses
   - Mark suggested priorities (P0/P1/P2)
   - Let user accept, modify, or add custom goals

4. **Generate goals.json:**
   - Include selected goals with priorities and success criteria
   - Link to relevant concepts from codebase-index

---

## Goal Naming Conventions

Goals should be:
- **Outcome-focused** — "Onboarding flow complete" not "Build onboarding"
- **Verifiable** — Success criteria is measurable
- **Stage-appropriate** — Don't add Scale goals to MVP projects

**Good:** "Error messages are actionable"
**Bad:** "Improve error handling"

**Good:** "User can complete core flow in < 3 clicks"
**Bad:** "Better UX"
