# shipkit-preflight References

## Purpose
Comprehensive production readiness checklists for SaaS applications.

## Contents

### Checklists
- `checklists/universal-checks.md` — Applies to all projects
- `checklists/auth-checks.md` — Authentication & authorization
- `checklists/payment-checks.md` — Stripe, Lemon Squeezy, payments
- `checklists/database-checks.md` — Supabase, Postgres, data layer
- `checklists/deployment-checks.md` — Vercel, AWS, Railway, Docker
- `checklists/data-privacy-checks.md` — GDPR, PII handling

## How Checklists Are Used

1. Skill reads context (stack.md, why.md, architecture.md)
2. Determines which checklist sections apply
3. Scans codebase for evidence of each check
4. Generates prioritized audit report

## Adding New Checks

When adding checks to any checklist:

```markdown
### Check ID: [category]-[number]
**Check**: [What to verify]
**Scan for**: [How to detect in code]
**Pass criteria**: [What "good" looks like]
**Fail impact**: [What happens if not addressed]
**Fix guidance**: [How to resolve]
```

## Severity Guidelines

- **Blocker** (🔴): Will cause security breach, data loss, or crashes in production
- **Warning** (🟡): Creates risk, tech debt, or poor user experience
- **Info** (🟢): Best practice, nice-to-have, optimization opportunity
