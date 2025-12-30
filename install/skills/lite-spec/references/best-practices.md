# Frontend & Backend Best Practices

Comprehensive best practices to apply when specifying features. Use these checklists to ensure specs guide developers toward production-quality implementations.

---

## Frontend Best Practices

### 1. State Management

**Every feature needs these states:**

- [ ] **Loading states** - Show feedback during async operations
  - Skeleton screens for initial page load
  - Spinners for button actions
  - Disable controls during operations (prevent double-submit)
  - Show progress for long operations (upload progress bar)

- [ ] **Error states** - Handle all failure scenarios
  - Network failures (offline, timeout, connection dropped)
  - Server errors (500, 502, 503)
  - Validation errors (client-side and server-side)
  - Permission errors (401 unauthorized, 403 forbidden)
  - Not found errors (404)

- [ ] **Empty states** - Handle zero-data scenarios
  - No data available (new user, fresh install)
  - No search results (show suggestions)
  - Filtered data returns nothing (clear filters CTA)
  - First-time user experience (onboarding, tutorial)

- [ ] **Success states** - Confirm actions completed
  - Toast notifications for actions ("Recipe saved")
  - Visual feedback (checkmarks, color changes)
  - State updates reflect success (list refreshes, count updates)
  - Auto-dismiss or require user acknowledgment

- [ ] **Optimistic updates** - Show changes immediately
  - Update UI before server confirms (faster perceived performance)
  - Revert on failure with error message
  - Show loading indicator if taking longer than expected
  - Sync state after successful confirmation

**Why this matters:** Users need feedback at every step. Blank screens, missing loading indicators, and unclear errors destroy trust.

---

### 2. User Feedback & Communication

**Every user action needs clear feedback:**

