# Acceptance Test Checklist: [Feature Name]

**Spec:** [Link to spec.md]
**Plan:** [Link to plan.md]
**Created:** [Date]

---

## Purpose

This checklist translates spec requirements into testable acceptance criteria. Use this to verify the feature is complete before marking it done.

**Generated with:** `--with-checklist` flag

---

## Functional Requirements

### [Requirement 1 from spec]

- [ ] **Given:** [Precondition]
  **When:** [Action]
  **Then:** [Expected result]
  **Test:** [How to verify - manual steps or automated test name]

- [ ] **Given:** [Precondition for edge case]
  **When:** [Action]
  **Then:** [Expected result]
  **Test:** [How to verify]

### [Requirement 2 from spec]

- [ ] **Given:** [Precondition]
  **When:** [Action]
  **Then:** [Expected result]
  **Test:** [How to verify]

---

## Non-Functional Requirements

### Performance

- [ ] **Response time:** <[X]ms p95 (from spec)
  **Test:** Load test with [Y] concurrent users, measure p95 latency
  **Tools:** [k6/Artillery/JMeter]

- [ ] **Throughput:** [X] requests/sec
  **Test:** Sustained load test for 5 minutes
  **Pass criteria:** No errors, latency stable

### Security

- [ ] **Authentication:** Only authenticated users can [action]
  **Test:** Attempt [action] without auth token → 401 Unauthorized

- [ ] **Authorization:** Users can only [action] their own [resources]
  **Test:** User A attempts to [action] User B's resource → 403 Forbidden

- [ ] **Input validation:** Malicious input rejected
  **Test:** Submit SQL injection / XSS payload → 400 Bad Request, no execution

- [ ] **Data protection:** Sensitive fields never exposed
  **Test:** Inspect API response → password hash not present

### Reliability

- [ ] **Error handling:** Graceful degradation on [external service] failure
  **Test:** Mock [external service] failure → User sees friendly error, system continues

- [ ] **Retry logic:** Failed [operations] retry automatically
  **Test:** Simulate transient failure → Observe retry (with backoff), eventual success

### Accessibility

- [ ] **Screen reader:** All interactive elements labeled
  **Test:** Navigate with screen reader (NVDA/JAWS) → All elements announced

- [ ] **Keyboard navigation:** All actions keyboard-accessible
  **Test:** Unplug mouse, complete user flow → Success without mouse

- [ ] **Color contrast:** WCAG AA compliance
  **Test:** Use contrast checker → All text meets 4.5:1 ratio

---

## User Experience

### User Journey (from spec)

**Step 1:** [User action]
- [ ] UI shows [expected element]
- [ ] Element behaves as expected (click/tap)
- [ ] Visual feedback provided (<200ms)

**Step 2:** [User action]
- [ ] System responds within [X]ms
- [ ] User sees [expected result]
- [ ] Can proceed to Step 3

**Step 3:** [User action]
- [ ] Final state matches spec
- [ ] Success message shown
- [ ] User can [next action]

### UI Requirements (from spec)

- [ ] **Component:** [Name, e.g., "Save button"]
  **Appearance:** [From brand guidelines]
  **Behavior:** [From interaction design]
  **Test:** Visual inspection + interaction test

- [ ] **Responsive:** Works on mobile/tablet/desktop
  **Test:** Resize browser 320px → 1920px → No layout breaks

---

## Edge Cases (from spec)

### [Edge Case 1, e.g., "Empty state"]

- [ ] **Scenario:** User has no [items]
  **Expected:** Show [empty state message/illustration]
  **Test:** Delete all items → Verify empty state displays

### [Edge Case 2, e.g., "Max capacity"]

- [ ] **Scenario:** User reaches [limit, e.g., "100 saved items"]
  **Expected:** Show [warning/error], prevent further adds
  **Test:** Add 100 items → Attempt 101st → Verify rejection

### [Edge Case 3, e.g., "Network failure"]

- [ ] **Scenario:** User loses network mid-operation
  **Expected:** [Queue operation/show retry/graceful failure]
  **Test:** Disable network during operation → Verify behavior

---

## Error Handling (from spec)

### Client Errors (4xx)

- [ ] **400 Bad Request:** Invalid input
  **Test:** Submit malformed request → 400 + helpful error message
  **Message:** [From spec, e.g., "Please check your input and try again"]

- [ ] **401 Unauthorized:** Missing/invalid auth
  **Test:** Request without token → 401 + redirect to login
  **Message:** "Please log in to continue"

- [ ] **404 Not Found:** Resource doesn't exist
  **Test:** Request non-existent ID → 404 + friendly message
  **Message:** "We couldn't find that item"

- [ ] **422 Validation Error:** Invalid data
  **Test:** Submit invalid data → 422 + field-specific errors
  **Message:** Lists all validation failures

### Server Errors (5xx)

- [ ] **500 Internal Error:** Unexpected server error
  **Test:** Trigger server exception → 500 + generic user message + detailed logging
  **User message:** "Something went wrong. We've been notified."
  **Logging:** Full stack trace logged

