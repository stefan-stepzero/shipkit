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

## Architecture Patterns (DRY & Centralization)

**These patterns prevent the "patching 10 pages" problem.**

### 1. Authentication - Global Middleware, Not Per-Page

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Auth check duplicated on every page
// pages/dashboard.tsx
export default function Dashboard() {
  const { user } = useAuth();
  if (!user) redirect('/login');  // Duplicated everywhere
  // ...
}

// pages/settings.tsx
export default function Settings() {
  const { user } = useAuth();
  if (!user) redirect('/login');  // Same check, copied
  // ...
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Centralized auth middleware
// middleware.ts (Next.js) or auth-guard.tsx (React)
export function middleware(request: NextRequest) {
  const session = await getSession(request);

  if (protectedRoutes.includes(request.pathname) && !session) {
    return NextResponse.redirect('/login');
  }
}

// Or: Layout-level protection
// app/(protected)/layout.tsx
export default async function ProtectedLayout({ children }) {
  const session = await getSession();
  if (!session) redirect('/login');
  return <>{children}</>;
}
```

**Why It Matters:**
- One place to update auth logic
- Impossible to forget auth on new pages
- Easier to audit security
- Consistent behavior across routes

---

### 2. Error Handling - Global Boundary, Not Per-Component Try/Catch

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Try/catch scattered everywhere
function ComponentA() {
  try {
    const data = await fetchData();
  } catch (e) {
    return <div>Error occurred</div>;  // Inconsistent error UI
  }
}

function ComponentB() {
  try {
    const data = await fetchOther();
  } catch (e) {
    console.error(e);  // Different handling, no UI
  }
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Centralized error boundary + consistent handling
// app/error.tsx (Next.js) or ErrorBoundary.tsx
export default function GlobalError({ error, reset }) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <ErrorPage
      message="Something went wrong"
      onRetry={reset}
    />
  );
}

// Components just throw - boundary catches
function Component() {
  const data = await fetchData(); // Throws on error, boundary catches
  return <Display data={data} />;
}
```

**Why It Matters:**
- Consistent error UI across app
- Centralized error logging (Sentry, etc.)
- Components stay clean (no try/catch noise)
- One place to update error handling behavior

---

### 3. Data Fetching - Provider Pattern, Not Prop Drilling

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Fetching same data in multiple places
function Page() {
  const user = await getUser();  // Fetched here
  return <Header user={user} />;  // Passed down
}

function Header({ user }) {
  return <Avatar user={user} />;  // Passed again
}

function Avatar({ user }) {
  return <img src={user.avatar} />;  // Finally used
}

// Later: Another component needs user
function Sidebar() {
  const user = await getUser();  // Fetched AGAIN!
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Centralized data provider + hooks
// context/user-context.tsx
const UserContext = createContext<User | null>(null);

export function UserProvider({ children }) {
  const user = useSWR('/api/user', fetcher);  // Cached, single fetch
  return <UserContext.Provider value={user}>{children}</UserContext.Provider>;
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be within UserProvider');
  return context;
}

// Any component can access without prop drilling
function Avatar() {
  const { user } = useUser();  // Gets cached user
  return <img src={user.avatar} />;
}
```

**Why It Matters:**
- Single source of truth for data
- No duplicate API calls
- Any component can access without drilling
- Cache invalidation in one place

---

### 4. Logging & Monitoring - Central Service, Not Scattered Console.log

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Inconsistent logging everywhere
function handleSubmit() {
  console.log('Form submitted');  // No structure
}

function fetchData() {
  console.error('API Error:', error);  // Different format
}

function processPayment() {
  console.log({ event: 'payment', amount });  // Yet another format
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Centralized logger with consistent structure
// lib/logger.ts
class Logger {
  private send(level: 'info' | 'warn' | 'error', event: string, data?: object) {
    const payload = {
      timestamp: new Date().toISOString(),
      level,
      event,
      ...data,
      userId: getCurrentUserId(),  // Auto-attached
      sessionId: getSessionId(),
    };

    if (process.env.NODE_ENV === 'production') {
      sendToLoggingService(payload);  // Datadog, LogRocket, etc.
    } else {
      console.log(JSON.stringify(payload, null, 2));
    }
  }

  info(event: string, data?: object) { this.send('info', event, data); }
  warn(event: string, data?: object) { this.send('warn', event, data); }
  error(event: string, error: Error, data?: object) {
    this.send('error', event, { ...data, error: error.message, stack: error.stack });
    Sentry.captureException(error);
  }
}

export const logger = new Logger();

// Usage - consistent everywhere
logger.info('form.submitted', { formId: 'signup' });
logger.error('api.failed', error, { endpoint: '/users' });
```

**Why It Matters:**
- Consistent log format (parseable by tools)
- Automatic context (userId, sessionId)
- One place to add/change logging destinations
- Easy to search/filter logs in production

---

### 5. Configuration - Environment Abstraction, Not Scattered env Access

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: process.env scattered everywhere
function sendEmail() {
  const apiKey = process.env.SENDGRID_API_KEY;  // Here
}

function connectDB() {
  const url = process.env.DATABASE_URL;  // And here
}

function stripe() {
  const key = process.env.STRIPE_SECRET_KEY!;  // And here (with !)
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Centralized, typed, validated config
// lib/config.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  SENDGRID_API_KEY: z.string().min(1),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

// Validates at startup - fails fast if missing
const parsed = envSchema.safeParse(process.env);
if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.flatten());
  process.exit(1);
}

export const config = parsed.data;

// Usage - typed, validated, single source
import { config } from '@/lib/config';
const db = connectDB(config.DATABASE_URL);  // TypeScript knows it's string
```

**Why It Matters:**
- Fails fast on startup if env missing (not at runtime)
- TypeScript knows exact types
- One file documents all required env vars
- No `!` assertions scattered everywhere

---

### 6. API Response Format - Consistent Structure, Not Ad-hoc

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Different response shapes per endpoint
// /api/users
return { users: [...] };

// /api/posts
return { data: [...], count: 10 };

// /api/orders
return [...];  // Just array, no wrapper

// Error handling equally inconsistent
return { error: 'Failed' };
return { message: 'Not found', code: 404 };
return new Error('Unauthorized');
```

**The Solution:**
```typescript
// ✅ PATTERN: Consistent API response wrapper
// lib/api-response.ts
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: { message: string; code: string } };

function success<T>(data: T): ApiResponse<T> {
  return { success: true, data };
}

function error(message: string, code: string): ApiResponse<never> {
  return { success: false, error: { message, code } };
}

// Usage - consistent everywhere
export async function GET() {
  const users = await db.user.findMany();
  return Response.json(success(users));
}

export async function POST(request: Request) {
  const body = await request.json();
  const result = schema.safeParse(body);

  if (!result.success) {
    return Response.json(error('Validation failed', 'VALIDATION_ERROR'), { status: 400 });
  }

  const user = await db.user.create({ data: result.data });
  return Response.json(success(user), { status: 201 });
}
```

**Why It Matters:**
- Frontend can use single response handler
- Consistent error shape for error boundaries
- TypeScript can narrow on `success` boolean
- API documentation is predictable

---

## TypeScript Patterns & Anti-Patterns

**TypeScript-specific patterns that prevent bugs and improve DX.**

### 1. The `any` Escape Hatch Problem

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: any defeats TypeScript's purpose
function processData(data: any) {
  return data.user.profile.name.toUpperCase();  // No type safety
}

// Later crashes: Cannot read property 'name' of undefined
```

**The Solution:**
```typescript
// ✅ PATTERN: Proper typing or unknown + narrowing
// Option A: Define the type
interface UserData {
  user: {
    profile: {
      name: string;
    };
  };
}

function processData(data: UserData) {
  return data.user.profile.name.toUpperCase();  // Type safe
}

// Option B: Use unknown + type guard
function processData(data: unknown) {
  if (!isUserData(data)) {
    throw new Error('Invalid data shape');
  }
  return data.user.profile.name.toUpperCase();  // Safe after guard
}

function isUserData(data: unknown): data is UserData {
  return (
    typeof data === 'object' && data !== null &&
    'user' in data && typeof data.user === 'object'
    // ... full validation
  );
}
```

---

### 2. Type Assertions (`as`) Overuse

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: as bypasses type checking
const user = response.data as User;  // Assumes shape is correct
const element = document.getElementById('root') as HTMLDivElement;  // Might be null

// Crashes later when assumptions are wrong
```

**The Solution:**
```typescript
// ✅ PATTERN: Type guards and proper null handling
// For API responses: Validate with Zod
const userSchema = z.object({ id: z.string(), name: z.string() });
const user = userSchema.parse(response.data);  // Throws if wrong shape

// For DOM: Handle null case
const element = document.getElementById('root');
if (!(element instanceof HTMLDivElement)) {
  throw new Error('Root element not found or wrong type');
}
// Now element is HTMLDivElement
```

---

### 3. Non-null Assertion (`!`) Everywhere

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: ! ignores null possibility
const user = users.find(u => u.id === id)!;  // Might be undefined
const config = process.env.API_KEY!;  // Might be undefined

user.name;  // Runtime error if not found
```

**The Solution:**
```typescript
// ✅ PATTERN: Handle the null case explicitly
// Option A: Throw meaningful error
const user = users.find(u => u.id === id);
if (!user) {
  throw new Error(`User not found: ${id}`);
}
// user is now User (not User | undefined)

// Option B: Provide default
const config = process.env.API_KEY ?? 'default-key';

// Option C: Early validation (for env vars - see config pattern above)
```

---

### 4. Zod as Single Source of Truth

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Types and validation defined separately
interface User {
  id: string;
  email: string;
  age: number;
}

// Validation duplicates the same info
function validateUser(data: unknown) {
  if (typeof data.id !== 'string') throw new Error('id must be string');
  if (typeof data.email !== 'string') throw new Error('email must be string');
  // ... duplicated logic, can drift from interface
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Zod schema is the single source of truth
import { z } from 'zod';

// Schema defines shape AND validation in one place
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().positive().max(120),
});

// Type is inferred from schema - always in sync
type User = z.infer<typeof userSchema>;

// Validation uses the same schema
function validateUser(data: unknown): User {
  return userSchema.parse(data);  // Throws ZodError if invalid
}

// Safe parse for handling errors
const result = userSchema.safeParse(data);
if (!result.success) {
  console.error(result.error.flatten());
}
```

---

### 5. Discriminated Unions for State

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Separate booleans for state
interface FetchState {
  isLoading: boolean;
  isError: boolean;
  data: User | null;
  error: Error | null;
}

// Impossible states are possible
const state: FetchState = {
  isLoading: true,
  isError: true,  // Loading AND error?
  data: user,     // Has data while loading?
  error: err,     // Has error while has data?
};
```

**The Solution:**
```typescript
// ✅ PATTERN: Discriminated union makes impossible states impossible
type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// TypeScript enforces valid states
const state: FetchState<User> = { status: 'loading' };  // ✓

// Exhaustive handling
function render(state: FetchState<User>) {
  switch (state.status) {
    case 'idle':
      return <Placeholder />;
    case 'loading':
      return <Spinner />;
    case 'success':
      return <UserCard user={state.data} />;  // data available here
    case 'error':
      return <Error message={state.error.message} />;  // error available here
    default:
      const _exhaustive: never = state;  // Compile error if case missed
      return _exhaustive;
  }
}
```

---

### 6. Branded Types for IDs

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: All IDs are just strings
function getUser(userId: string) { /* ... */ }
function getOrder(orderId: string) { /* ... */ }

// Easy to mix up - no compile error
getUser(orderId);  // Wrong! But TypeScript doesn't catch it
getOrder(userId);  // Wrong! But TypeScript doesn't catch it
```

**The Solution:**
```typescript
// ✅ PATTERN: Branded types prevent ID mixups
type Brand<K, T> = K & { __brand: T };

type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;

function getUser(userId: UserId) { /* ... */ }
function getOrder(orderId: OrderId) { /* ... */ }

// Create branded IDs
const userId = 'user_123' as UserId;
const orderId = 'order_456' as OrderId;

// Now TypeScript catches mixups
getUser(userId);   // ✓
getUser(orderId);  // ✗ Type error!
getOrder(orderId); // ✓
getOrder(userId);  // ✗ Type error!
```

---

### 7. Exhaustive Switch with `never`

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Switch without exhaustive check
type Status = 'pending' | 'approved' | 'rejected';

function getStatusColor(status: Status) {
  switch (status) {
    case 'pending': return 'yellow';
    case 'approved': return 'green';
    // Forgot 'rejected'! No compile error, returns undefined
  }
}

// Later: Status type extended
type Status = 'pending' | 'approved' | 'rejected' | 'cancelled';
// Old switch silently broken - no compile error
```

**The Solution:**
```typescript
// ✅ PATTERN: Exhaustive check catches missing cases at compile time
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

function getStatusColor(status: Status): string {
  switch (status) {
    case 'pending': return 'yellow';
    case 'approved': return 'green';
    case 'rejected': return 'red';
    default:
      return assertNever(status);  // Compile error if case missing!
  }
}

// When 'cancelled' is added to Status:
// TypeScript error: Argument of type '"cancelled"' is not assignable to parameter of type 'never'
// Forces you to handle the new case
```

---

### 8. Const Assertions for Literal Types

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Object loses literal types
const config = {
  endpoint: '/api/users',
  method: 'GET',
};
// Type is { endpoint: string; method: string }
// Lost the literal values!

function fetch(url: string, method: 'GET' | 'POST') { /* ... */ }
fetch(config.endpoint, config.method);  // Error: string is not 'GET' | 'POST'
```

**The Solution:**
```typescript
// ✅ PATTERN: as const preserves literal types
const config = {
  endpoint: '/api/users',
  method: 'GET',
} as const;
// Type is { readonly endpoint: "/api/users"; readonly method: "GET" }

fetch(config.endpoint, config.method);  // ✓ Works!

// Also great for arrays
const STATUSES = ['pending', 'approved', 'rejected'] as const;
type Status = typeof STATUSES[number];  // 'pending' | 'approved' | 'rejected'
```

---

### 9. Generic Constraints for Reusable Functions

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: any to make it "flexible"
function getProperty(obj: any, key: string) {
  return obj[key];  // Returns any, no type safety
}

// Or overly specific - not reusable
function getUserName(user: User) {
  return user.name;
}
```

**The Solution:**
```typescript
// ✅ PATTERN: Generics with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];  // Return type is exactly T[K]
}

