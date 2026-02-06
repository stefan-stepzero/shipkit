# Growth Tier Checks

For teams with traction preparing to scale. These checks ensure you can handle 10x users and debug production issues effectively.

---

## Security Hardening

### SEC-SCALE-001: Security Headers Configured
**Check**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options set
**Scan for**:
```
Grep: pattern="helmet|contentSecurityPolicy|X-Frame-Options|HSTS"
      glob="**/*.{ts,js,json}"
```
**Pass criteria**: Security headers middleware configured
**Fail impact**: Vulnerable to clickjacking, XSS, MIME sniffing
**Severity**: 🟡 Warning

### SEC-SCALE-002: Session Expiry Configured
**Check**: Sessions expire and refresh tokens rotate
**Scan for**:
```
Grep: pattern="maxAge|expiresIn|sessionTimeout|refreshToken"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Explicit expiry set, refresh logic exists
**Fail impact**: Sessions never expire, stolen tokens valid forever
**Severity**: 🟡 Warning

### SEC-SCALE-003: Admin Routes Extra-Protected
**Check**: Admin endpoints have additional auth beyond standard
**Scan for**:
```
Glob: pattern="**/admin/**/*.{ts,js}"
Grep: pattern="requireAdmin|isAdmin|role.*admin"
```
**Pass criteria**: Admin routes check for admin role specifically
**Fail impact**: Any authenticated user could access admin
**Severity**: 🔴 Critical

### SEC-SCALE-004: Sensitive Actions Require Re-auth
**Check**: Password change, email change, delete account require password
**Scan for**:
```
Grep: pattern="confirmPassword|requirePassword|verifyPassword"
      glob="**/*.{ts,tsx}"
```
**Pass criteria**: Critical account actions require password confirmation
**Fail impact**: Compromised session = compromised account
**Severity**: 🟡 Warning

### SEC-SCALE-005: API Keys Scoped and Rotatable
**Check**: API keys have scopes, can be rotated
**Scan for**:
```
Grep: pattern="apiKey.*scope|keyRotation|revokeKey"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Key management exists if API keys used
**Fail impact**: Leaked key = full access forever
**Severity**: 🟡 Warning (if applicable)

---

## Database Optimization

### DB-SCALE-001: Indexes on Query Patterns
**Check**: Database indexes exist for common queries
**Scan for**:
```
Grep: pattern="CREATE INDEX|@@index|@index|.createIndex"
      glob="**/*.{sql,prisma,ts}"
```
**Pass criteria**: Indexes on foreign keys and frequently filtered columns
**Fail impact**: Slow queries as data grows
**Severity**: 🟡 Warning

### DB-SCALE-002: No N+1 Query Patterns
**Check**: No database queries inside loops
**Scan for**:
```
Grep: pattern="\.map\(.*await.*find|\.forEach\(.*await.*query"
      glob="**/*.{ts,js}"

# Also check for:
Grep: pattern="for\s*\(.*\)\s*\{[^}]*await.*prisma\."
      glob="**/*.{ts,js}"
```
**Pass criteria**: Data fetched in bulk, not per-item
**Fail impact**: 100 items = 101 queries, kills performance
**Severity**: 🔴 Critical

### DB-SCALE-003: Connection Pooling Configured
**Check**: Database connection pool settings exist
**Scan for**:
```
Grep: pattern="pool|connectionLimit|max_connections|poolSize"
      glob="**/*.{ts,js,json,env*}"
```
**Pass criteria**: Pool size configured for expected load
**Fail impact**: Connection exhaustion under load
**Severity**: 🟡 Warning

### DB-SCALE-004: Query Performance Monitoring
**Check**: Slow query logging or APM configured
**Scan for**:
```
Grep: pattern="slow_query|query.*log|$queryRaw.*log"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Can identify slow queries in production
**Fail impact**: Can't diagnose performance issues
**Severity**: 🟡 Warning

### DB-SCALE-005: Backup Restore Tested
**Check**: Backups exist AND restore has been tested
**Verification**: 👤 Human-Verify
**Pass criteria**: Team has restored from backup at least once
**Fail impact**: Backups may be corrupted or incomplete
**Severity**: 🔴 Critical

---

## Observability

### OBS-SCALE-001: Structured Logging
**Check**: Using logger library, not console.log
**Scan for**:
```
# Find console.log usage
Grep: pattern="console\.(log|info|debug)"
      glob="**/src/**/*.{ts,tsx,js}"
      output_mode="count"

# Find logger usage
Grep: pattern="(logger|log)\.(info|debug|warn|error)"
      glob="**/*.{ts,js}"
      output_mode="count"
```
**Pass criteria**: Logger usage > console.log usage; console.log = 0 ideal
**Fail impact**: Can't search/filter logs, no structure
**Severity**: 🟡 Warning

### OBS-SCALE-002: Log Levels Configured
**Check**: Debug logs off in production
**Scan for**:
```
Grep: pattern="LOG_LEVEL|logLevel|level:.*debug"
      glob="**/*.{ts,js,json,env*}"