- [ ] **503 Service Unavailable:** Dependency down
  **Test:** Mock dependency failure → 503 + retry-after header
  **User message:** "Service temporarily unavailable. Try again in a moment."

---

## Integration Points

### External Service 1: [Name, e.g., "Payment API"]

- [ ] **Happy path:** Successful integration
  **Test:** Complete flow with real/staging API → Success

- [ ] **Failure:** Service returns error
  **Test:** Mock API error → System handles gracefully

- [ ] **Timeout:** Service doesn't respond
  **Test:** Mock slow API (>5s) → Timeout + retry

### External Service 2: [Name]

- [ ] **Happy path:** [Test]
- [ ] **Failure:** [Test]
- [ ] **Timeout:** [Test]

---

## Data Integrity

- [ ] **Data persistence:** Changes survive app restart
  **Test:** Make change → Close app → Reopen → Verify change persisted

- [ ] **Data validation:** Invalid data rejected at all layers
  **Test:** Submit invalid data → Rejected at UI, API, and DB layers

- [ ] **Data consistency:** Related data stays in sync
  **Test:** Update parent record → Child records reflect change

- [ ] **Data migration:** Existing data unaffected
  **Test:** Run migration → Verify old data intact + new fields added

---

## Browser/Device Compatibility

- [ ] **Chrome:** [Version +]
- [ ] **Firefox:** [Version +]
- [ ] **Safari:** [Version +]
- [ ] **Edge:** [Version +]
- [ ] **Mobile Safari:** iOS [Version +]
- [ ] **Mobile Chrome:** Android [Version +]

**Test:** Complete user flow on each browser/device → No broken functionality

---

## Performance Budgets (from spec)

- [ ] **Page load:** <[X]s on 3G
  **Test:** Throttle to 3G → Load page → Measure time

- [ ] **Bundle size:** <[X]KB
  **Test:** Build production → Check bundle size → Under budget

- [ ] **API latency:** <[X]ms p95
  **Test:** Load test → Measure p95 → Under target

- [ ] **Database queries:** <[X] queries per request
  **Test:** Enable query logging → Complete flow → Count queries

---

## Security Checklist (OWASP Top 10)

- [ ] **SQL Injection:** Parameterized queries used
- [ ] **XSS:** User input sanitized on output
- [ ] **CSRF:** CSRF tokens on state-changing requests
- [ ] **Authentication:** Secure password hashing (bcrypt/argon2)
- [ ] **Session Management:** Secure cookies (HttpOnly, Secure, SameSite)
- [ ] **Access Control:** Authorization checked on every request
- [ ] **Cryptography:** Sensitive data encrypted (TLS, at-rest encryption)
- [ ] **Configuration:** No secrets in code/logs
- [ ] **Dependencies:** No known vulnerabilities (npm audit/snyk)
- [ ] **Logging:** No sensitive data in logs

---

## Code Quality

- [ ] **Tests pass:** All unit/integration/e2e tests green
  **Command:** `npm test`

- [ ] **Coverage:** Meets target (from constitution, e.g., "80%")
  **Command:** `npm run test:coverage`
  **Target:** [X]% coverage

- [ ] **Linting:** No lint errors
  **Command:** `npm run lint`

- [ ] **Type checking:** No type errors
  **Command:** `npm run type-check`

- [ ] **Build:** Production build succeeds
  **Command:** `npm run build`

---

## Documentation

- [ ] **README:** Updated with new feature
- [ ] **API docs:** OpenAPI spec updated (if API changes)
- [ ] **Code comments:** Complex logic explained
- [ ] **Changelog:** Feature added to CHANGELOG.md

---

## Deployment Readiness

- [ ] **Migrations:** Database migrations tested on staging
- [ ] **Environment variables:** New env vars documented + set in all environments
- [ ] **Feature flags:** Configured (if using feature flags)
- [ ] **Monitoring:** Metrics/alerts configured
- [ ] **Rollback plan:** Documented and tested

---

## User Acceptance

- [ ] **Stakeholder review:** PM/Designer approved
- [ ] **User testing:** [If applicable] Tested with real users → Positive feedback
- [ ] **Accessibility audit:** Passed WCAG AA audit
- [ ] **Analytics:** Tracking events implemented

---

## Success Criteria (from spec)

- [ ] **Metric 1:** [From spec, e.g., "Reduce signup drop-off to <15%"]
  **Measured:** [How to measure]
  **Current:** [Baseline]
  **Target:** [Goal]

- [ ] **Metric 2:** [From spec]
  **Measured:** [How to measure]
  **Current:** [Baseline]
  **Target:** [Goal]

---

## Sign-off

- [ ] **Developer:** All items checked, tests pass, code reviewed
- [ ] **QA:** Manual testing complete, edge cases verified
- [ ] **PM/Designer:** Feature matches spec, UX approved
- [ ] **Security:** Security checklist complete, no vulnerabilities
- [ ] **DevOps:** Deployment plan reviewed, monitoring ready

**Ready to deploy:** [Yes/No]
**Deployment date:** [Date]
