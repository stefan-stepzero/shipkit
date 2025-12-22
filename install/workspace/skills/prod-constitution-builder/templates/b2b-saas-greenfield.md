# Established B2B Product Constitution

**Context:** Enterprise B2B SaaS with proven product-market fit
**Generated:** [Date]

---

## Prime Directive
Enterprise trust and reliability above all else.

---

## FORBIDDEN

- ❌ **Breaking existing integrations** (SSO, SCIM, APIs - sacred)
- ❌ **Shipping without security review** (pen test findings must be addressed)
- ❌ **Ignoring compliance requirements** (SOC 2, GDPR, HIPAA per contract)
- ❌ **Removing features without 6mo notice** (enterprise moves slow)
- ❌ **Breaking API backward compatibility** (version, deprecate, migrate)
- ❌ **Bypassing change management** (customers need advance notice)
- ❌ **Downtime during business hours** (maintenance windows only)
- ❌ **Surprise pricing changes** (honor contract terms)
- ❌ **Ignoring enterprise feature requests** (they pay the bills)
- ❌ **Skipping documentation** (admins need detailed docs)

---

## REQUIRED

- ✅ **SSO/SCIM support** (Okta, Azure AD, Google Workspace)
- ✅ **Audit logs** (who did what, when - immutable)
- ✅ **Role-based access control** (granular permissions)
- ✅ **Data residency options** (EU, US regions minimum)
- ✅ **SLA commitments met** (99.9% or contract-specific)
- ✅ **Security questionnaires answered** (maintain library of answers)
- ✅ **Penetration testing** (annual minimum, quarterly for high-security)
- ✅ **Change notifications** (30 days minimum for major changes)
- ✅ **Customer success check-ins** (QBRs for enterprise accounts)
- ✅ **Comprehensive API documentation** (OpenAPI spec, examples, SDKs)

---

## ALLOWED TECHNICAL DEBT

**Almost none. Enterprise customers expect:**

- Production-grade code
- Comprehensive testing
- Security best practices
- Detailed monitoring

**Exception:** Internal tools can be scrappy

---

## Decision Framework

**For new features:**

1. **Enterprise need or SMB delight?** (enterprise pays 80% of revenue)
2. **Integration complexity?** (customers have complex stacks)
3. **Security implications?** (CISO will review)
4. **Compliance impact?** (legal/compliance review)
5. **Backward compatibility?** (can't break existing customers)

**For pricing changes:**

1. **Grandfather existing customers?** (usually yes for 12 months)
2. **Customer success notified?** (they'll field the calls)
3. **Value justification clear?** (tie to new capabilities)

**For deprecations:**

1. **Telemetry shows <5% usage?** (data-driven decisions)
2. **6-month deprecation notice?** (enterprise needs time)
3. **Migration path documented?** (with support)
4. **Key accounts consulted?** (avoid churn)

---

## Quality Standards

**What "done" means:**

**For features:**
- [ ] Security review completed (threat model, pen test if needed)
- [ ] Compliance checked (GDPR, SOC 2, industry-specific)
- [ ] Admin controls (who can enable/configure?)
- [ ] Audit logging (track usage for compliance)
- [ ] API documented (if exposes new endpoints)
- [ ] Pricing impact analyzed (affects tiers/limits?)
- [ ] Customer success trained (can demo, troubleshoot)
- [ ] Help docs published (admin + end-user)
- [ ] Release notes written (technical + business value)
- [ ] Backward compatible (or versioned API)

**For bugs:**
- [ ] Severity: P0 (system down) / P1 (major feature broken) / P2 (minor issue)
- [ ] Customer impact assessed (how many customers affected?)
- [ ] Root cause documented (post-mortem for P0/P1)
- [ ] Tests added to prevent regression
- [ ] SLA met: P0 (2hrs), P1 (24hrs), P2 (1 week)

**For releases:**
- [ ] Change advisory sent (30 days for major, 7 days for minor)
- [ ] Staging environment validated (run through smoke tests)
- [ ] Rollback plan ready (can revert in < 15 min)
- [ ] On-call engineer assigned (24/7 coverage)
- [ ] Monitoring dashboards updated
- [ ] Customer success team briefed

---

## Metrics That Matter

**Health metrics:**

- **Reliability:** 99.9%+ uptime (per SLA), p95 latency < 500ms
- **Security:** Zero high/critical vulnerabilities, security audit compliance
- **Customer health:** NRR > 100%, Gross retention > 90%, NPS > 30
- **Support:** < 2hr first response (critical), < 95% CSAT

**Business metrics:**

- Logo retention (especially enterprise accounts)
- Expansion revenue (upsells, cross-sells)
- Time to value (days to first value for new customers)
- Admin adoption (% of purchased seats actively used)

---

## Enterprise-Grade Requirements

**Security:**
- Penetration testing: Annual (external), Quarterly (internal)
- Vulnerability management: Patch critical within 48hrs
- Access control: MFA enforced, IP whitelisting available
- Data encryption: At rest (AES-256), In transit (TLS 1.3+)
- Incident response: Plan tested quarterly, customers notified within 24hrs

**Compliance:**
- SOC 2 Type II (required)
- GDPR compliance (required)
- HIPAA BAA available (if handling PHI)
- Industry-specific: FINRA, FedRAMP as needed

**Reliability:**
- Multi-region deployment (DR/failover)
- Automated backups (hourly incremental, daily full)
- RTO < 4 hours, RPO < 1 hour
- Zero data loss tolerance

**Integration:**
- RESTful APIs (versioned, rate-limited)
- Webhooks (reliable delivery, retry logic)
- SCIM for user provisioning
- SSO via SAML 2.0 / OIDC

---

## Customer Success Principles

**We ensure enterprise success by:**

1. **Onboarding:** Dedicated CSM, implementation plan, success metrics
2. **Training:** Admin training, end-user training, office hours
3. **Support:** 24/7 for critical (phone + email), dedicated slack channel
4. **QBRs:** Quarterly business reviews with usage analytics, roadmap preview
5. **Escalation:** Executive sponsor for >$100K accounts

**Red flag:** Enterprise account health score drops → Immediate intervention

---

## Change Management

**Communication tiers:**

**30 days notice (Major):**
- Breaking API changes (with migration guide)
- Pricing changes
- Feature deprecations
- Security/compliance updates

**7 days notice (Minor):**
- New features (opt-in)
- UI improvements
- Performance optimizations
- Non-breaking API additions

**No notice (Patches):**
- Bug fixes
- Security patches (zero-day)
- Performance fixes

**Channels:**
- Email to admins
- In-app notifications
- Status page (status.company.com)
- API changelog
- Customer success managers (for enterprise accounts)

---

## Success Criteria

**Product is enterprise-ready when:**
- ✓ SLA commitments consistently met (99.9%+ uptime)
- ✓ Compliance certifications current (SOC 2, GDPR, etc.)
- ✓ Net Revenue Retention > 100% (customers expand)
- ✓ Enterprise customers are reference-able (happy to recommend)
- ✓ Security posture is defensible (pass customer audits)

---

**Review this constitution:** Quarterly (or when compliance requirements change)
**Update when:** New compliance needs, major enterprise customer onboarding, security incidents
