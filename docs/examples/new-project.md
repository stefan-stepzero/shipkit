# Example: Starting a New Project

A complete walkthrough of using Shipkit to build a new product from scratch.

---

## Scenario

You're building **RecipeShare** — a simple app where users can save and share recipes. You have 2 weeks for an MVP.

---

## Day 1: Project Setup

### Install Shipkit

```bash
mkdir recipeshare && cd recipeshare
git init
npx shipkit-dev init
```

### Define Your Vision

```
/shipkit-why-project
```

**Questions asked:**
- What problem are you solving?
- Who is this for?
- What does success look like?
- What constraints do you have?

**Creates:** `.shipkit/why.json`

```markdown
# RecipeShare - Why

## Problem
Home cooks lose track of recipes they find online. Bookmarks get messy,
screenshots are unsearchable.

## Solution
A simple app to save, organize, and share recipes.

## Target User
Home cooks who collect recipes from multiple sources.

## Success Criteria
- User can save a recipe in < 30 seconds
- Recipes are searchable by ingredient
- MVP in 2 weeks

## Constraints
- Solo developer
- 2-week timeline
- Start simple, iterate
```

### Discover Users

```
/shipkit-product-discovery
```

**Creates:** `.shipkit/personas/home-cook.md`

Quick persona capturing goals, pain points, and context.

---

## Day 2: First Feature Spec

### Create Spec for Recipe Saving

```
/shipkit-spec "Save a recipe from URL"
```

**Questions asked:**
- What's the core user flow?
- What data do we need to capture?
- What's the happy path?

**Creates:** `.shipkit/specs/active/save-recipe-from-url.json`

```markdown
# Save Recipe from URL

## Overview
User pastes a URL, app extracts recipe details automatically.

## User Flow
1. User clicks "Add Recipe"
2. Pastes URL
3. App fetches and parses recipe
4. User reviews and saves

## Acceptance Criteria
- Given a valid recipe URL
- When user submits it
- Then recipe title, ingredients, and instructions are extracted

## Technical Approach
- Use recipe-scrapers library for extraction
- Store in Supabase
- Simple form UI
```

---

## Day 3: Implementation Planning

### Create Implementation Plan

```
/shipkit-plan
```

**Reads:** The spec you just created

**Creates:** `.shipkit/plans/active/save-recipe-from-url.json`

```markdown
# Implementation Plan: Save Recipe from URL

## Tasks
1. Set up Supabase project and recipes table
2. Create recipe scraping utility
3. Build "Add Recipe" form component
4. Connect form to scraper
5. Save to database
6. Show success/error feedback

## Order
1 → 2 → 3 → 4 → 5 → 6 (sequential)

## Estimated Time
4-6 hours
```

---

## Day 3-4: Implementation

No skill needed — just ask Claude:

```
Let's implement the save-recipe-from-url feature.
Start with task 1 from the plan.
```

Claude reads the plan and spec, then implements.

### Log Architecture Decisions

When you make a significant choice:

```
/shipkit-architecture-memory
```

**Example decision logged:**

```markdown
## 2026-02-03: Recipe Storage Schema

**Decision:** Store ingredients as JSONB array, not separate table

**Rationale:**
- Simpler queries for MVP
- Can normalize later if needed
- Ingredients always fetched with recipe

**Trade-off:** Harder to search by ingredient across recipes
```

---

## Day 5: Verify Quality

```
/shipkit-verify
```

**Checks:**
- Does implementation match spec?
- Are acceptance criteria met?
- Any obvious issues?

**Output:**

```markdown
## Verification: Save Recipe from URL

### Spec Compliance
✅ URL input works
✅ Recipe extraction works
✅ Data saves to Supabase

### Issues Found
⚠️ No error handling for invalid URLs
⚠️ No loading state during fetch

### Recommended Fixes
1. Add try/catch around scraper
2. Add loading spinner to form
```

---

## Day 6+: Iterate

Repeat the cycle:

1. `/shipkit-spec` for next feature
2. `/shipkit-plan` to plan it
3. Implement (natural capability)
4. `/shipkit-verify` to check quality

---

## End of Day: Session Memory

Before ending a session:

```
/shipkit-work-memory
```

**Creates/updates:** `.shipkit/progress.json`

```markdown
## Session: 2026-02-03

### Completed
- Implemented save-recipe-from-url feature
- Fixed URL validation
- Added loading states

### Next Session
- Implement recipe list view
- Add search by ingredient

### Blockers
None
```

---

## Final Project Structure

After 2 weeks:

```
recipeshare/
├── CLAUDE.md
├── .shipkit/
│   ├── why.json
│   ├── stack.json
│   ├── architecture.json
│   ├── progress.json
│   ├── personas/
│   │   └── home-cook.md
│   ├── specs/active/
│   │   ├── save-recipe-from-url.json
│   │   ├── recipe-list.json
│   │   └── search-recipes.json
│   └── plans/
│       ├── save-recipe-from-url-plan.json
│       └── ...
├── src/
│   └── ... (your code)
└── ...
```

---

## Key Takeaways

1. **Vision first** — `/shipkit-why-project` sets the foundation
2. **Spec before code** — Even small features benefit from a quick spec
3. **Let Claude implement** — Skills capture decisions, Claude writes code
4. **Log decisions** — Architecture decisions in context survive sessions
5. **End sessions cleanly** — Work memory ensures continuity

---

## Time Investment

| Activity | Skill | Time |
|----------|-------|------|
| Define vision | `/shipkit-why-project` | 15-20 min |
| Create persona | `/shipkit-product-discovery` | 10-15 min |
| Write spec | `/shipkit-spec` | 10-15 min |
| Create plan | `/shipkit-plan` | 5-10 min |
| Verify quality | `/shipkit-verify` | 5-10 min |
| Log decision | `/shipkit-architecture-memory` | 5 min |
| Session wrap | `/shipkit-work-memory` | 5 min |

**Total overhead:** ~1 hour per feature cycle

**Value:** Context that survives sessions, decisions that don't get lost
