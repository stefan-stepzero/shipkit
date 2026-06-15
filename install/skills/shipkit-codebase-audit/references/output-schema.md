# Output Schema

## Artifact: `.shipkit/codebase-audit.json`

Follows the Shipkit JSON artifact convention. Written on **every tier** (quick/deep/exhaustive). Overwrite-with-archive.

```json
{
  "$schema": "shipkit-artifact",
  "type": "codebase-audit",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-codebase-audit",
  "summary": {
    "tier": "quick | deep | exhaustive",
    "scope": "repo root | <directory>",
    "commit": "<git short hash, if available>",
    "packageManager": "npm | pnpm | yarn | bun | none",
    "tooling": "knip (ephemeral) | knip (installed) | depcheck | ... | none",
    "intentSource": "shipkit | code-surface | none",
    "filesScanned": 0,
    "coverage": { "expectedUnits": 0, "reconciledUnits": 0 },
    "counts": {
      "modeA": { "unusedExports": 0, "unusedFiles": 0, "unusedDependencies": 0, "unusedDevDependencies": 0, "unresolvedImports": 0 },
      "modeB": { "contractDrift": 0, "halfWiredSeams": 0, "declaredbutUnbuilt": 0, "builtButUndeclared": 0 }
    }
  },
  "findings": [
    {
      "id": "MA-001 | MB-001",
      "mode": "A | B",
      "category": "unusedExport | unusedFile | unusedDependency | unresolvedImport | contractDrift | halfWiredSeam | declaredButUnbuilt | builtButUndeclared",
      "severity": "high | medium | low",
      "title": "short description",
      "file": "path",
      "line": 0,
      "evidence": "tool output excerpt or file:line proof",
      "impact": "why it matters",
      "suggestion": "what to do (report-only — not auto-applied)"
    }
  ],
  "deltas": {
    "new": ["finding ids new since last audit"],
    "fixed": ["finding ids present last audit, gone now"],
    "regressions": ["finding ids that returned"]
  },
  "auditHistory": [
    { "date": "YYYY-MM-DD", "commit": "hash", "tier": "...", "totalFindings": 0 }
  ]
}
```

### Notes
- `severity`: deterministic Mode A findings default to `medium` (unused) / `high` (unresolved import = likely breakage). Mode B contract drift that breaks a caller = `high`.
- `coverage.reconciledUnits` must equal `expectedUnits` before an `exhaustive` run is reported complete.
- `intentSource: "none"` is valid (non-Shipkit repo, Mode B ran on code surface only) — surface the caveat in the presented summary.

---

## Contract Ledger (exhaustive tier, internal)

Each per-file/slice worker writes a ledger to disk (e.g. `.shipkit/audits/ledgers/<unit>.json`). The reconcile step JOINS these — it is not part of the final artifact, but its mismatches become Mode B `findings`.

```json
{
  "unit": "src/services/auth.ts",
  "provides": [
    { "symbol": "verifyToken", "kind": "function", "signature": "(token: string) => Promise<User>", "exported": true }
  ],
  "expects": [
    { "fromModule": "./db", "symbol": "getUser", "kind": "function", "signature": "(id: string) => Promise<User>" }
  ],
  "integrity": [
    { "category": "deadCode | incoherence | internalContract", "line": 0, "detail": "..." }
  ]
}
```

### Reconcile-join algorithm
For every `expects` entry across all ledgers, resolve `fromModule` + `symbol` to a `provides` entry in the target unit's ledger:
- **No match** → `MB` finding `unresolvedImport`/`halfWiredSeam` (expected-but-unprovided).
- **Signature mismatch** → `MB` finding `contractDrift` (high).
- A `provides` entry with `exported: true` that no ledger `expects` → candidate `builtButUndeclared` / unused export (cross-check Mode A to avoid double-reporting).

The join is the only place cross-file drift surfaces — a single-file worker never holds both sides of a contract.
