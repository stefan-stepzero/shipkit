# Verification Protocol

Standard verification patterns for Shipkit skills. Reference this protocol when making claims about codebase state.

---

## Core Principle

**Never claim without evidence.** Every claim about codebase state requires tool verification.

Claims like "file not created" or "component unused" without verification are **verification theater**.

---

## State Classification

Classify each finding into ONE of these states:

| State | Definition | Evidence Pattern |
|-------|------------|------------------|
| `NOT_CREATED` | File/component doesn't exist | Glob returns empty |
| `CREATED_UNUSED` | File exists but nothing imports/uses it | Glob finds file + Grep returns 0 imports |
| `CREATED_WRONG` | File exists but implementation doesn't match spec | Read file + compare to spec |
| `WIRING_MISSING` | Component exists but not connected to app | Grep for render/route registration returns 0 |
| `BROKEN_IMPORT` | Import statement points to nonexistent file | Read shows import + Glob for target returns empty |
| `CIRCULAR` | Mutual imports between files | Read both files show cross-imports |
| `STALE` | File exists but outdated vs related files | Compare timestamps or content |
| `INCONSISTENT` | Multiple instances don't match each other | Grep finds variations |

---

## Common Verification Patterns

### File Existence

```
Glob: pattern="**/filename.*"
- Empty result → NOT_CREATED
- Match found → exists (read to verify content)
```

### Symbol Usage

```
Grep: pattern="import.*SymbolName|<SymbolName"
      glob="**/*.{ts,tsx}"
- 0 matches → never imported
- 1 match (definition only) → CREATED_UNUSED
- 2+ matches → used
```

### Pattern Consistency

```
Grep: pattern="pattern-keyword" glob="**/*.{ts,tsx}"
For each match:
  Read file, verify pattern implementation
  Report inconsistencies
```

### Timestamp Comparison

```
For freshness checks:
1. Read file, extract timestamp (expect ISO 8601: YYYY-MM-DDTHH:MM:SSZ)
2. Parse: new Date(timestamp)
3. Compare to current date
4. Report: fresh (<7 days) or stale (>7 days)

If timestamp unparseable → treat as stale
```

---

## Verification Sequence

Before reporting ANY finding, execute these steps:

| Step | Action | Example |
|------|--------|---------|
| **1. IDENTIFY** | What tool call proves this claim? | "I need to confirm `UserCard` is unused" |
| **2. RUN** | Execute the tool call | `Grep: pattern="UserCard" glob="**/*.{ts,tsx}"` |
| **3. READ** | Examine full output | "Found 2 matches: definition + one import" |
| **4. CLASSIFY** | Determine exact state from evidence | "CREATED_USED (imported in Dashboard.tsx:14)" |
| **5. REPORT** | State finding WITH evidence | "UserCard is imported in Dashboard.tsx:14" |

---

## Evidence Citation Format

When reporting findings, use this format:

```markdown
**[Issue Type]** [STATE_CLASSIFICATION]
- Evidence: `[Tool]("[pattern]")` → [result]
- File: `path/to/file.ts:line`
- Impact: [consequence if not fixed]
```

**Example:**
```markdown
**Structural: Orphan component** [CREATED_UNUSED]
- Evidence: `Glob("**/UserCard.tsx")` → found at src/components/UserCard.tsx
- Evidence: `Grep("UserCard" in "**/*.tsx")` → 1 match (definition only)
- File: `src/components/UserCard.tsx`
- Classification: CREATED_UNUSED (exported but never imported)
- Impact: Dead code, likely incomplete feature
```

---

## Language Precision Rules

Use precise language that matches verification evidence:

| Claim | Required Evidence | Tool |
|-------|-------------------|------|
| "File not created" | Glob returns empty | `Glob: pattern="**/UserCard.*"` |
| "File exists but unused" | Glob finds file AND Grep for imports returns 0 | Glob + Grep |
| "Component orphaned" | File exists + no imports + no exports used | Glob + Grep |
| "Import broken" | Import statement exists + target file missing | Read + Glob |
| "Missing wiring" | Component exists + not rendered/registered anywhere | Grep for component usage |
| "Circular dependency" | A imports B AND B imports A | Read both files |

**Never say:**
- ❌ "This file is not used" (without grepping for imports)
- ❌ "This component doesn't exist" (without globbing)
- ❌ "The route is missing" (without checking route registration)

**Always say:**
- ✅ "Grep for `UserCard` returned 0 matches → unused"
- ✅ "Glob for `**/auth-callback.*` returned empty → not created"
- ✅ "Found `import UserCard` but Glob for UserCard.tsx returned empty → broken import"

---

## Anti-Patterns

❌ **Assumption without verification:**
```
"The UserCard component appears unused"
→ No Grep was run to verify
```

❌ **Vague classification:**
```
"There might be issues with the auth flow"
→ No specific finding, no evidence, no file:line
```

❌ **Tool mention without execution:**
```
"You should check if UserCard is imported anywhere"
→ YOU should check, not tell user to check
```

❌ **Conflating states:**
```
"UserCard is missing"
→ Missing = not created? Or created but not wired? Different fixes.
```

---

## Skills Using This Protocol

Reference this protocol in your skill's verification section:

```markdown
**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.
```

This protocol applies to:
- `shipkit-verify` — Primary verification skill
- `shipkit-codebase-index` — Index entry verification
- `shipkit-project-context` — Stack detection verification
- `shipkit-architecture-memory` — Decision consistency verification
- `shipkit-data-contracts` — Type/schema alignment verification
- `shipkit-integration-docs` — Service and freshness verification
