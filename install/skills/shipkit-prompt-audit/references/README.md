# shipkit-prompt-audit References

## Purpose
Detection patterns, audit checklists, and anti-pattern catalogs for auditing LLM prompt pipeline architecture.

## Contents

- `detection-patterns.md` — Grep/Glob patterns for discovering LLM integrations by provider (OpenAI, Anthropic, Gemini, LangChain, Vercel AI SDK), prompt templates, schema definitions, pipeline patterns, fallback patterns
- `audit-checklist.md` — Detailed checks per audit dimension with IDs (PA-DEC-001, PA-PAR-001, etc.), severity levels, scan methods, and pass/fail criteria
- `anti-patterns.md` — 8 common prompt architecture anti-patterns with detection methods and resolutions

## How References Are Used

1. **Detection patterns** are used in Step 1 (Discover) to find all LLM integration points
2. **Audit checklist** is used in Step 3 (Audit) to systematically check each dimension
3. **Anti-patterns** are cross-referenced against discovered code to flag known structural problems

## Severity Guidelines

- **Critical**: Will cause failures, security issues, or data corruption in production
- **Should Fix**: Quality/reliability issues, performance problems, technical debt
- **Minor**: Suggestions, optimizations, best practices

## Adding New Checks

When adding checks to the audit checklist:

```markdown
### PA-[DIM]-[NNN]: [Title]
**Severity**: [Critical / Should Fix / Minor]
**Scan**: [How to detect in code — grep patterns, file reading, etc.]
**Pass**: [What "good" looks like]
**Fail**: [What triggers this finding]
**Fix**: [How to resolve]
```

Dimension codes: DEC (decomposition), PAR (parallelization), SCH (schema), CHN (chain), CAC (cache), FBK (fallback), CTX (context), CON (constraint), INP (input), REF (reference).