const user = { id: 1, name: 'Alice', email: 'alice@example.com' };
const name = getProperty(user, 'name');  // Type: string
const id = getProperty(user, 'id');      // Type: number
getProperty(user, 'age');                // Error: 'age' not in keyof User

// Generic with constraint
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

---

### 10. Utility Types Instead of Manual Typing

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Manually redefining types
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

// For API response (no password)
interface PublicUser {
  id: string;
  name: string;
  email: string;
}

// For creation (no id)
interface CreateUser {
  name: string;
  email: string;
  password: string;
}

// For update (all optional)
interface UpdateUser {
  name?: string;
  email?: string;
  password?: string;
}
// Duplicated! Will drift out of sync.
```

**The Solution:**
```typescript
// ✅ PATTERN: Derive types with utility types
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

type PublicUser = Omit<User, 'password'>;
type CreateUser = Omit<User, 'id'>;
type UpdateUser = Partial<Omit<User, 'id'>>;

// Other useful utilities:
type RequiredUser = Required<User>;          // All fields required
type ReadonlyUser = Readonly<User>;          // All fields readonly
type NameAndEmail = Pick<User, 'name' | 'email'>;  // Only these fields
type UserRecord = Record<string, User>;      // Dictionary of users
```

---

### 11. Satisfies for Type Checking Without Widening

**The Problem:**
```typescript
// ❌ ANTI-PATTERN: Type annotation widens the type
const routes: Record<string, string> = {
  home: '/',
  about: '/about',
  contact: '/contact',
};