```
**Pass criteria**: Log level configurable, debug disabled in prod
**Fail impact**: Verbose logs, performance impact, noise
**Severity**: 🟢 Info

### OBS-SCALE-003: Request Correlation
**Check**: Requests have correlation/request ID
**Scan for**:
```
Grep: pattern="requestId|correlationId|x-request-id|traceId"
      glob="**/*.{ts,js}"
```
**Pass criteria**: ID generated and passed through request lifecycle
**Fail impact**: Can't trace request across services/logs
**Severity**: 🟡 Warning

### OBS-SCALE-004: Error Tracking Context
**Check**: Errors include user/request context
**Scan for**:
```
Grep: pattern="setUser|setContext|setExtra|withScope"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Sentry/similar captures user, request info
**Fail impact**: Errors hard to reproduce, no context
**Severity**: 🟡 Warning

### OBS-SCALE-005: Error Alerting
**Check**: Team notified on error spikes
**Verification**: 👤 Human-Verify
**How to verify**: Check Sentry/PagerDuty for alert rules
**Pass criteria**: Alerts configured for error rate thresholds
**Fail impact**: Issues go unnoticed until users complain
**Severity**: 🟡 Warning

### OBS-SCALE-006: Useful Health Endpoint
**Check**: Health endpoint checks dependencies
**Scan for**:
```
Read: path="**/health/route.ts" or "**/health.ts"
Check: Does it verify DB connection, external services?
```
**Pass criteria**: Returns dependency status, not just 200
**Fail impact**: Appears healthy when DB is down
**Severity**: 🟡 Warning

---

## Performance

### PERF-SCALE-001: Core Web Vitals
**Check**: LCP, FID, CLS within thresholds
**Verification**: 👤 Human-Verify
**How to verify**: Run Lighthouse or check PageSpeed Insights
**Pass criteria**: LCP < 2.5s, FID < 100ms, CLS < 0.1
**Fail impact**: Poor UX, SEO penalty
**Severity**: 🟡 Warning

### PERF-SCALE-002: Bundle Size Optimized
**Check**: JavaScript bundle not bloated
**Scan for**:
```
# Check for bundle analyzer
Grep: pattern="@next/bundle-analyzer|webpack-bundle-analyzer"
      glob="**/*.{js,json}"

# Check for heavy deps used lightly
Grep: pattern="from 'moment'|from 'lodash'"
      glob="**/*.{ts,tsx}"
```
**Pass criteria**: Bundle analyzer used, no heavy deps for light use
**Fail impact**: Slow initial load, poor mobile experience
**Severity**: 🟡 Warning

### PERF-SCALE-003: Code Splitting
**Check**: Routes/components lazy loaded
**Scan for**:
```
Grep: pattern="dynamic\(|React\.lazy|import\(\)"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Non-critical routes/components lazy loaded
**Fail impact**: All code loaded upfront, slow TTI
**Severity**: 🟡 Warning

### PERF-SCALE-004: Image Optimization
**Check**: Images optimized and responsive
**Scan for**:
```
Grep: pattern="next/image|srcset|loading=\"lazy\"|webp"
      glob="**/*.{tsx,jsx,html}"
```
**Pass criteria**: Using optimized image component or srcset
**Fail impact**: Large images kill mobile performance
**Severity**: 🟡 Warning

### PERF-SCALE-005: Cache Headers
**Check**: Static assets have cache headers
**Scan for**:
```
Grep: pattern="Cache-Control|max-age|immutable"
      glob="**/*.{ts,js,json}"
```
**Pass criteria**: Static assets cached, API responses cached where appropriate
**Fail impact**: Unnecessary requests, slow repeat visits
**Severity**: 🟢 Info

### PERF-SCALE-006: API Response Caching
**Check**: Expensive endpoints cached
**Scan for**:
```
Grep: pattern="redis|cache\.get|unstable_cache|revalidate"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Expensive/frequent endpoints use caching
**Fail impact**: Unnecessary computation, slow responses
**Severity**: 🟡 Warning

---

## Reliability

### REL-SCALE-001: External Call Timeouts
**Check**: All external HTTP calls have timeouts
**Scan for**:
```
Grep: pattern="timeout:|timeout=|AbortController|signal:"
      glob="**/*.{ts,js}"

# Find fetch without timeout
Grep: pattern="fetch\([^)]+\)(?!.*timeout)"
      glob="**/*.{ts,js}"
```
**Pass criteria**: All external calls have explicit timeout
**Fail impact**: Hung requests, thread exhaustion
**Severity**: 🔴 Critical

### REL-SCALE-002: Retry with Backoff
**Check**: Failed requests retry with exponential backoff
**Scan for**:
```
Grep: pattern="retry|backoff|exponential"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Transient failures retried appropriately
**Fail impact**: Single failure = user failure
**Severity**: 🟡 Warning

### REL-SCALE-003: Graceful Degradation
**Check**: App works (partially) when dependencies fail
**Scan for**:
```
Grep: pattern="fallback|defaultValue|optional\?"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Non-critical features fail gracefully
**Fail impact**: One service down = entire app down
**Severity**: 🟡 Warning

