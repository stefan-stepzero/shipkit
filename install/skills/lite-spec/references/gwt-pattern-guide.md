# Given/When/Then Pattern Guide

How to write effective behavior scenarios for feature specifications.

---

## Pattern Structure

```
**Given**: [Preconditions - state before action]
**When**: [User action - what they do]
**Then**: [Expected outcomes - what should happen]
```

**Purpose:**
- **Given** sets the stage (starting conditions)
- **When** describes the trigger (user action)
- **Then** specifies results (multiple outcomes expected)

---

## Good Examples

### Example 1: Feature Activation

```markdown
**Given**: User owns a recipe
**When**: User toggles "Share publicly" switch
**Then**:
- System generates unique share token
- Share link becomes available to copy
- Recipe is publicly accessible via link
- Success toast appears: "Recipe shared successfully"
```

**Why this works:**
- Clear precondition (user owns recipe)
- Specific action (toggle switch, not vague "shares")
- Multiple concrete outcomes
- Includes user feedback (toast message)

---

### Example 2: Reversal/Undo

```markdown
**Given**: User has previously shared a recipe
**When**: User toggles share off
**Then**:
- Share token is revoked immediately
- Public link returns "Recipe not available"
- Original recipe remains in user's account
- Share button changes to "Share recipe"
```

**Why this works:**
- Tests reversal of action
- Specifies both backend (token revoked) and frontend (button text)
- Confirms data integrity (recipe still exists)

---

### Example 3: Error Scenario

```markdown
**Given**: User attempts to share recipe
**When**: Network request fails
**Then**:
- Toggle switch reverts to previous state
- Error toast appears: "Failed to share. Try again."
- Retry button appears
- Error is logged to console
```

**Why this works:**
- Tests failure path
- Specifies rollback behavior
- Includes user recovery option (retry)
- Mentions logging (for debugging)

---

### Example 4: Permission Check

```markdown
**Given**: User views someone else's recipe
**When**: User attempts to click "Share publicly" toggle
**Then**:
- Toggle is disabled (grayed out)
- Tooltip appears: "Only recipe owner can share"
- No API request is made
```

**Why this works:**
- Tests authorization
- Prevents wasted API calls
- Clear user feedback via tooltip

---

### Example 5: Boundary Condition

```markdown
**Given**: User has already created 100 active share links (quota limit)
**When**: User tries to share another recipe
**Then**:
- Modal appears: "Share limit reached (100 active shares)"
- "Upgrade to Pro" button shown
- Share action is blocked
- User can revoke existing shares to free quota
```

**Why this works:**
- Tests quota enforcement
- Provides upgrade path
- Offers alternative solution (revoke existing)

---

## Tips for Writing Scenarios

### 1. Be Specific

**Bad:**
```markdown
**When**: Share the recipe
```

**Good:**
```markdown
**When**: User toggles "Share publicly" switch
```

**Why:** "Share the recipe" is ambiguous. Toggle switch is a concrete UI action.

---

### 2. State Expected UI Changes

**Bad:**
```markdown
**Then**: UI updates
```

**Good:**
```markdown
**Then**:
- Share button changes to "Shared ✓"
- Copy link button becomes active
- Share URL appears below toggle
```

**Why:** Specific UI changes are testable. "UI updates" is too vague.

---

### 3. Include User Feedback

**Bad:**
```markdown
**Then**: User knows it worked
```

**Good:**
```markdown
**Then**:
- Success toast appears: "Recipe shared successfully"
- Share link is highlighted for easy copying
```

**Why:** Explicit feedback messages are implementable. "User knows" is subjective.

---

### 4. Cover State Changes

**Bad:**
```markdown
**Then**: Recipe is shared
```

**Good:**
```markdown
**Then**:
- `share_token` field is populated in database
- `is_public` flag set to `true`
- Recipe is accessible at `/recipes/[share_token]`
```

**Why:** Backend state changes are important for implementation. Vague "is shared" doesn't help.

---