routes.home;     // Type: string (lost the literal '/')
routes.invalid;  // No error! Record<string, string> allows any key

// Or: as const loses the type constraint
const routes = {
  home: '/',
  about: '/about',
  contact: 123,  // No error! No type checking
} as const;
```

**The Solution:**
```typescript
// ✅ PATTERN: satisfies checks type while preserving literals
const routes = {
  home: '/',
  about: '/about',
  contact: '/contact',
} satisfies Record<string, string>;

routes.home;     // Type: "/" (literal preserved!)
routes.invalid;  // Error: Property 'invalid' does not exist

// Type checking still works
const badRoutes = {
  home: '/',
  about: 123,  // Error: number is not assignable to string
} satisfies Record<string, string>;
```

---

## Architecture Pattern Checklist

**Use this checklist during `/lite-plan` to catch anti-patterns early.**

### Before Implementation, Ask:

- [ ] **Auth**: Will auth be checked in middleware/layout, or per-page?
  - If per-page → STOP: Centralize first

- [ ] **Error Handling**: Is there a global error boundary?
  - If no → STOP: Add error boundary first

- [ ] **Data Fetching**: Will same data be fetched in multiple components?
  - If yes → STOP: Create provider/context first

- [ ] **Logging**: Is there a central logger service?
  - If no → STOP: Create logger first

- [ ] **Config**: Are env vars validated at startup?
  - If no → STOP: Create config validation first

- [ ] **API Responses**: Is there a consistent response wrapper?
  - If no → STOP: Define response format first

### TypeScript Checks:

- [ ] **No `any`**: Are there `any` types that should be properly typed?
- [ ] **No `as` abuse**: Are type assertions used only when necessary?
- [ ] **No `!` abuse**: Are non-null assertions replaced with proper checks?
- [ ] **Zod schemas**: Are runtime validations using Zod with inferred types?
- [ ] **Discriminated unions**: Are state types using discriminated unions?
- [ ] **Exhaustive switches**: Do all switches have `never` exhaustive check?

---

**Remember:** Best practices prevent 90% of production issues. Invest upfront to save debugging time later.
