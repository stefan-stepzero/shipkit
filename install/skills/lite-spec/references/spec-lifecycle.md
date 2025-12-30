# Spec Lifecycle

How specifications move through the development process from active to implemented.

---

## Spec States

### Active Specs (`.shipkit-lite/specs/active/`)

**Purpose:** Work in progress, not yet implemented

**Characteristics:**
- Feature not yet built or currently being built
- Can be modified during planning/implementation
- Source of truth during development
- Living document (refinements allowed)

**When to modify:**
- During planning (add technical notes)
- During implementation (clarify ambiguities)
- When edge cases discovered during testing
- When acceptance criteria need adjustment

**Location:** `.shipkit-lite/specs/active/[feature-name].md`

---

### Implemented Specs (`.shipkit-lite/specs/implemented/`)

**Purpose:** Historical record of completed features

**Characteristics:**
- Feature is live in production
- Read-only historical record
- Includes completion metadata
- Used for future reference and auditing

**Completion metadata added:**
```markdown
---
**Status**: Implemented
**Date**: 2025-01-20
**Implemented by**: Claude + User
**Final notes**: Shipped with all Must Have criteria. Deferred Should Have items to v2.
**Deviations**: Changed API endpoint from POST to PUT per performance testing.
---
```

**Location:** `.shipkit-lite/specs/implemented/[feature-name].md`

---

## Moving Between States

### From Active → Implemented

**Triggered by:**
1. Manual move (user decides feature is complete)
2. Via `/lite-quality-confidence` when feature passes quality checks

**Steps:**
1. Add completion metadata to spec
2. Move file: `specs/active/[name].md` → `specs/implemented/[name].md`
3. Update any cross-references in related specs
4. Update progress tracking (if using `/lite-work-memory`)

**Completion metadata template:**
```markdown
---
**Status**: Implemented
**Date**: [YYYY-MM-DD]
**Implemented by**: [Who built it]
**Final notes**: [Summary of what shipped]
**Deviations**: [Any changes from original spec]
**Deferred items**: [Should Have items moved to backlog]
---
```

---

### From Implemented → Active (Rare)

**When this happens:**
- Major refactor requires re-implementation
- Feature removed from production, needs rebuild
- Spec was prematurely moved (feature wasn't actually done)

**Steps:**
1. Remove completion metadata
2. Move file back: `specs/implemented/[name].md` → `specs/active/[name].md`
3. Update status to "Active - Rework"
4. Document why feature needs re-implementation

**Not recommended:** This indicates planning or quality issues. Better to create a new spec for v2.

---

## Spec Modification Guidelines

### Active Specs (Can Modify)

**Allowed modifications:**
- ✅ Add new edge cases discovered during implementation
- ✅ Clarify ambiguous Given/When/Then scenarios
- ✅ Add technical notes from implementation learnings
- ✅ Adjust acceptance criteria (with justification)
- ✅ Update status (Active → Active - In Progress → Active - Testing)

**Modification process:**
1. Read current spec
2. Use Write tool to overwrite with updated version
3. Add changelog note at bottom documenting changes
4. No version history needed (active specs are working documents)

**Example changelog:**
```markdown
## Changelog

**2025-01-15:** Added rate limiting edge case (10 requests/min)
**2025-01-16:** Clarified share token expiration (30 days)
**2025-01-17:** Updated technical notes with Supabase RLS policy name
```

---

### Implemented Specs (Read-Only)

**Do not modify implemented specs.**

**If changes needed:**
- Create new spec for v2 of feature
- Reference original implemented spec
- Document what's changing and why

**Example v2 spec:**
```markdown
# Recipe Sharing v2

**Based on:** specs/implemented/recipe-sharing.md
**Created:** 2025-02-01

## Changes from v1
- Add share expiration dates (user-configurable)
- Add share analytics (view count, last accessed)
- Add password-protected shares

## User Story
As a recipe author, I want to set expiration dates on shares, so I can control how long recipes are publicly accessible.

[... rest of spec ...]
```

---

## Archiving Strategy

### Why Archive (Move to Implemented)

**Benefits:**
- Clear separation: active vs historical
- Easier to find in-progress work (only look in active/)
- Historical record of what shipped when
- Completion metadata captured

**When to archive:**
- Feature fully implemented and tested
- All Must Have criteria met
- Feature deployed to production
- Quality checks passed

---

### Why NOT to Archive

**Keep in active/ if:**
- Feature partially implemented
- Still making changes during iteration
- Waiting for production deployment
- Quality issues not yet resolved

---

## Folder Structure

```
.shipkit-lite/specs/
  active/
    recipe-sharing.md          # In progress
    user-authentication.md     # Planned
    advanced-search.md         # Being built
  implemented/
    recipe-crud.md             # Shipped v1
    recipe-images.md           # Shipped v1.1
    social-sharing.md          # Shipped v1.2
```

---

## Common Workflows

### Workflow 1: Feature from Scratch

```
1. User describes feature
2. /lite-spec creates specs/active/feature.md
3. /lite-plan reads active spec
4. /lite-implement builds feature
5. /lite-quality-confidence validates
   → If passed: Moves specs/active/feature.md → specs/implemented/feature.md
   → If failed: Spec stays in active/, fix issues
```

---

### Workflow 2: Feature with Iteration

```
1. /lite-spec creates specs/active/search.md
2. /lite-implement starts building
3. During build: Discover new edge case (slow queries)
4. Update specs/active/search.md (add timeout handling)
5. Continue implementation with updated spec
6. /lite-quality-confidence passes
7. Move specs/active/search.md → specs/implemented/search.md
```

---

### Workflow 3: Feature v2

```
1. specs/implemented/recipe-sharing.md exists (v1 shipped)
2. User wants to add new features
3. /lite-spec creates specs/active/recipe-sharing-v2.md
4. New spec references old spec
5. Implement v2
6. When done: Move specs/active/recipe-sharing-v2.md → specs/implemented/
7. Both v1 and v2 specs exist in implemented/ folder
```

---

## File Naming Conventions

**Active specs:**
- Use kebab-case: `recipe-sharing.md`, `user-authentication.md`
- Descriptive feature name
- No version numbers (unless explicit v2)

**Implemented specs:**
- Keep original filename when moving
- Add version suffix if needed: `recipe-sharing-v2.md`
- Preserve case from active/

---

## Cross-References

**Active specs can reference:**
- ✅ Implemented specs (learn from past features)
- ✅ Other active specs (understand dependencies)
- ✅ Architecture decisions (.shipkit-lite/architecture.md)

**Implemented specs reference:**
- ✅ Other implemented specs at time of completion
- ⚠️ Don't update references in implemented specs (historical snapshot)

---

## Backup and History

**Built-in through archiving:**
- Moving to implemented/ preserves original spec
- Completion metadata captures final state
- No Git needed (though Git recommended for team projects)

**If using Git:**
- Commit active specs before implementation
- Commit implemented specs after shipping
- Git history provides detailed version control

**If not using Git:**
- Implemented folder serves as backup
- Can reference old specs for future features

---

**Remember:** Active = working document (modify as needed). Implemented = historical record (read-only).
