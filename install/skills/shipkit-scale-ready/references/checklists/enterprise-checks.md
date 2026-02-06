# Enterprise Tier Checks

For teams with enterprise customers or high-stakes production systems. These checks ensure compliance, operational maturity, and enterprise-grade reliability.

**Prerequisite**: Growth tier checks should pass first.

---

## Security (Enterprise)

### SEC-ENT-001: Penetration Testing Done
**Check**: Professional security audit completed
**Verification**: 👤 Human-Verify
**How to verify**: Request pentest report from security team/vendor
**Pass criteria**: Pentest completed within last 12 months, findings addressed
**Fail impact**: Unknown vulnerabilities in production
**Severity**: 🔴 Critical (for enterprise customers)

### SEC-ENT-002: Security Audit Completed
**Check**: Code/architecture security review done
**Verification**: 👤 Human-Verify
**How to verify**: Request security audit documentation
**Pass criteria**: Audit completed, critical findings addressed
**Fail impact**: Systemic security issues unidentified
**Severity**: 🔴 Critical

### SEC-ENT-003: SOC2 Type I/II
**Check**: SOC2 compliance certification
**Verification**: 👤 Human-Verify
**How to verify**: Request SOC2 report
**Pass criteria**: SOC2 Type II within last 12 months
**Fail impact**: Cannot serve enterprise customers requiring SOC2
**Severity**: 🔴 Critical (if enterprise sales)

### SEC-ENT-004: Vulnerability Disclosure Program
**Check**: Process for external security reports
**Scan for**:
```
Glob: pattern="**/SECURITY.md"
Grep: pattern="security@|vulnerability|responsible disclosure"
      glob="**/*.md"
```
**Pass criteria**: Security contact published, process documented
**Fail impact**: No channel for security researchers
**Severity**: 🟡 Warning

---

## Database (Enterprise)

### DB-ENT-001: Read Replicas
**Check**: Read-heavy workloads use replicas
**Verification**: 👤 Human-Verify
**How to verify**: Check database infrastructure configuration
**Pass criteria**: Read replicas configured and used for read queries
**Fail impact**: Primary database overloaded
**Severity**: 🟡 Warning

### DB-ENT-002: Encryption at Rest
**Check**: Database encrypted at rest
**Verification**: 👤 Human-Verify
**How to verify**: Check database/cloud provider settings
**Pass criteria**: Encryption enabled with managed keys
**Fail impact**: Data exposed if disk accessed
**Severity**: 🔴 Critical (if PII stored)

### DB-ENT-003: Point-in-Time Recovery
**Check**: Can restore to any point in time
**Verification**: 👤 Human-Verify
**How to verify**: Check database backup settings
**Pass criteria**: PITR enabled with appropriate retention
**Fail impact**: Can only restore to backup snapshots
**Severity**: 🟡 Warning

### DB-ENT-004: Database Failover
**Check**: Database has automatic failover
**Verification**: 👤 Human-Verify
**How to verify**: Check database high availability config
**Pass criteria**: Multi-AZ or equivalent failover configured
**Fail impact**: Database failure = complete outage
**Severity**: 🔴 Critical

---

## Observability (Enterprise)

### OBS-ENT-001: Distributed Tracing
**Check**: Requests traceable across services
**Scan for**:
```
Grep: pattern="opentelemetry|datadog.*trace|newrelic|jaeger"
      glob="**/*.{ts,js,json}"
```
**Pass criteria**: Tracing SDK configured, spans created
**Fail impact**: Can't diagnose cross-service issues
**Severity**: 🟡 Warning

### OBS-ENT-002: Business Metrics Dashboard
**Check**: Key business metrics tracked
**Verification**: 👤 Human-Verify
**How to verify**: Request access to metrics dashboard
**Pass criteria**: Signups, conversions, revenue tracked and visualized
**Fail impact**: No visibility into business health
**Severity**: 🟡 Warning

