# Scale-Ready References

Detailed checklists for scale readiness audits.

## Files

| File | Description |
|------|-------------|
| `checklists/growth-checks.md` | Growth tier checks — for teams with traction |
| `checklists/enterprise-checks.md` | Enterprise tier checks — for high-stakes production |

## Tier Progression

```
MVP (preflight)
    ↓
Growth (scale-ready default)
    ↓
Enterprise (scale-ready --enterprise)
```

## Check ID Format

- `SEC-SCALE-XXX` — Security, Growth tier
- `SEC-ENT-XXX` — Security, Enterprise tier
- `DB-SCALE-XXX` — Database, Growth tier
- `OBS-SCALE-XXX` — Observability, Growth tier
- `PERF-SCALE-XXX` — Performance, Growth tier
- `REL-SCALE-XXX` — Reliability, Growth tier
- `OPS-SCALE-XXX` — Operational, Growth tier
- `CODE-SCALE-XXX` — Code Maturity, Growth tier
- `COMP-ENT-XXX` — Compliance, Enterprise tier

## Human-Verify Items

Some checks cannot be verified by Claude (require external tools, infra access, or documentation review). These are marked with:

```
**Verification**: 👤 Human-Verify
**How to verify**: [Steps for human to verify]
```

The skill will collect these into a checklist for the team to complete.
