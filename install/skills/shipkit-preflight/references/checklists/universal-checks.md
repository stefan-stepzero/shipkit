# Universal Production Checks (MVP)

Applies to ALL projects regardless of stack. These are MVP-critical checks.

For growth/enterprise checks (observability, performance, operational maturity), see `/shipkit-scale-ready`.

---

## Auth & Security Patterns

### UNI-SEC-004: Brute Force Prevention
**Check**: Login attempts are rate-limited with lockout
**Pattern**: Counter in DB, lockout or exponential delay after N failures
**Scan for**:
```
Grep: pattern="failedAttempts|loginAttempts|lockout|accountLocked"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Failed login tracking exists, lockout logic implemented
**Fail impact**: Automated credential stuffing attacks succeed
**Severity**: 🔴 Blocker

### UNI-SEC-005: Form Abuse Prevention
**Check**: Public forms protected against bot spam
**Pattern**: Honeypot field (hidden field bots fill) + timing check (< 2s = bot)
**Scan for**:
```
Grep: pattern="honeypot|botCheck|formTiming|spamProtection"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Contact/signup forms have spam protection
**Fail impact**: Inbox flooded with bot submissions
**Severity**: 🟡 Warning

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

### UNI-ERR-005: Error Visibility Pattern
**Check**: Errors logged with context for debugging
**Pattern**: Structured error logging with user/request context; optional error tracking service
**Scan for**:
```
Grep: pattern="Sentry|LogRocket|errorTracking|captureException"
      glob="**/*.{ts,tsx,js}"
# Or structured logging
Grep: pattern="error.*userId|error.*requestId|logError"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Errors include enough context to debug (user, action, stack)
**Fail impact**: Can see errors but can't reproduce or understand them
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

### UNI-UX-005: Mobile Actually Works
**Check**: Core flow works on mobile — responsive, touch-friendly, survives auto-lock
**Scan for**: Fixed widths, hover-only UI, missing touch handling
**Pass criteria**: Usable on 375px width, 44px+ tap targets, state survives background
**Fail impact**: 50%+ of users lost immediately — no second chances on mobile
**Severity**: 🔴 Blocker (if web app targeting consumers)

**Mobile Killers to check:**
| Issue | Detection | Why Critical |
|-------|-----------|--------------|
| Horizontal scroll | Fixed widths > 375px | Unusable, user leaves |
| Tiny tap targets | Interactive elements < 44px | Can't tap accurately |
| Hover-only interactions | Dropdowns/tooltips need hover | Inaccessible on touch |
| Session lost on lock | No `visibilitychange` handler | Lost work = rage quit |
| No offline handling | No service worker or offline UI | White screen on spotty connection |
| Slow load on 3G | No code splitting, large bundles | Abandoned before content shows |
| Keyboard breaks layout | Fixed bottom elements | Can't see input while typing |

**Quick scan:**
```
# Fixed widths that break mobile
Grep: pattern="width:\s*(1000|800|600|500)px"
      glob="**/*.{css,scss,tsx}"

# Hover-only patterns
Grep: pattern=":hover\s*{[^}]*display:"
      glob="**/*.{css,scss}"

# Session persistence
Grep: pattern="visibilitychange|pagehide"
      glob="**/*.{ts,tsx,js}"
```

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

---

## External Service Boundaries

When a project integrates external services (LLM APIs, payment providers, storage, email, auth), the operational boundaries of those integrations must be explicitly configured. Without this, the app works in dev but fails unpredictably in production under real latency, load, and platform constraints.

### UNI-EXT-001: External Calls Have Timeout Config
**Check**: Every external API/SDK call has an explicit timeout
**Pattern**: HTTP clients configured with timeout, or AbortController/signal used
**Scan for**:
```
# Find external SDK usage
Grep: pattern="openai|anthropic|gemini|stripe|supabase|resend|sendgrid|clerk|replicate|fetch\("
      glob="**/src/**/*.{ts,js}"

# Check for timeout configuration nearby
Grep: pattern="timeout:|timeout=|AbortController|signal:|maxDuration"
      glob="**/src/**/*.{ts,js}"
```
**Pass criteria**: Every file with external calls also has timeout config
**Fail impact**: Hung call blocks serverless function until platform kills it; user sees blank screen
**Severity**: 🔴 Blocker (serverless) / 🟡 Warning (long-running server)

### UNI-EXT-002: Resource Limits Configured on External Calls
**Check**: External calls that generate or return variable-size data have explicit limits
**Pattern**: LLM calls have `maxTokens`/`maxOutputTokens`/`max_tokens`; file uploads have size limits; pagination on list endpoints
**Scan for**:
```
# LLM token limits
Grep: pattern="maxTokens|maxOutputTokens|max_tokens|max_completion_tokens"
      glob="**/*.{ts,js}"

# File upload limits
Grep: pattern="maxFileSize|fileSizeLimit|sizeLimit|maxBodyLength"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Calls that produce unbounded output have explicit caps
**Fail impact**: Runaway costs, slow responses, memory exhaustion
**Severity**: 🟡 Warning

