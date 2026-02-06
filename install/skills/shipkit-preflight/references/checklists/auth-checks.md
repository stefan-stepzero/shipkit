# Authentication & Authorization Checks (MVP)

Applies when project has user authentication.

**MVP focus**: Auth on routes, session management, rate limiting, brute force prevention.
**Moved to scale-ready**: Security headers, admin route hardening, API key rotation.

---

## Authentication

### AUTH-001: Protected Routes Have Auth
**Check**: All non-public routes require authentication
**Scan for**: API routes without auth middleware, pages without session check
**Pass criteria**: Every protected resource checks auth
**Fail impact**: Unauthorized access to user data
**Severity**: 🔴 Blocker

### AUTH-002: Session Expiry
**Check**: Sessions expire and refresh properly
**Scan for**: Token expiry configuration, refresh token handling
**Pass criteria**: Sessions expire, refresh works, expired sessions rejected
**Fail impact**: Stale sessions, security risk
**Severity**: 🔴 Blocker

### AUTH-003: Logout Clears Session
**Check**: Logout invalidates session server-side
**Scan for**: Logout handler, session invalidation
**Pass criteria**: Session token invalid after logout
**Fail impact**: Session hijacking possible
**Severity**: 🔴 Blocker

### AUTH-004: Password Requirements (if applicable)
**Check**: Passwords meet minimum security standards
**Scan for**: Password validation logic
**Pass criteria**: Min 8 chars, complexity rules
**Fail impact**: Weak passwords accepted
**Severity**: 🟡 Warning

### AUTH-005: Rate Limiting on Auth Endpoints
**Check**: Login/register endpoints rate limited
**Scan for**: Rate limit middleware on auth routes
**Pass criteria**: Brute force attempts blocked
**Fail impact**: Credential stuffing attacks
**Severity**: 🔴 Blocker

### AUTH-006: Brute Force Prevention Pattern
**Check**: Account lockout or exponential delay after failed attempts
**Pattern**: Counter in DB tracking failed attempts, lockout threshold
**Scan for**:
```
Grep: pattern="failedAttempts|loginAttempts|lockout|accountLocked"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Failed login tracking exists, lockout or delay logic
**Fail impact**: Automated credential stuffing succeeds eventually
**Severity**: 🔴 Blocker

### AUTH-007: Form Abuse Prevention Pattern
**Check**: Public forms protected against bot spam
**Pattern**: Honeypot field (hidden, bots fill it) + timing check (< 2s = bot)
**Scan for**:
```
Grep: pattern="honeypot|botCheck|formTiming|spamProtection"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Contact/signup forms have spam protection
**Fail impact**: Inbox flooded with bot submissions
**Severity**: 🟡 Warning

### AUTH-008: Password Reset Flow Secure
**Check**: Password reset uses time-limited tokens
**Scan for**: Reset token generation, expiry check
**Pass criteria**: Token expires, single use, secure delivery
**Fail impact**: Account takeover via reset
**Severity**: 🔴 Blocker

---

## OAuth (if applicable)

### AUTH-OAUTH-001: State Parameter Used
**Check**: OAuth flow uses state parameter for CSRF
**Scan for**: State generation and validation in OAuth callback
**Pass criteria**: State validated on callback
**Fail impact**: CSRF attacks on OAuth
**Severity**: 🔴 Blocker

### AUTH-OAUTH-002: Tokens Stored Securely
**Check**: OAuth tokens not exposed to client
**Scan for**: Access tokens in localStorage, cookies without httpOnly
**Pass criteria**: Tokens in httpOnly cookies or server-side
**Fail impact**: Token theft via XSS
**Severity**: 🔴 Blocker

---

## Authorization

### AUTHZ-001: User Can Only Access Own Data
**Check**: Users cannot access other users' resources
**Scan for**: Queries without user_id filter, missing ownership checks
**Pass criteria**: All queries scoped to current user
**Fail impact**: IDOR vulnerability, data breach
**Severity**: 🔴 Blocker

### AUTHZ-002: Admin Routes Protected
**Check**: Admin functionality requires admin role
**Scan for**: Admin routes, role checks
**Pass criteria**: Admin actions verify admin role
**Fail impact**: Privilege escalation
**Severity**: 🔴 Blocker

### AUTHZ-003: Role Checks Server-Side
**Check**: Authorization checked on server, not just UI
**Scan for**: Role checks only in frontend
**Pass criteria**: Server validates permissions
**Fail impact**: Bypass via direct API calls
**Severity**: 🔴 Blocker

---

## Security Headers

### AUTH-HDR-001: CSRF Protection
**Check**: CSRF tokens on state-changing requests
**Scan for**: CSRF middleware, token validation
**Pass criteria**: POST/PUT/DELETE require valid CSRF token
**Fail impact**: Cross-site request forgery
**Severity**: 🔴 Blocker

### AUTH-HDR-002: Secure Cookie Flags
**Check**: Auth cookies have secure flags
**Scan for**: Cookie settings (httpOnly, secure, sameSite)
**Pass criteria**: httpOnly=true, secure=true, sameSite=strict/lax
**Fail impact**: Cookie theft, CSRF
**Severity**: 🔴 Blocker

---

## Multi-Tenancy (if applicable)

### AUTH-MT-001: Tenant Isolation
**Check**: Users only see their organization's data
**Scan for**: Queries without org_id/tenant_id filter
**Pass criteria**: All queries scoped to tenant
**Fail impact**: Cross-tenant data leak
**Severity**: 🔴 Blocker

### AUTH-MT-002: Tenant in JWT/Session
**Check**: Tenant context stored in auth token
**Scan for**: Tenant ID handling in auth
**Pass criteria**: Tenant verified on each request
**Fail impact**: Tenant spoofing
**Severity**: 🔴 Blocker
