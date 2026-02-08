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

#### Product/UX Lens (First Impressions Critical)

**Why this matters for MVP:** Users form opinions in 3-5 seconds. A janky first impression = no users, no revenue. Polish the core path ruthlessly.

| Goal | Success Criteria | Why Critical |
|------|------------------|--------------|
| **Value clear in 5 seconds** | Headline/hero explains what this does and for whom | Users bounce if confused |
| **Core action is obvious** | Primary CTA visible above fold, clear verb | Confused users don't convert |
| **First-run experience exists** | New user guided to first success moment | "Aha!" creates retention |
| **Loading states present** | Skeleton screens or spinners on all async actions | Slow = broken in users' minds |
| **No dead-ends** | Every error/empty state has a next action | Stuck users = lost users |
| **Mobile actually works** | Core flow works on phone — responsive, touch-friendly, survives auto-lock | 50%+ of traffic is mobile, no second chances |
| **Feels fast** | Core action completes in <1s (or appears to) | Perceived speed = quality |

**First Impression Killers (avoid these):**
- Blank screens while loading
- Generic error messages ("Something went wrong")
- Requiring signup before showing value
- Walls of text instead of clear actions
- Broken responsive layout on mobile

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

#### Product/UX Lens (Retention & Trust)

**Why this matters for Production:** First impressions got them in. Now polish keeps them. Trust signals convert free → paid.

| Goal | Success Criteria | Why Critical |
|------|------------------|--------------|
| **Onboarding flow complete** | User guided to first success in <2 minutes | Fast time-to-value = activation |
| **Empty states guide users** | Every empty state has a clear CTA | Stuck users churn |
| **Error messages are actionable** | User knows what to do, not just what failed | Confusion = support tickets |
| **Form validation inline** | Errors shown at field level before submit | Frustration = abandonment |
| **Confirmation on destructive actions** | Delete/remove requires explicit confirm | Accidents = lost trust |
| **Trust signals visible** | Security badges, testimonials, or social proof where users decide | Doubt = no conversion |
| **Consistent UI patterns** | Buttons, forms, modals behave the same everywhere | Predictability = confidence |
| **Feedback on every action** | User knows their action was received (toast, animation) | Silence = uncertainty |

**Trust Killers (especially before payment):**
- No visible security on payment forms
- Unclear pricing or hidden fees
- No way to contact support
- Broken or missing terms/privacy links
- Inconsistent visual design (feels amateur)

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

### If `concepts.mobile` or `concepts.pwa` exists (Mobile Web App)

**Why critical:** 50%+ of web traffic is mobile. Phones have unique behaviors that break naive implementations.

| Stage | Add Goals |
|-------|-----------|
| POC → MVP | **Responsive sizing works** (no horizontal scroll, tap targets ≥44px), **Touch interactions work** (no hover-dependent UI), **Viewport meta tag set** |
| MVP → Prod | **PWA installable** (manifest.json, service worker, icons), **Works offline or degrades gracefully** (cached assets, offline indicator), **Auto-lock safe** (no data loss when phone locks/unlocks, session survives background), **Keyboard doesn't break layout** (inputs visible when keyboard opens), **Pull-to-refresh works** (if applicable) |
| Prod → Scale | **App store presence** (TWA for Play Store or App Clip), **Push notifications** (with permission UX), **Deep linking works** (URLs open in app) |

**Mobile Killers:**
- Tiny tap targets (< 44px)
- Hover-only interactions (tooltips, dropdowns)
- Fixed positioning breaking on keyboard open
- Session lost when app backgrounded
- No offline handling (white screen when signal drops)
- Slow initial load on 3G (> 3 seconds)

---

## Project Type Variations

Adjust lens weights based on project type:

### SaaS Web App
- All lenses apply
- Growth lens high priority
- Operational lens high priority

### Mobile Web App / PWA
- Technical lens: PWA requirements, offline support, service workers
- Product/UX lens: **highest priority** — touch interactions, responsive sizing, auto-lock handling, keyboard behavior
- Growth lens: app store presence, push notifications, deep linking
- Operational lens: device testing matrix, performance on slow networks

**Critical for mobile:** First impression happens on a small screen with spotty connectivity. If it feels slow or janky, users delete immediately. No second chances.

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
