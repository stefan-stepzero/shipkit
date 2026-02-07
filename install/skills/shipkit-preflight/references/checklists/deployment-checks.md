# Deployment Checks (MVP)

Platform-specific checks for common deployment targets.

**MVP focus**: Build passes, domain works, HTTPS, health endpoint.
**Moved to scale-ready**: Rollback procedure, zero-downtime deploys.

---

## Universal Deployment

### DEPLOY-001: Environment Variables Set
**Check**: All required env vars configured in platform
**Scan for**: .env.example vs platform env config
**Pass criteria**: All required vars have values
**Fail impact**: App crashes or misbehaves
**Severity**: 🔴 Blocker

### DEPLOY-002: Domain Configured
**Check**: Custom domain set up with SSL
**Scan for**: Domain configuration
**Pass criteria**: App accessible on production domain
**Fail impact**: Users can't access app
**Severity**: 🔴 Blocker

### DEPLOY-003: HTTPS Enforced
**Check**: HTTP redirects to HTTPS
**Scan for**: SSL/redirect configuration
**Pass criteria**: No HTTP access in production
**Fail impact**: Insecure connections possible
**Severity**: 🔴 Blocker

### DEPLOY-004: Build Succeeds in CI
**Check**: Build passes in deployment environment
**Scan for**: CI/CD build logs
**Pass criteria**: Clean build in production-like environment
**Fail impact**: Works locally but fails in prod
**Severity**: 🔴 Blocker

---

## Vercel Specific

### DEPLOY-VERCEL-001: Framework Detected
**Check**: Vercel correctly detects framework
**Scan for**: vercel.json, framework settings
**Pass criteria**: Correct build settings applied
**Fail impact**: Wrong build process
**Severity**: 🟡 Warning

### DEPLOY-VERCEL-002: Serverless Function Limits
**Check**: Functions stay under size/time limits
**Scan for**: Function bundle size, execution time
**Pass criteria**: Functions under 50MB, 10s default timeout
**Fail impact**: Functions fail or timeout
**Severity**: 🟡 Warning

### DEPLOY-VERCEL-003: Edge Runtime Compatibility
**Check**: Edge functions use compatible APIs
**Scan for**: Node.js APIs in edge functions
**Pass criteria**: Only edge-compatible APIs used
**Fail impact**: Functions fail at edge
**Severity**: 🔴 Blocker (if using edge)

### DEPLOY-VERCEL-004: Environment Variables Scoped
**Check**: Env vars set for correct environments
**Scan for**: Production vs preview vs development vars
**Pass criteria**: Sensitive vars not in preview
**Fail impact**: Test data in prod or vice versa
**Severity**: 🟡 Warning

### DEPLOY-VERCEL-005: Cron Jobs Configured (if needed)
**Check**: Scheduled functions set up
**Scan for**: vercel.json crons, @vercel/cron
**Pass criteria**: Crons running as expected
**Fail impact**: Scheduled tasks don't run
**Severity**: 🟡 Warning (if applicable)

### DEPLOY-VERCEL-006: External Service Routes Have maxDuration
**Check**: Routes calling external services export `maxDuration` matching plan
**Scan for**:
```
# Find routes with external calls
Grep: pattern="openai|anthropic|gemini|stripe|fetch\("
      glob="**/app/**/route.{ts,js}"

# Check those same files for maxDuration
Grep: pattern="export.*maxDuration"
      glob="**/app/**/route.{ts,js}"
```
**Pass criteria**: Every route with external service calls exports `maxDuration`
**Fail impact**: Route killed at 10s (Hobby) or 60s (Pro) mid-LLM-call
**Severity**: 🔴 Blocker

---

## AWS Specific

### DEPLOY-AWS-001: IAM Roles Configured
**Check**: Minimal IAM permissions
**Scan for**: IAM policy, role configuration
**Pass criteria**: Least privilege access
**Fail impact**: Over-permissioned, security risk
**Severity**: 🟡 Warning

### DEPLOY-AWS-002: Secrets in Secrets Manager
**Check**: Secrets not in environment variables
**Scan for**: AWS Secrets Manager usage
**Pass criteria**: Secrets fetched from Secrets Manager
**Fail impact**: Secrets visible in console
**Severity**: 🟡 Warning

### DEPLOY-AWS-003: CloudWatch Logging
**Check**: Logs going to CloudWatch
**Scan for**: Logging configuration
**Pass criteria**: Logs accessible in CloudWatch
**Fail impact**: Can't debug production issues
**Severity**: 🟡 Warning

### DEPLOY-AWS-004: Auto Scaling Configured
**Check**: App scales under load
**Scan for**: Auto scaling policies
**Pass criteria**: Scales up on demand
**Fail impact**: Outages under load
**Severity**: 🟡 Warning (production)

---

## Railway Specific

### DEPLOY-RAILWAY-001: Healthcheck Configured
**Check**: Railway health check endpoint set
**Scan for**: railway.json, health check config
**Pass criteria**: Railway monitors app health
**Fail impact**: No automatic restart on failure
**Severity**: 🟡 Warning

### DEPLOY-RAILWAY-002: Private Networking
**Check**: Internal services use private network
**Scan for**: Service communication configuration
**Pass criteria**: Internal traffic not public
**Fail impact**: Unnecessary public exposure
**Severity**: 🟡 Warning

### DEPLOY-RAILWAY-003: Volume Persistence (if needed)
**Check**: Persistent storage configured
**Scan for**: Volume configuration
**Pass criteria**: Data survives redeploys
**Fail impact**: Data loss on redeploy
**Severity**: 🔴 Blocker (if needed)

---

## Docker Specific

### DEPLOY-DOCKER-001: Multi-Stage Build
**Check**: Production image is minimal
**Scan for**: Multi-stage Dockerfile
**Pass criteria**: Final image has only runtime deps
**Fail impact**: Large images, slow deploys
**Severity**: 🟢 Info

### DEPLOY-DOCKER-002: Non-Root User
**Check**: Container runs as non-root
**Scan for**: USER directive in Dockerfile
**Pass criteria**: App runs as unprivileged user
**Fail impact**: Container escape risk
**Severity**: 🟡 Warning

### DEPLOY-DOCKER-003: Health Check in Dockerfile
**Check**: HEALTHCHECK instruction present
**Scan for**: HEALTHCHECK in Dockerfile
**Pass criteria**: Docker can monitor container health
**Fail impact**: Orchestrator can't detect failures
**Severity**: 🟡 Warning

### DEPLOY-DOCKER-004: No Secrets in Image
**Check**: Secrets not baked into image
**Scan for**: Hardcoded secrets in Dockerfile or source
**Pass criteria**: Secrets passed at runtime
**Fail impact**: Secrets exposed in image layers
**Severity**: 🔴 Blocker

---

## CI/CD

### DEPLOY-CI-001: Tests Run Before Deploy
**Check**: Tests gate deployment
**Scan for**: CI configuration, test step before deploy
**Pass criteria**: Failed tests block deployment
**Fail impact**: Broken code reaches production
**Severity**: 🟡 Warning

### DEPLOY-CI-002: Rollback Possible
**Status**: ➡️ MOVED TO SCALE-READY (operational maturity)
**Check**: Can revert to previous version
**Severity**: 🟡 Warning — see `/shipkit-scale-ready`

### DEPLOY-CI-003: Deploy Notifications
**Check**: Team notified of deployments
**Scan for**: Notification configuration
**Pass criteria**: Slack/email on deploy
**Fail impact**: Team unaware of changes
**Severity**: 🟢 Info
