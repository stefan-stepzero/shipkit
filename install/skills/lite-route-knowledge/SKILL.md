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

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit-lite/.queues/routes-to-document.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for routes/APIs needing documentation
2. For each pending route:
   - Read route handler code
   - Extract request/response schemas (Step 2-3 logic)
   - Document API contract in `.shipkit-lite/api-contracts.md`
   - Move item from Pending to Completed in queue
3. Skip Step 1 questions (routes already identified)
4. Continue with Step 2-5 for each route

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode - ask what to document)

---

### Step 1: (Manual Mode) Ask Questions First

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

**Based on stack.md, find route patterns**.

**See `references/detection-patterns.md` for:**
- Framework-specific route file patterns (Next.js, SvelteKit, React Router, Nuxt)
- Glob patterns for each framework
- How to map file paths to route paths

**Use Glob tool to find route files**, filtered by framework from stack.md.

---

### Step 4: Extract Route Information

**For EACH route file, extract**:

1. **Route Path** - Derive URL path from file structure
2. **Data Fetching Strategy** - Server Component vs Client Component vs Hybrid
3. **Auth Requirements** - Middleware, component guards, server-side checks
4. **RLS Policies** - Supabase Row Level Security policies referenced
5. **Dependencies** - Hooks, components, utilities, server actions imported

**See `references/detection-patterns.md` for:**
- Complete data fetching classification (Server Component, Client Component, Hybrid, Server Actions, API Routes)
- Auth pattern detection methods (middleware, component guards, server-side checks, RLS)
- Dependency extraction patterns (hooks, components, utilities)

---

### Step 5: Generate Documentation Entry

**For each route, create entry using standard template**.

**See `references/templates.md` for:**
- Route documentation entry template
- Complete file structure template
- Example entries (simple, complex, hybrid, API routes)
- Minimal entry format for static pages

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

## When This Skill Integrates with Others

### Before This Skill

- `/lite-implement` - Builds the route implementation
  - **When**: After completing route/page development
  - **Why**: Can't document routes that don't exist yet
  - **Trigger**: User built new routes and wants to document them

- `/lite-spec` - Defines feature requirements
  - **When**: Before implementation
  - **Why**: Specs guide what routes to build
  - **Trigger**: Spec defines routes needed for feature

- `/lite-project-context` - Scans stack and generates stack.md
  - **When**: Project initialization or stack changes
  - **Why**: Route detection depends on knowing framework (Next.js vs SvelteKit vs etc)
  - **Trigger**: stack.md must exist to determine route file patterns

### After This Skill

- `/lite-quality-confidence` - Verifies route implementations
  - **When**: After documenting routes
  - **Why**: Documentation reveals what to test (auth, data fetching, RLS)
  - **Trigger**: User asks "ready to ship?" after implementing routes

- `/lite-component-knowledge` - Documents shared components
  - **When**: After route documentation finds component dependencies
  - **Why**: Routes use components - both should be documented
  - **Trigger**: Route documentation lists `<ComponentName>` dependencies

- `/lite-work-memory` - Logs documentation session progress
  - **When**: After completing route documentation session
  - **Why**: Track what was documented and when
  - **Trigger**: User wants to log session or end of work session

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

## Example Documentation Scenarios

**See `references/example-scenarios.md` for 10 complete scenarios:**
- Scenario 1: First Time Documentation (no implementations.md exists)
- Scenario 2: Incremental Update (only changed routes)
- Scenario 3: Force Full Re-scan (after refactoring)
- Scenario 4: No Changes (nothing modified)
- Scenario 5: Specific Route Documentation
- Scenario 6: Multi-Framework Project
- Scenario 7: Discovering Undocumented Components
- Scenario 8: Auth Pattern Evolution
- Scenario 9: Hybrid Data Fetching Detection
- Scenario 10: API Route Documentation

---

## Detection Patterns

**See `references/detection-patterns.md` for comprehensive patterns:**

**Framework Detection**:
- Next.js App Router (Server Components)
- Next.js Pages Router (SSR/SSG/Client)
- SvelteKit (Server load functions)
- React Router / Vite (Client-only SPA)

**Data Fetching Classification**:
- Server Component (async, direct DB/fetch)
- Client Component ('use client', hooks)
- Hybrid (Server layout + Client children)
- Server Actions ('use server', form mutations)
- API Routes (REST endpoints)

**Auth Pattern Detection**:
- Middleware-Based Protection (middleware.ts matchers)
- Component-Level Guards (early returns checking user/session)
- Server-Side Checks (getServerSession, auth())
- RLS (Row Level Security - Supabase policies)

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
