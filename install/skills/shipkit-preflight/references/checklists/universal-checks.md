# Universal Production Checks

Applies to ALL projects regardless of stack.

---

## Error Handling

### UNI-ERR-001: Unhandled Promise Rejections
**Check**: All async/await operations have error handling
**Scan for**: `await` without surrounding `try/catch`, `.then()` without `.catch()`
**Pass criteria**: Every async operation handles failure case
**Fail impact**: Application crashes on any API/network failure
**Severity**: 🔴 Blocker

### UNI-ERR-002: Consistent Error Responses
**Check**: API endpoints return consistent error shape
**Scan for**: Different error response formats across endpoints
**Pass criteria**: All errors return `{ error: string, code?: string }`
**Fail impact**: Frontend can't reliably handle errors
**Severity**: 🟡 Warning

### UNI-ERR-003: User-Friendly Error Messages
**Check**: Errors shown to users are helpful, not stack traces
**Scan for**: `error.message` or `error.stack` rendered in UI
**Pass criteria**: User sees actionable message, devs see details in logs
**Fail impact**: Confused users, exposed internals
**Severity**: 🟡 Warning

### UNI-ERR-004: Error Logging
**Check**: Errors are logged for debugging
**Scan for**: Errors caught but not logged
**Pass criteria**: `console.error` or logging service captures errors
**Fail impact**: Can't debug production issues
**Severity**: 🟡 Warning

---

## Environment & Configuration

### UNI-ENV-001: Environment Variables Documented
**Check**: All required env vars listed in .env.example
**Scan for**: `process.env.X` or `import.meta.env.X` not in .env.example
**Pass criteria**: Every env var used has a documented example
**Fail impact**: Deployment fails, team can't set up locally
**Severity**: 🔴 Blocker

### UNI-ENV-002: No Hardcoded URLs
**Check**: API endpoints and URLs come from config
**Scan for**: Hardcoded `http://`, `https://`, `localhost` in source
**Pass criteria**: All URLs from env vars or config
**Fail impact**: Works locally, breaks in prod
**Severity**: 🔴 Blocker

### UNI-ENV-003: No Secrets in Code
**Check**: API keys, passwords, tokens not in source
**Scan for**: Patterns like `sk_`, `pk_`, `api_key`, `password`, `secret`
**Pass criteria**: All secrets in env vars
**Fail impact**: Credentials exposed in git history
**Severity**: 🔴 Blocker

### UNI-ENV-004: No Secrets in Git History
**Check**: Secrets never committed (even if removed now)
**Scan for**: Git history contains secret patterns
**Pass criteria**: Clean history or secrets rotated
**Fail impact**: Leaked credentials still valid
**Severity**: 🔴 Blocker

---

## Build & Deploy

### UNI-BUILD-001: Build Passes
**Check**: `npm run build` or equivalent succeeds
**Scan for**: Run build command
**Pass criteria**: Exit code 0, no errors
**Fail impact**: Can't deploy
**Severity**: 🔴 Blocker

### UNI-BUILD-002: No Build Warnings
**Check**: Build has no warnings
**Scan for**: Warning output during build
**Pass criteria**: Clean build output
**Fail impact**: Hidden issues, larger bundles
**Severity**: 🟡 Warning

### UNI-BUILD-003: TypeScript Strict (if applicable)
**Check**: No TypeScript errors in strict mode
**Scan for**: `tsc --noEmit` output
**Pass criteria**: No type errors
**Fail impact**: Runtime type errors possible
**Severity**: 🟡 Warning

---

## UX Resilience

### UNI-UX-001: Loading States
**Check**: All async operations show loading indicator
**Scan for**: `useState` for data without loading state, fetch without pending UI
**Pass criteria**: User sees feedback during waits
**Fail impact**: User thinks app is broken
**Severity**: 🟡 Warning

### UNI-UX-002: Empty States
**Check**: Lists and data views handle zero items
**Scan for**: `.map()` without empty check, no "no results" UI
**Pass criteria**: Helpful message when no data
**Fail impact**: Blank/broken UI for new users
**Severity**: 🟡 Warning

### UNI-UX-003: Destructive Action Confirmation
**Check**: Delete/remove actions require confirmation
**Scan for**: Delete handlers without confirm dialog
**Pass criteria**: User must confirm destructive actions
**Fail impact**: Accidental data loss
**Severity**: 🟡 Warning

### UNI-UX-004: Form Validation Feedback
**Check**: Forms show clear validation errors
**Scan for**: Form submit without validation, errors not displayed
**Pass criteria**: User knows what to fix
**Fail impact**: Frustrated users, abandoned forms
**Severity**: 🟡 Warning

### UNI-UX-005: Mobile Responsive
**Check**: UI works on mobile viewports
**Scan for**: Fixed widths, no responsive breakpoints
**Pass criteria**: Usable on 375px width
**Fail impact**: Lost mobile users
**Severity**: 🟡 Warning (if web app)

---

## Security Basics

### UNI-SEC-001: HTTPS Only
**Check**: App enforces HTTPS in production
**Scan for**: HTTP links in production config
**Pass criteria**: All traffic over HTTPS
**Fail impact**: Data transmitted insecurely
**Severity**: 🔴 Blocker

### UNI-SEC-002: Input Sanitization
**Check**: User input is sanitized before use
**Scan for**: Direct use of req.body, form data in queries/HTML
**Pass criteria**: Input validated and sanitized
**Fail impact**: XSS, injection attacks
**Severity**: 🔴 Blocker

### UNI-SEC-003: No Console Logs in Prod
**Check**: Debug console.logs removed or conditional
**Scan for**: `console.log` in source (not error/warn)
**Pass criteria**: No debug logs in production bundle
**Fail impact**: Leaked internals, performance
**Severity**: 🟢 Info

---

## Monitoring & Observability

### UNI-MON-001: Error Tracking
**Check**: Error tracking service configured (Sentry, etc.)
**Scan for**: Error tracking initialization
**Pass criteria**: Errors reported to dashboard
**Fail impact**: Blind to production errors
**Severity**: 🟡 Warning

### UNI-MON-002: Health Check Endpoint
**Check**: `/health` or `/api/health` endpoint exists
**Scan for**: Health route returning 200
**Pass criteria**: Endpoint returns status
**Fail impact**: Can't monitor uptime
**Severity**: 🟡 Warning

---

## Documentation

### UNI-DOC-001: README Setup Instructions
**Check**: README has setup instructions
**Scan for**: README.md with install/run steps
**Pass criteria**: New developer can get started
**Fail impact**: Onboarding friction
**Severity**: 🟢 Info

### UNI-DOC-002: Deployment Instructions
**Check**: Deployment process documented
**Scan for**: Deploy docs or CI/CD config
**Pass criteria**: Deployment is repeatable
**Fail impact**: Bus factor risk
**Severity**: 🟡 Warning
