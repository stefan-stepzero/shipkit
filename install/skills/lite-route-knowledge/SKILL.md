---
name: lite-route-knowledge
description: Documents page/route implementations with data flows, auth patterns, and dependencies. Uses timestamp-based freshness checking to scan routes modified since last documentation. Extracts data fetching strategies, auth requirements, RLS policies, and dependencies.
---

# route-knowledge-lite - Route Implementation Documentation

**Purpose**: Automatically document page/route implementations to maintain knowledge about data fetching patterns, auth strategies, RLS policies, and dependencies as routes are built.

---

## When to Invoke

**User triggers**:
- "Document this route"
- "Document this page"
- "Log this route implementation"
- "Add route documentation"
- "What routes have I built?"

**After**:
- `/lite-implement` completes a route/page
- User builds a new page or route
- Route is modified and needs re-documentation

**Auto-suggest context**:
- After implementing any route/page component
- When user asks about existing routes
- Before quality checks (helps understand what's built)

---

## Prerequisites

**Optional but helpful**:
- Implementation exists: User has built at least one route/page
- Stack defined: `.shipkit-lite/stack.md` (to understand framework patterns)

**Not required**:
- Can document routes in any state
- Works with partial implementations

---

## Process

### Step 1: Ask Questions First

**Before scanning or generating**, ask user 2-3 questions:

1. **Which routes should I document?**
   - "All routes modified since last documentation?"
   - "Specific route/page you just built?"
   - "Entire routes directory?"

2. **What changed?**
   - "Did you add new data fetching?"
   - "Did auth patterns change?"
   - "New dependencies added?"

3. **Documentation depth?**
   - "Quick summary (data + auth only)?"
   - "Detailed (include all dependencies and RLS policies)?"

**Why ask first**: Avoid scanning entire codebase if user just wants to document one route.

---

### Step 2: Determine Freshness (Timestamp-Based)

**Check when routes were last documented**:

1. Read `.shipkit-lite/implementations.md`
2. Look for "Last route documentation scan: [timestamp]" at top of file
3. Compare file modification times of route files vs. last scan time
4. Only process routes modified AFTER last scan (unless user specifies all)

**First time (no implementations.md exists)**:
- Scan all routes in project
- Document everything

**Subsequent runs**:
- Only document routes modified since last scan timestamp
- User can override and force full scan

---

### Step 3: Detect Route Files

**Based on stack.md, find route patterns**:

**Next.js (App Router)**:
```bash
app/**/page.tsx
app/**/page.ts
app/**/layout.tsx
```

**Next.js (Pages Router)**:
```bash
pages/**/*.tsx
pages/**/*.ts
```

**React Router / Vite**:
```bash
src/routes/**/*.tsx
src/pages/**/*.tsx
```

**SvelteKit**:
```bash
src/routes/**/+page.svelte
src/routes/**/+layout.svelte
src/routes/**/+page.server.ts
```

**Nuxt**:
```bash
pages/**/*.vue
```

**Use Glob tool to find route files**, filtered by framework from stack.md.

---

### Step 4: Extract Route Information

**For EACH route file, extract**:

#### 1. Route Path
- Next.js App: `/dashboard` from `app/dashboard/page.tsx`
- Next.js Pages: `/profile` from `pages/profile.tsx`
- React Router: Infer from file structure

#### 2. Data Fetching Strategy
Look for patterns indicating:

**Server Component (Next.js App Router)**:
```tsx
// NO 'use client' directive
async function Page() {
  const data = await fetch(...) // Direct async
  const dbData = await supabase.from(...) // Direct DB query
}
```

**Client Component**:
```tsx
'use client'
useEffect(() => { fetch(...) }) // Client-side fetching
const { data } = useSWR(...) // SWR
const { data } = useQuery(...) // React Query
```

**Server Actions (Next.js)**:
```tsx
import { createTodo } from '@/actions/todos'
// Uses Server Actions for mutations
```

**API Routes**:
```tsx
// Calls /api/* endpoints
fetch('/api/users')
```

#### 3. Auth Requirements
Look for:

**Middleware protection**:
```tsx
// Check if middleware.ts protects this route
// Common patterns: matcher in middleware.ts
```

**Component-level auth**:
```tsx
const { user } = useUser()
if (!user) redirect('/login')
```

**Auth hooks/utilities**:
```tsx
import { requireAuth } from '@/lib/auth'
import { getServerSession } from 'next-auth'
```

#### 4. RLS Policies Used
Look for Supabase queries with RLS context:

```tsx
supabase.from('dashboard_data')...
// Check for RLS policy name in comments or docs
// Infer policy from table name if possible
```

#### 5. Dependencies
Extract imports and identify:
- **Custom hooks**: `useUser`, `useDashboard`
- **Components**: `<DashboardLayout>`, `<DataTable>`
- **Utilities**: `formatDate`, `validateInput`
- **Server Actions**: `createItem`, `updateItem`

---

### Step 5: Generate Documentation Entry

**For each route, create entry**:

```markdown
### `/route-path` - [Page Type]

**File**: `path/to/file.tsx`
**Last documented**: [timestamp]

**Data Strategy**:
- Fetching: [Server Component | Client Component | Hybrid]
- Method: [Direct async | useEffect | SWR | React Query | Server Actions]
- Sources: [Supabase | API route | External API]

**Auth**:
- Protected: [Yes/No]
- Method: [Middleware | Component guard | Server-side check]
- Requires: [Authenticated user | Specific role | RLS policy]

**RLS Policies** (if using Supabase):
- `dashboard_access` - User can only see own dashboard data
- `team_member` - User must be team member

**Dependencies**:
- Hooks: `useUser`, `useDashboard`
- Components: `DashboardLayout`, `StatsCard`
- Actions: `updateDashboard` (Server Action)
- Utils: `formatCurrency`, `calculateStats`

**Key Patterns**:
- [Notable implementation detail 1]
- [Notable implementation detail 2]

---
```

---

### Step 6: Update implementations.md (OVERWRITE AND ARCHIVE)

**Write strategy: OVERWRITE AND ARCHIVE**

**If file doesn't exist (first run)**:
1. Create new `.shipkit-lite/implementations.md` with header and all routes
2. No archiving needed

**If file exists (subsequent runs)**:
1. **Archive current version**:
   - Read current `.shipkit-lite/implementations.md`
   - Write to `.shipkit-lite/archives/implementations-[timestamp].md`
   - Check archive count (keep last 5, delete older)
2. **Write new version**:
   - Completely replace `.shipkit-lite/implementations.md`
   - Include all current routes (both unchanged and updated ones)
   - Update "Last route documentation scan" timestamp to current time
3. **Result**: Clean snapshot of current route architecture

**File structure**:
```markdown
# Implementations

**Last route documentation scan**: [current timestamp]
**Last component documentation scan**: [timestamp or "Not yet scanned"]

---

## Routes

[All route entries - complete current state]

---

## Components

[Component entries from component-knowledge-lite]

---
```

**Benefits of OVERWRITE AND ARCHIVE**:
- Clean file structure (no duplicate entries)
- Historical snapshots preserved in archives
- Easy to see what changed between versions (diff archived snapshots)
- No complex deduplication logic needed

---

### Step 7: Suggest Next Step

**After documentation complete**:

```
✅ Route documentation updated

📁 Updated: .shipkit-lite/implementations.md

📋 Documented routes:
  • /dashboard - Server Component with Supabase query
  • /profile - Client Component with SWR
  • /settings - Protected route via middleware

🔍 Data patterns found:
  • 2 Server Components (direct DB queries)
  • 1 Client Component (SWR)
  • 3 protected routes (middleware)
  • 2 RLS policies referenced

👉 Next options:
  1. /lite-quality-confidence - Verify routes work correctly
  2. /lite-component-knowledge - Document shared components
  3. /lite-work-memory - Log session progress
  4. Continue implementing next route

What would you like to do?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Timestamp-based freshness (only scan changed files)
- ✅ Auto-detection of data fetching strategies
- ✅ Auth pattern recognition
- ✅ RLS policy extraction
- ✅ Dependency mapping
- ✅ Framework-aware route detection

**Not included** (vs full route-knowledge):
- ❌ Performance metrics (load time, bundle size)
- ❌ SEO metadata extraction
- ❌ API contract validation
- ❌ Route param validation
- ❌ Error boundary documentation
- ❌ Internationalization detection

**Philosophy**: Document what developers need to understand data flow and auth. Skip production optimization concerns for POC/MVP.

---

## Timestamp-Based Freshness Pattern

**How it works**:

1. **First run**: No timestamp exists
   - Scan ALL route files
   - Document everything
   - Write timestamp: `Last route documentation scan: 2025-12-28T10:30:00Z`

2. **Subsequent runs**: Timestamp exists
   - Compare file modification time vs. last scan time
   - Only process files modified AFTER timestamp
   - Update timestamp after scan

3. **Force full scan**: User can override
   - User says "document all routes"
   - Ignore timestamp, scan everything
   - Update timestamp

**Benefits**:
- Efficient: Only documents what changed
- Incremental: Keeps docs fresh without re-scanning everything
- Fast: Skips unchanged files

**Implementation**:
```bash
# Pseudo-logic
LAST_SCAN=$(grep "Last route documentation scan:" implementations.md | extract_timestamp)

for ROUTE_FILE in $(glob_routes); do
  FILE_MODIFIED=$(stat -c %Y $ROUTE_FILE)

  if [ $FILE_MODIFIED -gt $LAST_SCAN ]; then
    # Document this route (it changed)
  fi
done

# Update timestamp
echo "Last route documentation scan: $(date -Iseconds)"
```

---

## Integration with Other Skills

**Before route-knowledge-lite**:
- `/lite-implement` - Builds the route
- `/lite-spec` - Defines what route should do
- `/lite-project-context` - Generates stack.md (framework info)

**After route-knowledge-lite**:
- `/lite-quality-confidence` - Verifies routes work
- `/lite-component-knowledge` - Documents shared components
- `/lite-work-memory` - Logs documentation session

**Complements**:
- `/lite-data-consistency` - Uses types documented here
- `/lite-architecture-memory` - References patterns found here

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit-lite/stack.md` - Framework info (Next.js vs. SvelteKit)
- `.shipkit-lite/implementations.md` - Existing docs + timestamp

**Secondary** (optional):
- `.shipkit-lite/architecture.md` - Established auth patterns
- `.shipkit-lite/types.md` - Data types used in routes
- `middleware.ts` or `middleware.js` - Auth middleware patterns

**Source files** (scanned):
- `app/**/*.tsx` or `pages/**/*.tsx` or framework-specific routes
- Route files based on stack.md framework

---

## Context Files This Skill Writes

### Write Strategy: OVERWRITE AND ARCHIVE

**Primary file**:
- `.shipkit-lite/implementations.md` - Complete current route documentation

**Write behavior**:
1. **On first run**: Create new `implementations.md` with all routes
2. **On subsequent runs**:
   - Archive current `implementations.md` to `.shipkit-lite/archives/implementations-[timestamp].md`
   - Write new complete version with updated routes
   - Update "Last route documentation scan" timestamp

**Why OVERWRITE AND ARCHIVE**:
- **History matters**: Route architecture evolves (client→server components, auth migrations)
- **Audit trail**: Archived snapshots show when patterns changed (RLS policies added, middleware introduced)
- **Clean deduplication**: Replacing entries in append-only files is fragile
- **File size**: Growing projects (20+ routes) need fresh snapshots instead of accumulating entries
- **Timestamp versioning**: Each scan creates a snapshot of route architecture at that moment

**Archive retention**:
- Keep last 5 snapshots (configurable)
- Delete older archives automatically
- User can disable archiving if not needed

**Never creates**:
- No additional files beyond implementations.md and archives

**Never modifies**:
- Source route files (read-only analysis)
- Stack, architecture, specs (read-only)

---

## Lazy Loading Behavior

**This skill loads context progressively**:

1. User invokes `/lite-route-knowledge`
2. Claude asks which routes to document
3. Claude reads `.shipkit-lite/stack.md` (~200 tokens)
4. Claude reads `.shipkit-lite/implementations.md` for timestamp (~500 tokens)
5. **During scanning**, Claude loads on demand:
   - Route files only if modified since last scan
   - Architecture.md only if auth patterns unclear
   - Types.md only if data structures referenced
6. Total context: ~1000-3000 tokens (focused)

**Not loaded unless needed**:
- Unmodified route files
- Specs or plans
- User tasks
- Session logs

---

## Success Criteria

Documentation is complete when:
- [ ] All modified routes identified (via timestamp comparison)
- [ ] Data fetching strategy extracted for each route
- [ ] Auth requirements documented
- [ ] RLS policies identified (if applicable)
- [ ] Dependencies mapped
- [ ] implementations.md updated with new entries
- [ ] Timestamp updated to current time
- [ ] No duplicate entries (old entries replaced if re-documenting)

---

## Common Scenarios

### Scenario 1: First Time Documentation

```
User: "Document all my routes"

Claude:
1. Check .shipkit-lite/implementations.md
2. No "Last route documentation scan" found → First run
3. Read .shipkit-lite/stack.md (see Next.js App Router)
4. Glob app/**/page.tsx (find all routes)
5. For each route:
   - Extract data strategy
   - Identify auth
   - Map dependencies
6. Create implementations.md with Routes section
7. Add timestamp: "Last route documentation scan: 2025-12-28T14:30:00Z"
```

### Scenario 2: Incremental Update

```
User: "Document the new dashboard route I just built"

Claude:
1. Read implementations.md
2. See "Last route documentation scan: 2025-12-28T10:00:00Z"
3. Check app/dashboard/page.tsx modified at 14:00:00
4. File is newer than last scan → Document it
5. Extract:
   - Data: Server Component with direct Supabase query
   - Auth: Protected via middleware
   - RLS: Uses 'dashboard_access' policy
   - Deps: useUser hook, DashboardLayout component
6. Append to implementations.md
7. Update timestamp to 14:30:00
```

### Scenario 3: Force Full Re-scan

```
User: "Re-document all routes, patterns changed"

Claude:
1. User explicitly requests full scan
2. Ignore timestamp (override freshness check)
3. Glob all route files
4. Document all routes (replace old entries)
5. Update timestamp
```

### Scenario 4: No Changes

```
User: "Document routes"

Claude:
1. Read implementations.md
2. Last scan: 2025-12-28T14:00:00Z
3. Check all route files
4. No files modified after 14:00:00
5. "No routes modified since last documentation. All routes are up to date."
6. Don't update timestamp (nothing changed)
```

---

## Framework-Specific Detection Patterns

### Next.js App Router (Server Components)

**Route detection**:
```bash
app/**/page.tsx
app/**/layout.tsx
app/**/loading.tsx
app/**/error.tsx
```

**Data strategy indicators**:
```tsx
// Server Component (no 'use client')
export default async function Page() {
  const data = await db.query(...) // Direct DB
  const res = await fetch(..., { cache: 'no-store' }) // Server fetch
}

// Client Component
'use client'
export default function Page() {
  const { data } = useSWR(...) // Client fetch
}
```

**Auth patterns**:
```tsx
// Middleware protection
// Check middleware.ts matcher: ['/dashboard/:path*']

// Server-side check
import { auth } from '@/auth'
const session = await auth()
if (!session) redirect('/login')
```

### Next.js Pages Router

**Route detection**:
```bash
pages/**/*.tsx
pages/api/**/*.ts (API routes)
```

**Data strategy indicators**:
```tsx
// SSR
export async function getServerSideProps() { ... }

// SSG
export async function getStaticProps() { ... }

// Client
export default function Page() {
  useEffect(() => fetch(...))
}
```

### SvelteKit

**Route detection**:
```bash
src/routes/**/+page.svelte
src/routes/**/+page.server.ts
src/routes/**/+layout.svelte
```

**Data strategy indicators**:
```ts
// Server load
export async function load({ fetch }) {
  const data = await fetch(...) // Server-side
}
```

### React Router / Vite

**Route detection**:
```bash
src/routes/**/*.tsx
src/pages/**/*.tsx
```

**Data strategy indicators**:
```tsx
// Client-only (typical for SPA)
useEffect(() => fetch(...))
const { data } = useQuery(...)
```

---

## Data Fetching Strategy Classification

**Server Component** (Next.js App Router):
- No `'use client'` directive
- `async function` component
- Direct `await fetch()` or `await db.query()`
- **Pros**: SEO-friendly, secure, fast initial load
- **Cons**: Can't use React hooks

**Client Component**:
- Has `'use client'` directive
- Uses `useEffect`, `useSWR`, `useQuery`, etc.
- **Pros**: Interactive, real-time updates
- **Cons**: Client-side bundle, slower initial render

**Hybrid**:
- Layout is Server Component
- Child components are Client Components
- Combines benefits

**Server Actions** (Next.js):
- `'use server'` directive
- Form mutations without API routes
- **Pattern**: Server Component + Server Action for mutations

**API Routes**:
- Separate `/api/*` endpoints
- Called from client via `fetch()`
- **Pattern**: Traditional REST API

---

## Auth Pattern Detection

### Middleware-Based Protection

**File**: `middleware.ts` or `middleware.js`

**Pattern**:
```ts
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
}

export function middleware(req: NextRequest) {
  const token = req.cookies.get('session')
  if (!token) return NextResponse.redirect('/login')
}
```

**Detection**: Check if route path matches middleware matcher

### Component-Level Guards

**Pattern**:
```tsx
export default function ProtectedPage() {
  const { user, isLoading } = useUser()

  if (isLoading) return <Spinner />
  if (!user) redirect('/login')

  return <Dashboard />
}
```

**Detection**: Look for early returns checking `user` or `session`

### Server-Side Checks

**Pattern**:
```tsx
export default async function Page() {
  const session = await getServerSession()
  if (!session) redirect('/login')
}
```

**Detection**: `getServerSession`, `auth()`, or similar in Server Component

### RLS (Row Level Security) - Supabase

**Pattern**:
```tsx
// Automatically enforced by Supabase
const { data } = await supabase
  .from('dashboard_data')
  .select('*')
// RLS policy 'dashboard_access' filters results by user_id
```

**Detection**:
- Look for comments mentioning policy names
- Check table name (e.g., `user_profiles` likely has user RLS)
- Infer from context (authenticated queries assume RLS)

---

## Tips for Effective Route Documentation

**Be specific about data sources**:
- ❌ "Fetches data from database"
- ✅ "Server Component with direct Supabase query to `dashboard_stats` table"

**Clarify auth at both levels**:
- Route-level: "Protected by middleware matcher `/dashboard/:path*`"
- RLS-level: "Uses `user_owned_data` policy - filters by `user_id = auth.uid()`"

**Document dependencies clearly**:
- Distinguish hooks vs. components vs. utilities
- Note if dependency is custom or third-party

**Flag unusual patterns**:
- "Hybrid: Layout is Server Component, but uses Client Component for interactive chart"
- "No auth middleware, but uses component-level guard"

**Update when patterns change**:
- If route changes from client to server component → re-document
- If new RLS policy added → update entry

**When to upgrade to full /route-knowledge**:
- Need performance metrics (Core Web Vitals)
- SEO metadata important
- API contract validation needed
- Production observability required

---

## Example Output

**Route documentation in `.shipkit-lite/implementations.md`**:

```markdown
# Implementations

**Last route documentation scan**: 2025-12-28T14:30:00Z
**Last component documentation scan**: Not yet scanned

---

## Routes

### `/dashboard` - Dashboard Page

**File**: `app/dashboard/page.tsx`
**Last documented**: 2025-12-28T14:30:00Z

**Data Strategy**:
- Fetching: Server Component
- Method: Direct async Supabase query
- Sources: Supabase `dashboard_stats` table

**Auth**:
- Protected: Yes
- Method: Middleware + RLS
- Requires: Authenticated user

**RLS Policies**:
- `dashboard_access` - User can only see stats where `user_id = auth.uid()`

**Dependencies**:
- Components: `DashboardLayout`, `StatsCard`, `RecentActivity`
- Utils: `formatCurrency`, `calculateGrowth`

**Key Patterns**:
- Pure Server Component (no client-side JS needed)
- Real-time updates via Supabase Realtime subscription in StatsCard
- Uses React Suspense with loading.tsx

---

### `/profile` - User Profile Page

**File**: `app/profile/page.tsx`
**Last documented**: 2025-12-28T14:15:00Z

**Data Strategy**:
- Fetching: Client Component
- Method: SWR with revalidation
- Sources: API route `/api/user/profile`

**Auth**:
- Protected: Yes
- Method: Component-level guard
- Requires: Authenticated user (checked via `useUser` hook)

**Dependencies**:
- Hooks: `useUser`, `useSWR`
- Components: `ProfileLayout`, `AvatarUpload`, `SettingsForm`
- Actions: `updateProfile` (Server Action for mutations)

**Key Patterns**:
- Client Component for real-time updates
- Form uses Server Action for optimistic updates
- SWR cache invalidation on successful mutation

---

### `/api/user/profile` - Profile API Endpoint

**File**: `app/api/user/profile/route.ts`
**Last documented**: 2025-12-28T14:20:00Z

**Data Strategy**:
- Fetching: API Route Handler (GET, PATCH)
- Method: Direct Supabase query
- Sources: Supabase `user_profiles` table

**Auth**:
- Protected: Yes
- Method: Token validation in API route
- Requires: Valid session token in Authorization header

**RLS Policies**:
- `user_profiles_policy` - User can only update own profile

**Dependencies**:
- Utils: `validateSession`, `sanitizeInput`

**Key Patterns**:
- RESTful API pattern (GET for fetch, PATCH for update)
- Input validation before mutation
- Returns typed response matching `UserProfile` type

---

## Components

(Component documentation from component-knowledge-lite would appear here)

---
```

---

**Remember**: This skill documents routes to maintain knowledge of data flows and auth patterns. It's called after implementation to keep implementations.md fresh. Use timestamp-based scanning to stay efficient and only process what changed.