### OBS-ENT-003: Log Retention Policy
**Check**: Logs retained per compliance requirements
**Verification**: 👤 Human-Verify
**How to verify**: Check log management settings
**Pass criteria**: Retention period set, compliant with regulations
**Fail impact**: Compliance violation, can't investigate old issues
**Severity**: 🟡 Warning

### OBS-ENT-004: Anomaly Detection
**Check**: Automated alerting on anomalies
**Verification**: 👤 Human-Verify
**How to verify**: Check monitoring tool for anomaly rules
**Pass criteria**: Anomaly detection on key metrics
**Fail impact**: Issues not caught until major
**Severity**: 🟢 Info

---

## Performance (Enterprise)

### PERF-ENT-001: Load Testing Completed
**Check**: System tested under expected load
**Verification**: 👤 Human-Verify
**How to verify**: Request load test report
**Pass criteria**: Tested at 2-10x expected peak traffic
**Fail impact**: Unknown breaking point
**Severity**: 🔴 Critical

### PERF-ENT-002: Auto-Scaling Configured
**Check**: System scales with demand
**Verification**: 👤 Human-Verify
**How to verify**: Check cloud provider auto-scaling settings
**Pass criteria**: Auto-scaling configured with appropriate limits
**Fail impact**: Manual intervention needed for traffic spikes
**Severity**: 🟡 Warning

### PERF-ENT-003: CDN Configured
**Check**: Static assets served from CDN
**Scan for**:
```
Grep: pattern="cloudfront|cloudflare|fastly|cdn"
      glob="**/*.{json,yml,yaml,ts,js}"
```
**Pass criteria**: CDN in front of static assets
**Fail impact**: Slow global performance, high origin load
**Severity**: 🟡 Warning

### PERF-ENT-004: Performance Baseline
**Check**: Performance metrics baselined and monitored
**Verification**: 👤 Human-Verify
**How to verify**: Request APM dashboard access
**Pass criteria**: P50, P95, P99 latencies tracked over time
**Fail impact**: Can't detect performance regressions
**Severity**: 🟡 Warning

---

## Reliability (Enterprise)

### REL-ENT-001: Circuit Breakers
**Check**: External service failures isolated
**Scan for**:
```
Grep: pattern="circuitBreaker|circuit-breaker|opossum|cockatiel"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Circuit breakers on external dependencies
**Fail impact**: Cascade failures when dependency degrades
**Severity**: 🟡 Warning

### REL-ENT-002: Bulkhead Pattern
**Check**: Resource isolation between tenants/features
**Scan for**:
```
Grep: pattern="bulkhead|isolat|partition"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Critical paths isolated from non-critical
**Fail impact**: One bad actor affects all users
**Severity**: 🟡 Warning

### REL-ENT-003: Chaos Testing
**Check**: System tested under failure conditions
**Verification**: 👤 Human-Verify
**How to verify**: Request chaos test results
**Pass criteria**: Chaos experiments run, weaknesses addressed
**Fail impact**: Unknown failure modes
**Severity**: 🟢 Info

### REL-ENT-004: Multi-Region
**Check**: System available across regions
**Verification**: 👤 Human-Verify
**How to verify**: Check infrastructure deployment
**Pass criteria**: Deployed to 2+ regions with failover
**Fail impact**: Regional outage = complete outage
**Severity**: 🟡 Warning (depends on SLA)

### REL-ENT-005: Disaster Recovery Tested
**Check**: DR plan tested
**Verification**: 👤 Human-Verify
**How to verify**: Request DR test documentation
**Pass criteria**: DR tested within last 6 months
**Fail impact**: DR plan may not work when needed
**Severity**: 🔴 Critical

---

## Operational Readiness (Enterprise)

### OPS-ENT-001: Incident Response Process
**Check**: Documented incident handling
**Scan for**:
```
Glob: pattern="**/INCIDENT*.md"
Glob: pattern="**/incident*/**"
Grep: pattern="incident response|on-call|escalation"
      glob="**/*.md"
```
**Pass criteria**: Incident process documented, roles defined
**Fail impact**: Chaos during incidents
**Severity**: 🔴 Critical