### 5. Test Both Paths

**Every feature needs:**
- ✅ Happy path (action succeeds)
- ✅ Error path (action fails)
- ✅ Reversal path (undo action)
- ✅ Permission path (unauthorized attempt)

**Example:**
```markdown
**Scenario 1: Happy path** - Toggle share, token generated, link works
**Scenario 2: Error path** - Network fails, toggle reverts, error shown
**Scenario 3: Reversal** - Toggle off, token revoked, link dead
**Scenario 4: Permission** - Non-owner can't toggle, disabled with tooltip
```

---

## Common Patterns

### Pattern 1: Create/Read/Update/Delete (CRUD)

**Create:**
```markdown
**Given**: User is on dashboard
**When**: User clicks "New Recipe"
**Then**: Empty recipe form appears with autofocus on title field
```

**Read:**
```markdown
**Given**: Recipe exists with ID 123
**When**: User navigates to `/recipes/123`
**Then**: Recipe details load and display
```

**Update:**
```markdown
**Given**: User owns recipe
**When**: User edits title and clicks "Save"
**Then**: Title updates in database, success toast appears
```

**Delete:**
```markdown
**Given**: User owns recipe
**When**: User clicks "Delete" and confirms
**Then**: Recipe is soft-deleted, user redirected to dashboard
```

---

### Pattern 2: Multi-Step Flows

**Use numbered scenarios for sequential steps:**

```markdown
**Scenario 1: Start flow**
**Given**: User is logged in
**When**: User clicks "Create Recipe"
**Then**: Step 1 form appears (title, description)

**Scenario 2: Continue flow**
**Given**: User completed step 1
**When**: User clicks "Next"
**Then**: Step 2 form appears (ingredients)

**Scenario 3: Complete flow**
**Given**: User completed all steps
**When**: User clicks "Publish"
**Then**: Recipe is saved, user redirected to recipe page
```

---

### Pattern 3: Conditional Behavior

**Use Given to set conditions:**

```markdown
**Scenario 1: New user**
**Given**: User has no recipes
**When**: User views dashboard
**Then**: Onboarding message appears with "Create first recipe" CTA

**Scenario 2: Existing user**
**Given**: User has 5 recipes
**When**: User views dashboard
**Then**: Recipe list displays with most recent first
```

---

## Anti-Patterns (Avoid These)

### Anti-Pattern 1: Vague Actions

❌ **Bad:**
```markdown
**When**: User interacts with the system
```

✅ **Good:**
```markdown
**When**: User clicks "Share" button
```

---

### Anti-Pattern 2: Implementation Details

❌ **Bad:**
```markdown
**Then**: `POST /api/recipes/share` is called with token in body
```

✅ **Good:**
```markdown
**Then**: Share token is generated and recipe becomes publicly accessible
```

**Why:** Specs describe behavior, not implementation. The plan/tasks will determine HTTP methods.

---

### Anti-Pattern 3: Multiple Actions in When

❌ **Bad:**
```markdown
**When**: User clicks share, copies link, and pastes in new tab
```

✅ **Good:**
Split into 3 scenarios:
```markdown
**Scenario 1**: User clicks share → Token generated
**Scenario 2**: User copies link → Copied to clipboard
**Scenario 3**: User pastes link in new tab → Recipe loads
```

---

### Anti-Pattern 4: Missing Failure Cases

❌ **Bad:**
Only spec happy path

✅ **Good:**
Spec happy + error + edge cases

---

## Checklist for Scenarios

Before saving spec, verify each scenario:
- [ ] Given states clear preconditions
- [ ] When describes specific user action (not vague)
- [ ] Then lists multiple concrete outcomes
- [ ] User feedback is explicit (toast messages, UI changes)
- [ ] Backend state changes documented
- [ ] Error cases covered
- [ ] Reversal/undo tested
- [ ] Permissions tested

---

**Remember:** Good scenarios are implementable. If a developer reads your Given/When/Then and doesn't know what to build, it's too vague.