### REL-SCALE-004: Idempotent Operations
**Check**: Critical operations safe to retry
**Scan for**:
```
Grep: pattern="idempotency|idempotent|Idempotency-Key"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Payments, emails, etc. use idempotency keys
**Fail impact**: Duplicate charges, spam emails
**Severity**: 🔴 Critical (for payment/email operations)

### REL-SCALE-005: Queue Job Reliability
**Check**: Background jobs are retriable
**Scan for**:
```
Grep: pattern="maxRetries|retryDelay|deadLetter"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Failed jobs retry, dead letter for permanent failures
**Fail impact**: Lost jobs, inconsistent state
**Severity**: 🟡 Warning (if using queues)

---

## Operational Readiness

### OPS-SCALE-001: Runbooks Exist
**Check**: Documentation for common operational tasks
**Scan for**:
```
Glob: pattern="**/runbook*/**"
Glob: pattern="**/*RUNBOOK*.md"
Glob: pattern="**/docs/operations/**"
```
**Pass criteria**: Runbooks for deploy, rollback, common issues
**Fail impact**: Only original dev can operate system
**Severity**: 🟡 Warning

### OPS-SCALE-002: Rollback Documented
**Check**: Can rollback quickly if deploy fails
**Scan for**:
```
Grep: pattern="rollback"
      glob="**/*.md"

# Check CI for rollback capability
Grep: pattern="rollback|revert|previous"
      glob="**/.github/**/*.yml"
```
**Pass criteria**: Rollback procedure documented and tested
**Fail impact**: Stuck with broken deploy
**Severity**: 🟡 Warning

### OPS-SCALE-003: Zero-Downtime Deploy
**Check**: Deploys don't cause outage
**Scan for**:
```
Grep: pattern="rolling|blue-green|canary"
      glob="**/*.{yml,yaml,json}"
```
**Pass criteria**: Deployment strategy handles traffic during deploy
**Fail impact**: Deploy = downtime
**Severity**: 🟡 Warning

### OPS-SCALE-004: Staging Environment
**Check**: Changes tested before production
**Verification**: 👤 Human-Verify
**How to verify**: Confirm staging environment exists
**Pass criteria**: Staging environment mirrors production
**Fail impact**: First test is production
**Severity**: 🟡 Warning

### OPS-SCALE-005: Feature Flags
**Check**: Can toggle features without deploy
**Scan for**:
```
Grep: pattern="featureFlag|LaunchDarkly|unleash|feature.*toggle"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Feature flag system for gradual rollout
**Fail impact**: All-or-nothing releases
**Severity**: 🟢 Info

---

## Code Maturity

### CODE-SCALE-001: Test Coverage Critical Paths
**Check**: Core flows have test coverage
**Scan for**:
```
Glob: pattern="**/*.test.{ts,tsx,js}"
Glob: pattern="**/*.spec.{ts,tsx,js}"

# Check for tests on critical paths
Grep: pattern="(checkout|payment|auth|login)"
      glob="**/*.test.{ts,tsx}"
```
**Pass criteria**: Auth, payment, core flows have tests
**Fail impact**: Regressions on critical paths go unnoticed
**Severity**: 🟡 Warning

### CODE-SCALE-002: No Duplicate Components
**Check**: Components not duplicated across features
**Scan for**:
```
# Find components with same name in different dirs
Glob: pattern="**/components/**/*.tsx"
# Group by basename, flag duplicates
```
**Pass criteria**: Each component exists in one location
**Fail impact**: Inconsistent UI, maintenance burden
**Severity**: 🟢 Info

### CODE-SCALE-003: Shared Components Used
**Check**: Features import from shared, not local copies
**Scan for**:
```
Grep: pattern="from ['\"].*/(shared|common|ui)/components"
      glob="**/features/**/*.{ts,tsx}"
```
**Pass criteria**: Features use shared components
**Fail impact**: Duplicated code, inconsistent patterns
**Severity**: 🟢 Info

### CODE-SCALE-004: Types Centralized
**Check**: Core types in one location
**Scan for**:
```
Glob: pattern="**/types/**/*.ts"
Grep: pattern="export (type|interface) (User|Project)"
      glob="**/*.ts"
```
**Pass criteria**: Core types in shared/types, not scattered
**Fail impact**: Type conflicts, refactoring pain
**Severity**: 🟢 Info

### CODE-SCALE-005: No TODO on Core Flows
**Check**: Critical paths don't have TODO/FIXME
**Scan for**:
```
Grep: pattern="TODO|FIXME|HACK|XXX"
      glob="**/auth/**/*.{ts,tsx}"

Grep: pattern="TODO|FIXME|HACK|XXX"
      glob="**/payment/**/*.{ts,tsx}"
```
**Pass criteria**: No TODOs in critical paths
**Fail impact**: Known issues in production code
**Severity**: 🟡 Warning

### CODE-SCALE-006: Dependencies Clean
**Check**: No known vulnerabilities
**Scan for**:
```bash
npm audit --audit-level=high
# or
pnpm audit --audit-level=high
```
**Pass criteria**: No high/critical vulnerabilities
**Fail impact**: Known exploits in dependencies
**Severity**: 🔴 Critical