### OPS-ENT-002: On-Call Rotation
**Check**: Someone always responsible
**Verification**: 👤 Human-Verify
**How to verify**: Check PagerDuty/OpsGenie configuration
**Pass criteria**: On-call rotation configured, documented
**Fail impact**: No one responsible after hours
**Severity**: 🔴 Critical

### OPS-ENT-003: Post-Mortem Process
**Check**: Learning from incidents
**Scan for**:
```
Glob: pattern="**/postmortem*/**"
Glob: pattern="**/*POST*MORTEM*.md"
Grep: pattern="post-?mortem|incident review|blameless"
      glob="**/*.md"
```
**Pass criteria**: Post-mortem template exists, process documented
**Fail impact**: Same incidents repeat
**Severity**: 🟡 Warning

### OPS-ENT-004: SLAs Defined
**Check**: Service level agreements documented
**Scan for**:
```
Glob: pattern="**/SLA*.md"
Grep: pattern="SLA|uptime|availability.*99|service level"
      glob="**/*.md"
```
**Pass criteria**: SLAs defined, monitored, reported
**Fail impact**: No accountability for reliability
**Severity**: 🔴 Critical (for enterprise contracts)

### OPS-ENT-005: Change Management
**Check**: Changes reviewed and tracked
**Scan for**:
```
Grep: pattern="CODEOWNERS|require.*review|protected.*branch"
      glob="**/*"
```
**Pass criteria**: PRs required, reviews enforced
**Fail impact**: Unreviewed changes cause incidents
**Severity**: 🟡 Warning

---

## Compliance (Enterprise)

### COMP-ENT-001: GDPR Data Export
**Check**: Users can export their data
**Scan for**:
```
Grep: pattern="export.*data|data.*export|downloadData"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Data export endpoint exists and works
**Fail impact**: GDPR non-compliance
**Severity**: 🔴 Critical (if EU users)

### COMP-ENT-002: GDPR Data Deletion
**Check**: Users can delete their data
**Scan for**:
```
Grep: pattern="deleteAccount|delete.*user|gdpr.*delete"
      glob="**/*.{ts,tsx,js}"
```
**Pass criteria**: Account deletion removes all user data
**Fail impact**: GDPR non-compliance
**Severity**: 🔴 Critical (if EU users)

### COMP-ENT-003: Audit Logging
**Check**: Sensitive actions logged
**Scan for**:
```
Grep: pattern="auditLog|audit.*log|logAction|trackEvent"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Auth, data access, admin actions logged
**Fail impact**: Can't investigate security incidents
**Severity**: 🟡 Warning

### COMP-ENT-004: Data Retention Enforced
**Check**: Old data cleaned up per policy
**Scan for**:
```
Grep: pattern="retention|cleanup|purge|deleteOld"
      glob="**/*.{ts,js}"
```
**Pass criteria**: Automated cleanup of expired data
**Fail impact**: Data hoarding, compliance risk
**Severity**: 🟡 Warning

### COMP-ENT-005: SOC2 Type II
**Check**: SOC2 Type II certification current
**Verification**: 👤 Human-Verify
**How to verify**: Request current SOC2 report
**Pass criteria**: SOC2 Type II report within last 12 months
**Fail impact**: Cannot close enterprise deals requiring SOC2
**Severity**: 🔴 Critical (for enterprise sales)

### COMP-ENT-006: HIPAA Compliance
**Check**: Healthcare data handled correctly
**Verification**: 👤 Human-Verify
**How to verify**: Request HIPAA compliance documentation
**Pass criteria**: BAA in place, controls implemented
**Fail impact**: Illegal to handle healthcare data
**Severity**: 🔴 Critical (if handling PHI)

---

## Summary: Enterprise Critical Path

**Must-have for enterprise customers:**
1. SOC2 Type II (or in progress)
2. Penetration testing completed
3. Incident response process
4. On-call rotation
5. SLAs defined
6. GDPR compliance (if EU)
7. Encryption at rest
8. Database failover
9. Disaster recovery tested

**Nice-to-have but expected:**
- Distributed tracing
- Chaos testing
- Multi-region
- Audit logging