### UNI-EXT-003: Platform Execution Limits Configured
**Check**: Serverless routes that call external services export platform-appropriate duration limits
**Pattern**: `export const maxDuration` on Vercel; timeout config on AWS Lambda; Railway timeout setting
**Scan for**:
```
# Vercel maxDuration
Grep: pattern="export.*maxDuration"
      glob="**/app/**/route.{ts,js}"

# Check which routes have external calls but no maxDuration
# (cross-reference UNI-EXT-001 results with route files)
```
**Pass criteria**: Routes with external calls have explicit execution duration matching platform plan
**Fail impact**: Function killed at default timeout (10s Hobby, 60s Pro on Vercel) mid-operation
**Severity**: 🔴 Blocker (serverless)

**Platform reference** (verify against current docs):
| Platform | Default | Configurable Max |
|----------|---------|-----------------|
| Vercel Hobby | 10s serverless, 30s streaming | 60s (Pro) / 300s streaming |
| AWS Lambda | 3s | 900s |
| Cloudflare Workers | 30s | 30s (standard) |
| Railway | 60s | Configurable |

### UNI-EXT-004: Failure Modes Handled for Each External Service
**Check**: Each external service has explicit error handling for its failure modes
**Pattern**: Network timeout → user feedback; rate limit (429) → backoff; auth failure → clear error; service down → graceful degradation
**Scan for**:
```
# External service error handling
Grep: pattern="429|rate.?limit|too.?many.?requests|ECONNREFUSED|ETIMEDOUT"
      glob="**/*.{ts,js}"

# Catch blocks near external calls
Grep: pattern="catch.*{[^}]*(timeout|rate|limit|unavailable)"
      glob="**/*.{ts,js}"
```
**Pass criteria**: External call error paths produce user-visible feedback, not silent failures
**Fail impact**: User sees broken UI or infinite spinner; no error context for debugging
**Severity**: 🟡 Warning

---

## Code Structure & Reuse

### UNI-REUSE-001: No Duplicate Component Names
**Check**: Same component name doesn't exist in multiple feature directories
**Scan for**:
```
# Find component files, group by basename
Glob: pattern="**/components/**/*.{tsx,jsx}"
# Flag if Button.tsx exists in both features/auth/ and features/dashboard/
```
**Pass criteria**: Each component name exists in ONE location (preferably shared)
**Fail impact**: Inconsistent UI, duplicated maintenance, divergent behavior
**Severity**: 🟡 Warning

### UNI-REUSE-002: Shared Components Used
**Check**: Features import from shared/common/ui directories, not local copies
**Scan for**:
```
# Check for shared directory
Glob: pattern="**/+(shared|common|ui)/components/**/*.{tsx,jsx}"

# Check import patterns from feature code
Grep: pattern="from ['\"].*/(shared|common|ui)/components"
      glob="**/features/**/*.{tsx,jsx}"
```
**Pass criteria**: Features import shared components; no local copies of shared components
**Fail impact**: Technical debt, harder to maintain design consistency
**Severity**: 🟡 Warning

### UNI-REUSE-003: Consistent Component Naming
**Check**: No synonymous component names for same purpose (Modal vs Dialog vs Popup)
**Scan for**:
```
# Find similar-purpose components
Glob: pattern="**/*{Modal,Dialog,Popup}*.tsx"
Glob: pattern="**/*{Card,Tile,Panel}*.tsx"
Glob: pattern="**/*{Button,Btn,CTA}*.tsx"
```
**Pass criteria**: One naming convention for each component type
**Fail impact**: Confusing codebase, inconsistent patterns
**Severity**: 🟢 Info

### UNI-REUSE-004: Utils Not Duplicated
**Check**: Utility functions and hooks don't exist in multiple places
**Scan for**:
```
# Find utils/hooks directories in features
Glob: pattern="**/features/*/+(utils|hooks|helpers)/**"

# Compare with shared utils
Glob: pattern="**/+(shared|common|lib)/+(utils|hooks|helpers)/**"

# Flag overlap (e.g., features/auth/hooks/useAuth.ts AND shared/hooks/useAuth.ts)
```
**Pass criteria**: Utilities exist in one canonical location
**Fail impact**: Divergent implementations, hard to fix bugs globally
**Severity**: 🟡 Warning

### UNI-REUSE-005: Types Centralized
**Check**: Shared types defined in one location, not scattered
**Scan for**:
```
# Find type definition files
Glob: pattern="**/types/**/*.{ts,d.ts}"
Glob: pattern="**/*.types.ts"

# Flag if same type name defined multiple times
Grep: pattern="^export (type|interface) (User|Project|Settings)"
      glob="**/*.ts"
```
**Pass criteria**: Core types in shared/types or similar, features extend not duplicate
**Fail impact**: Type conflicts, refactoring pain
**Severity**: 🟡 Warning

### Detection Summary

| Check | Quick Detection | Pass Signal |
|-------|-----------------|-------------|
| UNI-REUSE-001 | Glob + group by basename | Each basename appears once |
| UNI-REUSE-002 | Grep for shared imports | Features use `from '@/shared'` |
| UNI-REUSE-003 | Glob for synonyms | One Modal, not Modal+Dialog |
| UNI-REUSE-004 | Glob utils in features vs shared | No overlap |
| UNI-REUSE-005 | Grep for type definitions | Core types in one place |