- [ ] **Actionable error messages** - Tell users what to do
  - ❌ Bad: "Error occurred"
  - ✅ Good: "Connection lost. Check your internet and try again."
  - Include retry/recovery actions (Retry button, Help link)
  - Preserve user input on error (don't clear form fields)

- [ ] **Confirmation for destructive actions** - Prevent accidents
  - Delete operations require confirmation modal
  - Show what will be deleted ("Delete 'Chocolate Cake'?")
  - Provide undo option if possible (10-second undo toast)
  - Use clear language ("Delete permanently" vs "Delete")

- [ ] **Progress indicators** - Show system is working
  - Use specific messages ("Uploading... 45%")
  - Estimated time remaining for long operations
  - Indeterminate spinners for unknown duration
  - Don't show progress bars that get stuck at 99%

- [ ] **Success feedback** - Confirm completion
  - Toast notifications ("Recipe shared successfully")
  - Visual state changes (button changes to "Shared ✓")
  - Navigate to result (redirect to new recipe page)
  - Update related UI (recipe count increments)

**Why this matters:** Silent failures and unclear feedback lead to user confusion and repeated actions.

---

### 3. Accessibility (a11y)

**Make features usable for everyone:**

- [ ] **Keyboard navigation** - Works without mouse
  - All interactive elements are keyboard accessible (Tab, Enter, Space)
  - Focus order follows logical reading order
  - Focus indicators are visible (outline, highlight)
  - Skip links for long navigation menus
  - Escape key closes modals/dialogs

- [ ] **Screen reader support** - Works with assistive tech
  - Semantic HTML (use `<button>`, `<nav>`, `<main>` not just `<div>`)
  - ARIA labels for icon-only buttons (`aria-label="Delete recipe"`)
  - ARIA live regions for dynamic content (`aria-live="polite"`)
  - Alt text for images (descriptive, not decorative)
  - Form labels associated with inputs (`<label for="email">`)

- [ ] **Color contrast** - Readable for low vision
  - Text meets WCAG AA contrast ratio (4.5:1 for normal text)
  - Don't rely on color alone (use icons + text)
  - Focus indicators have sufficient contrast
  - Error states use multiple cues (color + icon + text)

- [ ] **Forms accessibility** - Usable for everyone
  - Every input has associated label (visible or aria-label)
  - Error messages linked to fields (aria-describedby)
  - Required fields marked (aria-required, visual indicator)
  - Autocomplete attributes for common fields (name, email, address)

**Why this matters:** 15-20% of users have accessibility needs. It's also the law in many jurisdictions.

---

### 4. Performance

**Keep UI responsive and fast:**

- [ ] **Debounce user input** - Reduce unnecessary requests
  - Search inputs debounced 300-500ms
  - Autocomplete debounced 200-300ms
  - Resize/scroll handlers debounced 100-200ms
  - Form validation debounced on input, immediate on blur

- [ ] **Virtualize long lists** - Don't render everything
  - Use virtual scrolling for 100+ items (react-window, react-virtuoso)
  - Pagination for data tables (show 25-50 per page)
  - Infinite scroll with intersection observer
  - Show "X more items" collapse for very long lists

- [ ] **Lazy load resources** - Load only what's needed
  - Code splitting for routes (dynamic imports)
  - Lazy load images (loading="lazy", intersection observer)
  - Defer non-critical CSS/JS (async, defer attributes)
  - Preload critical resources (fonts, hero images)

- [ ] **Cache data** - Avoid redundant fetches
  - Use SWR/React Query for client-side caching
  - Cache static resources with service workers
  - Use ETags/Last-Modified for conditional requests
  - Implement stale-while-revalidate pattern

**Why this matters:** Slow UIs frustrate users. Performance is a feature.

---

### 5. Security (Frontend)

**Protect users from client-side attacks:**

- [ ] **XSS prevention** - Sanitize all user input
  - Use framework auto-escaping (React, Vue escape by default)
  - Sanitize HTML if rendering user content (DOMPurify)
  - Don't use dangerouslySetInnerHTML without sanitization
  - Validate and sanitize URLs before rendering links

- [ ] **No sensitive data client-side** - Keep secrets server-side
  - Never store passwords in client state
  - Don't log sensitive data to console
  - API keys stay server-side only
  - Use httpOnly cookies for auth tokens

- [ ] **Validate on client AND server** - Never trust client
  - Client validation for UX (instant feedback)
  - Server validation for security (client can be bypassed)
  - Use same validation schema on both (Zod, Yup)
  - Don't expose validation logic that reveals business rules

- [ ] **HTTPS only** - Encrypt all traffic
  - No mixed content (all resources over HTTPS)
  - Redirect HTTP to HTTPS automatically
  - Use secure cookies (Secure, SameSite flags)
  - HSTS header to enforce HTTPS

**Why this matters:** Client-side security prevents common web attacks (XSS, CSRF, data exposure).

---

### 6. Forms

**Make forms easy and error-free:**

- [ ] **Clear validation** - Help users succeed
  - Show requirements upfront (password: 8+ chars, 1 uppercase)
  - Inline validation on blur (don't wait for submit)
  - Highlight invalid fields with red border + icon
  - Error messages next to fields, not just at top
  - Show valid state (green checkmark for correct fields)

- [ ] **Smart defaults** - Reduce user effort
  - Pre-fill known values (email from session)
  - Use sensible defaults (country from IP geolocation)
  - Remember user preferences (keep me logged in)
  - Autofocus first field on form load

- [ ] **Submit states** - Prevent errors
  - Disable submit button during submission
  - Show loading state ("Saving...")
  - Prevent double-submit (disable button, debounce handler)
  - Re-enable on error with clear message

- [ ] **Error recovery** - Don't lose user work
  - Preserve form data on validation errors
  - Save to localStorage for long forms (draft recovery)
  - Show which fields have errors (count, list)
  - Allow fixing errors without re-entering valid data

**Why this matters:** Forms are conversion points. Bad form UX kills conversion rates.

---

### 7. Navigation & Routing

**Make navigation intuitive and reliable:**

- [ ] **Deep linking** - URLs reflect application state
  - Every view has unique URL
  - Query params for filters, sort, pagination
  - Modal states in URL (for shareable links)
  - Preserve state on page refresh

- [ ] **Browser history** - Back/forward work correctly
  - Don't break back button (avoid location.replace)
  - Modal close returns to previous view
  - Form submission adds to history
  - Use history.pushState for client-side routing

- [ ] **Loading states during navigation** - Show progress
  - Route transitions show loading indicator
  - Skeleton screens for new page content
  - Preserve scroll position on back navigation
  - Cancel pending requests on navigation

- [ ] **Error boundaries** - Catch React errors gracefully
  - Wrap routes in error boundaries
  - Show user-friendly error page (not blank screen)
  - Log error to monitoring service (Sentry)
  - Provide recovery action (Go home, Refresh page)

**Why this matters:** Broken navigation breaks mental model and prevents sharing/bookmarking.

---

## Backend Best Practices

### 1. Input Validation

**Validate every input, every time:**

- [ ] **Schema validation** - Enforce structure
  - Use validation libraries (Zod, Yup, class-validator, Joi)
  - Validate on API route entry point (before business logic)
  - Type-check runtime values (don't trust TypeScript alone)
  - Return 400 Bad Request with field-specific errors

- [ ] **Sanitization** - Clean user input
  - Strip HTML tags (unless explicitly allowing rich text)
  - Escape SQL special characters (or use parameterized queries)
  - Trim whitespace from strings
  - Normalize email addresses (lowercase, trim)

- [ ] **Boundary checks** - Enforce limits
  - String length limits (title max 100 chars, bio max 500)
  - Number ranges (age 0-120, quantity 1-999)
  - Array size limits (max 10 tags, max 5 images)
  - Date ranges (birth date not in future)

- [ ] **Type validation** - Enforce data types
  - Email format (regex or library)
  - URL format (valid protocol, domain)
  - UUID format (valid v4 UUID)
  - Enum values (status must be "draft" | "published" | "archived")

**Why this matters:** Invalid input causes bugs, crashes, and security vulnerabilities.

---

### 2. Authentication & Authorization

**Secure every endpoint:**

- [ ] **Authentication check** - Verify identity
  - Check auth token on every protected endpoint
  - Validate JWT signature and expiration
  - Reject missing, expired, or invalid tokens (401)
  - Use secure session storage (httpOnly cookies, server-side sessions)

- [ ] **Authorization check** - Verify permissions
  - Check user has permission for action (403 if not)
  - Role-based access control (RBAC: admin, user, viewer)
  - Resource ownership (only owner can edit/delete)
  - Fail closed (deny by default, allow explicitly)

- [ ] **Row-level security** - Database-level protection
  - Use RLS policies (Supabase, PostgreSQL)
  - Filter queries by user ID automatically
  - Prevent data leaks via joins/aggregations
  - Test RLS policies with different user roles

- [ ] **Token management** - Handle auth securely
  - Short-lived access tokens (15 min - 1 hour)
  - Refresh tokens for session extension
  - Revoke tokens on logout
  - Rotate refresh tokens on use

**Why this matters:** Auth failures expose user data and allow unauthorized actions.

---

### 3. Error Handling

**Handle errors gracefully:**

- [ ] **Never expose internals** - Protect system details
  - Don't return stack traces to client (log server-side only)
  - Don't expose database errors (table names, column names)
  - Don't reveal file paths or server info
  - Return generic "Internal server error" for 500s

- [ ] **User-friendly messages** - Help users understand
  - 400: "Invalid email format" (not "Validation failed")
  - 401: "Please log in to continue" (not "Unauthorized")
  - 403: "You don't have permission" (not "Forbidden")
  - 404: "Recipe not found" (not "Not found")
  - 500: "Something went wrong. Try again." (not stack trace)

- [ ] **Proper HTTP status codes** - Use semantics correctly
  - 200: Success (with response body)
  - 201: Created (return new resource)
  - 400: Bad request (validation errors)
  - 401: Unauthenticated (missing/invalid auth)
  - 403: Forbidden (authenticated but not authorized)
  - 404: Not found (resource doesn't exist)
  - 429: Too many requests (rate limit exceeded)
  - 500: Internal server error (unhandled exceptions)

- [ ] **Comprehensive logging** - Debug production issues
  - Log all errors with context (user ID, request ID, timestamp, stack trace)
  - Use structured logging (JSON format for parsing)
  - Log to monitoring service (Sentry, LogRocket, Datadog)
  - Include request details (method, path, IP, user agent)
  - Never log sensitive data (passwords, tokens, credit cards)

**Why this matters:** Good error handling aids debugging without exposing security vulnerabilities.

---

### 4. Data Integrity

**Maintain database consistency:**

- [ ] **Transactions** - All-or-nothing operations
  - Use transactions for multi-step updates (transfer funds = debit + credit)
  - Rollback on any step failure
  - Isolate concurrent transactions (read committed, serializable)
  - Keep transactions short (hold locks briefly)

- [ ] **Database constraints** - Enforce rules at DB level
  - Foreign keys (prevent orphaned records)
  - Unique constraints (prevent duplicate emails)
  - Not null constraints (require critical fields)
  - Check constraints (age > 0, status in enum)

- [ ] **Cascade operations** - Handle relationships
  - Cascade deletes where appropriate (delete user → delete user's posts)
  - Prevent deletes where inappropriate (can't delete category with recipes)
  - Soft deletes for audit trail (mark as deleted, don't remove)
  - Orphan cleanup (scheduled job to remove abandoned data)

- [ ] **Optimistic locking** - Handle concurrent edits
  - Version field (increment on update)
  - Detect stale updates (version mismatch = conflict)
  - Return 409 Conflict on stale update
  - Let client decide how to merge changes

**Why this matters:** Data inconsistency causes bugs that are hard to trace and fix.

---

### 5. Security (Backend)

**Protect against common attacks:**

- [ ] **Rate limiting** - Prevent abuse
  - Per-user limits (10 requests/min per user)
  - Per-IP limits (100 requests/min per IP)
  - Endpoint-specific limits (login: 5 attempts/hour)
  - Return 429 with Retry-After header
  - Use sliding window or token bucket algorithm

- [ ] **SQL injection prevention** - Never concatenate SQL
  - Use parameterized queries (prepared statements)
  - Use ORM/query builder (Prisma, Drizzle, Knex)
  - Validate input even with parameterized queries
  - Escape user input if dynamic SQL required (rare)

- [ ] **CSRF protection** - Prevent cross-site attacks
  - CSRF tokens for state-changing operations (POST, PUT, DELETE)
  - SameSite cookies (Strict or Lax)
  - Verify origin/referer headers
  - Double-submit cookie pattern

- [ ] **Idempotency** - Safe to retry
  - Idempotency keys for critical operations (payments)
  - GET requests always idempotent
  - PUT requests idempotent (update to same value)
  - POST should use idempotency keys (prevent duplicates)
  - Store idempotency key results (return cached response)

**Why this matters:** Security vulnerabilities expose user data and enable attackers.

---

### 6. Performance (Backend)

**Keep APIs fast and scalable:**

- [ ] **Database indexes** - Speed up queries
  - Index foreign keys (for joins)
  - Index frequently filtered columns (user_id, status, created_at)
  - Compound indexes for multi-column queries
  - Monitor slow queries (EXPLAIN ANALYZE)

- [ ] **Pagination** - Never return unbounded lists
  - Limit results (25-100 per page)
  - Cursor-based pagination for real-time data
  - Offset-based pagination for static data
  - Return total count separately (expensive, cache it)

- [ ] **Caching** - Reduce database load
  - Redis for session data, rate limiting
  - Cache expensive queries (dashboard stats)
  - Set appropriate TTL (5 min for volatile, 1 hour for stable)
  - Invalidate on mutation (clear cache on update/delete)

- [ ] **N+1 query prevention** - Batch database calls
  - Eager load relationships (JOIN or separate batch query)
  - Use data loaders (batch + cache within request)
  - Monitor query counts (should be O(1), not O(n))
  - Use tools like DataLoader, Prisma findMany

**Why this matters:** Slow APIs create slow UIs. Performance affects user experience.

---

### 7. API Design

**Build consistent, intuitive APIs:**

- [ ] **RESTful conventions** - Use standard patterns
  - GET for reads (idempotent, cacheable)
  - POST for creates (not idempotent)
  - PUT for full updates (idempotent)
  - PATCH for partial updates
  - DELETE for removes (idempotent)

- [ ] **Consistent response format** - Predictable structure
  - Success: `{ data: {...} }`
  - Error: `{ error: "message", code: "ERROR_CODE" }`
  - List: `{ data: [...], total: 123, page: 1 }`
  - Created: Return new resource with 201 status

- [ ] **Versioning** - Manage breaking changes
  - Version in URL path (/api/v1/recipes)
  - Or in Accept header (Accept: application/vnd.api+json;version=1)
  - Support old versions for transition period
  - Document deprecation timeline

- [ ] **Documentation** - Make APIs discoverable
  - OpenAPI/Swagger spec for all endpoints
  - Include request/response examples
  - Document error codes and meanings
  - Provide Postman collection or cURL examples

**Why this matters:** Consistent APIs are easier to use, test, and maintain.

---

## How to Apply These Practices

### During Spec Creation

**Step 1: Identify feature type**
- Is it frontend-heavy (UI, forms, navigation)?
- Is it backend-heavy (API, data processing, auth)?
- Is it full-stack (both frontend and backend)?

**Step 2: Apply relevant checklists**
- Frontend feature → Use Frontend sections 1-7
- Backend feature → Use Backend sections 1-7
- Full-stack → Apply both

**Step 3: Add to spec edge cases**
For each applicable category, add specific checks:

```markdown
## Edge Cases

### Frontend: State Management
- [x] Loading state during share token generation
- [x] Error state if network fails (show retry button)
- [x] Success toast: "Recipe shared successfully"
- [x] Optimistic update (show "Shared" immediately, revert on failure)

### Frontend: Accessibility
- [x] Share toggle keyboard accessible (Enter to toggle)
- [x] ARIA label for toggle ("Share recipe publicly")
- [x] Focus indicator visible on toggle

### Backend: Input Validation
- [x] Validate recipe ownership (Zod schema)
- [x] Sanitize recipe title before saving
- [x] Check string length (title max 100 chars)

### Backend: Security
- [x] Auth check (only owner can share)
- [x] Rate limit: 10 shares per minute per user
- [x] SQL injection prevention (use Prisma)
```

**Step 4: Reference in Technical Notes**
```markdown
## Technical Notes

**Frontend requirements:**
- See `references/best-practices.md` sections 1-3 (State, Feedback, Accessibility)
- Must handle all error states per best practices
- Keyboard navigation required for accessibility

**Backend requirements:**
- See `references/best-practices.md` sections 1-2, 5 (Validation, Auth, Security)
- Zod schema validation on all inputs
- Rate limiting: 10 requests/min per user
- Auth + ownership check required
```

---

## When to Waive Best Practices

**Valid reasons to skip:**
- ✅ POC/prototype (explicitly scoped as throwaway)
- ✅ Internal tool (single user, controlled environment)
- ✅ Performance constraint (documented trade-off)
- ✅ Technical limitation (library doesn't support feature)

**Invalid reasons:**
- ❌ "We'll add it later" (usually doesn't happen)
- ❌ "Takes too long" (technical debt compounds)
- ❌ "Not in scope" (without explicit exception)
- ❌ "We don't need it" (without understanding risk)

**Document waivers:**
```markdown
## Known Limitations

**Accessibility:**
- Keyboard navigation not implemented (waived for internal admin tool, 2 power users)
- Will add if tool becomes customer-facing

**Performance:**
- No pagination on recipe list (waived for POC with <50 recipes)
- Will add if list grows beyond 100 items
```

---

**Remember:** Best practices prevent 90% of production issues. Invest upfront to save debugging time later.
