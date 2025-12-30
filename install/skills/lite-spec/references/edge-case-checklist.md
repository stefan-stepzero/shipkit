# Edge Case Checklist

Comprehensive edge case categories to apply to every feature specification.

---

## Complete Checklist

**Apply ALL 6 categories to EVERY feature. No exceptions.**

### 1. Loading States

Standard async operation handling:
- [ ] Initial load - Show skeleton/spinner during data fetch
- [ ] Action in progress - Disable controls, show loading indicator
- [ ] Timeout handling - >5 seconds, show error/retry option
- [ ] Prevent duplicate actions - Debounce, disable on submit

**Why these matter:**
- Users need feedback that system is working
- Prevent confusion during slow operations
- Avoid duplicate requests/data corruption
- Build trust through responsive UI

---

### 2. Error States

Comprehensive error handling:
- [ ] Network failures - Offline, timeout, connection dropped → Show retry
- [ ] Server errors - 500, 502, 503 → User-friendly message, log to monitoring
- [ ] Validation errors - Client-side and server-side → Inline feedback
- [ ] Permission errors - 401 (auth required), 403 (forbidden) → Redirect or message
- [ ] Not found errors - 404 → Show "not found" page

**Why these matter:**
- Things will fail - network, servers, validation
- Users shouldn't see stack traces
- Clear error messages prevent support tickets
- Proper logging aids debugging

---

### 3. Empty/Missing States

Zero-data scenarios:
- [ ] No data available - New user, fresh install → Show helpful CTA
- [ ] Search with no results - Show "no results" with suggestions
- [ ] Deleted/archived items - Handle gracefully, show tombstone
- [ ] Filter applied with no matches - "No items match this filter"
- [ ] First-time user experience - Onboarding, tutorial, sample data

**Why these matter:**
- Blank screens confuse users
- First-time users need guidance
- Empty states are conversion opportunities
- Help users succeed faster

---

### 4. Permission States

Access control scenarios:
- [ ] Unauthenticated users - Redirect to login or show public-safe view
- [ ] Authenticated but unauthorized - "You don't have access to this"
- [ ] Role-based restrictions - Hide unavailable features for role
- [ ] Ownership checks - Only owner can edit/delete
- [ ] Shared resource permissions - Viewer vs editor vs admin

**Why these matter:**
- Security requires proper access control
- Users shouldn't see features they can't use
- Ownership prevents data tampering
- Shared resources need permission levels

---

### 5. Boundary Conditions

Limits and extremes:
- [ ] Minimum values - 0, empty string, null, undefined
- [ ] Maximum values - String length (255, 1000, 10000), array size, number ranges
- [ ] Rate limits - Too many requests (429) → "Slow down, try again in X seconds"
- [ ] Quota limits - Storage, API calls, feature usage → Upgrade prompt
- [ ] Character limits - Input fields (show "X/255 characters")
- [ ] Pagination limits - Max page size, deep pagination performance

**Why these matter:**
- Prevent system abuse
- Protect database/API from overload
- Guide users to reasonable usage
- Prevent unexpected behavior at limits

---

### 6. Data Consistency

State management edge cases:
- [ ] Stale data - Refresh on focus, visibility change, pull-to-refresh
- [ ] Partial updates - Some fields succeed, others fail → Rollback or retry
- [ ] Cache invalidation - Clear related caches on mutation
- [ ] Optimistic updates - Revert on failure with error message
- [ ] Referential integrity - Cascading deletes, orphaned references
- [ ] Concurrent modifications - Last-write-wins vs conflict detection vs merge

**Why these matter:**
- Users expect current data
- Partial failures corrupt state
- Caches need invalidation strategy
- Optimistic UI needs rollback
- Concurrent edits cause conflicts

---

## How to Apply This Checklist

**During spec creation:**
1. Copy all 6 categories into spec template
2. For each category, check which items apply to your feature
3. Add specific implementation notes for checked items
4. Don't skip categories - every feature touches multiple categories

**Example application (recipe sharing feature):**

```markdown
## Edge Cases

### Loading States
- [x] Show spinner during share token generation
- [x] Disable toggle switch during API call
- [x] Handle timeout >5s with retry option
- [x] Prevent double-click on share button

### Error States
- [x] Network failure → Revert toggle, show error toast
- [x] Server error → Show "Failed to share. Try again."
- [x] Invalid recipe ID → Show "Recipe not found"

### Empty States
- [ ] N/A for this feature (always operates on existing recipe)

### Permission States
- [x] Only recipe owner can share
- [x] Unauthenticated users see "Sign in to share"
- [x] Shared recipe viewers cannot re-share

### Boundary Conditions
- [x] Rate limit: Max 10 shares per minute per user
- [x] Max 100 active share links per user (quota)

### Data Consistency
- [x] Refresh share status on page focus (in case revoked elsewhere)
- [x] Optimistic UI: Show "Shared" immediately, revert on failure
- [x] If recipe deleted, share link shows "Recipe not available"
```

---

## Common Mistakes

**Mistake 1: Skipping categories**
- ❌ "This feature doesn't have empty states"
- ✅ Think harder - first-time users, no data loaded yet, deleted items

**Mistake 2: Vague items**
- ❌ "Handle errors gracefully"
- ✅ "Network failure → Show retry button with message 'Connection lost. Retry?'"

**Mistake 3: Missing user feedback**
- ❌ "Validate input"
- ✅ "Invalid email → Show inline error 'Please enter valid email' below field"

**Mistake 4: Forgetting rollback**
- ❌ "Optimistically update UI"
- ✅ "Optimistically update UI, revert on failure with error toast"

---

**Remember:** These edge cases prevent 90% of production bugs. Don't skip them.
